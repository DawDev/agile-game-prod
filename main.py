import pygame
from pygame.locals import *
# import pygame_gui as pgui
# import pygame_gui.elements as el
import engine as eng
from scenes import *


class ExtendedSceneManager(eng.SceneManager):
    def __init__(self, engine: eng.Engine) -> None:
        super().__init__(engine)
        self.last_level_id: int = 0
    
    def change_to_next_level(self, _id: int) -> None:
        if _id >= self.last_level_id:
            self.change_scene("end_screen")
        self.change_scene(_id+1)

    def add_level(self, level: BaseLevelScene) -> None:
        self.add_scene(self.last_level_id, level)
        self.last_level_id += 1


if __name__ == "__main__":
    conf: eng.Config = eng.Config(
        (800, 600), 
        "Platformah", 
        60,
        SCENE_MANAGER=ExtendedSceneManager
    )

    game: eng.Engine = eng.Engine(conf)

    game.ev_manager.subscribe(QUIT, game.quit)

    game.scene_manager\
        .add_scene("menu", MenuScene(game.scene_manager))\
        .add_scene("level_selection", LevelSelectScene(game.scene_manager))\
        .change_scene("menu")
    for i in range(12):
        game.scene_manager.add_level(BaseLevelScene(game.scene_manager))
    
    game.main()
