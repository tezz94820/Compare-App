"""
Comparison Worker Thread
Handles PDF comparison in background without blocking UI
"""

from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path
import csv
import gc
from datetime import datetime

from utils.logger import get_logger
from core.comparators.pdf.pdf_comparison import PDFComparator
from core.comparators.pdf.pdf_generate_summary import PdfSummaryGenerator
from core.comparators.excel.excel_comparison import ExcelComparator
from core.comparators.excel.excel_generate_summary import ExcelSummaryGenerator
from core.comparators.txt.txt_comparison import TXTComparator
from core.comparators.txt.txt_generate_summary import TxtSummaryGenerator
from core.state_manager import app_state


logger = get_logger(__name__)


class ComparisonWorker(QThread):
    """
    Worker thread for running PDF/EXCEL/TXT comparisons in background.
    
    Signals:
        progress_updated: Emitted when progress changes (current, total, file_name, percentage)
        file_completed: Emitted when a single file comparison completes (file_info)
        comparison_complete: Emitted when all comparisons finish (master_summary_path)
        comparison_error: Emitted when an error occurs (error_message)
    """
    
    # Signals
    progress_updated = pyqtSignal(int, int, str, float)  # current, total, filename, percentage
    file_completed = pyqtSignal(dict)  # file_info dict
    comparison_complete = pyqtSignal(str)  # master_summary_path
    comparison_error = pyqtSignal(str)  # error_message
    # NEW: emit list of skipped mappings so UI can show them
    skipped_mappings = pyqtSignal(list)  # list of {'dev','prod','error'}
    
    def __init__(self, dev_folder: str, prod_folder: str, csv_file: str, 
                 output_folder: str, parent=None):
        super().__init__(parent)
        
        self.dev_folder = Path(dev_folder)
        self.prod_folder = Path(prod_folder)
        self.csv_file = Path(csv_file)
        self.output_folder = Path(output_folder)
        
        self.file_mappings = []
        self.comparison_results = []
        self.is_cancelled = False
        self.missing_files = []
        
        logger.info("Comparison worker initialized")
    
    def run(self):
        """Main worker thread execution"""
        try:
            logger.info("Starting comparison worker thread")
            
            # Load CSV mappings
            if not self._load_csv_mappings():
                self.comparison_error.emit("Failed to load CSV mappings")
                return
            
            if not self.file_mappings:
                self.comparison_error.emit("No valid file mappings found in CSV")
                return
            
            # Validate files exist
            self._validate_files()
            
            if not self.file_mappings:
                self.comparison_error.emit("No valid file pairs found to compare")
                return
            
            total_files = len(self.file_mappings)
            logger.info(f"Starting comparison of {total_files} file pairs")
            
            # Compare all files
            for idx, mapping in enumerate(self.file_mappings, 1):
                # Check if cancelled
                if self.is_cancelled:
                    logger.info("Comparison cancelled by user")
                    return
                
                # Update progress
                file_name = f"{mapping['dev']} ↔ {mapping['prod']}"
                percentage = (idx / total_files) * 100
                self.progress_updated.emit(idx, total_files, file_name, percentage)
                
                logger.info(f"[{idx}/{total_files}] Comparing: {mapping['dev']} vs {mapping['prod']}")
                
                # Run comparison
                try:
                    if(app_state.get_file_type() == 'pdf'):
                        comparator = PDFComparator(
                            str(mapping['dev_path']),
                            str(mapping['prod_path']),
                            str(self.output_folder)
                        )
                    elif(app_state.get_file_type() == 'excel'):
                        comparator = ExcelComparator(
                            str(mapping['dev_path']),
                            str(mapping['prod_path']),
                            str(self.output_folder),
                            80
                        )
                    elif(app_state.get_file_type() == 'txt'):
                        comparator = TXTComparator(
                            str(mapping['dev_path']),
                            str(mapping['prod_path']),
                            str(self.output_folder),
                            80
                        )
                    
                    report_path, analytics = comparator.compare()
                    
                    if report_path:
                        file_info = {
                            'index': idx,
                            'total': total_files,
                            'dev_filename': mapping['dev'],
                            'prod_filename': mapping['prod'],
                            'report_path': report_path,
                            'analytics': analytics,
                            'status': 'success'
                        }
                        
                        self.comparison_results.append(file_info)
                        self.file_completed.emit(file_info)
                        
                        logger.info(f"Successfully compared: {mapping['dev']}")
                    else:
                        logger.error(f"Comparison failed for: {mapping['dev']}")
                        
                    # Cleanup
                    del comparator
                    gc.collect()
                    
                except Exception as e:
                    error_msg = f"Error comparing {mapping['dev']}: {str(e)}"
                    logger.error(error_msg)
                    self.file_completed.emit({
                        'index': idx,
                        'total': total_files,
                        'dev_filename': mapping['dev'],
                        'prod_filename': mapping['prod'],
                        'status': 'error',
                        'error': str(e)
                    })
            
            # Check if cancelled before generating summary
            if self.is_cancelled:
                return
            
            # Generate master summary
            logger.info("Generating master summary report...")
            summary_path = self._generate_summary()
            
            if summary_path:
                logger.info(f"Master summary generated: {summary_path}")
                self.comparison_complete.emit(summary_path)
            else:
                self.comparison_error.emit("Failed to generate master summary")
                
        except Exception as e:
            error_msg = f"Critical error in comparison worker: {str(e)}"
            logger.exception(error_msg)
            self.comparison_error.emit(error_msg)
    
    def _load_csv_mappings(self) -> bool:
        """Load file mappings from CSV"""
        try:
            if not self.csv_file.exists():
                logger.error(f"CSV file not found: {self.csv_file}")
                return False
            
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                if reader.fieldnames is None:
                    logger.error("CSV file is empty")
                    return False
                
                # Normalize column names
                fieldnames = [col.strip().lower() for col in reader.fieldnames]
                
                dev_col = None
                prod_col = None
                
                # Find dev and prod columns
                for col in fieldnames:
                    if 'dev' in col and 'filename' in col:
                        dev_col = reader.fieldnames[fieldnames.index(col)]
                    elif 'prod' in col and 'filename' in col:
                        prod_col = reader.fieldnames[fieldnames.index(col)]
                
                if not dev_col or not prod_col:
                    logger.error("CSV must have 'Dev Filename' and 'Prod Filename' columns")
                    return False
                
                # Read all rows
                for row in reader:
                    dev_filename = row[dev_col].strip()
                    prod_filename = row[prod_col].strip()
                    
                    if dev_filename and prod_filename:
                        self.file_mappings.append({
                            'dev': dev_filename,
                            'prod': prod_filename
                        })
                
                logger.info(f"Loaded {len(self.file_mappings)} file mappings from CSV")
                return True
                
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return False
    
    def _validate_files(self):
        """Validate that files exist"""
        valid_mappings = []
        self.missing_files = []  # reset
        
        for mapping in self.file_mappings:
            dev_path = self.dev_folder / mapping['dev']
            prod_path = self.prod_folder / mapping['prod']
            
            if dev_path.exists() and prod_path.exists():
                valid_mappings.append({
                    'dev': mapping['dev'],
                    'prod': mapping['prod'],
                    'dev_path': dev_path,
                    'prod_path': prod_path
                })
            else:
                # build an informative error message
                error_msg = []
                if not dev_path.exists():
                    error_msg.append(f"Dev missing: {mapping['dev']}")
                if not prod_path.exists():
                    error_msg.append(f"Prod missing: {mapping['prod']}")
                missing_entry = {
                    'dev': mapping.get('dev'),
                    'prod': mapping.get('prod'),
                    'error': ' | '.join(error_msg)
                }
                self.missing_files.append(missing_entry)
                logger.warning(f"Skipping - File not found: {mapping['dev']} or {mapping['prod']}")
        
        # replace working mappings with only valid ones
        self.file_mappings = valid_mappings
        logger.info(f"Validated {len(valid_mappings)} file pairs")

        # NEW: notify UI of skipped mappings so ComparisonRunner can print them
        if self.missing_files:
            self.skipped_mappings.emit(self.missing_files)
    
    def _generate_summary(self) -> str:
        """Generate master summary report"""
        try:
            summary_path = ""
            if(app_state.get_file_type() == 'pdf'):
                summary_gen = PdfSummaryGenerator(str(self.output_folder))
                summary_path = summary_gen.generate_summary()
            elif(app_state.get_file_type() == 'excel'):
                summary_gen = ExcelSummaryGenerator(str(self.output_folder))
                summary_path = summary_gen.generate_summary()
            elif(app_state.get_file_type() == 'txt'):
                summary_gen = TxtSummaryGenerator(str(self.output_folder))
                summary_path = summary_gen.generate_summary()            
            return summary_path
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return ""
    
    def cancel(self):
        """Cancel the comparison process"""
        logger.info("Cancellation requested")
        self.is_cancelled = True