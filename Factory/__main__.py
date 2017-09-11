from Factory.Storage import Storage
from Factory.WorkingItem import WorkingItem
from Factory.Worker import Worker
from Factory.Building import Building
from Factory.PluginRegister import register

from time import sleep
import random

import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)

register("Factory")

engine = QQmlApplicationEngine()
engine.load(QUrl("main.qml"))

# find building
childrens = engine.rootObjects()[0].children()
building = None
for children in childrens:
    if type(children) is Building:
        building = children
        break
if building is None:
    raise Exception("Building missing, add it to the root")

building.add_storage(Storage(capacity=100, name="input"))
building.add_storage(Storage(capacity=1), storage_name="task1_storage")
building.add_storage(Storage(capacity=100), storage_name="output")

building.add_worker(Worker(building.storages["input"], building.storages["task1_storage"], name="task1"))
building.add_worker(Worker(building.storages["input"], building.storages["task1_storage"], name="task1_2"))
building.add_worker(Worker(building.storages["task1_storage"], building.storages["output"]), worker_name="task2")

building.start_workers()


def check_finished():
    if building.storages["output"].itemCount == 5:
        app.quit()


building.storages["output"].itemCountChanged.connect(check_finished)

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


def print_progress():
    print("progress: " + str(building.workers["task1"].progress) + " - " + building.workers["task1"].progressMessage)


building.workers["task1"].progressChanged.connect(print_progress)
building.storages["input"].add_item(test)
for i in range(0, 4):
    building.storages["input"].add_item(DummyWork(i))


def storage_1_capacity():
    print("Item count storage 1: " + str(building.storages["task1_storage"].itemCount))


building.storages["task1_storage"].itemCountChanged.connect(storage_1_capacity)

app.exec()

# while remaining:
#     building.storages["output"].acquire()
#     building.storages["output"].wait_for(building.storages["output"].is_not_empty)
#     item = building.storages["output"].pick_item()
#     building.storages["output"].release()
#     remaining -= 1
#     print("Completed, " + str(remaining) + " remaining")
#     print(item)
print("ALL WORK FINISHED")
building.stop_workers()

print("ENDED")
exit()
