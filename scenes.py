import engine as eng
import pygame

class MenuScene(eng.Scene):
    def __init__(self, manager: eng.SceneManager) -> None:
        super().__init__(manager)
        self.button_options = eng.UIOptions(
            antialias=True,
            border_radius=5,
            border_radia=(5, 5, 5, 5),
            draw_border=True,
            border_color=(200, 200, 200),
            border_width=2
        )
        self.label_options = eng.UIOptions(
            font_size=60,
            antialias=True,
            draw_background=False
        )
        self.button = eng.Button(
            pygame.Rect(350, 325, 100, 50),
            self.button_options,
            "Play!"
        )
        self.label = eng.Label(
            pygame.Rect(100, 200, 600, 50),
            self.label_options,
            text = "PLATFORMAH"
        )

    def load(self) -> None:
        pass

    def update(self) -> None:
        self.button.update()
        if self.button.is_clicked(1):
            self.scene_manager.change_scene("level_selection")

    def draw(self) -> None:
        self.surface.fill((150, 150, 150))
        self.button.draw(self.surface)
        self.label.draw(self.surface)


class LevelSelectScene(eng.Scene):
    def __init__(self, manager: eng.SceneManager) -> None:
        super().__init__(manager)

    def load(self) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.surface.fill((255, 255, 255))
