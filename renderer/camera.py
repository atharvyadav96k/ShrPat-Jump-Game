from .easing import easeOutQuad


class Camera:
    def __init__(self, screenWidth, screenHeight, levelWidth=None, levelHeight=None, zoomDuration=0.5, easing=easeOutQuad):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.levelWidth = levelWidth
        self.levelHeight = levelHeight
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.zoomStart = 1.0
        self.targetZoom = 1.0
        self.zoomDuration = zoomDuration
        self.zoomElapsed = 0
        self.easing = easing

    def setZoom(self, zoom, duration=None, easing=None):
        if zoom == self.targetZoom:
            return

        self.zoomStart = self.zoom
        self.targetZoom = zoom
        self.zoomElapsed = 0

        if duration is not None:
            self.zoomDuration = duration

        if easing is not None:
            self.easing = easing

    def update(self, delta):
        if self.zoom == self.targetZoom:
            return

        self.zoomElapsed += delta
        t = min(1, self.zoomElapsed / self.zoomDuration) if self.zoomDuration > 0 else 1
        self.zoom = self.zoomStart + (self.targetZoom - self.zoomStart) * self.easing(t)

    def follow(self, target):
        viewWidth = self.screenWidth / self.zoom
        viewHeight = self.screenHeight / self.zoom

        tx, ty, tw, th = target.getBounds()
        self.x = tx + tw / 2 - viewWidth / 2
        self.y = ty + th / 2 - viewHeight / 2

        if self.levelWidth is not None:
            if viewWidth >= self.levelWidth:
                self.x = (self.levelWidth - viewWidth) / 2
            else:
                self.x = max(0, min(self.x, self.levelWidth - viewWidth))

        if self.levelHeight is not None:
            if viewHeight >= self.levelHeight:
                self.y = (self.levelHeight - viewHeight) / 2
            else:
                self.y = max(0, min(self.y, self.levelHeight - viewHeight))

    def getOffset(self):
        return self.x, self.y

    def isNearEdge(self, target, margin=50):
        tx, ty, tw, th = target.getBounds()

        screenX = (tx - self.x) * self.zoom
        screenY = (ty - self.y) * self.zoom
        screenW = tw * self.zoom
        screenH = th * self.zoom

        return (
            screenX < margin
            or screenY < margin
            or screenX + screenW > self.screenWidth - margin
            or screenY + screenH > self.screenHeight - margin
        )
