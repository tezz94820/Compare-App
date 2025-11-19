"""
Application State Manager
Centralized state management for the application
"""

from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass, field
from datetime import datetime

from utils.constants import FileType, ComparisonStatus


@dataclass
class ComparisonSession:
    """Data class for a single comparison session"""
    session_id: str
    file_type: str
    dev_folder: Path
    prod_folder: Path
    csv_file: Path
    output_folder: Path
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    status: ComparisonStatus = ComparisonStatus.IDLE
    total_files: int = 0
    completed_files: int = 0
    master_summary_path: Optional[Path] = None
    individual_reports: List[Path] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class AppState:
    """
    Centralized application state manager.
    Single source of truth for all application state.
    """
    
    def __init__(self):
        # Current screen
        self.current_screen: str = "file_type_selector"
        self.screen_history: List[str] = []
        
        # File type selection
        self.selected_file_type: Optional[str] = None
        
        # Folder selections
        self.dev_folder: Optional[Path] = None
        self.prod_folder: Optional[Path] = None
        self.csv_file: Optional[Path] = None
        self.output_folder: Optional[Path] = None
        
        # Validation state
        self.is_validated: bool = False
        self.validation_errors: List[str] = []
        self.dev_files_count: int = 0
        self.prod_files_count: int = 0
        self.csv_mappings_count: int = 0
        self.output_folder_count:int = 0
        
        # Comparison state
        self.comparison_status: ComparisonStatus = ComparisonStatus.IDLE
        self.current_file_index: int = 0
        self.total_files: int = 0
        self.current_file_name: str = ""
        self.start_time: Optional[datetime] = None
        self.estimated_time_remaining: Optional[int] = None
        
        # Results
        self.current_session: Optional[ComparisonSession] = None
        self.completed_reports: List[Path] = []
        self.master_summary_path: Optional[Path] = None
        
        # Settings
        self.theme: str = "light"
        self.auto_open_reports: bool = True
        self.show_progress_details: bool = True
        
        # Recent comparisons
        self.recent_sessions: List[ComparisonSession] = []
    
    # ========================================================================
    # NAVIGATION METHODS
    # ========================================================================
    
    def navigate_to(self, screen_name: str):
        """Navigate to a screen and update history"""
        if self.current_screen != screen_name:
            self.screen_history.append(self.current_screen)
            self.current_screen = screen_name
    
    def can_go_back(self) -> bool:
        """Check if can navigate back"""
        return len(self.screen_history) > 0
    
    def go_back(self) -> Optional[str]:
        """Go back to previous screen"""
        if self.can_go_back():
            previous_screen = self.screen_history.pop()
            self.current_screen = previous_screen
            return previous_screen
        return None
    
    # ========================================================================
    # FILE TYPE METHODS
    # ========================================================================
    
    def set_file_type(self, file_type: str):
        """Set the selected file type"""
        if file_type in ["pdf", "excel", "txt"]:
            self.selected_file_type = file_type
            return True
        return False
    
    def get_file_type(self) -> Optional[str]:
        """Get the currently selected file type"""
        return self.selected_file_type
    
    # ========================================================================
    # FOLDER SELECTION METHODS
    # ========================================================================
    
    def set_dev_folder(self, folder_path: str):
        """Set dev folder path"""
        self.dev_folder = Path(folder_path) if folder_path else None
    
    def set_prod_folder(self, folder_path: str):
        """Set prod folder path"""
        self.prod_folder = Path(folder_path) if folder_path else None
    
    def set_csv_file(self, csv_path: str):
        """Set CSV file path"""
        self.csv_file = Path(csv_path) if csv_path else None
    
    def set_output_folder(self, output_path: str):
        """Set output folder path"""
        self.output_folder = Path(output_path) if output_path else None
    
    def are_folders_selected(self) -> bool:
        """Check if all required folders are selected"""
        return all([
            self.dev_folder,
            self.prod_folder,
            self.csv_file
        ])
    
    # ========================================================================
    # VALIDATION METHODS
    # ========================================================================
    
    def set_validation_result(self, success: bool, errors: List[str] = None):
        """Set validation results"""
        self.is_validated = success
        self.validation_errors = errors or []
    
    def set_file_counts(self, dev_count: int, prod_count: int, csv_count: int):
        """Set validated file counts"""
        self.dev_files_count = dev_count
        self.prod_files_count = prod_count
        self.csv_mappings_count = csv_count
    
    # ========================================================================
    # COMPARISON METHODS
    # ========================================================================
    
    def start_comparison(self, total_files: int):
        """Start a new comparison"""
        self.comparison_status = ComparisonStatus.RUNNING
        self.total_files = total_files
        self.current_file_index = 0
        self.start_time = datetime.now()
        
        # Create new session
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_session = ComparisonSession(
            session_id=session_id,
            file_type=self.selected_file_type,
            dev_folder=self.dev_folder,
            prod_folder=self.prod_folder,
            csv_file=self.csv_file,
            output_folder=self.output_folder,
            total_files=total_files
        )
    
    def update_progress(self, current_index: int, current_file: str = ""):
        """Update comparison progress"""
        self.current_file_index = current_index
        self.current_file_name = current_file
        
        if self.current_session:
            self.current_session.completed_files = current_index
    
    def complete_comparison(self, master_summary_path: str):
        """Mark comparison as complete"""
        self.comparison_status = ComparisonStatus.COMPLETED
        self.master_summary_path = Path(master_summary_path)
        
        if self.current_session:
            self.current_session.status = ComparisonStatus.COMPLETED
            self.current_session.end_time = datetime.now()
            self.current_session.master_summary_path = Path(master_summary_path)
            self.recent_sessions.insert(0, self.current_session)
            
            # Keep only last 10 sessions
            self.recent_sessions = self.recent_sessions[:10]
    
    def cancel_comparison(self):
        """Cancel ongoing comparison"""
        self.comparison_status = ComparisonStatus.CANCELLED
        if self.current_session:
            self.current_session.status = ComparisonStatus.CANCELLED
            self.current_session.end_time = datetime.now()
    
    def set_comparison_error(self, error_message: str):
        """Set comparison error"""
        self.comparison_status = ComparisonStatus.ERROR
        if self.current_session:
            self.current_session.status = ComparisonStatus.ERROR
            self.current_session.errors.append(error_message)
    
    # ========================================================================
    # RESET METHODS
    # ========================================================================
    
    def reset_for_new_comparison(self):
        """Reset state for a new comparison"""
        self.selected_file_type = None
        self.dev_folder = None
        self.prod_folder = None
        self.csv_file = None
        self.output_folder = None
        self.is_validated = False
        self.validation_errors = []
        self.dev_files_count = 0
        self.prod_files_count = 0
        self.csv_mappings_count = 0
        self.comparison_status = ComparisonStatus.IDLE
        self.current_file_index = 0
        self.total_files = 0
        self.current_file_name = ""
        self.start_time = None
        self.completed_reports = []
        self.master_summary_path = None
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def get_progress_percentage(self) -> float:
        """Get comparison progress as percentage"""
        if self.total_files == 0:
            return 0.0
        return (self.current_file_index / self.total_files) * 100
    
    def get_elapsed_time(self) -> Optional[int]:
        """Get elapsed time in seconds"""
        if self.start_time:
            return int((datetime.now() - self.start_time).total_seconds())
        return None
    
    def to_dict(self) -> dict:
        """Convert state to dictionary for saving"""
        return {
            "theme": self.theme,
            "auto_open_reports": self.auto_open_reports,
            "show_progress_details": self.show_progress_details,
            "recent_sessions": [
                {
                    "session_id": s.session_id,
                    "file_type": s.file_type,
                    "timestamp": s.start_time.isoformat(),
                    "total_files": s.total_files,
                    "status": s.status.name
                }
                for s in self.recent_sessions
            ]
        }


# ============================================================================
# GLOBAL STATE INSTANCE
# ============================================================================
# Single instance to be imported everywhere
app_state = AppState()