import pygame


class Animation:
    def __init__(self, frames, frameDuration=0.1, loop=True, waitForTrigger=False):
        self.frames = frames
        self.flipped = [pygame.transform.flip(frame, True, False) for frame in frames]
        self.frameDuration = frameDuration
        self.loop = loop
        self.waitForTrigger = waitForTrigger
        self.index = 0
        self.timer = 0
        self.triggered = False

    def reset(self):
        self.index = 0
        self.timer = 0
        self.triggered = False

    def trigger(self):
        if not self.waitForTrigger:
            return

        self.triggered = True
        self.index = len(self.frames) - 1

    def isFinished(self):
        return not self.loop and self.index >= len(self.frames) - 1

    def _maxIndex(self):
        if self.waitForTrigger and not self.triggered:
            return max(0, len(self.frames) - 2)

        return len(self.frames) - 1

    def update(self, delta):
        if not self.frames:
            return False

        if self.loop:
            self.timer += delta
            if self.timer < self.frameDuration:
                return False

            self.timer -= self.frameDuration
            self.index = (self.index + 1) % len(self.frames)
            return True

        maxIndex = self._maxIndex()
        if self.index >= maxIndex:
            return False

        self.timer += delta
        if self.timer < self.frameDuration:
            return False

        self.timer -= self.frameDuration
        self.index = min(self.index + 1, maxIndex)
        return True

    def currentFrame(self, flipped=False):
        frames = self.flipped if flipped else self.frames
        return frames[min(self.index, len(frames) - 1)]
