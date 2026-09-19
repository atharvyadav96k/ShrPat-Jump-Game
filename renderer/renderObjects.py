
class Renderer:
    def __init__(self, canvas):
        self.canvas = canvas

    def render(self, objects, delta):
        for object in objects:
            object.drawObject(self.canvas)
            object.update(delta)
