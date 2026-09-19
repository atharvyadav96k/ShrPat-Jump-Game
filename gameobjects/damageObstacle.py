from objects import Rectangle
from gameevents.controllableObject import ControllableObject


DESTROY_DELAY = 0.3
DAMAGE_COLOR = (255, 140, 0)


class DamageObstacle(ControllableObject):
    def __init__(self, gameObject, damage=20):
        super().__init__(gameObject, collidable=True, rigid=True, zIndex=3)
        self.damage = damage
        self.touched = False
        self.destroyTimer = 0
        self.destroyed = False

    @classmethod
    def fromRect(cls, position, size, damage=20, color=DAMAGE_COLOR):
        return cls(Rectangle(f"damage_{position[0]}_{position[1]}", position, size, color), damage=damage)

    def onCollision(self, other):
        super().onCollision(other)

        if self.touched:
            return

        if hasattr(other, "takeDamage"):
            other.takeDamage(self.damage)
            self.touched = True
            self.destroyTimer = 0

    def update(self, delta):
        super().update(delta)

        if self.touched and not self.destroyed:
            self.destroyTimer += delta
            if self.destroyTimer >= DESTROY_DELAY:
                self.destroyed = True
