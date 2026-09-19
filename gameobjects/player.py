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

        self.animationFrames = None
        self.animationFramesFlipped = None
        self.animationFrameDuration = 0.08
        self.animationIndex = 0
        self.animationTimer = 0

        self.bindSpeedKey(pygame.K_LEFT, 180, walkSpeed)
        self.bindSpeedKey(pygame.K_RIGHT, 0, walkSpeed)

    def jump(self):
        if self.grounded:
            self.vy = 0
            self.applyForce(270, self.jumpForce)
            self.grounded = False
            return

        if self.airJumpsRemaining <= 0 or self.airJumpLocked:
            return

        self.vy = 0
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

    def setAnimation(self, frames, frameDuration=0.1):
        self.animationFrames = frames
        self.animationFramesFlipped = [pygame.transform.flip(frame, True, False) for frame in frames]
        self.animationFrameDuration = frameDuration
        self.animationIndex = 0
        self.animationTimer = 0

        if frames and hasattr(self.gameObject, "setImage"):
            self.gameObject.setImage(self._currentFrames()[0])

    def _currentFrames(self):
        return self.animationFramesFlipped if self.facing == 180 else self.animationFrames

    def _advanceAnimation(self, delta):
        if not self.animationFrames:
            return

        self.animationTimer += delta
        if self.animationTimer < self.animationFrameDuration:
            return

        self.animationTimer -= self.animationFrameDuration
        self.animationIndex = (self.animationIndex + 1) % len(self.animationFrames)
        self.gameObject.setImage(self._currentFrames()[self.animationIndex])

    def handleKeyDown(self, key):
        if key == pygame.K_UP:
            self.jump()
            return

        if key == pygame.K_LEFT:
            self.setFacing(180)
        elif key == pygame.K_RIGHT:
            self.setFacing(0)

        super().handleKeyDown(key)

    def setFacing(self, angle):
        if self.facing == angle:
            return

        self.facing = angle

        if self.animationFrames:
            self.gameObject.setImage(self._currentFrames()[self.animationIndex])

    def update(self, delta):
        self.grounded = False

        if self.airJumpLocked:
            self.airJumpTimer += delta
            if self.airJumpTimer >= self.airJumpRefillTime:
                self.refillAirJumps()

        self._advanceAnimation(delta)

        super().update(delta)

    def onCollision(self, other):
        wasFalling = self.vy > 0
        super().onCollision(other)

        if wasFalling and self.vy == 0:
            self.grounded = True
            self.groundY = self.getBounds()[1]
            self.refillAirJumps()
