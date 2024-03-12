import os
import pygame
from pygame.locals import *
# import pygame_gui as pgui
# import pygame_gui.elements as el
import engine as eng
from scenes import *


def load_json_level(filename) -> str:
    with open(f"./levels/{filename}", "r") as file:
        return file.read()


def load_levels(game) -> str:
    level_files = os.listdir("./levels/")
    for filename in level_files:
        game.scene_manager.add_level(
            BaseLevelScene(game.scene_manager, load_json_level(filename))
        )


def on_button_down(ev: pygame.event.Event, game: eng.Engine) -> None:
    if ev.key == K_TAB:
        game.toggle_debug()
    if ev.key == K_r:
        game.scene_manager.player_coins -= game.scene_manager.get_scene().coinsGathered
        curr_scene = game.scene_manager.current_scene
        game.scene_manager.change_scene(curr_scene)


class ExtendedSceneManager(eng.SceneManager):
    def __init__(self, engine: eng.Engine) -> None:
        super().__init__(engine)
        self.current_level: int = 0
        self.levels: list[str] = []
        self.player_coins: int = 0
        self.level_time: float = 0.0
        self.game_time: float = 0.0
        label_options: eng.UIOptions = eng.UIOptions(
            draw_background=False,
            draw_border=False,
            antialias=True,
            align="left"
        )
        self.coins_label: eng.Label = eng.Label(
            pygame.Rect(50, 20, 150, 50), label_options, f"Coins: {self.player_coins}"
        )
        self.game_time_label: eng.Label = eng.Label(
            pygame.Rect(50, 70, 150, 50), label_options, f"Total time: {self.game_time}"
        )
        self.level_time_label: eng.Label = eng.Label(
            pygame.Rect(50, 120, 150, 50), label_options, f"Level time: {self.level_time}"
        )
    
    def change_to_next_level(self, _id: int) -> None:
        if len(self.levels) <= _id + 1:
            self.change_scene("end_screen")
            return
        self.current_level = _id + 1
        self.change_scene(_id+1)
        self.level_time = 0.0

    def add_level(self, level: BaseLevelScene) -> None:
        _id = len(self.levels)
        self.levels.append(_id)
        self.add_scene(_id, level)
        level.level_id = _id
    
    def draw(self) -> None:
        super().draw()
        if type(self.current_scene) is int: 
            surf: pygame.Surface = self.get_scene().surface
            self.coins_label.draw(surf)
            self.level_time_label.draw(surf)
            self.game_time_label.draw(surf)

    def update(self) -> None:
        super().update()
        if type(self.current_scene) is int: 
            self.coins_label.text = f"Coins: {self.player_coins}"
            self.game_time += eng.Globals().DELTA_TIME
            self.level_time += eng.Globals().DELTA_TIME
            self.game_time_label.text = f"Total time: {round(self.game_time, 2)}"
            self.level_time_label.text = f"Level time: {round(self.level_time, 2)}"
        
    def get_level_count(self) -> int:
        return self.last_level_id - 1


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
        .add_scene("end_screen", eng.Scene(game.scene_manager))\
        .change_scene("menu")
    # for i in range(12):
    #     game.scene_manager.add_level(BaseLevelScene(game.scene_manager))
    # game.scene_manager.add_level(BaseLevelScene(game.scene_manager, load_json_level("0.json")))
    load_levels(game)

    game.ev_manager.subscribe(KEYDOWN, lambda ev: on_button_down(ev, game))

    game.main()
