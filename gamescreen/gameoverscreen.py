from ui import Root, Panel, Text, Button


class GameOverScreen:
    def __init__(self, canvas, onRestart=None):
        self.canvas = canvas
        self.root = Root(canvas)
        self.root.visible = False

        panel = self.root.addChild(Panel(x=0.5, y=0.5, width=0.4, height=0.3, anchor="center", color=(20, 20, 20), borderRadius=8))
        panel.addChild(Text("Game Over", x=0.5, y=0.2, anchor="top", fontSize=48, color=(255, 0, 0)))
        panel.addChild(Button(
            x=0.5, y=0.7, width=0.5, height=0.25, anchor="center",
            text="Restart", onClick=onRestart,
        ))

    def show(self):
        self.root.visible = True

    def hide(self):
        self.root.visible = False

    def handleEvent(self, event):
        self.root.handleEvent(event)

    def draw(self, canvas):
        self.root.draw(canvas)
