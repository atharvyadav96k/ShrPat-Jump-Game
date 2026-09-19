import pygame
from game import Game
from gamescreen import StartScreen

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)


def showStartScreen():
    started = False

    def onStart():
        nonlocal started
        started = True

    startScreen = StartScreen(canvas, onStart=onStart)
    clock = pygame.time.Clock()

    while not started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            startScreen.handleEvent(event)

        canvas.fill((0, 0, 0))
        startScreen.draw(canvas)
        pygame.display.update()
        clock.tick(60)


showStartScreen()

game = Game(canvas)
game.gameLoop()
