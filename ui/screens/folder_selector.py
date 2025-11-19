"""
Folder Selector Screen
Second screen where users select dev/prod folders and CSV mapping file
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QFileDialog, QGroupBox,
                            QSpacerItem, QSizePolicy, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from pathlib import Path

import config
from utils.signals import signals
from utils.logger import get_logger
from core.state_manager import app_state
from ui.widgets.folder_picker import FolderPickerWidget


logger = get_logger(__name__)


class FolderSelectorScreen(QWidget):
    """
    Screen 2: Folder and CSV Selection
    
    Allows users to:
    - Select Dev folder (source files)
    - Select Prod folder (target files)
    - Select CSV mapping file
    - Optionally set output location
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
        
        logger.info("Folder Selector screen initialized")
    
    def _setup_ui(self):
        """Set up the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Header section
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Folder selection section
        folder_section = self._create_folder_section()
        main_layout.addWidget(folder_section)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Output location section
        output_section = self._create_output_section()
        main_layout.addWidget(output_section)
        
        # Add spacer
        main_layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        
        # Button section
        button_layout = self._create_button_section()
        main_layout.addLayout(button_layout)
    
    def _create_header(self) -> QVBoxLayout:
        """Create the header section"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)
        
        # Title
        self.title_label = QLabel("📄 File Comparison Setup") 
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setProperty("class", "section-title")
        title_font = self.title_label.font()
        title_font.setPointSize(50)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        
        # Subtitle
        subtitle = QLabel("Select the folders and mapping file for comparison")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle_font = subtitle.font()
        subtitle_font.setPointSize(18)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #666666;")
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)
        
        return layout
    
    def _create_folder_section(self) -> QGroupBox:
        """Create the folder selection section"""
        group = QGroupBox("Folder Selection")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(16)
        
        # Dev Folder
        self.dev_folder_picker = FolderPickerWidget(
            label="Step 1: Select Dev Folder",
            placeholder="Select the folder containing development files",
            folder_mode=True
        )
        self.dev_folder_picker.path_changed.connect(self._on_dev_folder_changed)
        group_layout.addWidget(self.dev_folder_picker)
        
        # Prod Folder
        self.prod_folder_picker = FolderPickerWidget(
            label="Step 2: Select Prod Folder",
            placeholder="Select the folder containing production files",
            folder_mode=True
        )
        self.prod_folder_picker.setDisabled(True)   # disable prod until dev selected
        self.prod_folder_picker.setToolTip("Select the Dev folder first")
        self.prod_folder_picker.path_changed.connect(self._on_prod_folder_changed)
        group_layout.addWidget(self.prod_folder_picker)
        
        # --- Download sample mappings link ---
        self.download_sample_label = QLabel('<a href="#">Download sample mappings file</a>')
        self.download_sample_label.setToolTip("Download a sample CSV you can edit")
        self.download_sample_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.download_sample_label.setOpenExternalLinks(False)
        self.download_sample_label.linkActivated.connect(self._on_download_sample_mappings_clicked)
        self.download_sample_label.setAlignment(Qt.AlignLeft)  # left align above Step 3
        self.download_sample_label.setStyleSheet(
            "QLabel { color: #1a73e8; text-decoration: underline; font-weight: 500; margin-bottom: 4px; }"
        )

        # Add the link above the Step 3 widget
        group_layout.addWidget(self.download_sample_label)

        # --- CSV Mapping File (original picker) ---
        self.csv_file_picker = FolderPickerWidget(
            label="Step 3: Select CSV Mapping File",
            placeholder="Select the CSV file with file name mappings",
            folder_mode=False,
            file_filter="CSV Files (*.csv)"
        )
        self.csv_file_picker.setDisabled(True)
        self.csv_file_picker.setToolTip("Select the Prod folder first")
        self.csv_file_picker.path_changed.connect(self._on_csv_file_changed)

        group_layout.addWidget(self.csv_file_picker)

        
        return group
    
    def _create_output_section(self) -> QGroupBox:
        """Create the output location section"""
        group = QGroupBox("Output Location (Empty Folder)")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(12)
        
        # Output folder picker
        self.output_folder_picker = FolderPickerWidget(
            label="Step 4: Select Output Location",
            placeholder="Please select an empty folder",
            folder_mode=True,
            empty_folder=True
        )
        self.output_folder_picker.setDisabled(True)   # disable Output folder until mappings is selected
        self.output_folder_picker.setToolTip("Select the CSV file first")
        self.output_folder_picker.path_changed.connect(self._on_output_folder_changed)
        group_layout.addWidget(self.output_folder_picker)
        
        return group
    
    def _create_button_section(self) -> QHBoxLayout:
        """Create the button section"""
        layout = QHBoxLayout()
        layout.setSpacing(12)
        
        # Back button
        self.back_button = QPushButton("← Back")
        self.back_button.setProperty("class", "secondary")
        self.back_button.setMinimumWidth(120)
        self.back_button.clicked.connect(self._on_back_clicked)
        layout.addWidget(self.back_button)
        
        # Add spacer
        layout.addSpacerItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )
        
        # Start Comparison button
        self.start_button = QPushButton("Start Comparison →")
        self.start_button.setProperty("class", "success")
        self.start_button.setMinimumWidth(200)
        self.start_button.setEnabled(False)  # Disabled until all fields are filled
        self.start_button.clicked.connect(self._on_start_clicked)
        layout.addWidget(self.start_button)
        
        return layout
    
    def _connect_signals(self):
        """Connect signals and slots"""
        # No additional signals needed for now
        pass
    
    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================
    
    def _on_dev_folder_changed(self, folder_path: str, file_count: int, is_valid: bool):
        """Handle dev folder selection change"""
        if is_valid:
            app_state.set_dev_folder(folder_path)
            app_state.dev_files_count = file_count
            logger.info(f"Dev folder selected: {folder_path} ({file_count} files)")
            signals.update_status.emit(f"Dev folder selected: {file_count} files found")
            # enable Prod picker, but keep CSV disabled until Prod is selected
            self.prod_folder_picker.setDisabled(False)
            # When Dev changes, clear downstream selections
            self.prod_folder_picker.clear()
            self.csv_file_picker.clear()
            app_state.set_prod_folder("")   # reset state
            app_state.set_csv_file("")
            app_state.prod_files_count = 0
            app_state.csv_mappings_count = 0
            self.prod_folder_picker.setToolTip("")  # remove warning
        else:
            app_state.set_dev_folder("")
            app_state.dev_files_count = 0
            self.prod_folder_picker.clear()
            self.prod_folder_picker.setDisabled(True)
            self.csv_file_picker.clear()
            self.csv_file_picker.setDisabled(True)
            app_state.set_prod_folder("")
            app_state.set_csv_file("")
            app_state.prod_files_count = 0
            app_state.csv_mappings_count = 0
            self.prod_folder_picker.setToolTip("Select the Dev folder first")
        
        self._validate_form()
    
    def _on_prod_folder_changed(self, folder_path: str, file_count: int, is_valid: bool):
        """Handle prod folder selection change"""
        if is_valid:
            app_state.set_prod_folder(folder_path)
            app_state.prod_files_count = file_count
            logger.info(f"Prod folder selected: {folder_path} ({file_count} files)")
            signals.update_status.emit(f"Prod folder selected: {file_count} files found")
            # enable CSV picker, clear previous CSV
            self.csv_file_picker.setDisabled(False)
            self.csv_file_picker.clear()
            app_state.set_csv_file("")   # reset csv state
            app_state.csv_mappings_count = 0
            self.csv_file_picker.setToolTip("")
        else:
            app_state.set_prod_folder("")
            app_state.prod_files_count = 0
            self.csv_file_picker.clear()
            self.csv_file_picker.setDisabled(True)
            app_state.set_csv_file("")
            app_state.csv_mappings_count = 0
            self.csv_file_picker.setToolTip("Select the Prod folder first")
        
        self._validate_form()
    
    def _on_csv_file_changed(self, csv_path: str, mapping_count: int, is_valid: bool):
        """Handle CSV file selection change"""
        if is_valid:
            app_state.set_csv_file(csv_path)
            app_state.csv_mappings_count = mapping_count
            logger.info(f"CSV file selected: {csv_path} ({mapping_count} mappings)")
            signals.update_status.emit(f"CSV file selected: {mapping_count} file pairs mapped")
            self.output_folder_picker.setDisabled(False)
            self.output_folder_picker.setToolTip("")
        else:
            app_state.set_csv_file("")
            app_state.csv_mappings_count = 0
            self.output_folder_picker.clear()
            app_state.set_output_folder("")
        
        self._validate_form()

    def _on_download_sample_mappings_clicked(self, _=None):
        """
        Handler for download sample link. Opens Save dialog and writes a small example CSV.
        """
        try:
            # Suggest a default filename (in user's Documents)
            from pathlib import Path
            default_dir = str(Path.home() / "Documents")
            default_name = "sample_mappings.csv"
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save sample mappings file",
                str(Path(default_dir) / default_name),
                "CSV Files (*.csv)"
            )

            if not save_path:
                # user cancelled save
                return

            # Build sample rows: header + one example mapping row
            import csv
            header = config.CSV_REQUIRED_COLUMNS
            # Provide a simple example row. Adjust filename examples to match selected file type
            file_type = app_state.get_file_type() or "txt"
            example_dev = f"example_dev{'.pdf' if file_type=='pdf' else ('.xlsx' if file_type=='excel' else '.txt')}"
            example_prod = f"example_prod{'.pdf' if file_type=='pdf' else ('.xlsx' if file_type=='excel' else '.txt')}"
            sample_row = ["1", example_dev, example_prod]

            # Write CSV
            with open(save_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerow(sample_row)

            # Notify user (use your signals infrastructure)
            signals.show_message.emit(
                "Sample Saved",
                f"Sample mappings file saved to:\n{save_path}",
                "success"
            )

        except Exception as e:
            logger.exception(f"Failed to create sample mappings file: {e}")
            signals.show_message.emit(
                "Error",
                f"Could not save sample mappings file:\n{e}",
                "error"
            )

    
    def _on_output_folder_changed(self, folder_path: str, file_count: int, is_valid: bool):
        """Handle output folder selection change"""
        if is_valid:
            app_state.set_output_folder(folder_path)
            app_state.output_folder_count = file_count
            logger.info(f"Output folder selected: {folder_path}")
        else:
            app_state.set_output_folder("")
            app_state.output_folder_count = 0
            logger.info(f"Output folder invalid/cleared: {folder_path}")
            signals.update_status.emit("Output folder invalid or not empty")

        self._validate_form()

    def _on_back_clicked(self):
        """Handle back button click"""
        logger.info("Navigating back to file type selector")
        signals.go_back.emit()
    
    def _on_start_clicked(self):
        """Handle start comparison button click"""
        # Final validation
        if not self._validate_form():
            signals.show_message.emit(
                "Validation Error",
                "Please fill in all required fields",
                "error"
            )
            return
        
        logger.info("Starting comparison process")
        signals.update_status.emit("Starting comparison...")
        
        # Navigate to comparison runner screen
        signals.navigate_to_screen.emit(config.SCREEN_COMPARISON_RUNNER)
        
        # Emit comparison started signal
        signals.comparison_started.emit()
    
    # ========================================================================
    # VALIDATION
    # ========================================================================
    
    def _validate_form(self) -> bool:
        # require dev -> prod -> csv sequence
        dev_ok = bool(app_state.dev_folder and app_state.dev_files_count > 0)
        prod_ok = bool(app_state.prod_folder and app_state.prod_files_count > 0)
        csv_ok = bool(app_state.csv_file and app_state.csv_mappings_count > 0)
        output_ok = bool(app_state.output_folder and app_state.output_folder_count == 0)

        is_valid = dev_ok and prod_ok and csv_ok and output_ok

        print("app_state.output_folder",app_state.output_folder)
        print("output_ok",output_ok)
        print("is_valid",is_valid)


        # Make sure UI reflects order (disable any pickers if upstream is missing)
        self.prod_folder_picker.setDisabled(not dev_ok)
        self.csv_file_picker.setDisabled(not (dev_ok and prod_ok))
        self.output_folder_picker.setDisabled(not (dev_ok and prod_ok and csv_ok))

        self.start_button.setEnabled(is_valid)
        return is_valid
    
    # ========================================================================
    # SCREEN EVENTS
    # ========================================================================
    
    def showEvent(self, event):
        """Handle show event - called when screen becomes visible"""
        super().showEvent(event)

        # Clear previous folder/file selections so the screen never "remembers" old paths
        try:
            # Clear UI widgets
            self.dev_folder_picker.clear()
            self.prod_folder_picker.clear()
            self.csv_file_picker.clear()
            self.output_folder_picker.clear()

            # Reset app state folder-related values and counts
            app_state.set_dev_folder("")
            app_state.set_prod_folder("")
            app_state.set_csv_file("")
            app_state.set_output_folder("")

            app_state.dev_files_count = 0
            app_state.prod_files_count = 0
            app_state.csv_mappings_count = 0
            app_state.output_folder_count = 0

            # Ensure downstream pickers are disabled until upstream selections are made
            self.prod_folder_picker.setDisabled(True)
            self.csv_file_picker.setDisabled(True)
            self.output_folder_picker.setDisabled(True)

            # Disable start button until a valid set of selections is made
            self.start_button.setEnabled(False)

        except Exception as e:
            logger.exception(f"Error while resetting Folder Selector on show: {e}")

        # RELOAD file type info on every show (preserve the existing behavior)
        file_type = app_state.get_file_type()
        file_info = config.FILE_TYPES.get(file_type, {})

        icon = file_info.get("icon", "📄")
        name = file_info.get("name", "File")

        self.title_label.setText(f"{icon} {name} Comparison Setup")
        self.title_label.setStyleSheet(f"color: {file_info.get('color', '#667eea')};")

        # Update status bar
        file_type = app_state.get_file_type()
        file_name = config.FILE_TYPES.get(file_type, {}).get("name", "File")
        signals.update_status.emit(f"{file_name} comparison - Select folders and CSV")

        logger.debug("Folder Selector screen shown")

    
    def hideEvent(self, event):
        """Handle hide event - called when screen becomes hidden"""
        super().hideEvent(event)
        logger.debug("Folder Selector screen hidden")