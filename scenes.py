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
        
        self.label = eng.Label(
            pygame.Rect(100, 200, 600, 50),
            self.label_options,
            text = "LEVEL SELECTION"
        )
        self.buttons: list[eng.Button] = []
        

    def load(self) -> None:
        btn_rect = pygame.Rect(
            100, 350, 100, 50
        )
        btn_margin = 25
        x_offset = 0
        y_offset = 0
        for i in range(self.scene_manager.last_level_id):
            if i % 5 == 0 and not i == 0:
                y_offset += btn_rect.height + btn_margin
                x_offset = 0
            if not i % 5 == 0:
                x_offset += btn_rect.width + btn_margin
            rect: pygame.Rect = btn_rect.copy()
            rect.x += x_offset
            rect.y += y_offset
            btn = eng.Button(rect, self.button_options, f"Level {i+1}")
            btn.level_id = i
            self.buttons.append(btn)

    def update(self) -> None:
        for btn in self.buttons:
            btn.update()
            if btn.is_clicked(1):
                print(btn.level_id)

    def draw(self) -> None:
        self.surface.fill((150, 150, 150))
        self.label.draw(self.surface)
        for btn in self.buttons:
            btn.draw(self.surface)


class BaseLevelScene(eng.Scene):
    def __init__(self, manager: eng.SceneManager) -> None:
        super().__init__(manager)
        self.terrain = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.level_id: int = None

    def update(self) -> None:
        self.coins.update()

    def draw(self) -> None:
        self.surface.fill((255, 255, 255))
        self.terrain.draw(self.surface)
        self.coins.draw(self.surface)