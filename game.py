import os
import pygame
from renderer import Renderer, HUD, Camera, Background, easing
from gameevents import InputHandler, CollisionSystem
from gameobjects import Player, ScoreCoin, JumpCoin
from levels import loadLevel, getLevelSize
from levels.maps import MAPS
from gamescreen import GameOverScreen, PauseScreen, StartScreen, LevelSelectScreen, WinScreen
from ui import Root, Button
from gamelogger import logger

EDGE_ZOOM_MARGIN = 80
ZOOM_DURATION = 0.4
ZOOM_EASING = easing.easeOutQuad
PLAYER_SIZE = [42, 70]
PLAYER_START = [100, 0]
CAMERA_ZOOM = 1.2
EDGE_ZOOM_OUT_FACTOR = 0.6
MIN_ZOOM = CAMERA_ZOOM * EDGE_ZOOM_OUT_FACTOR

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets", "female-character")
BG_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "assets", "bg.png")
BACKGROUND_PARALLAX = 0.8
PAUSE_BUTTON_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "assets", "ui", "buttons", "pause", "pause_button.png")


def _showLevelSelect(canvas, manager):
    manager.setScreen(LevelSelectScreen(
        canvas, len(MAPS),
        onSelectLevel=lambda index: manager.setScreen(Game(canvas, manager, levelMap=MAPS[index])),
    ))


def buildStartScreen(canvas, manager):
    return StartScreen(canvas, onStart=lambda: _showLevelSelect(canvas, manager))


class Game:
    def __init__(self, canvas, manager, levelMap=None):
        self.canvas = canvas
        self.manager = manager
        self.levelMap = levelMap
        screenWidth, screenHeight = canvas.get_size()

        self.player = Player.fromAssets(ASSETS_DIR, PLAYER_START, PLAYER_SIZE)
        self.background = Background(
            pygame.image.load(BG_IMAGE_PATH).convert(),
            parallaxFactor=BACKGROUND_PARALLAX,
            screenHeight=screenHeight,
            minZoom=MIN_ZOOM,
        )

        grounds = loadLevel(self.levelMap)
        levelWidth, levelHeight = getLevelSize(self.levelMap)

        self.renderer = Renderer(canvas)
        self.hud = HUD(canvas, self.player)
        self.camera = Camera(screenWidth, screenHeight, levelWidth, levelHeight)
        self.objects = [self.player, *grounds]
        self.inputHandler = InputHandler(self.objects)
        self.collisionSystem = CollisionSystem(self.objects)
        self.cameraZoom = CAMERA_ZOOM
        self.gameOverScreen = GameOverScreen(canvas, onRestart=self.restart, onQuit=self._quit)

        self.totalCoins = self._countCoins(grounds)
        self.won = False
        self.winScreen = WinScreen(canvas, onRestart=self.restart, onQuit=self._quit)

        self.paused = False
        self.pauseScreen = PauseScreen(canvas, onResume=self.togglePause, onQuit=self._quit)
        pauseButtonImage = pygame.image.load(PAUSE_BUTTON_IMAGE_PATH).convert_alpha()
        self.pauseUI = Root(canvas)
        self.pauseUI.addChild(Button(
            x=0.02, y=0.02, width=0.06, height=0.1, anchor="topleft",
            text="", onClick=self.togglePause, image=pauseButtonImage,
        ))

        logger.info(
            "level started: levelMap=%s objects=%d totalCoins=%d",
            "default" if self.levelMap is None else f"map(rows={len(self.levelMap)})",
            len(self.objects), self.totalCoins,
        )

    def restart(self):
        self.player = Player.fromAssets(ASSETS_DIR, PLAYER_START, PLAYER_SIZE)
        grounds = loadLevel(self.levelMap)
        self.objects = [self.player, *grounds]
        self.inputHandler = InputHandler(self.objects)
        self.collisionSystem = CollisionSystem(self.objects)
        self.hud.player = self.player
        self.gameOverScreen.hide()

        self.totalCoins = self._countCoins(grounds)
        self.won = False
        self.winScreen.hide()

        logger.info("level restarted: objects=%d totalCoins=%d", len(self.objects), self.totalCoins)

    @staticmethod
    def _countCoins(objects):
        return sum(1 for obj in objects if isinstance(obj, (ScoreCoin, JumpCoin)))

    def _quit(self):
        logger.info("quit to start screen")
        self.manager.setScreen(buildStartScreen(self.canvas, self.manager))

    def togglePause(self):
        if self.player is None or self.won:
            return

        self.paused = not self.paused
        logger.debug("pause toggled: paused=%s", self.paused)

        if self.paused:
            self.pauseScreen.show()
        else:
            self.pauseScreen.hide()

    def handleEvent(self, event):
        if self.player is None:
            self.gameOverScreen.handleEvent(event)
            return

        self.pauseUI.handleEvent(event)

        if self.won:
            self.winScreen.handleEvent(event)
        elif self.paused:
            self.pauseScreen.handleEvent(event)
        else:
            self.inputHandler.handleEvent(event)

    def update(self, delta):
        if self.player is not None:
            self.pauseUI.update(delta)

        if self.won:
            self.winScreen.update(delta)
            return

        if self.paused:
            self.pauseScreen.update(delta)
            return

        self.renderer.update(self.objects, delta)
        self.collisionSystem.resolve()
        self.objects[:] = [obj for obj in self.objects if not getattr(obj, "destroyed", False)]

        if self.player is not None and self.player.destroyed:
            logger.info("player removed after death animation")
            self.hud.player = None
            self.player = None
            self.gameOverScreen.show()

        if self.player is None:
            self.gameOverScreen.update(delta)

        if self.player is not None and self.totalCoins > 0 and self._countCoins(self.objects) == 0:
            logger.info("all coins collected, player won")
            self.won = True
            self.winScreen.show()

        if self.player is not None:
            self.camera.follow(self.player)

            if self.camera.shouldZoomOut(self.player, triggerMargin=EDGE_ZOOM_MARGIN):
                self.camera.setZoom(MIN_ZOOM, duration=ZOOM_DURATION, easing=ZOOM_EASING)
            else:
                self.camera.setZoom(self.cameraZoom, duration=ZOOM_DURATION, easing=ZOOM_EASING)

            self.camera.update(delta)
            self.camera.follow(self.player)

    def draw(self, canvas):
        ui = self.gameOverScreen if self.player is None else None
        self.renderer.draw(self.objects, self.camera.getOffset(), self.camera.zoom, self.background, ui=ui)
        self.hud.render()

        if self.player is not None:
            self.pauseUI.draw(canvas)

            if self.won:
                self.winScreen.draw(canvas)
            elif self.paused:
                self.pauseScreen.draw(canvas)
