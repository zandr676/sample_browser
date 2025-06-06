import sys
import os
import re
import pygame
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SampleTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def startDrag(self, supportedActions):
        rows = set(item.row() for item in self.selectedItems())
        if rows:
            drag = QDrag(self)
            mime = QMimeData()

            # Get file paths from selected rows
            urls = []
            for row in rows:
                # File path is stored in column 0's data
                file_path = self.item(row, 0).data(Qt.UserRole)
                if file_path:
                    urls.append(QUrl.fromLocalFile(file_path))

            mime.setUrls(urls)
            drag.setMimeData(mime)
            drag.exec_(Qt.CopyAction)

class SampleBrowser(QMainWindow):
    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        self.samples = []
        self.filtered_samples = []

        # Initialize pygame mixer for audio playback
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.current_playing_row = -1

        self.init_ui()
        self.scan_directory(directory)
        self.filter_samples()

    def init_ui(self):
        self.setWindowTitle("Sample Browser")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_samples)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Filter controls
        filter_layout = QHBoxLayout()

        # BPM filter
        filter_layout.addWidget(QLabel("BPM:"))
        self.bpm_min = QLineEdit()
        self.bpm_min.setMaximumWidth(60)
        self.bpm_min.textChanged.connect(self.filter_samples)
        filter_layout.addWidget(self.bpm_min)

        filter_layout.addWidget(QLabel("to"))
        self.bpm_max = QLineEdit()
        self.bpm_max.setMaximumWidth(60)
        self.bpm_max.textChanged.connect(self.filter_samples)
        filter_layout.addWidget(self.bpm_max)

        # Key filter
        filter_layout.addWidget(QLabel("Key:"))
        self.key_combo = QComboBox()
        self.key_combo.addItems(["All", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
        self.key_combo.currentTextChanged.connect(self.filter_samples)
        filter_layout.addWidget(self.key_combo)

        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # File table
        self.table = SampleTable()
        # Connect single click to play samples
        self.table.itemClicked.connect(self.play_sample)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Filename", "BPM", "Key"])
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        layout.addWidget(self.table)

    def play_sample(self, item):
        """Play or stop sample on single click"""
        row = item.row()

        # If clicking the currently playing sample, stop it
        if row == self.current_playing_row:
            pygame.mixer.music.stop()
            self.current_playing_row = -1
            return

        # Stop any currently playing sample
        pygame.mixer.music.stop()

        # Get file path from first column
        file_path = self.table.item(row, 0).data(Qt.UserRole)

        if file_path:
            try:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                self.current_playing_row = row
            except pygame.error as e:
                print(f"Could not play {file_path}: {e}")
                self.current_playing_row = -1

    def scan_directory(self, directory):
        supported_formats = ('.wav', '.aif', '.aiff', '.mp3', '.flac')

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(supported_formats):
                    file_path = os.path.join(root, file)

                    sample = {
                        'path': file_path,
                        'filename': file,
                        'bpm': self.extract_bpm(file),
                        'key': self.extract_key(file)
                    }

                    self.samples.append(sample)

    def extract_bpm(self, filename):
        # BPM patterns
        patterns = [
            r'(\d{2,3})[\s_-]?bpm',
            r'bpm[\s_-]?(\d{2,3})',
            r'_(\d{2,3})_'
        ]

        for pattern in patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                bpm = int(match.group(1))
                # Reasonable BPM range
                if 60 <= bpm <= 200:
                    return bpm

        return None

    def extract_key(self, filename):
        # Key pattern
        pattern = r'([A-G][#b]?)(m|min|maj|major)?'

        match = re.search(pattern, filename)
        if match:
            key = match.group(1)
            modifier = match.group(2) if match.group(2) else ''

            # Normalize key
            if modifier in ['m', 'min']:
                return key + 'm'
            elif modifier in ['maj', 'major']:
                return key
            else:
                return key

        return None

    def filter_samples(self):
        search_text = self.search_input.text().lower()
        bpm_min_text = self.bpm_min.text()
        bpm_max_text = self.bpm_max.text()
        key_filter = self.key_combo.currentText()

        self.filtered_samples = []

        for sample in self.samples:
            # Search filter
            if search_text and search_text not in sample['filename'].lower():
                continue

            # BPM filter
            if sample['bpm'] is not None:
                if bpm_min_text:
                    try:
                        if sample['bpm'] < int(bpm_min_text):
                            continue
                    except ValueError:
                        pass

                if bpm_max_text:
                    try:
                        if sample['bpm'] > int(bpm_max_text):
                            continue
                    except ValueError:
                        pass
            else:
                # If sample has no BPM and BPM filter is set, skip it
                if bpm_min_text or bpm_max_text:
                    continue

            # Key filter
            if key_filter != "All":
                if sample['key'] is None:
                    continue

                # Normalize key for comparison
                sample_key_root = sample['key'].replace('m', '').replace('min', '').replace('maj', '').replace('major', '')

                # Handle enharmonic equivalents
                enharmonics = {
                    'C#': ['C#', 'Db'],
                    'D#': ['D#', 'Eb'],
                    'F#': ['F#', 'Gb'],
                    'G#': ['G#', 'Ab'],
                    'A#': ['A#', 'Bb']
                }

                if key_filter in enharmonics:
                    if sample_key_root not in enharmonics[key_filter]:
                        continue
                else:
                    if sample_key_root != key_filter:
                        continue

            self.filtered_samples.append(sample)

        self.update_table(self.filtered_samples)

    def update_table(self, filtered_samples):
        # Reset playing state when table updates
        self.current_playing_row = -1
        pygame.mixer.music.stop()

        self.table.setRowCount(0)

        for sample in filtered_samples:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Filename
            filename_item = QTableWidgetItem(sample['filename'])
            filename_item.setData(Qt.UserRole, sample['path'])
            self.table.setItem(row, 0, filename_item)

            # BPM
            bpm_text = str(sample['bpm']) if sample['bpm'] is not None else "-"
            self.table.setItem(row, 1, QTableWidgetItem(bpm_text))

            # Key
            key_text = sample['key'] if sample['key'] is not None else "-"
            self.table.setItem(row, 2, QTableWidgetItem(key_text))

def get_default_splice_directory():
    """Get the default Splice sounds directory for the current user"""
    # Get the home directory using Path.home() for cross-platform compatibility
    home = Path.home()
    splice_dir = home / "Splice" / "sounds"

    # Check if the directory exists
    if splice_dir.exists() and splice_dir.is_dir():
        return str(splice_dir)

    return None

def main():
    app = QApplication(sys.argv)

    # First, check if the default Splice directory exists
    directory = get_default_splice_directory()

    if directory:
        print(f"Found Splice directory at: {directory}")
    else:
        # If default directory doesn't exist, show directory picker
        directory = QFileDialog.getExistingDirectory(None, "Select Sample Directory")

        if not directory:
            sys.exit(0)

    # Create and show main window
    browser = SampleBrowser(directory)
    browser.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
