"""
Folder Picker Widget
Reusable widget for selecting folders and files with validation
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from pathlib import Path
import csv

from utils.logger import get_logger
from core.state_manager import app_state
import config


logger = get_logger(__name__)


class FolderPickerWidget(QWidget):
    """
    Reusable folder/file picker widget with validation feedback
    
    Signals:
        path_changed: Emitted when path changes (path, count, is_valid)
    """
    
    # Signal: (path: str, count: int, is_valid: bool)
    path_changed = pyqtSignal(str, int, bool)
    
    def __init__(self, label: str, placeholder: str = "", 
                 folder_mode: bool = True, file_filter: str = "",
                 parent=None, empty_folder=False):
        """
        Initialize folder picker widget
        
        Args:
            label: Label text for the widget
            placeholder: Placeholder text for the input field
            folder_mode: True for folder selection, False for file selection
            file_filter: File filter for file selection (e.g., "CSV Files (*.csv)")
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.folder_mode = folder_mode
        self.file_filter = file_filter
        self._current_path = ""
        self._file_count = 0
        self._is_valid = False
        self.empty_folder = empty_folder
        
        self._setup_ui(label, placeholder)
        self._connect_signals()
    
    def _setup_ui(self, label: str, placeholder: str):
        """Set up the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)
        
        # Label
        self.label = QLabel(label)
        label_font = self.label.font()
        label_font.setBold(True)
        self.label.setFont(label_font)
        main_layout.addWidget(self.label)
        
        # Input row
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        
        # Path input field
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(placeholder)
        self.path_input.setReadOnly(False)
        self.path_input.textChanged.connect(self._on_path_text_changed)
        input_layout.addWidget(self.path_input, stretch=1)
        
        # Browse button
        self.browse_button = QPushButton("📁 Browse")
        self.browse_button.setMinimumWidth(100)
        self.browse_button.clicked.connect(self._on_browse_clicked)
        input_layout.addWidget(self.browse_button)
        
        main_layout.addLayout(input_layout)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #999999; font-size: 12px;")
        main_layout.addWidget(self.status_label)
    
    def _connect_signals(self):
        """Connect internal signals"""
        pass
    
    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================
    
    def _on_browse_clicked(self):
        """Handle browse button click"""
        if self.folder_mode:
            self._browse_folder()
        else:
            self._browse_file()
    
    def _on_path_text_changed(self, text: str):
        """Handle manual text input in path field"""
        # Only validate if user pressed Enter or field loses focus
        # This prevents validation on every keystroke
        pass
    
    def _browse_folder(self):
        """Open folder selection dialog"""
        # Get last used folder for this file type if available
        last_folder = ""
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            last_folder,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder:
            self._set_path(folder)
    
    def _browse_file(self):
        """Open file selection dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            self.file_filter
        )
        
        if file_path:
            self._set_path(file_path)
    
    # ========================================================================
    # PATH MANAGEMENT
    # ========================================================================
    
    def _set_path(self, path: str):
        """
        Set the path and validate it
        
        Args:
            path: Path to set
        """
        self._current_path = path
        self.path_input.setText(path)
        self._validate_path()
    
    def _validate_path(self):
        """Validate the current path"""
        if not self._current_path:
            self._set_status("", False)
            return

        path = Path(self._current_path)

        if self.folder_mode:
            if self.empty_folder:
                # For empty-folder mode, explicitely set file_count to 0,
                # update status and allow the signal emission below to run.
                try:
                    is_empty = not any(path.iterdir())
                except Exception:
                    # Path may not exist / permission error
                    self._set_status("❌ Folder does not exist or cannot be accessed", False)
                    self._file_count = 0
                    # emit signal about invalid path
                    self.path_changed.emit(self._current_path, self._file_count, self._is_valid)
                    return

                self._file_count = 0
                if not path.exists() or not path.is_dir():
                    self._set_status("❌ Folder does not exist", False)
                elif not is_empty:
                    self._set_status("❌ Folder is not empty", False)
                else:
                    self._set_status("✅ Folder is empty", True)
            else:
                self._validate_folder(path)
        else:
            self._validate_file(path)

        # Emit signal
        self.path_changed.emit(self._current_path, self._file_count, self._is_valid)


    def _validate_folder(self, path: Path):
        """
        Validate folder path and count files
        
        Args:
            path: Path to validate
        """
        if not path.exists():
            self._set_status("❌ Folder does not exist", False)
            return
        
        if not path.is_dir():
            self._set_status("❌ Not a valid folder", False)
            return
        
        # Count files based on selected file type
        file_type = app_state.get_file_type()
        extensions = config.FILE_TYPES.get(file_type, {}).get("extensions", [])
        
        file_count = 0
        if extensions:
            for ext in extensions:
                file_count += len(list(path.glob(f"*{ext}")))
        else:
            # Count all files if no extensions specified
            file_count = len([f for f in path.iterdir() if f.is_file()])
        
        self._file_count = file_count
        
        if file_count == 0:
            self._set_status(f"⚠️ No matching files found", False)
        else:
            self._set_status(f"✅ {file_count} file(s) found", True)
    
    def _validate_file(self, path: Path):
        """
        Validate file path
        
        Args:
            path: Path to validate
        """
        if not path.exists():
            self._set_status("❌ File does not exist", False)
            return
        
        if not path.is_file():
            self._set_status("❌ Not a valid file", False)
            return
        
        # If CSV file, count mappings
        if path.suffix.lower() == '.csv':
            mapping_count = self._count_csv_mappings(path)
            self._file_count = mapping_count
            
            if mapping_count == 0:
                self._set_status("⚠️ No valid mappings found in CSV", False)
            else:
                self._set_status(f"✅ {mapping_count} file pair(s) mapped", True)
        else:
            self._file_count = 1
            self._set_status("✅ File selected", True)
    
    def _count_csv_mappings(self, csv_path: Path) -> int:
        """
        Count valid mappings in CSV file
        
        Args:
            csv_path: Path to CSV file
            
        Returns:
            Number of valid mappings
        """
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Check if required columns exist (case-insensitive)
                if not reader.fieldnames:
                    return 0
                
                fieldnames_lower = [col.lower().strip() for col in reader.fieldnames]
                
                required_columns = [col.lower() for col in config.CSV_REQUIRED_COLUMNS]
                
                if not all(col in fieldnames_lower for col in required_columns):
                    logger.warning(f"CSV missing required columns: {config.CSV_REQUIRED_COLUMNS}")
                    return 0
                
                # Count valid rows (non-empty dev and prod filenames)
                valid_count = 0
                for row in reader:
                    # Get values with case-insensitive column names
                    row_lower = {k.lower().strip(): v for k, v in row.items()}
                    
                    dev_file = row_lower.get('dev filename', '').strip()
                    prod_file = row_lower.get('prod filename', '').strip()
                    
                    if dev_file and prod_file:
                        valid_count += 1
                
                return valid_count
                
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return 0
    
    def _set_status(self, message: str, is_valid: bool):
        """
        Set status message and validation state
        
        Args:
            message: Status message to display
            is_valid: Whether the path is valid
        """
        self.status_label.setText(message)
        self._is_valid = is_valid
        
        # Update style based on validation state
        if not message:
            self.path_input.setStyleSheet("")
        elif is_valid:
            self.path_input.setStyleSheet("border-color: #28a745;")
            self.status_label.setStyleSheet("color: #28a745; font-size: 12px;")
        else:
            self.path_input.setStyleSheet("border-color: #dc3545;")
            self.status_label.setStyleSheet("color: #dc3545; font-size: 12px;")
    
    # ========================================================================
    # PUBLIC METHODS
    # ========================================================================
    
    def get_path(self) -> str:
        """Get the current path"""
        return self._current_path
    
    def get_file_count(self) -> int:
        """Get the file count"""
        return self._file_count
    
    def is_valid(self) -> bool:
        """Check if current path is valid"""
        return self._is_valid
    
    def clear(self):
        """Clear the path"""
        self._current_path = ""
        self._file_count = 0
        self._is_valid = False
        self.path_input.clear()
        self.status_label.clear()
        self.path_input.setStyleSheet("")