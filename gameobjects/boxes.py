from gameevents.controllableObject import ControllableObject


class Boxes(ControllableObject):
    def __init__(self, gameObject):
        super().__init__(gameObject, collidable=False, rigid=True, zIndex=3)
