from PyQt5.QtCore import (
    pyqtSignal,
)
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QCheckBox,
    QGroupBox,
    QFormLayout,
    QPushButton,
)


class PlotOptionsWidget(QWidget):
    """
    A widget that holds all the plot options (columns, ranges, log scale, etc.).
    Emits a signal when the user clicks "Plot."
    """
    plotRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        options_group = QGroupBox("Plot Options")
        options_layout = QFormLayout(options_group)

        # X Column
        self.x_column_combo = QComboBox()
        self.x_column_combo.addItems(["Column 1", "Column 2"])
        options_layout.addRow(QLabel("X Column:"), self.x_column_combo)

        # Y Column
        self.y_column_combo = QComboBox()
        self.y_column_combo.addItems(["Column 2", "Column 3"])
        options_layout.addRow(QLabel("Y Column:"), self.y_column_combo)

        # Plot style
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Lines", "Points", "Dots"])
        options_layout.addRow(QLabel("Plot Style:"), self.style_combo)

        # X range
        x_range_layout = QHBoxLayout()
        self.x_min = QLineEdit()
        self.x_min.setPlaceholderText("xmin")
        self.x_max = QLineEdit()
        self.x_max.setPlaceholderText("xmax")
        x_range_layout.addWidget(self.x_min)
        x_range_layout.addWidget(self.x_max)
        options_layout.addRow(QLabel("X Range:"), x_range_layout)

        # Y range
        y_range_layout = QHBoxLayout()
        self.y_min = QLineEdit()
        self.y_min.setPlaceholderText("ymin")
        self.y_max = QLineEdit()
        self.y_max.setPlaceholderText("ymax")
        y_range_layout.addWidget(self.y_min)
        y_range_layout.addWidget(self.y_max)
        options_layout.addRow(QLabel("Y Range:"), y_range_layout)

        # Log scale
        log_layout = QHBoxLayout()
        self.logx_check = QCheckBox("Log Scale X")
        self.logy_check = QCheckBox("Log Scale Y")
        log_layout.addWidget(self.logx_check)
        log_layout.addWidget(self.logy_check)
        options_layout.addRow(QLabel("Log Scale:"), log_layout)

        # Plot button
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.on_plot_button_clicked)
        options_layout.addRow(self.plot_button)

        layout.addWidget(options_group)
        self.setLayout(layout)

    def on_plot_button_clicked(self):
        """Emit a signal so the main window knows to re-plot."""
        self.plotRequested.emit()

