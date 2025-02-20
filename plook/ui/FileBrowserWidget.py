# ui/FileBrowserWidget.py

import os
from PyQt5.QtCore import (
    Qt, QDir, QModelIndex, pyqtSignal
)
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTreeView, QFileSystemModel,
    QMenu, QAction
)


class FileBrowserWidget(QWidget):
    """
    A widget that displays files/folders in a QTreeView.
    It omits the '.' entry, but shows '..'.
    - Right-click a folder -> option to navigate into it.
    - Double-click '..' -> navigate up.
    - Double-click a file -> fileDoubleClicked(str) signal emitted.
    """

    fileDoubleClicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Create the QFileSystemModel
        self.file_model = QFileSystemModel(self)
        # Filter to hide '.' but keep '..'
        # (NoDot excludes '.', NoDotDot would exclude '..', so we do NOT set NoDotDot)
        self.file_model.setFilter(QDir.AllDirs | QDir.AllEntries | QDir.NoDot)

        # Use the current working directory as the initial root
        current_path = os.path.abspath(os.curdir)
        self.file_model.setRootPath(current_path)

        # Create a QTreeView to display the model
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(current_path))

        # Hide unneeded columns (size, file type, last modified)
        for col in range(1, 4):
            self.tree_view.hideColumn(col)

        # Handle double-click events
        self.tree_view.doubleClicked.connect(self.on_item_double_clicked)

        # Enable a custom context menu for right-click
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(self.tree_view)

    def on_item_double_clicked(self, index: QModelIndex):
        """ 
        Handle double-clicking items:
        - If it's the '..' folder, navigate up one level.
        - If it's a directory (other than '..'), the default QTreeView behavior (expand/collapse).
        - If it's a file, emit our fileDoubleClicked signal.
        """
        if not index.isValid():
            return

        file_path = self.file_model.filePath(index)
        if not file_path:
            return

        # Check if user clicked '..'
        if os.path.basename(file_path) == "..":
            # Navigate up from current root
            current_root = self.file_model.rootPath()
            parent_dir = os.path.dirname(current_root)
            self.tree_view.setRootIndex(self.file_model.index(parent_dir))
            return

        # If it's a directory (other than '..'), QTreeView will expand/collapse by default.
        # If it's a file, emit the signal
        if not self.file_model.isDir(index):
            self.fileDoubleClicked.emit(file_path)

    def show_context_menu(self, pos):
        """
        Show a right-click context menu.
        If the user right-clicked a directory, offer to navigate into it.
        """
        index = self.tree_view.indexAt(pos)
        if not index.isValid():
            return

        file_path = self.file_model.filePath(index)
        if not file_path:
            return

        # If it's a directory, show a "Navigate into folder" option
        if self.file_model.isDir(index) and os.path.basename(file_path) != "..":
            menu = QMenu(self)
            go_action = QAction("Navigate into folder", self)
            # Use a lambda to capture the index we right-clicked
            go_action.triggered.connect(lambda: self.navigate_into_folder(index))
            menu.addAction(go_action)
            menu.exec_(self.tree_view.mapToGlobal(pos))

    def navigate_into_folder(self, index: QModelIndex):
        """
        Set the given directory as the new root index (i.e., 'navigate down').
        """
        if self.file_model.isDir(index):
            self.tree_view.setRootIndex(index)
