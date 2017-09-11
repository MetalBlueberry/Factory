from PyQt5.QtCore import pyqtSignal, pyqtProperty
from Factory.WorkingItem import WorkingItem
from RecursiveUncompress.FileManager import CompressedFile


class UncompressWork(WorkingItem):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._filename = None

    filenameChanged = pyqtSignal()

    @pyqtProperty(str, notify=filenameChanged)
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if value != self._filename:
            self._filename = value
            self.description = "File uncompress " + value
            self.filenameChanged.emit()

    def do_work(self):
        self.set_progress(0)
        self.set_progress_message("Extracting file")
        file = CompressedFile(self._filename[7:])
        file.recursive_uncompress()
        self.set_progress_message("Done")
        self.set_progress(1)
