import pygame
from time import time
from objects import Rectangle
from renderer import Renderer, HUD, Camera, easing
from gameevents import Obstacle, InputHandler, CollisionSystem
from gameobjects import Player
from levels import loadLevel, getLevelSize

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Board")


player = Player(Rectangle("player", [100, 0], [20, 70], (255, 255, 255)))

grounds = loadLevel()
LEVEL_WIDTH, LEVEL_HEIGHT = getLevelSize()

class Game():
    def __init__(self):
        self.exit = False
        self.renderer = Renderer(canvas)
        self.hud = HUD(canvas, player)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_WIDTH, LEVEL_HEIGHT)
        self.objects = [player, *grounds]
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
            self.renderer.update(self.objects, self.delta)
            self.collisionSystem.resolve()

            if player.grounded:
                self.camera.setZoom(1.0, duration=0.35, easing=easing.easeOutCubic)
            else:
                self.camera.setZoom(0.8, duration=0.5, easing=easing.easeOutQuad)

            self.camera.update(self.delta)
            self.camera.follow(player)

            self.renderer.draw(self.objects, self.camera.getOffset(), self.camera.zoom)
            self.hud.render()
            pygame.display.update()

        pygame.quit()

game = Game()
game.gameLoop()
