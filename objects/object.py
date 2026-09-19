from abc import ABC, abstractmethod


class Object(ABC):
    @abstractmethod
    def drawObject(self, canvas):
        pass
    @abstractmethod
    def getObjName(self):
        pass
    @abstractmethod
    def moveObject(self, directionAngle, directionSpeed):
        pass

    @abstractmethod
    def getBounds(self):
        pass

    @abstractmethod
    def setPosition(self, x, y):
        pass

    @abstractmethod
    def objectCollision(self):
        pass