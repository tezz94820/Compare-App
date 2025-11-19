"""
Main Application Window
Container for all screens with navigation management
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QStackedWidget, QStatusBar, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

import config
from utils.signals import signals
from utils.logger import get_logger
from core.state_manager import app_state
from ui.styles.themes import get_complete_stylesheet
from ui.screens.file_type_selector import FileTypeSelectorScreen
from ui.screens.folder_selector import FolderSelectorScreen 
from ui.screens.comparison_runner import ComparisonRunnerScreen



logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window with screen navigation.
    Uses QStackedWidget to switch between different screens.
    """
    
    def __init__(self):
        super().__init__()
        
        self._setup_window()
        self._setup_ui()
        self._apply_theme()
        self._connect_signals()
        
        logger.info("Main window initialized")
    
    def _setup_window(self):
        """Configure main window properties"""
        # Set window title
        self.setWindowTitle(config.WINDOW_TITLE)
        
        # Set window size
        self.setMinimumSize(
            config.WINDOW_MIN_WIDTH,
            config.WINDOW_MIN_HEIGHT
        )
        self.resize(
            config.WINDOW_DEFAULT_WIDTH,
            config.WINDOW_DEFAULT_HEIGHT
        )
        
        # Center window on screen
        self._center_on_screen()
        
        # Set window icon (if available)
        # self.setWindowIcon(QIcon("path/to/icon.png"))
    
    def _setup_ui(self):
        """Set up the user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Stacked widget for screens
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Initialize screens
        self._init_screens()
        
        # Status bar
        self._setup_status_bar()
    
    def _init_screens(self):
        """Initialize and add all application screens"""
        # Screen 1: File Type Selector
        self.file_type_screen = FileTypeSelectorScreen()
        self.stacked_widget.addWidget(self.file_type_screen)
        
        # Screen 2: Folder Selector 
        self.folder_selector_screen = FolderSelectorScreen()
        self.stacked_widget.addWidget(self.folder_selector_screen)
        
        # Screen 3: Comparison Runner 
        self.comparison_screen = ComparisonRunnerScreen()
        self.stacked_widget.addWidget(self.comparison_screen)
        
        # Screen 4: Report Viewer (placeholder for now)
        # self.report_viewer_screen = ReportViewerScreen()
        # self.stacked_widget.addWidget(self.report_viewer_screen)
        
        # Map screen names to indices
        self.screen_indices = {
            config.SCREEN_FILE_TYPE_SELECTOR: 0,
            config.SCREEN_FOLDER_SELECTOR: 1,
            config.SCREEN_COMPARISON_RUNNER: 2,
            # config.SCREEN_REPORT_VIEWER: 3,
        }
        
        # Set initial screen
        self.stacked_widget.setCurrentIndex(0)
    
    def _setup_status_bar(self):
        """Set up the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Set initial status
        self.status_bar.showMessage("Ready")
        
        # Style status bar
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #ffffff;
                border-top: 1px solid #e0e0e0;
                padding: 6px 12px;
            }
        """)
    
    def _apply_theme(self):
        """Apply application theme"""
        theme = app_state.theme
        stylesheet = get_complete_stylesheet(theme)
        self.setStyleSheet(stylesheet)
        
        logger.info(f"Applied {theme} theme")
    
    def _connect_signals(self):
        """Connect signals to slots"""
        # Navigation signals
        signals.navigate_to_screen.connect(self._navigate_to_screen)
        signals.go_back.connect(self._go_back)
        
        # Status bar signals
        signals.update_status.connect(self._update_status)
        
        # Message signals
        signals.show_message.connect(self._show_message)
        
        # Error signals
        signals.error_occurred.connect(self._handle_error)
        signals.critical_error.connect(self._handle_critical_error)
    
    def _center_on_screen(self):
        """Center the window on the screen"""
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    
    # ========================================================================
    # NAVIGATION METHODS
    # ========================================================================
    
    def _navigate_to_screen(self, screen_name: str):
        """
        Navigate to a specific screen
        
        Args:
            screen_name: Name of the screen to navigate to
        """
        if screen_name in self.screen_indices:
            index = self.screen_indices[screen_name]
            self.stacked_widget.setCurrentIndex(index)
            app_state.navigate_to(screen_name)
            
            logger.info(f"Navigated to screen: {screen_name}")
        else:
            logger.warning(f"Unknown screen name: {screen_name}")
            self._show_message(
                "Navigation Error",
                f"Screen '{screen_name}' not found",
                "error"
            )
    
    def _go_back(self):
        """Navigate back to previous screen"""
        previous_screen = app_state.go_back()
        if previous_screen:
            self._navigate_to_screen(previous_screen)
        else:
            logger.debug("Cannot go back - no previous screen")
    
    # ========================================================================
    # STATUS BAR METHODS
    # ========================================================================
    
    def _update_status(self, message: str):
        """
        Update status bar message
        
        Args:
            message: Status message to display
        """
        self.status_bar.showMessage(message)
    
    # ========================================================================
    # MESSAGE BOX METHODS
    # ========================================================================
    
    def _show_message(self, title: str, message: str, msg_type: str = "info"):
        """
        Show a message box to the user
        
        Args:
            title: Message box title
            message: Message content
            msg_type: Type of message ("info", "success", "warning", "error")
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        # Set icon based on type
        icon_map = {
            "info": QMessageBox.Information,
            "success": QMessageBox.Information,
            "warning": QMessageBox.Warning,
            "error": QMessageBox.Critical
        }
        msg_box.setIcon(icon_map.get(msg_type, QMessageBox.Information))
        
        # Add appropriate button
        msg_box.setStandardButtons(QMessageBox.Ok)
        
        msg_box.exec_()
        
        logger.info(f"Showed {msg_type} message: {title}")
    
    def _handle_error(self, error_type: str, error_message: str):
        """
        Handle non-critical errors
        
        Args:
            error_type: Type of error
            error_message: Error message
        """
        logger.error(f"{error_type}: {error_message}")
        self._show_message(error_type, error_message, "error")
    
    def _handle_critical_error(self, error_message: str):
        """
        Handle critical errors
        
        Args:
            error_message: Critical error message
        """
        logger.critical(f"Critical error: {error_message}")
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Critical Error")
        msg_box.setText("A critical error occurred:")
        msg_box.setInformativeText(error_message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setStandardButtons(QMessageBox.Ok)
        
        msg_box.exec_()
    
    # ========================================================================
    # WINDOW EVENTS
    # ========================================================================
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Ask for confirmation if comparison is running
        if app_state.comparison_status.name == "RUNNING":
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "A comparison is currently running. Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                event.ignore()
                return
        
        logger.info("Application closing")
        event.accept()
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        # Escape key to go back
        if event.key() == Qt.Key_Escape:
            self._go_back()
        
        super().keyPressEvent(event)