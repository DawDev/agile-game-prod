import pygame
from pygame.locals import *
import engine as eng
from scenes import BaseLevelScene

class ExtendedSceneManager(eng.SceneManager):
    def __init__(self, engine: eng.Engine) -> None:
        super().__init__(engine)
        self.current_level: int = 0
        self.levels: list[str] = []
        self.player_coins: int = 0
        self.level_time: float = 0.0
        self.game_time: float = 0.0
        self.show_gui: bool = False
        label_options: eng.UIOptions = eng.UIOptions(
            draw_background=False,
            draw_border=False,
            antialias=True,
            align="left"
        )
        self.gui_surface: pygame.Surface = pygame.Surface((150, 90))
        self.gui_surface.fill((255, 255, 255))
        self.coins_label: eng.Label = eng.Label(
            pygame.Rect(10, 0, 150, 30), label_options, f"Coins: {self.player_coins}"
        )
        self.game_time_label: eng.Label = eng.Label(
            pygame.Rect(10, 30, 150, 30), label_options, f"Total time: {self.game_time}"
        )
        self.level_time_label: eng.Label = eng.Label(
            pygame.Rect(10, 60, 150, 30), label_options, f"Level time: {self.level_time}"
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
        if type(self.current_scene) is int and self.show_gui: 
            surf: pygame.Surface = self.get_scene().surface
            self.gui_surface.fill((255, 255, 255))
            self.coins_label.draw(self.gui_surface)
            self.level_time_label.draw(self.gui_surface)
            self.game_time_label.draw(self.gui_surface)
            surf.blit(self.gui_surface, (10, 10))

    def update(self) -> None:
        self.show_gui = pygame.key.get_pressed()[K_TAB]
        super().update()
        if type(self.current_scene) is int and self.show_gui: 
            self.coins_label.text = f"Coins: {self.player_coins}"
            self.game_time += eng.Globals().DELTA_TIME
            self.level_time += eng.Globals().DELTA_TIME
            self.game_time_label.text = f"Total time: {round(self.game_time, 2)}"
            self.level_time_label.text = f"Level time: {round(self.level_time, 2)}"
        
    def get_level_count(self) -> int:
        return self.last_level_id - 1
