import pygame
from time import time
from objects import Rectangle
from renderer import Renderer, HUD
from gameevents import ControllableObject, Obstacle, InputHandler, CollisionSystem
from gameobjects import Player

pygame.init()

canvas = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("My Board")


player = Player(Rectangle("player", [100, 0], [50, 100], (255, 255, 255)))

ground1 = ControllableObject(
    Rectangle("background", [0, 201], [900, 100], (255, 255, 255)),
    collidable=True,
    rigid=True,
)

ground2 = ControllableObject(
    Rectangle("background", [300, 501], [900, 100], (255, 255, 255)),
    collidable=True,
    rigid=True,
)

opstical = Obstacle(Rectangle("wall", [400, 150], [50, 50], (255, 0, 0)))

class Game():
    def __init__(self):
        self.exit = False
        self.renderer = Renderer(canvas)
        self.hud = HUD(canvas, player)
        self.objects = [player, ground1, ground2, opstical]
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
            self.hud.render()
            pygame.display.update()

        pygame.quit()

game = Game()
game.gameLoop()
