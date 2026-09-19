from .animation import Animation


class Animator:
    def __init__(self, target):
        self.target = target
        self.animations = {}
        self.state = None
        self.facing = 0

    def add(self, name, frames, frameDuration=0.1, loop=True, waitForTrigger=False):
        self.animations[name] = Animation(frames, frameDuration, loop, waitForTrigger)

        if name == self.state:
            self.animations[name].reset()
            self._apply()

    def setState(self, name, restart=False):
        if name not in self.animations:
            return

        if name == self.state and not restart:
            return

        self.state = name
        self.animations[name].reset()
        self._apply()

    def setFacing(self, angle):
        if self.facing == angle:
            return

        self.facing = angle
        self._apply()

    def trigger(self):
        anim = self.animations.get(self.state)
        if not anim:
            return

        anim.trigger()
        self._apply()

    def update(self, delta):
        anim = self.animations.get(self.state)
        if not anim:
            return

        if anim.update(delta):
            self._apply()

    def currentState(self):
        return self.state

    def _apply(self):
        anim = self.animations.get(self.state)
        if not anim or not hasattr(self.target, "setImage"):
            return

        self.target.setImage(anim.currentFrame(flipped=self.facing == 180))
