import pygame
from game import Game
from gamescreen import StartScreen
from screenmanager import ScreenManager

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)

manager = ScreenManager(canvas)
manager.setScreen(StartScreen(canvas, onStart=lambda: manager.setScreen(Game(canvas, manager))))
manager.run()
