from objects import Rectangle
from gameevents.controllableObject import ControllableObject


KILL_COLOR = (200, 0, 0)


class KillObstacle(ControllableObject):
    def __init__(self, gameObject):
        super().__init__(gameObject, collidable=True, rigid=True, zIndex=3)

    @classmethod
    def fromRect(cls, position, size, color=KILL_COLOR):
        return cls(Rectangle(f"kill_{position[0]}_{position[1]}", position, size, color))

    def onCollision(self, other):
        super().onCollision(other)

        if hasattr(other, "takeDamage"):
            other.takeDamage(other.maxHealth)
