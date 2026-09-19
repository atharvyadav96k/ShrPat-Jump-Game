from gameevents.controllableObject import ControllableObject


class Ground(ControllableObject):
    def __init__(self, gameObject):
        super().__init__(gameObject, collidable=True, rigid=True)
