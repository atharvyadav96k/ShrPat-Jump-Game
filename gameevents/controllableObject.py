import math


class ControllableObject:
    def __init__(self, gameObject, bindings=None, collidable=False, rigid=False, gravity=False, gravityAccel=900):
        self.gameObject = gameObject
        self.bindings = dict(bindings) if bindings else {}
        self.vx = 0
        self.vy = 0
        self.collidable = collidable
        self.rigid = rigid
        self.previousBounds = gameObject.getBounds()
        self.gravity = gravity
        self.gravityAccel = gravityAccel

    def enableCollision(self):
        self.collidable = True

    def disableCollision(self):
        self.collidable = False

    def enableGravity(self, accel=900):
        self.gravity = True
        self.gravityAccel = accel

    def disableGravity(self):
        self.gravity = False

    def getBounds(self):
        return self.gameObject.getBounds()

    def onCollision(self, other):
        if self.rigid:
            return

        x, y, _, _ = self.previousBounds
        self.gameObject.setPosition(x, y)
        self.vx = 0
        self.vy = 0

    def bindKey(self, key, angle, force):
        self.bindings[key] = (angle, force)

    def unbindKey(self, key):
        self.bindings.pop(key, None)

    def getObjName(self):
        return self.gameObject.getObjName()

    def applyForce(self, angle, magnitude):
        rad = math.radians(angle)
        self.vx += math.cos(rad) * magnitude
        self.vy += math.sin(rad) * magnitude

    def handleKeyDown(self, key):
        if key not in self.bindings:
            return

        angle, force = self.bindings[key]
        self.applyForce(angle, force)

    def drawObject(self, canvas):
        self.gameObject.drawObject(canvas)

    def update(self, delta):
        self.previousBounds = self.gameObject.getBounds()

        if self.gravity:
            self.applyForce(90, self.gravityAccel * delta)

        self.gameObject.translate(self.vx * delta, self.vy * delta)
