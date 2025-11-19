"""
Comparison Tool - Main Entry Point
Professional file comparison desktop application
"""

import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

import config
from utils.logger import get_logger, log_info
from ui.main_window import MainWindow


# Initialize logger
logger = get_logger(__name__)


def main():
    """Main application entry point"""
    
    try:
        # Log application startup
        log_info("="*80)
        log_info(f"{config.APP_NAME} v{config.APP_VERSION}")
        log_info("="*80)
        log_info("Application starting...")
        
        # Create Qt Application
        app = QApplication(sys.argv)
        
        # Set application metadata
        app.setApplicationName(config.APP_NAME)
        app.setApplicationVersion(config.APP_VERSION)
        app.setOrganizationName(config.APP_AUTHOR)
        
        # Enable high DPI scaling
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        log_info("Qt Application initialized")
        
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        log_info("Main window displayed")
        log_info("Application ready")
        
        # Start event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.exception(f"Fatal error during application startup: {e}")
        
        # Try to show error dialog if possible
        try:
            from PyQt5.QtWidgets import QMessageBox
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowTitle("Fatal Error")
            error_msg.setText("Application failed to start")
            error_msg.setInformativeText(str(e))
            error_msg.setStandardButtons(QMessageBox.Ok)
            error_msg.exec_()
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()