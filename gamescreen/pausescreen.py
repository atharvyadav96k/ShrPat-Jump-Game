from ui import Root, Panel, Text, Button


class PauseScreen:
    def __init__(self, canvas, onResume=None, onQuit=None):
        self.canvas = canvas
        self.root = Root(canvas)
        self.root.visible = False

        panel = self.root.addChild(Panel(x=0.5, y=0.5, width=0.4, height=0.45, anchor="center", color=(20, 20, 20), borderRadius=8))
        panel.addChild(Text("Paused", x=0.5, y=0.15, anchor="top", fontSize=48, color=(255, 255, 255)))
        panel.addChild(Button(
            x=0.5, y=0.55, width=0.6, height=0.18, anchor="center",
            text="Resume", onClick=onResume,
        ))
        panel.addChild(Button(
            x=0.5, y=0.8, width=0.6, height=0.18, anchor="center",
            text="Quit", onClick=onQuit,
        ))

    def show(self):
        self.root.visible = True

    def hide(self):
        self.root.visible = False

    def handleEvent(self, event):
        self.root.handleEvent(event)

    def update(self, delta):
        self.root.update(delta)

    def draw(self, canvas):
        self.root.draw(canvas)
