class CollisionSystem:
    def __init__(self, objects):
        self.objects = objects

    def resolve(self):
        collidables = [obj for obj in self.objects if obj.collidable]

        for i, a in enumerate(collidables):
            for b in collidables[i + 1:]:
                if self._overlaps(a.getBounds(), b.getBounds()):
                    a.onCollision(b)
                    b.onCollision(a)

    @staticmethod
    def _overlaps(boundsA, boundsB):
        xA, yA, wA, hA = boundsA
        xB, yB, wB, hB = boundsB
        return xA < xB + wB and xA + wA > xB and yA < yB + hB and yA + hA > yB
