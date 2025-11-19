"""
File Type Selection Card Widget
Clickable card widget for selecting file type
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QCursor, QPalette, QColor

import config
from utils.constants import CARD_WIDTH, CARD_HEIGHT


class FileTypeCard(QWidget):
    """
    A clickable card widget for file type selection.
    Displays icon, title, and description.
    """
    
    # Signal emitted when card is clicked
    clicked = pyqtSignal(str)  # Emits file_type
    
    def __init__(self, file_type: str, parent=None):
        super().__init__(parent)
        
        self.file_type = file_type
        self.file_config = config.FILE_TYPES.get(file_type, {})
        
        self._is_hovered = False
        self._setup_ui()
        self._apply_styling()
    
    def _setup_ui(self):
        """Set up the widget UI"""
        # Set fixed size
        self.setFixedSize(QSize(CARD_WIDTH, CARD_HEIGHT))
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)
        
        # Icon label
        self.icon_label = QLabel(self.file_config.get("icon", "📄"))
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setProperty("class", "card-icon")
        icon_font = self.icon_label.font()
        icon_font.setPointSize(48)
        self.icon_label.setFont(icon_font)
        layout.addWidget(self.icon_label)
        
        # Add spacing
        layout.addSpacing(8)
        
        # Title label
        self.title_label = QLabel(self.file_config.get("name", "File Type"))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setProperty("class", "card-title")
        self.title_label.setWordWrap(True)
        title_font = self.title_label.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        layout.addWidget(self.title_label)
        
        # Description label
        self.description_label = QLabel(self.file_config.get("description", ""))
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setProperty("class", "card-description")
        self.description_label.setWordWrap(True)
        desc_font = self.description_label.font()
        desc_font.setPointSize(11)
        self.description_label.setFont(desc_font)
        layout.addWidget(self.description_label)
        
        # Add stretch to push content to center
        layout.addStretch()
    
    def _apply_styling(self):
        """Apply custom styling to the card"""
        self.setProperty("class", "card-clickable")
        
        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#ffffff"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
    
    def mousePressEvent(self, event):
        """Handle mouse press event"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.file_type)
            # Visual feedback - slightly darken
            self._apply_pressed_style()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release event"""
        if self._is_hovered:
            self._apply_hover_style()
        else:
            self._apply_normal_style()
    
    def enterEvent(self, event):
        """Handle mouse enter event (hover)"""
        self._is_hovered = True
        self._apply_hover_style()
    
    def leaveEvent(self, event):
        """Handle mouse leave event"""
        self._is_hovered = False
        self._apply_normal_style()
    
    def _apply_normal_style(self):
        """Apply normal (non-hovered) style"""
        self.setStyleSheet("""
            QWidget[class="card-clickable"] {
                background-color: white;
                border: 3px solid #e0e0e0;
                border-radius: 16px;
            }
        """)
    
    def _apply_hover_style(self):
        """Apply hover style"""
        color = self.file_config.get("color", "#667eea")
        self.setStyleSheet(f"""
            QWidget[class="card-clickable"] {{
                background-color: #f8f9ff;
                border: 3px solid {color};
                border-radius: 16px;
            }}
        """)
    
    def _apply_pressed_style(self):
        """Apply pressed style"""
        self.setStyleSheet("""
            QWidget[class="card-clickable"] {
                background-color: #e8e9f5;
                border: 3px solid #667eea;
                border-radius: 16px;
            }
        """)
    
    def get_file_type(self) -> str:
        """Get the file type of this card"""
        return self.file_type