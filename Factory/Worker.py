from threading import Thread
from .Storage import Storage
from PyQt5.QtCore import pyqtProperty, pyqtSignal, QObject


class Worker(QObject):
    def __init__(self, input_storage: Storage = None, output_storage: Storage = None, name=""):
        super().__init__()
        self._input_storage = input_storage
        self._output_storage = output_storage
        self.id_name = name
        self._request_stop = False
        self._thread = Thread(target=self.run)
        self.join = self._thread.join
        self.start = self._thread.start

    # Qt Signals
    inputStorageChanged = pyqtSignal()

    @pyqtProperty(Storage, notify=inputStorageChanged)
    def inputStorage(self):
        return self._input_storage

    @inputStorage.setter
    def inputStorage(self, value):
        self._input_storage = value
        self.inputStorageChanged.emit()

    outputStorageChanged = pyqtSignal()

    @pyqtProperty(Storage, notify=outputStorageChanged)
    def outputStorage(self):
        return self._output_storage

    @outputStorage.setter
    def outputStorage(self, value):
        self._output_storage = value
        self.outputStorageChanged.emit()

    # Thread managment
    def stop(self):
        self._request_stop = True
        self._input_storage.acquire()
        self._input_storage.notify_all()
        self._input_storage.release()

    def check_input_or_end(self):
        if self._request_stop:
            print("STOPPING")
            self._input_storage.release()
            exit()
        return self._input_storage.is_not_empty()

    def run(self):
        while True:
            self._input_storage.acquire()
            print(self.id_name + " waiting for input")
            self._input_storage.wait_for(self.check_input_or_end)

            print(self.id_name + " working")
            working_item = self._input_storage.pick_item()
            self._input_storage.release()

            result = working_item.do_work()

            self._output_storage.acquire()
            self._output_storage.wait_for(self._output_storage.is_not_full)
            self._output_storage.add_item(result)
            self._output_storage.release()
