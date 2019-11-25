from abc import ABC, abstractmethod
from interface import Interface


class Observer():
    def __init__(self):
        pass
    #@abstractmethod
    def update(self, subject) -> None:
        pass


class Subject(Interface):
    #@abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    #@abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    #@abstractmethod
    def notify(self) -> None:
        pass
