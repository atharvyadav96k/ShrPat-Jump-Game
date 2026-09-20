from objects import Rectangle, Image
from gameevents.controllableObject import ControllableObject
from gamelogger import logger


FALL_DELAY = 0.2
PLATFORM_COLOR = (150, 90, 40)


class FallingPlatform(ControllableObject):
    def __init__(self, gameObject, gravityAccel=900):
        super().__init__(gameObject, collidable=True, rigid=True, zIndex=3)
        self.fallGravityAccel = gravityAccel
        self.touched = False
        self.falling = False
        self.fallTimer = 0

    @classmethod
    def fromRect(cls, position, size, color=PLATFORM_COLOR):
        return cls(Rectangle(f"fallplatform_{position[0]}_{position[1]}", position, size, color))

    @classmethod
    def fromAssets(cls, position, size, image):
        return cls(Image(f"fallplatform_{position[0]}_{position[1]}", position, size, image))

    def onCollision(self, other):
        super().onCollision(other)

        if not self.touched and not self.falling:
            self.touched = True
            self.fallTimer = 0
            logger.debug(
                "fallingPlatform %s touched by %s at pos=%s",
                self.getObjName(), other.getObjName(), self.getBounds(),
            )

    def update(self, delta):
        if self.touched and not self.falling:
            self.fallTimer += delta
            if self.fallTimer >= FALL_DELAY:
                self.falling = True
                self.disableCollision()
                self.enableGravity(self.fallGravityAccel)
                logger.debug("fallingPlatform %s started falling at pos=%s", self.getObjName(), self.getBounds())

        super().update(delta)
