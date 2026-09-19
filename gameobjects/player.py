import os
import pygame
from objects import Image
from animation import Animator
from gameevents.controllableObject import ControllableObject


class Player(ControllableObject):
    _frameCache = {}

    def __init__(self, gameObject, walkSpeed=200, jumpForce=400, maxAirJumps=1, airJumpRefillTime=5,
                 gravityAccel=900, friction=0, zIndex=1, maxHealth=100):
        super().__init__(gameObject, collidable=True, gravity=True, gravityAccel=gravityAccel, friction=friction, zIndex=zIndex)
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.jumpForce = jumpForce
        self.grounded = False
        self.groundY = gameObject.getBounds()[1]

        self.maxAirJumps = maxAirJumps
        self.airJumpsRemaining = maxAirJumps
        self.airJumpRefillTime = airJumpRefillTime
        self.airJumpLocked = False
        self.airJumpTimer = 0
        self.facing = 0

        self.animator = Animator(gameObject)
        self.animState = "idle"
        self.airborneVelocityThreshold = 100
        self.destroyed = False
        self.score = 0

        self.bindSpeedKey(pygame.K_LEFT, 180, walkSpeed)
        self.bindSpeedKey(pygame.K_RIGHT, 0, walkSpeed)

    def jump(self):
        if self.grounded:
            self.vy = 0
            self.applyForce(270, self.jumpForce)
            self.grounded = False
            self._setAnimState("jump", restart=True)
            return

        if self.airJumpsRemaining <= 0 or self.airJumpLocked:
            return

        self.vy = 0
        self.applyForce(270, self.jumpForce)
        self.airJumpsRemaining -= 1
        self._setAnimState("jump", restart=True)

        if self.airJumpsRemaining <= 0:
            self.airJumpLocked = True
            self.airJumpTimer = 0

    def refillAirJumps(self):
        self.airJumpsRemaining = self.maxAirJumps
        self.airJumpLocked = False

    def grantExtraJump(self, amount=1):
        self.airJumpsRemaining = min(self.maxAirJumps, self.airJumpsRemaining + amount)
        if self.airJumpsRemaining > 0:
            self.airJumpLocked = False

    def addScore(self, amount):
        self.score += amount

    def takeDamage(self, amount):
        if not self.isAlive():
            return

        self.health = max(0, self.health - amount)
        if not self.isAlive():
            self._setAnimState("die", restart=True)

    def heal(self, amount):
        self.health = min(self.maxHealth, self.health + amount)

    def isAlive(self):
        return self.health > 0

    @classmethod
    def fromAssets(cls, assetsDir, position, size, **kwargs):
        frames = cls._getFrames(assetsDir)

        player = cls(Image("player", position, size, frames["idle"][0]), **kwargs)
        player.animator.add("idle", frames["idle"], loop=True)
        player.animator.add("walk", frames["walk"], frameDuration=0.04, loop=True)
        player.animator.add("jump", frames["jump"], frameDuration=0.08, loop=False)
        player.animator.add("fall", frames["fall"], frameDuration=0.08, loop=False, waitForTrigger=True)
        player.animator.add("die", frames["die"], frameDuration=0.1, loop=False)
        player.animator.setState("idle")
        return player

    @classmethod
    def _getFrames(cls, assetsDir):
        if assetsDir not in cls._frameCache:
            idleFrame = pygame.image.load(os.path.join(assetsDir, "0.png")).convert_alpha()
            walkFrames = [
                pygame.image.load(os.path.join(assetsDir, f"{i}.png")).convert_alpha()
                for i in range(1, 8)
            ]
            cls._frameCache[assetsDir] = {
                "idle": [idleFrame],
                "walk": walkFrames,
                "jump": cls._loadFrameSequence(os.path.join(assetsDir, "jump")),
                "fall": cls._loadFrameSequence(os.path.join(assetsDir, "falling")),
                "die": cls._loadFrameSequence(os.path.join(assetsDir, "die")),
            }

        return cls._frameCache[assetsDir]

    @staticmethod
    def _loadFrameSequence(dirPath):
        entries = [f for f in os.listdir(dirPath) if os.path.splitext(f)[0].isdigit()]
        files = sorted(entries, key=lambda f: int(os.path.splitext(f)[0]))
        return [pygame.image.load(os.path.join(dirPath, f)).convert_alpha() for f in files]

    def heightAboveGround(self):
        return max(0, self.groundY - self.getBounds()[1])

    def isWalking(self):
        return self.speed != 0

    def _setAnimState(self, name, restart=False):
        self.animState = name
        self.animator.setState(name, restart=restart)

    def _determineState(self, grounded):
        if grounded:
            return "walk" if self.isWalking() else "idle"

        if self.vy < -self.airborneVelocityThreshold:
            return "jump"

        if self.vy > self.airborneVelocityThreshold:
            return "fall"

        if self.animState in ("jump", "fall"):
            return self.animState

        return "walk" if self.isWalking() else "idle"

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
        self.animator.setFacing(angle)

    def update(self, delta):
        if not self.isAlive():
            self.animator.update(delta)
            if self.animator.animations["die"].isFinished():
                self.destroyed = True
            return

        wasGrounded = self.grounded
        self.grounded = False

        if self.airJumpLocked:
            self.airJumpTimer += delta
            if self.airJumpTimer >= self.airJumpRefillTime:
                self.refillAirJumps()

        self._setAnimState(self._determineState(wasGrounded))
        self.animator.update(delta)

        super().update(delta)

    def onCollision(self, other):
        wasFalling = self.vy > 0
        super().onCollision(other)

        if wasFalling and self.vy == 0:
            self.animator.trigger()
            self.grounded = True
            self.groundY = self.getBounds()[1]
            self.refillAirJumps()
