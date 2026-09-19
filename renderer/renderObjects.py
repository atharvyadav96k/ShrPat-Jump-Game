
class Renderer:
    def __init__(self, canvas):
        self.canvas = canvas

    def render(self, objects,delta, events):
        for index ,object in enumerate(objects):
            object.drawObject(self.canvas)
            if index in events:
                self.movementEvent(object, delta)

    def movementEvent(self, object, delta):
        object.moveObject(180, 1, delta)