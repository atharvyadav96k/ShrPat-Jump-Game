
class Renderer:
    def __init__(self, canvas):
        self.canvas = canvas

    def render(self, objects,delta, events):
        for object in enumerate(objects):
            object.drawObject(self.canvas)
            if events.contains(object.getObjName()):
                self.movementEvent(object, delta, events[object.getObjName()])

    def movementEvent(self, object, delta, event):
        angle, speed = object.getMoveProperties()
        object.moveObject(angle, speed, delta)
