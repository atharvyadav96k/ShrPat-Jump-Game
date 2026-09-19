
class Renderer:
    def __init__(self, canvas):
        self.canvas = canvas

    def render(self, objects, delta):
        for object in objects:
            object.update(delta)

        for object in sorted(objects, key=lambda o: o.zIndex):
            object.drawObject(self.canvas)
