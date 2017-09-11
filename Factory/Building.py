from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtQml import QQmlListProperty
from PyQt5.QtQuick import QQuickItem

from Factory.Storage import Storage
from Factory.Worker import Worker
from Factory.WorkingItem import WorkingItem


class Building(QQuickItem):
    def __init__(self, parent=None, default_input=None, default_output=None):
        super().__init__(parent=parent)
        self._default_input = default_input
        self._defaout_output = default_output
        self.storages = dict()
        self.workers = dict()
        self.id = "factory"

    # Qt Properties
    storagesChanged = pyqtSignal()

    @pyqtProperty(QQmlListProperty, notify=storagesChanged)
    def storagesList(self):
        return QQmlListProperty(Storage, self,
                                sorted(list(self.storages.values()), key=lambda storages: storages.id_name))

    workersChanged = pyqtSignal()

    @pyqtProperty(QQmlListProperty, notify=workersChanged)
    def workersList(self):
        return QQmlListProperty(Worker, self, sorted(list(self.workers.values()), key=lambda worker: worker.id_name))

    defaultInputChanged = pyqtSignal()

    @pyqtProperty(Storage, notify=defaultInputChanged)
    def defaultInput(self):
        return self._default_input

    @defaultInput.setter
    def defaultInput(self, value):
        self._default_input = value
        self.defaultInputChanged.emit()

    defaultOutputChanged = pyqtSignal()

    @pyqtProperty(Storage, notify=defaultOutputChanged)
    def defaultOutput(self):
        return self._default_output

    @defaultOutput.setter
    def defaultOutput(self, value):
        print("Setting default input")
        self._default_output = value
        self.defaultOutputChanged.emit()

    # python functions

    def add_storage(self, storage: Storage, storage_name: str = None):
        if storage_name is None:
            storage_name = storage.id_name
        else:
            storage.id_name = storage_name

        if not storage_name:
            raise Exception("storage not defined")
        if storage_name in self.storages:
            raise Exception("storage_name already in use")
        print(storage_name)
        self.storages[storage_name] = storage
        self.storagesChanged.emit()

    def add_worker(self, worker: Worker, worker_name: str = None):
        if worker_name is None:
            worker_name = worker.id_name
        else:
            worker.id_name = worker_name

        if not worker_name:
            raise Exception("worker_name not defined")
        if worker_name in self.workers:
            raise Exception("worker_name already in use")

        self.workers[worker_name] = worker
        self.workersChanged.emit()

    def start_workers(self):
        for name, worker in self.workers.items():
            worker.start()

    def stop_workers(self):
        for name, worker in self.workers.items():
            worker.stop()
            # for name, worker in self.workers.items():
            #     worker.join()
