import pygame
from objects import Rectangle
from renderer import Renderer
pygame.init()

canvas = pygame.display.set_mode((500, 500))
pygame.display.set_caption("My Board")


obj = Rectangle([100, 100], [200, 100])

class Game():
    def __init__(self):
        self.exit = False

    def gameLoop(self):
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            canvas.fill((0, 0, 0))
            Renderer(canvas, [obj]).render()
            pygame.display.update()

        pygame.quit()

game = Game()
game.gameLoop()
