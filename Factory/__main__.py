from Factory.Storage import Storage
from Factory.WorkingItem import WorkingItem
from Factory.Worker import Worker
from Factory.Building import Building
from Factory.PluginRegister import register

from time import sleep
import random

import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)

register("Factory")

engine = QQmlApplicationEngine()
engine.load(QUrl(os.path.dirname(__file__) + "/main.qml"))

# find building
childrens = engine.rootObjects()[0].children()
building = None
for children in childrens:
    if type(children) is Building:
        building = children
        break
if building is None:
    raise Exception("Building missing, add it to the root")

building.add_storage(Storage(capacity=100), storage_name="_input")
building.add_storage(Storage(capacity=1), storage_name="1_temp")
building.add_storage(Storage(capacity=2), storage_name="2_temp")
building.add_storage(Storage(capacity=1), storage_name="3_temp")
building.add_storage(Storage(capacity=100), storage_name="_output")

building.add_worker(Worker(building.storages["_input"], building.storages["1_temp"]), worker_name="task1")
building.add_worker(Worker(building.storages["1_temp"], building.storages["2_temp"]), worker_name="task2")
building.add_worker(Worker(building.storages["2_temp"], building.storages["3_temp"]), worker_name="task3")
building.add_worker(Worker(building.storages["3_temp"], building.storages["_output"]), worker_name="task4")

building.start_workers()


def check_finished():
    if building.storages["_output"].itemCount == 5:
        app.quit()


building.storages["_output"].itemCountChanged.connect(check_finished)

sleep(1)
print("STARTING")


class DummyWork(WorkingItem):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def do_work(self):
        working_time = random.randrange(5, 10)
        # print(str(self.id) + ": working for " + str(working_time))
        self.set_progress_message("starting")
        for i in range(0, 10):
            self.set_progress(i / 10)
            sleep(working_time / 10)
            if i == 5:
                self.set_progress_message("half done")
        self.set_progress(1)
        self.set_progress_message("completed")

        # print(str(self.id) + ": done")
        return DummyWork(10 + self.id)


test = DummyWork(1)




for i in range(0, 4):
    building.storages["_input"].add_item(DummyWork(i))


app.exec()

print("ALL WORK FINISHED")
building.stop_workers()

print("ENDED")
exit()
