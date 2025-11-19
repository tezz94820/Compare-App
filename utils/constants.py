"""
Constants and Enumerations
Centralized constants for the application
"""

from enum import Enum, auto


# ============================================================================
# ENUMS
# ============================================================================

class FileType(Enum):
    """File types supported by the application"""
    PDF = "pdf"
    EXCEL = "excel"
    TXT = "txt"


class ComparisonStatus(Enum):
    """Status of comparison process"""
    IDLE = auto()
    VALIDATING = auto()
    RUNNING = auto()
    PAUSED = auto()
    COMPLETED = auto()
    ERROR = auto()
    CANCELLED = auto()


class MessageType(Enum):
    """Types of messages to show to user"""
    INFO = auto()
    SUCCESS = auto()
    WARNING = auto()
    ERROR = auto()


class ScreenName(Enum):
    """Application screen identifiers"""
    FILE_TYPE_SELECTOR = "file_type_selector"
    FOLDER_SELECTOR = "folder_selector"
    COMPARISON_RUNNER = "comparison_runner"
    REPORT_VIEWER = "report_viewer"


# ============================================================================
# UI CONSTANTS
# ============================================================================

# Colors
COLOR_PRIMARY = "#667eea"
COLOR_SECONDARY = "#764ba2"
COLOR_SUCCESS = "#28a745"
COLOR_WARNING = "#ffc107"
COLOR_ERROR = "#dc3545"
COLOR_INFO = "#17a2b8"

# Card dimensions
CARD_WIDTH = 280
CARD_HEIGHT = 200
CARD_SPACING = 20

# Button sizes
BUTTON_HEIGHT_SMALL = 32
BUTTON_HEIGHT_MEDIUM = 40
BUTTON_HEIGHT_LARGE = 48

# Icon sizes
ICON_SIZE_SMALL = 16
ICON_SIZE_MEDIUM = 24
ICON_SIZE_LARGE = 48
ICON_SIZE_XLARGE = 64

# Font sizes
FONT_SIZE_SMALL = 11
FONT_SIZE_NORMAL = 13
FONT_SIZE_MEDIUM = 15
FONT_SIZE_LARGE = 18
FONT_SIZE_XLARGE = 24
FONT_SIZE_TITLE = 32

# Spacing
SPACING_SMALL = 8
SPACING_MEDIUM = 16
SPACING_LARGE = 24
SPACING_XLARGE = 32

# Border radius
RADIUS_SMALL = 4
RADIUS_MEDIUM = 8
RADIUS_LARGE = 12
RADIUS_XLARGE = 16


# ============================================================================
# COMPARISON CONSTANTS
# ============================================================================

# File validation
MIN_FILE_SIZE_BYTES = 1  # 1 byte minimum
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB

# Progress updates
PROGRESS_UPDATE_THROTTLE_MS = 50  # Minimum time between progress updates

# CSV validation
CSV_REQUIRED_COLUMNS = ["dev filename", "prod filename"]  # Case-insensitive
CSV_MAX_MAPPINGS = 1000  # Maximum number of file pairs


# ============================================================================
# STATUS MESSAGES
# ============================================================================

STATUS_IDLE = "Ready"
STATUS_VALIDATING = "Validating files..."
STATUS_COMPARING = "Comparing files..."
STATUS_GENERATING_REPORTS = "Generating reports..."
STATUS_COMPLETE = "Comparison complete"
STATUS_ERROR = "An error occurred"
STATUS_CANCELLED = "Comparison cancelled"


# ============================================================================
# ERROR MESSAGES
# ============================================================================

ERROR_NO_FILES_FOUND = "No files found in the selected folder"
ERROR_CSV_NOT_FOUND = "CSV mapping file not found"
ERROR_CSV_INVALID = "Invalid CSV file format"
ERROR_FILE_TOO_LARGE = "File size exceeds maximum limit ({} MB)"
ERROR_INVALID_FILE_TYPE = "Invalid file type selected"
ERROR_FOLDER_NOT_EXIST = "Selected folder does not exist"
ERROR_NO_WRITE_PERMISSION = "No write permission for output directory"


# ============================================================================
# SUCCESS MESSAGES
# ============================================================================

SUCCESS_VALIDATION_COMPLETE = "Validation completed successfully"
SUCCESS_COMPARISON_COMPLETE = "Comparison completed successfully"
SUCCESS_REPORTS_GENERATED = "Reports generated successfully"


# ============================================================================
# FILE ICONS (Emoji fallbacks)
# ============================================================================

ICON_PDF = "📄"
ICON_EXCEL = "📊"
ICON_TXT = "📝"
ICON_FOLDER = "📁"
ICON_CSV = "📋"
ICON_SUCCESS = "✅"
ICON_ERROR = "❌"
ICON_WARNING = "⚠️"
ICON_INFO = "ℹ️"
ICON_LOADING = "⏳"
ICON_SETTINGS = "⚙️"
ICON_BACK = "⬅️"
ICON_FORWARD = "➡️"
ICON_REFRESH = "🔄"
ICON_SEARCH = "🔍"
ICON_REPORT = "📊"
ICON_HOME = "🏠"


# ============================================================================
# KEYBOARD SHORTCUTS
# ============================================================================

SHORTCUT_QUIT = "Ctrl+Q"
SHORTCUT_NEW_COMPARISON = "Ctrl+N"
SHORTCUT_OPEN_REPORTS = "Ctrl+O"
SHORTCUT_SETTINGS = "Ctrl+,"
SHORTCUT_REFRESH = "F5"
SHORTCUT_BACK = "Backspace"
SHORTCUT_HELP = "F1"