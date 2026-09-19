import pygame
from time import time
from objects import Rectangle
from renderer import Renderer

pygame.init()

canvas = pygame.display.set_mode((500, 500))
pygame.display.set_caption("My Board")


obj = Rectangle([100, 100], [200, 100])

class Game():
    def __init__(self):
        self.exit = False
        self.renderer = Renderer(canvas)
        self.delta = 0
        self.prevTime = time()
        self.currTime = time()

    def deltaTime(self):
        self.currTime = time()
        self.delta = self.currTime - self.prevTime
        self.prevTime = self.currTime

    def gameLoop(self):
        gameEvents = [0]

        while not self.exit:
            self.deltaTime()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            canvas.fill((0, 0, 0))
            self.renderer.render([obj],self.delta, gameEvents)
            pygame.display.update()

        pygame.quit()

game = Game()
game.gameLoop()
