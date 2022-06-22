from abc import ABC, abstractmethod


class IService(ABC):
    @abstractmethod
    def findAll(self):
        pass

    @abstractmethod
    def findOne(self, dataId: int):
        pass

    @abstractmethod
    def findOneBy(self, **kwargs):
        pass


    @abstractmethod
    def insert(self, data):
        pass

    @abstractmethod
    def update(self, dataId: int, data):
        pass

    @abstractmethod
    def delete(self, dataId: int):
        pass