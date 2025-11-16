import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QPushButton, QLabel, QTextEdit, QFileDialog, 
                              QMessageBox, QProgressBar, QTabWidget)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QFont
import time


class WorkerThread(QThread):
    """Test worker thread that simulates work"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    
    def run(self):
        for i in range(101):
            time.sleep(0.05)  # Simulate work
            self.progress.emit(i)
        self.finished.emit("Test completed successfully!")


class TestApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('PyQt5 Test Application')
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('🚀 PyQt5 Test Application')
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Tab widget
        tabs = QTabWidget()
        
        # Tab 1: Basic Controls
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        
        # Info label
        info_label = QLabel('Click buttons to test functionality:')
        tab1_layout.addWidget(info_label)
        
        # Test buttons
        btn_messagebox = QPushButton('Test MessageBox')
        btn_messagebox.clicked.connect(self.test_messagebox)
        tab1_layout.addWidget(btn_messagebox)
        
        btn_folder = QPushButton('Test Folder Dialog')
        btn_folder.clicked.connect(self.test_folder_dialog)
        tab1_layout.addWidget(btn_folder)
        
        btn_file = QPushButton('Test File Dialog')
        btn_file.clicked.connect(self.test_file_dialog)
        tab1_layout.addWidget(btn_file)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        tab1_layout.addWidget(self.progress_bar)
        
        btn_progress = QPushButton('Test Progress Bar (Threading)')
        btn_progress.clicked.connect(self.test_progress)
        tab1_layout.addWidget(btn_progress)
        
        # Text output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumHeight(150)
        tab1_layout.addWidget(self.output)
        
        tab1_layout.addStretch()
        tab1.setLayout(tab1_layout)
        tabs.addTab(tab1, "Basic Tests")
        
        # Tab 2: Web Engine Test
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        
        web_label = QLabel('Testing QWebEngineView (HTML Report Viewer):')
        tab2_layout.addWidget(web_label)
        
        self.web_view = QWebEngineView()
        test_html = """
        <html>
        <head>
            <style>
                body { font-family: Arial; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
                .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                h1 { color: #667eea; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>✅ WebEngine Working!</h1>
                <p>If you can see this styled page, QWebEngineView is working correctly.</p>
                <p>This is how your comparison reports will be displayed inside the application.</p>
            </div>
        </body>
        </html>
        """
        self.web_view.setHtml(test_html)
        tab2_layout.addWidget(self.web_view)
        
        tab2.setLayout(tab2_layout)
        tabs.addTab(tab2, "Web View Test")
        
        layout.addWidget(tabs)
        
        # Status
        self.status = QLabel('Status: Ready')
        self.status.setStyleSheet('color: green; font-weight: bold;')
        layout.addWidget(self.status)
        
        central_widget.setLayout(layout)
        
        self.log("Application started successfully!")
        self.log("All imports working correctly!")
        
    def test_messagebox(self):
        QMessageBox.information(self, 'Test', '✅ MessageBox is working!')
        self.log("MessageBox test: PASSED")
        
    def test_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.log(f"Folder selected: {folder}")
            QMessageBox.information(self, 'Success', f'Selected: {folder}')
        else:
            self.log("Folder selection cancelled")
            
    def test_file_dialog(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Select File', '', 'All Files (*.*)')
        if file:
            self.log(f"File selected: {file}")
            QMessageBox.information(self, 'Success', f'Selected: {file}')
        else:
            self.log("File selection cancelled")
            
    def test_progress(self):
        self.log("Starting threading test...")
        self.status.setText('Status: Running...')
        self.status.setStyleSheet('color: orange; font-weight: bold;')
        
        self.worker = WorkerThread()
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.work_finished)
        self.worker.start()
        
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        
    def work_finished(self, message):
        self.log(message)
        self.log("Threading test: PASSED")
        self.status.setText('Status: Ready')
        self.status.setStyleSheet('color: green; font-weight: bold;')
        QMessageBox.information(self, 'Test Complete', message)
        
    def log(self, message):
        self.output.append(f"[{time.strftime('%H:%M:%S')}] {message}")


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = TestApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()