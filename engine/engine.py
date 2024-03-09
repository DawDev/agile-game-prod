import pygame
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config import Config
    from .scene_manager import SceneManager
from .globals import Globals
from .event_manager import EventManager


class Engine:
    def __init__(self, config: "Config") -> None:
        pygame.init()
        self.config: "Config" = config
        self.window: pygame.Surface = pygame.display.set_mode(config.WINDOW_SIZE)
        pygame.display.set_caption(config.WINDOW_CAPTION)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = True
        self.ev_manager: EventManager = EventManager()
        self.scene_manager: "SceneManager" = config.SCENE_MANAGER(self)
        self.globals: Globals = Globals()
        self.globals.CONFIG = config

    def main(self) -> None:
        while self.running:
            self.globals.DELTA_TIME = self.clock.tick(self.config.DESIRED_FPS) / 1000
            self.process_events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit(0)
    
    def process_events(self) -> None:
        self.ev_manager.process_events()

    def update(self) -> None:
        self.scene_manager.update()

    def draw(self) -> None:
        self.scene_manager.draw()
        self.window.blit(
            self.scene_manager.get_scene().surface,
            (0, 0)
        )
        pygame.display.update()
    
    def quit(self, _) -> None:
        self.running = False