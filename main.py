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
        pygame.K_UP: (270, 400),
    },
    speedBindings={
        pygame.K_RIGHT: (0, 200),
        pygame.K_LEFT: (180, 200),
    },
    collidable=True,
    gravity=True,
    friction=0,
)

ground = ControllableObject(
    Rectangle("background", [0, 201], [1200, 100], (255, 255, 255)),
    collidable=True,
    rigid=True,
)

opstical = ControllableObject(
    Rectangle("wall", [400, 100], [50, 50], (255, 0, 0)),
    collidable=True,
    gravity=True
)

class Game():
    def __init__(self):
        self.exit = False
        self.renderer = Renderer(canvas)
        self.objects = [player, ground, opstical]
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
