import pygame


class HUD:
    def __init__(self, canvas, player):
        self.canvas = canvas
        self.player = player
        self.font = pygame.font.SysFont(None, 28)

    def render(self):
        healthText = f"Health: {self.player.health}/{self.player.maxHealth}"
        healthSurface = self.font.render(healthText, True, (255, 255, 255))
        healthRect = healthSurface.get_rect(topleft=(10, 10))
        self.canvas.blit(healthSurface, healthRect)

        if self.player.airJumpLocked:
            remaining = max(0, self.player.airJumpRefillTime - self.player.airJumpTimer)
            text = f"Boost: recharging {remaining:.1f}s"
            color = (255, 120, 120)
        else:
            text = f"Boost: {self.player.airJumpsRemaining}/{self.player.maxAirJumps}"
            color = (255, 255, 255)

        surface = self.font.render(text, True, color)
        rect = surface.get_rect(topright=(self.canvas.get_width() - 10, 10))
        self.canvas.blit(surface, rect)
