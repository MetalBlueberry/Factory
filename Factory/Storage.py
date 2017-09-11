from threading import Condition
from collections import deque

from PyQt5.QtCore import pyqtProperty, pyqtSignal, QObject
from PyQt5.QtQml import QQmlListProperty

from Factory.WorkingItem import WorkingItem


class Storage(QObject):
    def __init__(self, parent=None, capacity=10, name=""):
        self._capacity = capacity
        self._items = deque()
        self.id_name = name
        self._condition = Condition()
        self.acquire = self._condition.acquire
        self.release = self._condition.release
        self.notify_all = self._condition.notify_all
        self.wait_for = self._condition.wait_for

        super().__init__(parent)

    capacityChanged = pyqtSignal()

    # Qt Properties
    @pyqtProperty(int, notify=capacityChanged)
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        if value != self._capacity:
            self._capacity = value
            self.capacityChanged.emit()

    itemCountChanged = pyqtSignal()

    @pyqtProperty(int, notify=itemCountChanged)
    def itemCount(self):
        return len(self._items)

    itemsChanged = pyqtSignal()

    @pyqtProperty(QQmlListProperty, notify=itemsChanged)
    def items(self):
        return QQmlListProperty(WorkingItem, self, self._items)

    idNameChanged = pyqtSignal()

    @pyqtProperty(str, notify=idNameChanged)
    def idName(self):
        return self.id_name

    # queue functions
    def add_item(self, item):
        # print(self.id_name + ": adding")
        self.acquire()
        self._items.append(item)
        self.notify_all()
        self.release()
        self.itemCountChanged.emit()

    def _item_at(self, list_index):
        return self._items[list_index]

    def pick_item(self):
        self.acquire()
        item = self._items.popleft()
        self.notify_all()
        self.release()
        self.itemCountChanged.emit()
        return item

    def get_capacity(self):
        return self._capacity

    def is_empty(self):
        return not self.is_not_empty()

    def is_not_empty(self):
        # print(self.id_name + ": " + str(len(self._items) > 0))
        return len(self._items) > 0 or len(self._items) < 0

    def is_full(self):
        return len(self._items) >= self._capacity

    def is_not_full(self):
        return not self.is_full()

    def __le__(self, other):
        return self.id_name.__le__(other)

    def __lt__(self, other):
        return self.id_name.__lt__(other)

    def __eq__(self, other):
        return self.id_name.__eq__(other)