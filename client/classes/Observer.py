from abc import ABC, abstractmethod


class Observer():
    def __init__(self):
        pass

    #@abstractmethod
    def update(self, subject) -> None:
        pass


class Subject():
    #@abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    #@abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    #@abstractmethod
    def notify(self) -> None:
        pass
