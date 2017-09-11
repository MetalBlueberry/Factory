from PyQt5.QtQml import qmlRegisterType
from Factory.Storage import Storage
from Factory.WorkingItem import WorkingItem
from Factory.Worker import Worker
from Factory.Building import Building


def register(uri):
    qmlRegisterType(Building, uri, 1, 0, "Building")
    qmlRegisterType(Storage, uri, 1, 0, "Storage")
    qmlRegisterType(Worker, uri, 1, 0, "Worker")
    qmlRegisterType(WorkingItem, uri, 1, 0, "WorkingItem")
