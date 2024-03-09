import pygame
from pygame.locals import *
import pygame_gui as pgui
import engine as eng


class MenuScene(eng.Scene):
    def __init__(self, manager: eng.SceneManager) -> None:
        super().__init__(manager)
        self.play_button = pgui.elements.UIButton(
            relative_rect=pygame.Rect((350, 275), (100, 50)),
            text="Play",
            manager=self.UI_manager
        )
    
    def load(self) -> None:
        pass

    def update(self) -> None:
        for ev in eng.EventManager().get_events(pgui.UI_BUTTON_PRESSED):
            if ev.ui_element == self.play_button:
                self.scene_manager.change_scene("main")

    def draw(self) -> None:
        self.surface.fill((255, 255, 255))
        self.UI_manager.draw_ui(self.surface)


if __name__ == "__main__":
    conf: eng.Config = eng.Config(
        (800, 600), 
        "Platformah", 
        60,
    )

    game: eng.Engine = eng.Engine(conf)

    game.ev_manager.subscribe(QUIT, game.quit)

    game.scene_manager.add_scene("menu", MenuScene(game.scene_manager)).change_scene("menu")
    game.main()