from gameevents.controllableObject import ControllableObject


class Ground(ControllableObject):
    def __init__(self, gameObject, zIndex=0):
        super().__init__(gameObject, collidable=True, rigid=True, zIndex=zIndex)
