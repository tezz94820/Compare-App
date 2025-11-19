"""
Application Themes and Styles
QSS (Qt Style Sheets) for the application
"""

# ============================================================================
# LIGHT THEME
# ============================================================================

LIGHT_THEME = """
/* Main Window */
QMainWindow {
    background-color: #f5f5f5;
}

/* Central Widget */
QWidget {
    background-color: #f5f5f5;
    color: #333333;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}

/* Buttons */
QPushButton {
    background-color: #667eea;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 600;
    min-height: 40px;
}

QPushButton:hover {
    background-color: #764ba2;
}

QPushButton:pressed {
    background-color: #5568d3;
}

QPushButton:disabled {
    background-color: #cccccc;
    color: #666666;
}

/* Secondary Button */
QPushButton[class="secondary"] {
    background-color: #f0f0f0;
    color: #333333;
    border: 2px solid #e0e0e0;
}

QPushButton[class="secondary"]:hover {
    background-color: #e8e8e8;
    border-color: #d0d0d0;
}

/* Success Button */
QPushButton[class="success"] {
    background-color: #28a745;
}

QPushButton[class="success"]:hover {
    background-color: #218838;
}

/* Danger Button */
QPushButton[class="danger"] {
    background-color: #dc3545;
}

QPushButton[class="danger"]:hover {
    background-color: #c82333;
}

/* Labels */
QLabel {
    color: #333333;
    background: transparent;
}

QLabel[class="title"] {
    font-size: 32px;
    font-weight: 700;
    color: #667eea;
}

QLabel[class="subtitle"] {
    font-size: 16px;
    color: #666666;
}

QLabel[class="section-title"] {
    font-size: 18px;
    font-weight: 600;
    color: #333333;
    padding: 8px 0;
}

/* Line Edit (Input Fields) */
QLineEdit {
    background-color: white;
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    padding: 10px 12px;
    font-size: 13px;
    color: #333333;
}

QLineEdit:focus {
    border-color: #667eea;
}

QLineEdit:disabled {
    background-color: #f5f5f5;
    color: #999999;
}

/* Combo Box (Dropdown) */
QComboBox {
    background-color: white;
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    padding: 8px 12px;
    min-height: 30px;
}

QComboBox:hover {
    border-color: #667eea;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: url(none);
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #666666;
    margin-right: 10px;
}

/* Progress Bar */
QProgressBar {
    background-color: #e9ecef;
    border: none;
    border-radius: 10px;
    height: 20px;
    text-align: center;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #667eea, stop:1 #764ba2);
    border-radius: 10px;
}

/* Scroll Bar */
QScrollBar:vertical {
    background-color: #f0f0f0;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #cccccc;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #999999;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Status Bar */
QStatusBar {
    background-color: #ffffff;
    border-top: 1px solid #e0e0e0;
    color: #666666;
    font-size: 12px;
}

/* Tool Tip */
QToolTip {
    background-color: #333333;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 12px;
}

/* Message Box */
QMessageBox {
    background-color: white;
}

QMessageBox QLabel {
    color: #333333;
    font-size: 13px;
}

/* Splitter */
QSplitter::handle {
    background-color: #e0e0e0;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #667eea;
}

/* Group Box */
QGroupBox {
    background-color: white;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    margin-top: 12px;
    padding: 16px;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #667eea;
}

/* Tab Widget */
QTabWidget::pane {
    background-color: white;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
}

QTabBar::tab {
    background-color: #f0f0f0;
    color: #666666;
    border: none;
    padding: 10px 20px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTabBar::tab:selected {
    background-color: white;
    color: #667eea;
    font-weight: 600;
}

QTabBar::tab:hover {
    background-color: #e8e8e8;
}

/* List Widget */
QListWidget {
    background-color: white;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 8px;
}

QListWidget::item {
    padding: 8px;
    border-radius: 4px;
}

QListWidget::item:selected {
    background-color: #667eea;
    color: white;
}

QListWidget::item:hover {
    background-color: #f0f0f0;
}

/* Tree Widget */
QTreeWidget {
    background-color: white;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
}

QTreeWidget::item {
    padding: 6px;
}

QTreeWidget::item:selected {
    background-color: #667eea;
    color: white;
}

QTreeWidget::item:hover {
    background-color: #f0f0f0;
}
"""


# ============================================================================
# DARK THEME (Future enhancement)
# ============================================================================

DARK_THEME = """
/* Dark theme will be added in future version */
"""


# ============================================================================
# CARD WIDGET STYLE
# ============================================================================

CARD_STYLE = """
QWidget[class="card"] {
    background-color: white;
    border-radius: 16px;
    padding: 24px;
}

QWidget[class="card"]:hover {
    background-color: #fafafa;
}

QWidget[class="card-clickable"] {
    background-color: white;
    border: 3px solid #e0e0e0;
    border-radius: 16px;
    padding: 24px;
}

QWidget[class="card-clickable"]:hover {
    border-color: #667eea;
    background-color: #f8f9ff;
}

QLabel[class="card-icon"] {
    font-size: 64px;
}

QLabel[class="card-title"] {
    font-size: 20px;
    font-weight: 700;
    color: #333333;
}

QLabel[class="card-description"] {
    font-size: 13px;
    color: #666666;
}
"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_theme(theme_name: str = "light") -> str:
    """
    Get the stylesheet for a specific theme
    
    Args:
        theme_name: Name of the theme ("light" or "dark")
    
    Returns:
        Complete stylesheet string
    """
    if theme_name == "dark":
        return DARK_THEME
    return LIGHT_THEME


def get_card_style() -> str:
    """Get the card widget stylesheet"""
    return CARD_STYLE


def get_complete_stylesheet(theme_name: str = "light") -> str:
    """Get complete stylesheet including theme and components"""
    return get_theme(theme_name) + "\n" + get_card_style()