"""
Application Signals Hub
Centralized PyQt signals for communication between components
"""

from PyQt5.QtCore import QObject, pyqtSignal


class AppSignals(QObject):
    """
    Global signal hub for application-wide communication.
    All signals are defined here to avoid circular imports.
    """
    
    # ========================================================================
    # NAVIGATION SIGNALS
    # ========================================================================
    navigate_to_screen = pyqtSignal(str)  # screen_name
    go_back = pyqtSignal()
    go_forward = pyqtSignal()
    
    # ========================================================================
    # FILE TYPE SELECTION SIGNALS
    # ========================================================================
    file_type_selected = pyqtSignal(str)  # file_type ("pdf", "excel", "txt")
    
    # ========================================================================
    # FOLDER SELECTION SIGNALS
    # ========================================================================
    dev_folder_selected = pyqtSignal(str)  # folder_path
    prod_folder_selected = pyqtSignal(str)  # folder_path
    csv_file_selected = pyqtSignal(str)  # csv_path
    output_folder_selected = pyqtSignal(str)  # output_path
    
    # ========================================================================
    # VALIDATION SIGNALS
    # ========================================================================
    validation_started = pyqtSignal()
    validation_progress = pyqtSignal(dict)  # {step, message, progress}
    validation_complete = pyqtSignal(bool, list)  # (success, errors)
    
    # ========================================================================
    # COMPARISON SIGNALS
    # ========================================================================
    comparison_started = pyqtSignal()
    comparison_progress = pyqtSignal(dict)  # Progress data
    comparison_file_complete = pyqtSignal(dict)  # File comparison result
    comparison_complete = pyqtSignal(str)  # master_summary_path
    comparison_error = pyqtSignal(str)  # error_message
    comparison_cancelled = pyqtSignal()
    
    # ========================================================================
    # STATUS & MESSAGE SIGNALS
    # ========================================================================
    show_message = pyqtSignal(str, str, str)  # (title, message, type)
    update_status = pyqtSignal(str)  # status_text
    show_notification = pyqtSignal(str, str)  # (title, message)
    
    # ========================================================================
    # REPORT SIGNALS
    # ========================================================================
    report_generated = pyqtSignal(str)  # report_path
    open_report = pyqtSignal(str)  # report_path
    refresh_reports = pyqtSignal()
    
    # ========================================================================
    # SETTINGS SIGNALS
    # ========================================================================
    settings_changed = pyqtSignal(dict)  # settings_dict
    theme_changed = pyqtSignal(str)  # theme_name
    
    # ========================================================================
    # ERROR SIGNALS
    # ========================================================================
    error_occurred = pyqtSignal(str, str)  # (error_type, error_message)
    critical_error = pyqtSignal(str)  # error_message


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================
# Single instance to be imported everywhere
signals = AppSignals()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def emit_info(message: str):
    """Emit an info message"""
    signals.show_message.emit("Information", message, "info")


def emit_success(message: str):
    """Emit a success message"""
    signals.show_message.emit("Success", message, "success")


def emit_warning(message: str):
    """Emit a warning message"""
    signals.show_message.emit("Warning", message, "warning")


def emit_error(message: str):
    """Emit an error message"""
    signals.show_message.emit("Error", message, "error")


def navigate_to(screen_name: str):
    """Navigate to a specific screen"""
    signals.navigate_to_screen.emit(screen_name)


def update_status(text: str):
    """Update status bar text"""
    signals.update_status.emit(text)