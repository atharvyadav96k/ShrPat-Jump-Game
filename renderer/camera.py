class Camera:
    def __init__(self, screenWidth, screenHeight, levelWidth=None, levelHeight=None, zoomSmoothing=4.0):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.levelWidth = levelWidth
        self.levelHeight = levelHeight
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.targetZoom = 1.0
        self.zoomSmoothing = zoomSmoothing

    def setZoom(self, zoom):
        self.targetZoom = zoom

    def update(self, delta):
        if self.zoom == self.targetZoom:
            return

        t = min(1, self.zoomSmoothing * delta)
        self.zoom += (self.targetZoom - self.zoom) * t

        if abs(self.targetZoom - self.zoom) < 0.001:
            self.zoom = self.targetZoom

    def follow(self, target):
        viewWidth = self.screenWidth / self.zoom
        viewHeight = self.screenHeight / self.zoom

        tx, ty, tw, th = target.getBounds()
        self.x = tx + tw / 2 - viewWidth / 2
        self.y = ty + th / 2 - viewHeight / 2

        if self.levelWidth is not None:
            self.x = max(0, min(self.x, max(0, self.levelWidth - viewWidth)))

        if self.levelHeight is not None:
            self.y = max(0, min(self.y, max(0, self.levelHeight - viewHeight)))

    def getOffset(self):
        return self.x, self.y
