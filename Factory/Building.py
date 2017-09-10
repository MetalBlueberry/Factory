from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtQml import QQmlListProperty

from Factory.Storage import Storage
from Factory.Worker import Worker
from Factory.WorkingItem import WorkingItem


class Building(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.storages = dict()
        self.workers = dict()

    @pyqtSlot(Storage, str)
    def add_storage(self, storage: Storage, storage_name: str = None):
        if storage_name is None:
            storage_name = storage.id_name
        if not storage_name:
            raise Exception("worker_name not defined")
        if storage_name in self.storages:
            raise Exception("worker_name already in use")
        print(storage_name)
        self.storages[storage_name] = storage

    @pyqtSlot(Worker, str)
    def add_worker(self, worker: Worker, worker_name: str = None):
        if worker_name is None:
            worker_name = worker.id_name
        if not worker_name:
            raise Exception("worker_name not defined")
        if worker_name in self.workers:
            raise Exception("worker_name already in use")

        self.workers[worker_name] = worker

    def start_workers(self):
        for name, worker in self.workers.items():
            worker.start()

    def stop_workers(self):
        for name, worker in self.workers.items():
            worker.stop()
        for name, worker in self.workers.items():
            worker.join()

