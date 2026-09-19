from .controllableObject import ControllableObject


class Obstacle(ControllableObject):
    def __init__(self, gameObject, gravityAccel=900):
        super().__init__(gameObject, collidable=True, gravity=True, gravityAccel=gravityAccel)
