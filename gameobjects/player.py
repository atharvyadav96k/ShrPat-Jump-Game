import pygame
from gameevents.controllableObject import ControllableObject


class Player(ControllableObject):
    def __init__(self, gameObject, walkSpeed=200, jumpForce=400, maxAirJumps=3, airJumpRefillTime=5,
                 gravityAccel=900, friction=0, zIndex=1):
        super().__init__(gameObject, collidable=True, gravity=True, gravityAccel=gravityAccel, friction=friction, zIndex=zIndex)
        self.jumpForce = jumpForce
        self.grounded = False
        self.groundY = gameObject.getBounds()[1]

        self.maxAirJumps = maxAirJumps
        self.airJumpsRemaining = maxAirJumps
        self.airJumpRefillTime = airJumpRefillTime
        self.airJumpLocked = False
        self.airJumpTimer = 0
        self.facing = 0

        self.bindSpeedKey(pygame.K_LEFT, 180, walkSpeed)
        self.bindSpeedKey(pygame.K_RIGHT, 0, walkSpeed)

    def jump(self):
        if self.grounded:
            self.applyForce(270, self.jumpForce)
            self.grounded = False
            return

        if self.airJumpsRemaining <= 0 or self.airJumpLocked:
            return

        self.applyForce(270, self.jumpForce)
        self.airJumpsRemaining -= 1

        if self.airJumpsRemaining <= 0:
            self.airJumpLocked = True
            self.airJumpTimer = 0

    def refillAirJumps(self):
        self.airJumpsRemaining = self.maxAirJumps
        self.airJumpLocked = False

    def heightAboveGround(self):
        return max(0, self.groundY - self.getBounds()[1])

    def handleKeyDown(self, key):
        if key == pygame.K_UP:
            self.jump()
            return

        if key == pygame.K_LEFT:
            self.facing = 180
        elif key == pygame.K_RIGHT:
            self.facing = 0

        super().handleKeyDown(key)

    def update(self, delta):
        self.grounded = False

        if self.airJumpLocked:
            self.airJumpTimer += delta
            if self.airJumpTimer >= self.airJumpRefillTime:
                self.refillAirJumps()

        super().update(delta)

    def onCollision(self, other):
        wasFalling = self.vy > 0
        super().onCollision(other)

        if wasFalling and self.vy == 0:
            self.grounded = True
            self.groundY = self.getBounds()[1]
            self.refillAirJumps()
