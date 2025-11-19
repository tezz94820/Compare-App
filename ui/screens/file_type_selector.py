"""
File Type Selector Screen
First screen where user selects the type of files to compare
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt

import config
from utils.signals import signals
from utils.logger import get_logger
from core.state_manager import app_state
from ui.widgets.file_type_card import FileTypeCard


logger = get_logger(__name__)


class FileTypeSelectorScreen(QWidget):
    """
    Screen 1: File Type Selection
    
    Allows users to choose between PDF, Excel, or TXT file comparison.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
        
        logger.info("File Type Selector screen initialized")
    
    def _setup_ui(self):
        """Set up the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Add top spacer
        main_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        
        # Header section
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)
        
        # Add spacing
        main_layout.addSpacing(40)
        
        # Cards section
        cards_layout = self._create_cards()
        main_layout.addLayout(cards_layout)
        
        # Add spacing
        main_layout.addSpacing(30)
        
        # Recent comparisons section (optional - can be added later)
        # recent_layout = self._create_recent_section()
        # main_layout.addLayout(recent_layout)
        
        # Add bottom spacer
        main_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
    
    def _create_header(self) -> QVBoxLayout:
        """Create the header section with title and subtitle"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)
        
        # Title
        title = QLabel(config.APP_NAME)
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignCenter)
        title_font = title.font()
        title_font.setPointSize(32)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #667eea;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Select the type of files you want to compare")
        subtitle.setProperty("class", "subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle_font = subtitle.font()
        subtitle_font.setPointSize(14)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #666666;")
        layout.addWidget(subtitle)
        
        return layout
    
    def _create_cards(self) -> QHBoxLayout:
        """Create the file type selection cards"""
        layout = QHBoxLayout()
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignCenter)
        
        # Add left spacer
        layout.addSpacerItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )
        
        # Create cards for each file type
        self.cards = {}
        
        for file_type in ["pdf", "excel", "txt"]:
            card = FileTypeCard(file_type)
            card.clicked.connect(self._on_card_clicked)
            self.cards[file_type] = card
            layout.addWidget(card)
        
        # Add right spacer
        layout.addSpacerItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )
        
        return layout
    
    def _create_recent_section(self) -> QVBoxLayout:
        """Create recent comparisons section (optional)"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Section title
        recent_label = QLabel("Recent Comparisons")
        recent_label.setAlignment(Qt.AlignCenter)
        recent_font = recent_label.font()
        recent_font.setPointSize(12)
        recent_font.setBold(True)
        recent_label.setFont(recent_font)
        recent_label.setStyleSheet("color: #666666;")
        layout.addWidget(recent_label)
        
        # Recent items would be added here dynamically
        # For now, show a message if no recent comparisons
        if not app_state.recent_sessions:
            no_recent = QLabel("No recent comparisons")
            no_recent.setAlignment(Qt.AlignCenter)
            no_recent.setStyleSheet("color: #999999; font-style: italic;")
            layout.addWidget(no_recent)
        
        return layout
    
    def _connect_signals(self):
        """Connect signals and slots"""
        # No external signals needed for this screen yet
        pass
    
    def _on_card_clicked(self, file_type: str):
        """
        Handle card click event
        
        Args:
            file_type: The type of file selected ("pdf", "excel", "txt")
        """
        logger.info(f"File type selected: {file_type}")
        
        # Update application state
        app_state.set_file_type(file_type)
        
        # Emit signal for file type selection
        signals.file_type_selected.emit(file_type)
        
        # Navigate to folder selection screen
        signals.navigate_to_screen.emit(config.SCREEN_FOLDER_SELECTOR)
        
        # Update status
        file_name = config.FILE_TYPES[file_type]["name"]
        signals.update_status.emit(f"{file_name} comparison selected")
    
    def showEvent(self, event):
        """Handle show event - called when screen becomes visible"""
        super().showEvent(event)
        
        # Reset selection visual feedback when returning to this screen
        for card in self.cards.values():
            card._apply_normal_style()
        
        # Update status bar
        signals.update_status.emit("Ready - Select a file type to begin")
        
        logger.debug("File Type Selector screen shown")