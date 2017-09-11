from Factory.Storage import Storage
from Factory.WorkingItem import WorkingItem
from Factory.Worker import Worker
from Factory.Building import Building
from Factory.PluginRegister import register
from Factory.Utilities import find_building_in_engine
from time import sleep
import random

import sys
import os
from PyQt5.QtCore import QUrl, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType


class DummyWork(WorkingItem):
    def __init__(self, id=None):
        super().__init__()
        self.id = id
        self.working_time = random.randrange(500, 5000) / 1000
        self.description = str(id) + " for " + str(self.working_time)

    def do_work(self):
        self.set_progress_message("processing")
        for i in range(0, 10):
            self.set_progress(i / 10)
            sleep(self.working_time / 10)
            if i == 5:
                self.set_progress_message("half done")
        self.set_progress(1)
        self.set_progress_message("completed")

        # print(str(self.id) + ": done")
        return DummyWork(str(self.id))


class PrintFileName(WorkingItem):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self._filename = ""
        self.description = "File copy"

    filenameChanged = pyqtSignal()

    @pyqtProperty(str, notify=filenameChanged)
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if value != self._filename:
            self._filename = value
            self.description = "File copy " + value
            self.filenameChanged.emit()

    def do_work(self):
        print("Working on file " + self._filename)
        self.set_progress(0)
        self.set_progress_message("moving file " + self.filename)
        sleep(1)
        print("Completed on file " + self._filename)
        self.set_progress_message("completed move file " + self.filename)
        return DummyWork()


app = QGuiApplication(sys.argv)

register("Factory")
qmlRegisterType(DummyWork, "Factory", 1, 0, "DummyWork")
qmlRegisterType(PrintFileName, "Factory", 1, 0, "FileWork")

engine = QQmlApplicationEngine()
engine.load(QUrl(os.path.dirname(__file__) + "/main.qml"))

building = find_building_in_engine(engine)

building.add_storage(Storage(capacity=100), storage_name="_input")
building.add_storage(Storage(capacity=5), storage_name="1_temp")
building.add_storage(Storage(capacity=5), storage_name="2_temp")
building.add_storage(Storage(capacity=5), storage_name="3_temp")
building.add_storage(Storage(capacity=100), storage_name="_output")

building.defaultInput = building.storages["_input"]
building.defaultOutput = building.storages["_output"]

building.add_worker(Worker(building.storages["_input"], building.storages["1_temp"]), worker_name="task11")
building.add_worker(Worker(building.storages["_input"], building.storages["1_temp"]), worker_name="task12")
building.add_worker(Worker(building.storages["1_temp"], building.storages["2_temp"]), worker_name="task21")
building.add_worker(Worker(building.storages["1_temp"], building.storages["2_temp"]), worker_name="task22")
building.add_worker(Worker(building.storages["2_temp"], building.storages["3_temp"]), worker_name="task31")
building.add_worker(Worker(building.storages["2_temp"], building.storages["3_temp"]), worker_name="task32")
building.add_worker(Worker(building.storages["3_temp"], building.storages["_output"]), worker_name="task41")
building.add_worker(Worker(building.storages["3_temp"], building.storages["_output"]), worker_name="task42")

building.start_workers()


print("STARTING")

for i in range(0, 100):
    building.storages["_input"].add_item(DummyWork(i))

app.exec()

print("ALL WORK FINISHED")
building.stop_workers()

print("ENDED")
exit()
