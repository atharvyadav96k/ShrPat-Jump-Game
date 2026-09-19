from objects import Rectangle
from .killObstacle import KillObstacle, KILL_COLOR


class HorizontalMovingKillObstacle(KillObstacle):
    def __init__(self, gameObject, rangeStart, rangeEnd, speed=100):
        super().__init__(gameObject)
        self.zIndex = 5
        self.rangeStart = rangeStart
        self.rangeEnd = rangeEnd
        self.vx = speed

    @classmethod
    def fromRect(cls, position, size, travelDistance, speed=100, color=KILL_COLOR):
        rectObj = Rectangle(f"hkill_{position[0]}_{position[1]}", position, size, color)
        return cls(rectObj, rangeStart=position[0], rangeEnd=position[0] + travelDistance, speed=speed)

    def update(self, delta):
        x, y, w, h = self.getBounds()

        if x <= self.rangeStart:
            self.vx = abs(self.vx)
        elif x + w >= self.rangeEnd:
            self.vx = -abs(self.vx)

        super().update(delta)


class VerticalMovingKillObstacle(KillObstacle):
    def __init__(self, gameObject, rangeStart, rangeEnd, speed=100):
        super().__init__(gameObject)
        self.zIndex = 5
        self.rangeStart = rangeStart
        self.rangeEnd = rangeEnd
        self.vy = speed

    @classmethod
    def fromRect(cls, position, size, travelDistance, speed=100, color=KILL_COLOR):
        rectObj = Rectangle(f"vkill_{position[0]}_{position[1]}", position, size, color)
        return cls(rectObj, rangeStart=position[1], rangeEnd=position[1] + travelDistance, speed=speed)

    def update(self, delta):
        x, y, w, h = self.getBounds()

        if y <= self.rangeStart:
            self.vy = abs(self.vy)
        elif y + h >= self.rangeEnd:
            self.vy = -abs(self.vy)

        super().update(delta)
