from PyQt5.QtQml import qmlRegisterType, qmlRegisterUncreatableType
from Factory.Storage import Storage
from Factory.WorkingItem import WorkingItem
from Factory.Worker import Worker
from Factory.Building import Building


def register(uri):
    qmlRegisterType(Building, uri, 1, 0, "Building")
    qmlRegisterUncreatableType(Storage, uri, 1, 0, "Storage", "Not allowed, use python instead")
    qmlRegisterUncreatableType(Worker, uri, 1, 0, "Worker", "Not allowed, use python instead")
    qmlRegisterUncreatableType(WorkingItem, uri, 1, 0, "WorkingItem", "Not allowed, use python instead")
