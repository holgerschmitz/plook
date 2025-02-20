import os
from PyQt5.QtCore import (
    QDir,
    QModelIndex,
    pyqtSignal,
)
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeView,
    QFileSystemModel,
)

class FileBrowserWidget(QWidget):
    """
    A widget that displays files/folders in a QTreeView.
    It emits a signal when the user double-clicks a file.
    """
    fileDoubleClicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        
        self.file_model = QFileSystemModel()
        # Show hidden entries like '.' and '..'
        self.file_model.setFilter(QDir.AllEntries | QDir.AllDirs)
        current_path = os.path.abspath(os.curdir)
        self.file_model.setRootPath(current_path)
        
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(current_path))
        
        # Hide unneeded columns (optional)
        for col in range(1, 4):
            self.tree_view.hideColumn(col)
        
        self.tree_view.doubleClicked.connect(self.on_item_double_clicked)
        
        layout.addWidget(self.tree_view)
        
    def on_item_double_clicked(self, index: QModelIndex):
        if not index.isValid():
            return
        file_path = self.file_model.filePath(index)
        if file_path and not self.file_model.isDir(index):
            # It's a file; emit signal so others can respond
            self.fileDoubleClicked.emit(file_path)
