import math


class ControllableObject:
    def __init__(self, gameObject, bindings=None, speedBindings=None, collidable=False, rigid=False, gravity=False, gravityAccel=900, friction=0, zIndex=0):
        self.gameObject = gameObject
        self.bindings = dict(bindings) if bindings else {}
        self.speedBindings = dict(speedBindings) if speedBindings else {}
        self.vx = 0
        self.vy = 0
        self.angle = 0
        self.speed = 0
        self.activeSpeedKey = None
        self.collidable = collidable
        self.rigid = rigid
        self.previousBounds = gameObject.getBounds()
        self.gravity = gravity
        self.gravityAccel = gravityAccel
        self.friction = friction
        self.zIndex = zIndex

    def enableCollision(self):
        self.collidable = True

    def disableCollision(self):
        self.collidable = False

    def enableGravity(self, accel=900):
        self.gravity = True
        self.gravityAccel = accel

    def disableGravity(self):
        self.gravity = False

    def setFriction(self, friction):
        self.friction = friction

    def getBounds(self):
        return self.gameObject.getBounds()

    def onCollision(self, other):
        if self.rigid:
            return

        x, y, w, h = self.getBounds()
        ox, oy, ow, oh = other.getBounds()
        prevX, prevY, _, _ = self.previousBounds

        overlapX = min(x + w, ox + ow) - max(x, ox)
        overlapY = min(y + h, oy + oh) - max(y, oy)

        if overlapX < overlapY:
            self.gameObject.setPosition(prevX, y)
            self.vx = 0
            if abs(math.cos(math.radians(self.angle))) > 1e-9:
                self.speed = 0
        else:
            self.gameObject.setPosition(x, prevY)
            self.vy = 0
            if abs(math.sin(math.radians(self.angle))) > 1e-9:
                self.speed = 0

    def bindKey(self, key, angle, force):
        self.bindings[key] = (angle, force)

    def unbindKey(self, key):
        self.bindings.pop(key, None)

    def bindSpeedKey(self, key, angle, speed):
        self.speedBindings[key] = (angle, speed)

    def unbindSpeedKey(self, key):
        self.speedBindings.pop(key, None)

    def getObjName(self):
        return self.gameObject.getObjName()

    def applyForce(self, angle, magnitude):
        rad = math.radians(angle)
        self.vx += math.cos(rad) * magnitude
        self.vy += math.sin(rad) * magnitude

    def handleKeyDown(self, key):
        if key in self.bindings:
            angle, force = self.bindings[key]
            self.applyForce(angle, force)

        if key in self.speedBindings:
            self.angle, self.speed = self.speedBindings[key]
            self.activeSpeedKey = key

    def handleKeyUp(self, key):
        if self.activeSpeedKey != key:
            return

        self.angle, self.speed = 0, 0
        self.activeSpeedKey = None

    def drawObject(self, canvas, offset=(0, 0)):
        self.gameObject.drawObject(canvas, offset)

    def update(self, delta):
        self.previousBounds = self.gameObject.getBounds()

        if self.gravity:
            self.applyForce(90, self.gravityAccel * delta)

        if self.friction:
            self.vx = self._applyFriction(self.vx, self.friction * delta)

        rad = math.radians(self.angle)
        speedDx = math.cos(rad) * self.speed
        speedDy = math.sin(rad) * self.speed

        self.gameObject.translate((self.vx + speedDx) * delta, (self.vy + speedDy) * delta)

    @staticmethod
    def _applyFriction(velocity, drop):
        if velocity > 0:
            return max(0, velocity - drop)
        if velocity < 0:
            return min(0, velocity + drop)
        return velocity
