"""
Application Configuration
Central configuration file for the Comparison Tool
"""

import os
from pathlib import Path

# ============================================================================
# APPLICATION INFO
# ============================================================================
APP_NAME = "Comparison Tool"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"
APP_DESCRIPTION = "Professional file comparison tool for PDF, Excel, and Text files"

# ============================================================================
# PATHS
# ============================================================================
# Application root directory
BASE_DIR = Path(__file__).parent

# User data directories (in user's Documents folder)
USER_HOME = Path.home()
USER_DOCS = USER_HOME / "Documents"
APP_DATA_DIR = USER_DOCS / APP_NAME

# # Report storage
# REPORTS_DIR = APP_DATA_DIR / "reports"
# PDF_REPORTS_DIR = REPORTS_DIR / "pdf"
# EXCEL_REPORTS_DIR = REPORTS_DIR / "excel"
# TXT_REPORTS_DIR = REPORTS_DIR / "txt"

# Logs
LOGS_DIR = APP_DATA_DIR / "logs"

# Temporary files
TEMP_DIR = APP_DATA_DIR / "temp"

# Settings
SETTINGS_FILE = APP_DATA_DIR / "app_settings.json"

# ============================================================================
# FILE TYPE CONFIGURATIONS
# ============================================================================
FILE_TYPES = {
    "pdf": {
        "name": "PDF Documents",
        "description": "Compare PDF files page by page (.pdf)",
        "extensions": [".pdf"],
        "icon": "📄",
        "color": "#667eea",
        "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    },
    "excel": {
        "name": "Excel Spreadsheets", 
        "description": "Compare Excel files sheet by sheet (.xlsx)",
        "extensions": [".xlsx", ".xls"],
        "icon": "📊",
        "color": "#2ecc71",
        "gradient": "linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)"
    },
    "txt": {
        "name": "Text Files",
        "description": "Compare any text-based files (.txt, .log, .csv, .json, etc.)",
        "extensions": [],
        "icon": "📝",
        "color": "#3498db",
        "gradient": "linear-gradient(135deg, #3498db 0%, #2980b9 100%)"
    }
}

# ============================================================================
# UI SETTINGS
# ============================================================================
# Window settings
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600
WINDOW_DEFAULT_WIDTH = 1200
WINDOW_DEFAULT_HEIGHT = 700

# Screen names
SCREEN_FILE_TYPE_SELECTOR = "file_type_selector"
SCREEN_FOLDER_SELECTOR = "folder_selector"
SCREEN_COMPARISON_RUNNER = "comparison_runner"
SCREEN_REPORT_VIEWER = "report_viewer"

# ============================================================================
# COMPARISON SETTINGS
# ============================================================================
# Maximum file size for comparison (in MB)
MAX_FILE_SIZE_MB = 100

# Progress update frequency (in milliseconds)
PROGRESS_UPDATE_INTERVAL = 100

# Number of recent comparisons to show
MAX_RECENT_COMPARISONS = 10

# ============================================================================
# LOGGING SETTINGS
# ============================================================================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_LOG_FILES = 5
MAX_LOG_SIZE_MB = 10

# ============================================================================
# DEFAULT SETTINGS
# ============================================================================
DEFAULT_SETTINGS = {
    "theme": "light",
    "auto_open_reports": True,
    "show_progress_details": True,
    "save_comparison_history": True,
    "max_recent_comparisons": MAX_RECENT_COMPARISONS,
    "remember_last_folders": True,
    "last_used_folders": {
        "pdf": {"dev": "", "prod": "", "csv": ""},
        "excel": {"dev": "", "prod": "", "csv": ""},
        "txt": {"dev": "", "prod": "", "csv": ""}
    }
}

# csv required folders
CSV_REQUIRED_COLUMNS = ["Sr.No","Dev Filename","Prod Filename"] 