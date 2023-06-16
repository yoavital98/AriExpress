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

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def values(self):
        pass

    def items(self):
        for key, value in zip(self.keys(), self.values()):
            yield key, value

