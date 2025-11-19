"""
Comparison Runner Screen
Third screen where the actual comparison happens with progress tracking
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTextEdit, QScrollArea, QFrame,
                            QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont
from pathlib import Path
import webbrowser

import config
from utils.signals import signals
from utils.logger import get_logger
from core.state_manager import app_state
from workers.comparison_worker import ComparisonWorker
from ui.widgets.progress_widget import ProgressWidget


logger = get_logger(__name__)


class ComparisonRunnerScreen(QWidget):
    """
    Screen 3: Comparison Runner
    
    Displays progress and runs the comparison in background thread.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.worker = None
        self.completed_files = []
        
        self._setup_ui()
        self._connect_signals()
        
        logger.info("Comparison Runner screen initialized")
    
    def _setup_ui(self):
        """Set up the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Header section
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)
        
        # Progress section
        progress_section = self._create_progress_section()
        main_layout.addWidget(progress_section)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Activity log section
        log_section = self._create_log_section()
        main_layout.addWidget(log_section, stretch=1)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Button section
        button_layout = self._create_button_section()
        main_layout.addLayout(button_layout)
    
    def _create_header(self) -> QVBoxLayout:
        """Create the header section"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("⚡ Comparison in Progress")
        title.setAlignment(Qt.AlignCenter)
        title_font = title.font()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #667eea;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Please wait while we compare your files...")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle_font = subtitle.font()
        subtitle_font.setPointSize(14)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #666666;")
        layout.addWidget(subtitle)
        
        return layout
    
    def _create_progress_section(self) -> QFrame:
        """Create the progress display section"""
        # Container frame
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 30px;
                border: 2px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(20)
        
        # Progress widget
        self.progress_widget = ProgressWidget()
        layout.addWidget(self.progress_widget)
        
        return frame
    
    def _create_log_section(self) -> QFrame:
        """Create the activity log section"""
        # Container frame
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
                border: 2px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(12)
        
        # Section title
        title = QLabel("📋 Activity Log")
        title_font = title.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #667eea;")
        layout.addWidget(title)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                color: #333333;
            }
        """)
        layout.addWidget(self.log_text)
        
        return frame
    
    def _create_button_section(self) -> QHBoxLayout:
        """Create the button section"""
        layout = QHBoxLayout()
        layout.setSpacing(12)
        
        # Cancel button
        self.cancel_button = QPushButton("⏸️ Cancel")
        self.cancel_button.setProperty("class", "danger")
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.clicked.connect(self._on_cancel_clicked)
        layout.addWidget(self.cancel_button)
        
        # Add spacer
        layout.addSpacerItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )
        
        # View Reports button (initially hidden)
        self.view_reports_button = QPushButton("📊 View Reports")
        self.view_reports_button.setProperty("class", "success")
        self.view_reports_button.setMinimumWidth(150)
        self.view_reports_button.setVisible(False)
        self.view_reports_button.clicked.connect(self._on_view_reports_clicked)
        layout.addWidget(self.view_reports_button)
        
        # New Comparison button (initially hidden)
        self.new_comparison_button = QPushButton("🔄 New Comparison")
        self.new_comparison_button.setMinimumWidth(150)
        self.new_comparison_button.setVisible(False)
        self.new_comparison_button.clicked.connect(self._on_new_comparison_clicked)
        layout.addWidget(self.new_comparison_button)
        
        return layout
    
    def _connect_signals(self):
        """Connect signals and slots"""
        signals.comparison_started.connect(self._on_comparison_started)
    
    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================
    
    @pyqtSlot()
    def _on_comparison_started(self):
        """Handle comparison started signal"""
        logger.info("Comparison started signal received")
        self._start_comparison()
    
    def _start_comparison(self):
        """Start the comparison process"""
        # Reset UI
        self.log_text.clear()
        self.completed_files = []
        self.cancel_button.setVisible(True)
        self.view_reports_button.setVisible(False)
        self.new_comparison_button.setVisible(False)
        
        # Log start
        self._log_message("🚀 Starting comparison process...")
        self._log_message(f"📁 Dev Folder: {app_state.dev_folder}")
        self._log_message(f"📁 Prod Folder: {app_state.prod_folder}")
        self._log_message(f"📋 CSV File: {app_state.csv_file}")
        self._log_message(f"📂 Output Folder: {app_state.output_folder}")
        self._log_message("-" * 80)
        
        # Create and start worker thread
        self.worker = ComparisonWorker(
            dev_folder=str(app_state.dev_folder),
            prod_folder=str(app_state.prod_folder),
            csv_file=str(app_state.csv_file),
            output_folder=str(app_state.output_folder)
        )
        
        # Connect worker signals
        self.worker.progress_updated.connect(self._on_progress_updated)
        self.worker.file_completed.connect(self._on_file_completed)
        self.worker.comparison_complete.connect(self._on_comparison_complete)
        self.worker.comparison_error.connect(self._on_comparison_error)
        if hasattr(self.worker, 'skipped_mappings'):
            self.worker.skipped_mappings.connect(self._on_skipped_mappings)
        
        # Start progress widget
        self.progress_widget.start_progress(app_state.csv_mappings_count)
        
        # Start worker thread
        self.worker.start()
        
        # Update app state
        app_state.start_comparison(app_state.csv_mappings_count)
        
        logger.info("Comparison worker thread started")
    
    @pyqtSlot(int, int, str, float)
    def _on_progress_updated(self, current: int, total: int, file_name: str, percentage: float):
        """Handle progress update from worker"""
        # Update progress widget
        self.progress_widget.update_progress(current, total, file_name, percentage)
        
        # Update app state
        app_state.update_progress(current, file_name)
        
        # Log progress
        if current <= total:
            self._log_message(f"[{current}/{total}] Comparing: {file_name}")

    
    @pyqtSlot(list)
    def _on_skipped_mappings(self, missing_list: list):
        """Receive skipped mappings from worker and print them into Activity Log"""
        try:
            if not missing_list:
                return

            self._log_message("-" * 80)
            self._log_message(f"⚠️ Skipped {len(missing_list)} mappings due to missing files:")
            for miss in missing_list:
                dev = miss.get('dev', '<unknown>')
                prod = miss.get('prod', '<unknown>')
                err = miss.get('error', 'Missing file')
                # log a clear line that will be visible in Activity Log
                self._log_message(f"    • Dev: {dev}  |  Prod: {prod}  → {err}")
            self._log_message("-" * 80)
        except Exception as e:
            logger.exception(f"Failed to log skipped mappings: {e}")

    
    @pyqtSlot(dict)
    def _on_file_completed(self, file_info: dict):
        """Handle individual file completion"""
        if file_info.get('status') == 'success':
            analytics = file_info.get('analytics', {})
            similarity = analytics.get('similarity_percent', 0)
            
            self._log_message(
                f"  ✅ Completed: {file_info['dev_filename']} "
                f"(Similarity: {similarity}%)"
            )
            
            self.completed_files.append(file_info)
        else:
            error = file_info.get('error', 'Unknown error')
            self._log_message(
                f"  ❌ Error: {file_info['dev_filename']} - {error}"
            )
    
    @pyqtSlot(str)
    def _on_comparison_complete(self, master_summary_path: str):
        """Handle comparison completion"""
        logger.info(f"Comparison complete. Summary: {master_summary_path}")
        
        # Stop progress widget
        self.progress_widget.set_complete()
        
        # Update app state
        app_state.complete_comparison(master_summary_path)
        
        # Log completion
        self._log_message("-" * 80)
        self._log_message("🎉 Comparison completed successfully!")
        self._log_message(f"📊 Total files compared: {len(self.completed_files)}")
        self._log_message(f"📁 Master summary: {master_summary_path}")
        self._log_message("-" * 80)
        
        # Update UI
        self.cancel_button.setVisible(False)
        self.view_reports_button.setVisible(True)
        self.new_comparison_button.setVisible(True)
        
        # Update status
        signals.update_status.emit("Comparison completed successfully")
        
        # Show success message
        signals.show_message.emit(
            "Success",
            f"Comparison completed! {len(self.completed_files)} files processed.",
            "success"
        )
    
    @pyqtSlot(str)
    def _on_comparison_error(self, error_message: str):
        """Handle comparison error"""
        logger.error(f"Comparison error: {error_message}")
        
        # Stop progress widget
        self.progress_widget.set_error(error_message)
        
        # Update app state
        app_state.set_comparison_error(error_message)
        
        # Log error
        self._log_message("-" * 80)
        self._log_message(f"❌ Error occurred: {error_message}")
        self._log_message("-" * 80)
        
        # Update UI
        self.cancel_button.setText("← Back")
        self.cancel_button.setProperty("class", "secondary")
        self.cancel_button.style().unpolish(self.cancel_button)
        self.cancel_button.style().polish(self.cancel_button)
        
        # Show error message
        signals.show_message.emit(
            "Error",
            f"Comparison failed: {error_message}",
            "error"
        )
    
    def _on_cancel_clicked(self):
        """Handle cancel button click"""
        if self.worker and self.worker.isRunning():
            logger.info("Cancelling comparison...")
            
            # Cancel worker
            self.worker.cancel()
            self.worker.wait()  # Wait for thread to finish
            
            # Update progress widget
            self.progress_widget.set_cancelled()
            
            # Update app state
            app_state.cancel_comparison()
            
            # Log cancellation
            self._log_message("-" * 80)
            self._log_message("⚠️ Comparison cancelled by user")
            self._log_message("-" * 80)
            
            # Update UI
            self.cancel_button.setText("← Back")
            self.cancel_button.setProperty("class", "secondary")
            self.cancel_button.style().unpolish(self.cancel_button)
            self.cancel_button.style().polish(self.cancel_button)
            self.new_comparison_button.setVisible(True)
        else:
            # Go back to folder selector
            signals.go_back.emit()
    
    def _on_view_reports_clicked(self):
        """Handle view reports button click"""
        if app_state.master_summary_path:
            # Open master summary in browser
            summary_path = Path(app_state.master_summary_path)
            if summary_path.exists():
                webbrowser.open(f"file://{summary_path.absolute()}")
                logger.info(f"Opened master summary: {summary_path}")
            else:
                logger.error(f"Master summary not found: {summary_path}")
                signals.show_message.emit(
                    "Error",
                    "Master summary report not found",
                    "error"
                )
    
    def _on_new_comparison_clicked(self):
        """Handle new comparison button click"""
        # Reset app state
        app_state.reset_for_new_comparison()
        
        # Navigate to file type selector
        signals.navigate_to_screen.emit(config.SCREEN_FILE_TYPE_SELECTOR)
        
        logger.info("Starting new comparison")
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def _log_message(self, message: str):
        """Add message to activity log"""
        self.log_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    # ========================================================================
    # SCREEN EVENTS
    # ========================================================================
    
    def showEvent(self, event):
        """Handle show event - called when screen becomes visible"""
        super().showEvent(event)
        
        # Update status bar
        signals.update_status.emit("Comparison in progress...")
        
        logger.debug("Comparison Runner screen shown")
    
    def hideEvent(self, event):
        """Handle hide event - called when screen becomes hidden"""
        super().hideEvent(event)
        logger.debug("Comparison Runner screen hidden")