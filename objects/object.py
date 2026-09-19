from abc import ABC, abstractmethod


class Object(ABC):

    @abstractmethod
    def drawObject(self, canvas):
        pass

    @abstractmethod
    def objectCollision(self):
        pass