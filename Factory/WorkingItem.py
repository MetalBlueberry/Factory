from PyQt5.QtCore import pyqtProperty, pyqtSignal, QRunnable, QObject


class WorkingItem(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._progress = 0
        self._message = ""
        self._work = None

    # Qt Properties
    progressChanged = pyqtSignal()

    @pyqtProperty(float, notify=progressChanged)
    def progress(self):
        return self._progress

    def set_progress(self, value):
        if value != self._progress:
            self._progress = value
            self.progressChanged.emit()

    progressMessageChanged = pyqtSignal()

    @pyqtProperty(str, notify=progressMessageChanged)
    def progressMessage(self):
        return self._message

    def set_progress_message(self, message):
        if message != self._message:
            self._message = message
            self.progressMessageChanged.emit()

    workChanged = pyqtSignal()

    @pyqtProperty(QRunnable, notify=workChanged)
    def work(self):
        return self._work

    @work.setter
    def work(self, value):
        self._work = value
        self.workChanged.emit()
