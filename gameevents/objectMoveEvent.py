class ObjectMove():
    def __init__(self,angle = 0, speed = 0):
        self.angle = angle
        self.speed = speed

    def move(self, angle, speed):
        self.angle = angle
        self.speed = speed

    def getMoveProperties(self):
        return self.angle, self.speed

