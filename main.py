import pygame
from time import time
from objects import Rectangle
from renderer import Renderer
from gameevents import ObjectEventList, ObjectMove

pygame.init()

canvas = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("My Board")


obj = Rectangle("rect" ,[100, 100], [200, 100])

class Game():
    def __init__(self):
        self.exit = False
        self.renderer = Renderer(canvas)
        self.gameEvents = ObjectEventList()
        self.gameEvents.addOrUpdateObjectEvent("rect", ObjectMove(0, 0))
        self.delta = 0
        self.prevTime = time()
        self.currTime = time()

    def deltaTime(self):
        self.currTime = time()
        self.delta = self.currTime - self.prevTime
        self.prevTime = self.currTime

    def gameLoop(self):
        while not self.exit:
            self.deltaTime()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                moveEvent = self.gameEvents.getEvent("rect")
                if event.type == pygame.KEYDOWN:
                    print(event.key)
                    if event.key == pygame.K_LEFT:
                        moveEvent.move(180, 100)
                    elif event.key == pygame.K_RIGHT:
                        moveEvent.move(0, 100)
                    elif event.key == pygame.K_UP:
                        moveEvent.move(270, 100)
                    elif event.key == pygame.K_DOWN:
                        moveEvent.move(90, 100)
                if event.type == pygame.KEYUP:
                    moveEvent.move(0, 0)

            canvas.fill((0, 0, 0))
            self.renderer.render([obj], self.delta, self.gameEvents)
            pygame.display.update()

        pygame.quit()

game = Game()
game.gameLoop()
