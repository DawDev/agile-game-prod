import pygame
from typing import TYPE_CHECKING, Self

from .scene import Scene

if TYPE_CHECKING:
    from .engine import Engine
    

class SceneManager:
    def __init__(self, eng: "Engine") -> None:
        self.eng: "Engine" = eng
        self.scenes: dict[str, "Scene"] = {'default': Scene(self)}
        self.current_scene: str = "default"

    def get_scene(self) -> "Scene":
        return self.scenes.get(self.current_scene)

    def add_scene(self, name: str, scene: "Scene") -> Self:
        self.scenes[name] = scene
        return self
    
    def remove_scene(self, name: str) -> Self:
        del self.scenes[name]
        return self
    
    def change_scene(self, name: str) -> Self:
        print(name)
        self.get_scene().unload()
        self.current_scene = name
        self.get_scene().load()
        return self
    
    def update(self) -> None:
        self.get_scene().update()
        self.get_scene().update_gui()
    
    def draw(self) -> None:
        self.get_scene().draw()