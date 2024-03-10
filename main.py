import pygame
from pygame.locals import *
# import pygame_gui as pgui
# import pygame_gui.elements as el
import engine as eng
from scenes import *


class ExtendedSceneManager(eng.SceneManager):
    def __init__(self, engine: eng.Engine) -> None:
        super().__init__(engine)
        self.levels: list[eng.Scene] = [

        ]


if __name__ == "__main__":
    conf: eng.Config = eng.Config(
        (800, 600), 
        "Platformah", 
        60,
    )

    game: eng.Engine = eng.Engine(conf)

    game.ev_manager.subscribe(QUIT, game.quit)

    game.scene_manager\
        .add_scene("menu", MenuScene(game.scene_manager))\
        .add_scene("level_selection", LevelSelectScene(game.scene_manager))\
        .change_scene("menu")
    
    game.main()