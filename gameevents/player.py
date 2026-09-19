import pygame
from .controllableObject import ControllableObject


class Player(ControllableObject):
    def __init__(self, gameObject, walkSpeed=200, jumpForce=400, gravityAccel=900, friction=0):
        super().__init__(gameObject, collidable=True, gravity=True, gravityAccel=gravityAccel, friction=friction)
        self.jumpForce = jumpForce
        self.grounded = False

        self.bindSpeedKey(pygame.K_LEFT, 180, walkSpeed)
        self.bindSpeedKey(pygame.K_RIGHT, 0, walkSpeed)

    def jump(self):
        if not self.grounded:
            return

        self.applyForce(270, self.jumpForce)
        self.grounded = False

    def handleKeyDown(self, key):
        if key == pygame.K_UP:
            self.jump()
            return

        super().handleKeyDown(key)

    def update(self, delta):
        self.grounded = False
        super().update(delta)

    def onCollision(self, other):
        wasFalling = self.vy > 0
        super().onCollision(other)

        if wasFalling and self.vy == 0:
            self.grounded = True
