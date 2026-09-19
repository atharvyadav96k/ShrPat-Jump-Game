from objects import Rectangle
from gameevents.controllableObject import ControllableObject


DESTROY_DELAY = 0.3
WOOD_COLOR = (139, 69, 19)


class WoodBox(ControllableObject):
    def __init__(self, gameObject):
        super().__init__(gameObject, collidable=True, rigid=True, zIndex=3)
        self.touched = False
        self.destroyTimer = 0
        self.destroyed = False

    @classmethod
    def fromRect(cls, position, size, color=WOOD_COLOR):
        return cls(Rectangle(f"woodbox_{position[0]}_{position[1]}", position, size, color))

    def onCollision(self, other):
        super().onCollision(other)

        if not self.touched:
            self.touched = True
            self.destroyTimer = 0

    def update(self, delta):
        super().update(delta)

        if self.touched and not self.destroyed:
            self.destroyTimer += delta
            if self.destroyTimer >= DESTROY_DELAY:
                self.destroyed = True
