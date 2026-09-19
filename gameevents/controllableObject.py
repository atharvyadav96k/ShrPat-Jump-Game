class ControllableObject:
    def __init__(self, gameObject, bindings=None, collidable=False):
        self.gameObject = gameObject
        self.bindings = dict(bindings) if bindings else {}
        self.angle = 0
        self.speed = 0
        self.activeKey = None
        self.collidable = collidable
        self.previousBounds = gameObject.getBounds()

    def enableCollision(self):
        self.collidable = True

    def disableCollision(self):
        self.collidable = False

    def getBounds(self):
        return self.gameObject.getBounds()

    def onCollision(self, other):
        x, y, _, _ = self.previousBounds
        self.gameObject.setPosition(x, y)

    def bindKey(self, key, angle, speed):
        self.bindings[key] = (angle, speed)

    def unbindKey(self, key):
        self.bindings.pop(key, None)

    def getObjName(self):
        return self.gameObject.getObjName()

    def handleKeyDown(self, key):
        if key not in self.bindings:
            return

        self.angle, self.speed = self.bindings[key]
        self.activeKey = key

    def handleKeyUp(self, key):
        if self.activeKey != key:
            return

        self.angle, self.speed = 0, 0
        self.activeKey = None

    def drawObject(self, canvas):
        self.gameObject.drawObject(canvas)

    def update(self, delta):
        self.previousBounds = self.gameObject.getBounds()
        self.gameObject.moveObject(self.angle, self.speed, delta)
