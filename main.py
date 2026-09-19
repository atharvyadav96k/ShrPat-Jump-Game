import pygame
from game import Game
from gamescreen import StartScreen
from screenmanager import ScreenManager

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)

manager = ScreenManager(canvas)


def showStartScreen():
    manager.setScreen(StartScreen(canvas, onStart=showGame))


def showGame():
    manager.setScreen(Game(canvas, onQuit=showStartScreen))


showStartScreen()
manager.run()
