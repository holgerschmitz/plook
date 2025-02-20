import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QLabel,
)
from .ui import (
    FileBrowserWidget, 
    PlotWidget, 
    PlotOptionsWidget,
)

# run with 
# poetry run python -m plook.main

class MainWindow(QMainWindow):
    """
    The main window that ties it all together.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plook - Simple Plot Viewer")
        self.setGeometry(100, 100, 1000, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout: file browser on the left, plot & options in the middle/right
        main_layout = QHBoxLayout(main_widget)

        # 1) File Browser Widget
        self.file_browser = FileBrowserWidget()
        self.file_browser.fileDoubleClicked.connect(self.on_file_selected)

        # 2) Plot Widget
        self.plot_widget = PlotWidget()

        # 3) Plot Options Widget
        self.options_widget = PlotOptionsWidget()
        self.options_widget.plotRequested.connect(self.on_plot_requested)

        # A list to keep track of selected files
        self.selected_files_list = QListWidget()
        self.selected_files_list.setFixedWidth(200)

        # Put the file browser on the far left
        main_layout.addWidget(self.file_browser, stretch=1)

        # Next: a vertical container for the selected-files list & the plot area
        center_layout = QVBoxLayout()
        center_layout.addWidget(QLabel("Selected Files:"))
        center_layout.addWidget(self.selected_files_list)
        center_layout.addWidget(self.plot_widget, stretch=1)

        main_layout.addLayout(center_layout, stretch=2)

        # Finally, the plot options on the right
        main_layout.addWidget(self.options_widget, stretch=0)

        self.statusBar().showMessage("Ready")

    def on_file_selected(self, file_path: str):
        """
        Called when the user double-clicks a file in the FileBrowserWidget.
        We add it to the 'selected_files_list' if not already present.
        """
        for i in range(self.selected_files_list.count()):
            if self.selected_files_list.item(i).text() == file_path:
                return  # Already in the list
        self.selected_files_list.addItem(file_path)

    def on_plot_requested(self):
        """
        Called when the user clicks the 'Plot' button in the PlotOptionsWidget.
        We gather the selected files and the user settings, then update the PlotWidget.
        """
        # Collect selected files
        selected_files = []
        for i in range(self.selected_files_list.count()):
            selected_files.append(self.selected_files_list.item(i).text())

        # Collect user inputs from the options widget
        x_col = self.options_widget.x_column_combo.currentText()
        y_col = self.options_widget.y_column_combo.currentText()
        style = self.options_widget.style_combo.currentText()
        xmin = self.options_widget.x_min.text()
        xmax = self.options_widget.x_max.text()
        ymin = self.options_widget.y_min.text()
        ymax = self.options_widget.y_max.text()
        logx = self.options_widget.logx_check.isChecked()
        logy = self.options_widget.logy_check.isChecked()

        # Update the placeholder plot
        self.plot_widget.update_plot(
            files=selected_files,
            x_col=x_col,
            y_col=y_col,
            style=style,
            xmin=xmin,
            xmax=xmax,
            ymin=ymin,
            ymax=ymax,
            logx=logx,
            logy=logy
        )

        # Update status bar
        self.statusBar().showMessage("Plot updated")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
