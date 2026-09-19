import pygame


class ScreenManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.screen = None
        self.running = True
        self.clock = pygame.time.Clock()

    def setScreen(self, screen):
        self.screen = screen

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            delta = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.screen is not None:
                    self.screen.handleEvent(event)

            if self.screen is not None:
                self.screen.update(delta)

            self.canvas.fill((0, 0, 0))
            if self.screen is not None:
                self.screen.draw(self.canvas)

            pygame.display.update()

        pygame.quit()
