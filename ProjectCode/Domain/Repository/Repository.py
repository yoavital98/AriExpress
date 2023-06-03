from abc import ABC, abstractmethod


class Repository(ABC):


    #getAll if pk=None
    @abstractmethod
    def get(self, pk=None):
        pass

    @abstractmethod
    def add(self, **kwargs):
        pass

    @abstractmethod
    def remove(self, pk):
        pass
