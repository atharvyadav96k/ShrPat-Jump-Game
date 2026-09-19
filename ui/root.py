from .element import UIElement


class Root(UIElement):
    def __init__(self, canvas):
        super().__init__(relative=False)
        self.canvas = canvas

    def getRect(self):
        width, height = self.canvas.get_size()
        return (0, 0, width, height)
