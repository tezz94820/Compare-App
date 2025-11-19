"""
Progress Widget
Beautiful progress display with animations and stats
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QProgressBar, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from utils.logger import get_logger

logger = get_logger(__name__)


class ProgressWidget(QWidget):
    """
    Beautiful progress widget with animations.
    Shows current file, progress bar, and statistics.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_index = 0
        self.total_files = 0
        self.start_time = None
        
        self._setup_ui()
        
        # Timer for elapsed time updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_elapsed_time)
    
    def _setup_ui(self):
        """Set up the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Current file label
        self.current_file_label = QLabel("Preparing comparison...")
        self.current_file_label.setAlignment(Qt.AlignCenter)
        self.current_file_label.setWordWrap(True)
        font = self.current_file_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.current_file_label.setFont(font)
        self.current_file_label.setStyleSheet("color: #667eea; padding: 10px;")
        layout.addWidget(self.current_file_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedHeight(40)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 20px;
                text-align: center;
                font-size: 14px;
                font-weight: bold;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #667eea, stop:1 #764ba2);
                border-radius: 18px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Stats row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        # Files completed
        self.files_label = QLabel("0 / 0 files")
        self.files_label.setAlignment(Qt.AlignCenter)
        font = self.files_label.font()
        font.setPointSize(12)
        self.files_label.setFont(font)
        self.files_label.setStyleSheet("color: #666666;")
        stats_layout.addWidget(self.files_label, 1)
        
        # Elapsed time
        self.time_label = QLabel("Elapsed: 00:00:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        font = self.time_label.font()
        font.setPointSize(12)
        self.time_label.setFont(font)
        self.time_label.setStyleSheet("color: #666666;")
        stats_layout.addWidget(self.time_label, 1)
        
        # Estimated time remaining
        self.eta_label = QLabel("ETA: Calculating...")
        self.eta_label.setAlignment(Qt.AlignCenter)
        font = self.eta_label.font()
        font.setPointSize(12)
        self.eta_label.setFont(font)
        self.eta_label.setStyleSheet("color: #666666;")
        stats_layout.addWidget(self.eta_label, 1)
        
        layout.addLayout(stats_layout)
    
    def start_progress(self, total_files: int):
        """Start progress tracking"""
        from datetime import datetime
        
        self.total_files = total_files
        self.current_index = 0
        self.start_time = datetime.now()
        
        self.progress_bar.setValue(0)
        self.files_label.setText(f"0 / {total_files} files")
        
        # Start timer for elapsed time
        self.timer.start(1000)  # Update every second
        
        logger.info(f"Progress widget started for {total_files} files")
    
    def update_progress(self, current: int, total: int, file_name: str, percentage: float):
        """Update progress display"""
        self.current_index = current
        self.total_files = total
        
        # Update current file
        self.current_file_label.setText(f"📄 {file_name}")
        
        # Update progress bar
        self.progress_bar.setValue(int(percentage))
        
        # Update files count
        self.files_label.setText(f"{current} / {total} files")
        
        # Update ETA
        self._update_eta(current, total)
    
    def _update_elapsed_time(self):
        """Update elapsed time display"""
        if self.start_time:
            from datetime import datetime
            
            elapsed = datetime.now() - self.start_time
            hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            
            self.time_label.setText(f"Elapsed: {hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def _update_eta(self, current: int, total: int):
        """Update estimated time remaining"""
        if current == 0 or not self.start_time:
            self.eta_label.setText("ETA: Calculating...")
            return
        
        from datetime import datetime, timedelta
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        avg_time_per_file = elapsed / current
        remaining_files = total - current
        eta_seconds = int(avg_time_per_file * remaining_files)
        
        if eta_seconds < 60:
            self.eta_label.setText(f"ETA: {eta_seconds}s")
        else:
            minutes, seconds = divmod(eta_seconds, 60)
            if minutes < 60:
                self.eta_label.setText(f"ETA: {minutes}m {seconds}s")
            else:
                hours, minutes = divmod(minutes, 60)
                self.eta_label.setText(f"ETA: {hours}h {minutes}m")
    
    def stop_progress(self):
        """Stop progress tracking"""
        self.timer.stop()
        logger.info("Progress widget stopped")
    
    def set_complete(self):
        """Mark progress as complete"""
        self.timer.stop()
        self.progress_bar.setValue(100)
        self.current_file_label.setText("✅ Comparison Complete!")
        self.current_file_label.setStyleSheet("color: #28a745; padding: 10px;")
        self.eta_label.setText("ETA: Complete")
    
    def set_error(self, error_message: str):
        """Mark progress as error"""
        self.timer.stop()
        self.current_file_label.setText(f"❌ Error: {error_message}")
        self.current_file_label.setStyleSheet("color: #dc3545; padding: 10px;")
    
    def set_cancelled(self):
        """Mark progress as cancelled"""
        self.timer.stop()
        self.current_file_label.setText("⚠️ Comparison Cancelled")
        self.current_file_label.setStyleSheet("color: #ffc107; padding: 10px;")