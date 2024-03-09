from dataclasses import dataclass
from typing import Type, TYPE_CHECKING

# if TYPE_CHECKING:
from .scene_manager import SceneManager

@dataclass
class Config:
    WINDOW_SIZE: tuple[int, int]
    WINDOW_CAPTION: str 
    DESIRED_FPS: int 
    SCENE_MANAGER: Type[SceneManager] = SceneManager
