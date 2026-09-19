import pygame
from time import time
from objects import Rectangle
from renderer import Renderer
from gameevents import ControllableObject, InputHandler, CollisionSystem

pygame.init()

canvas = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("My Board")


player = ControllableObject(
    Rectangle("player", [100, 0], [50, 100], (255, 255, 255)),
    bindings={
        pygame.K_w: (270, 400),
        pygame.K_LEFT: (180, 150),
        pygame.K_RIGHT: (0, 150),
    },
    collidable=True,
    gravity=True,
)

ground = ControllableObject(
    Rectangle("background", [0, 201], [1200, 100], (255, 255, 255)),
    bindings={
        pygame.K_a: (180, 150),
        pygame.K_d: (0, 150),
    },
    collidable=True,
    rigid=True,
)

class Game():
    def __init__(self):
        self.exit = False
        self.renderer = Renderer(canvas)
        self.objects = [player, ground]
        self.inputHandler = InputHandler(self.objects)
        self.collisionSystem = CollisionSystem(self.objects)

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

                self.inputHandler.handleEvent(event)

            canvas.fill((0, 0, 0))
            self.renderer.render(self.objects, self.delta)
            self.collisionSystem.resolve()
            pygame.display.update()

        pygame.quit()

game = Game()
game.gameLoop()
