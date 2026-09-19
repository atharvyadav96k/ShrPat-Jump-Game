ANCHORS = {
    "topleft": (0.0, 0.0),
    "top": (0.5, 0.0),
    "topright": (1.0, 0.0),
    "left": (0.0, 0.5),
    "center": (0.5, 0.5),
    "right": (1.0, 0.5),
    "bottomleft": (0.0, 1.0),
    "bottom": (0.5, 1.0),
    "bottomright": (1.0, 1.0),
}


class UIElement:
    def __init__(self, x=0, y=0, width=1.0, height=1.0, relative=True, anchor="topleft"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.relative = relative
        self.anchor = anchor
        self.parent = None
        self.children = []
        self.visible = True

    def addChild(self, child):
        child.parent = self
        self.children.append(child)
        return child

    def getRect(self):
        px, py, pw, ph = self.parent.getRect() if self.parent else (0, 0, 0, 0)

        w = pw * self.width if self.relative else self.width
        h = ph * self.height if self.relative else self.height
        offsetX = pw * self.x if self.relative else self.x
        offsetY = ph * self.y if self.relative else self.y

        anchorX, anchorY = ANCHORS.get(self.anchor, (0.0, 0.0))
        posX = px + offsetX - w * anchorX
        posY = py + offsetY - h * anchorY

        return (posX, posY, w, h)

    def update(self, delta):
        for child in self.children:
            child.update(delta)

    def draw(self, canvas):
        if not self.visible:
            return

        self.drawSelf(canvas)
        for child in self.children:
            child.draw(canvas)

    def drawSelf(self, canvas):
        pass

    def handleEvent(self, event):
        if not self.visible:
            return

        for child in self.children:
            child.handleEvent(event)

        self.handleSelfEvent(event)

    def handleSelfEvent(self, event):
        pass
