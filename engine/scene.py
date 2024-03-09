import pygame
import pygame_gui as pgui
from typing import TYPE_CHECKING

# from .config import Config
if TYPE_CHECKING:
    from .scene_manager import SceneManager
from .event_manager import EventManager
from .globals import Globals

class Scene:
    def __init__(self, scene_manager: "SceneManager") -> None:
        self.scene_manager: "SceneManager" = scene_manager
        self.surface: pygame.Surface = pygame.Surface(scene_manager.eng.config.WINDOW_SIZE)
        self.UI_manager = pgui.UIManager(scene_manager.eng.config.WINDOW_SIZE)
    
    def load(self) -> None:
        pass

    def update_gui(self) -> None:
        for e in EventManager().frame_events:
            self.UI_manager.process_events(e)
        self.UI_manager.update(Globals().DELTA_TIME)

    def update(self) -> None:
        pass
    
    def draw(self) -> None:
        pass

    def unload(self) -> None:
        pass