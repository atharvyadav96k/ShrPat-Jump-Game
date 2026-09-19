from ui import Root, Panel, Text, Button


class LevelSelectScreen:
    def __init__(self, canvas, levelCount, onSelectLevel=None):
        self.canvas = canvas
        self.root = Root(canvas)

        panel = self.root.addChild(Panel(x=0.5, y=0.5, width=0.7, height=0.7, anchor="center", color=(20, 20, 20), borderRadius=8))
        panel.addChild(Text("Select Level", x=0.5, y=0.08, anchor="top", fontSize=44, color=(255, 255, 255)))

        columns = 5
        rows = (levelCount + columns - 1) // columns
        gridTop = 0.22
        gridBottom = 0.92
        cellWidth = 1.0 / columns
        cellHeight = (gridBottom - gridTop) / rows

        for i in range(levelCount):
            row = i // columns
            col = i % columns
            centerX = (col + 0.5) * cellWidth
            centerY = gridTop + (row + 0.5) * cellHeight

            panel.addChild(Button(
                x=centerX, y=centerY, width=cellWidth * 0.8, height=cellHeight * 0.7, anchor="center",
                text=str(i + 1),
                onClick=(lambda index=i: onSelectLevel(index)) if onSelectLevel else None,
            ))

    def handleEvent(self, event):
        self.root.handleEvent(event)

    def update(self, delta):
        self.root.update(delta)

    def draw(self, canvas):
        self.root.draw(canvas)
