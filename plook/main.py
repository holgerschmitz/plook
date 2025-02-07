# plook/main.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QFileDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel, QComboBox,
    QLineEdit, QCheckBox, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt


class PlotViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plook - Python Data Plotter")

        # --- Create central widget and main layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- File selection controls ---
        file_layout = QHBoxLayout()
        
        self.open_button = QPushButton("Open File(s)")
        self.open_button.clicked.connect(self.open_files)
        file_layout.addWidget(self.open_button)

        main_layout.addLayout(file_layout)

        # --- Selected files list ---
        self.files_list = QListWidget()
        main_layout.addWidget(self.files_list)

        # --- Plot options area ---
        # We'll group these options in a QGroupBox for clarity
        options_group = QGroupBox("Plot Options")
        options_layout = QFormLayout(options_group)

        # 1) X column selection
        self.x_column_combo = QComboBox()
        self.x_column_combo.addItem("Column 1")  # placeholder
        self.x_column_combo.addItem("Column 2")  # placeholder
        options_layout.addRow(QLabel("X Column:"), self.x_column_combo)

        # 2) Y column selection
        self.y_column_combo = QComboBox()
        self.y_column_combo.addItem("Column 2")  # placeholder
        self.y_column_combo.addItem("Column 3")  # placeholder
        options_layout.addRow(QLabel("Y Column:"), self.y_column_combo)

        # 3) Plot style (lines, points, dots)
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Lines", "Points", "Dots"])
        options_layout.addRow(QLabel("Plot Style:"), self.style_combo)

        # 4) X range (optional text fields for min, max)
        x_range_box = QHBoxLayout()
        self.xmin_edit = QLineEdit()
        self.xmin_edit.setPlaceholderText("xmin")
        self.xmax_edit = QLineEdit()
        self.xmax_edit.setPlaceholderText("xmax")
        x_range_box.addWidget(self.xmin_edit)
        x_range_box.addWidget(self.xmax_edit)
        options_layout.addRow(QLabel("X Range:"), x_range_box)

        # 5) Y range (optional text fields for min, max)
        y_range_box = QHBoxLayout()
        self.ymin_edit = QLineEdit()
        self.ymin_edit.setPlaceholderText("ymin")
        self.ymax_edit = QLineEdit()
        self.ymax_edit.setPlaceholderText("ymax")
        y_range_box.addWidget(self.ymin_edit)
        y_range_box.addWidget(self.ymax_edit)
        options_layout.addRow(QLabel("Y Range:"), y_range_box)

        # 6) Log scale checkboxes
        self.logx_check = QCheckBox("Log Scale X")
        self.logy_check = QCheckBox("Log Scale Y")
        log_box = QHBoxLayout()
        log_box.addWidget(self.logx_check)
        log_box.addWidget(self.logy_check)
        options_layout.addRow(QLabel("Log Scale:"), log_box)

        main_layout.addWidget(options_group)

        # --- Plot button (optional if you want manual plotting) ---
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_data)
        main_layout.addWidget(self.plot_button)

        # --- Status Bar (optional) ---
        self.statusBar().showMessage("Ready")

    def open_files(self):
        """
        Opens a file dialog to select one or more data files.
        For now, we just display them in the QListWidget.
        """
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Data Files",
            "",
            "Data Files (*.txt *.dat *.csv);;All Files (*)"
        )
        if files:
            self.files_list.clear()
            for f in files:
                self.files_list.addItem(f)
            # Here is where you might detect columns, etc.

    def plot_data(self):
        """
        Placeholder slot for the 'Plot' button click.
        You would integrate PyGnuplot or other logic here.
        """
        self.statusBar().showMessage("Plotting data... (not implemented yet)")
        # Example: read the combos, ranges, checks, etc. and call your plot logic.


def main():
    app = QApplication(sys.argv)
    viewer = PlotViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
