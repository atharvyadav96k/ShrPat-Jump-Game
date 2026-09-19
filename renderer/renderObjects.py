
class Renderer:
    def __init__(self, canvas,objects):
        self.objects = objects
        self.canvas = canvas

    def render(self):
        for object in self.objects:
            object.drawObject(self.canvas)