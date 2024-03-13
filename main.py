import os
import pygame
from pygame.locals import *
# import pygame_gui as pgui
# import pygame_gui.elements as el
import engine as eng
from scenes import *
from extended_scene_manager import ExtendedSceneManager


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
    if ev.key == K_AMPERSAND:
        game.toggle_debug()
    if ev.key == K_r:
        game.scene_manager.player_coins -= game.scene_manager.get_scene().coinsGathered
        curr_scene = game.scene_manager.current_scene
        game.scene_manager.change_scene(curr_scene)



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
