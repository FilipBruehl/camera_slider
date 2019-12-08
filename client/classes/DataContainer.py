from classes.Observer import Observer, Subject
from typing import List


# Implementation des Subjectes des ObserverPatterns, folgt dem Singleton Pattern
class DataContainer(Subject):
    _instance = None

    def __init__(self):
        if DataContainer._instance:
            raise Exception("DataContainer already initialized")
        else:
            self.__observers: List[Observer] = []
            self.data = {}

    @staticmethod
    def get_instance():
        if not DataContainer._instance:
            DataContainer._instance = DataContainer()
        return DataContainer._instance

    def attach(self, observer: Observer) -> None:
        self.__observers.append(observer)
        print(self.__observers)

    def detach(self, observer: Observer) -> None:
        self.__observers.remove(observer)
        print(self.__observers)

    def notify(self) -> None:
        print("notifying observers")
        for observer in self._instance.__observers:
            print(observer)
            observer.update(self)
        print("observers notified")

    def get_data(self, key):
        return self.data.pop(key, None)

    def add_data(self, key, data):
        self.data.update({key: data})
        print("add data", self.data)
        self.notify()

    def contains_key(self, key):
        return key in self.data.keys()