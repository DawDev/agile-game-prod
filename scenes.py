import pygame
import json
import engine as eng
from player import Player
from coin import Coin

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
        for i in range(len(self.scene_manager.levels)):
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
                self.scene_manager.change_scene(btn.level_id)

    def draw(self) -> None:
        self.surface.fill((150, 150, 150))
        self.label.draw(self.surface)
        for btn in self.buttons:
            btn.draw(self.surface)


class BaseLevelScene(eng.Scene):
    def __init__(self, manager: eng.SceneManager, map_json: str) -> None:
        super().__init__(manager)
        self.terrain: pygame.sprite.Group = pygame.sprite.Group()
        self.coins: pygame.sprite.Group = pygame.sprite.Group()
        self.player: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
        self.wins: pygame.sprite.Group = pygame.sprite.Group()
        self.level_id: int = None
        self.map_json: str = map_json

    def load(self) -> None:
        self.coinsGathered = 0
        map_dict = json.loads(self.map_json)
        tile_size = map_dict.get("tile_size")
        for tile in map_dict.get("tiles"):
            ttype = tile.get("tile_type")
            x_pos = int(tile.get("position")[0])
            y_pos = int(tile.get("position")[1])
            position = pygame.math.Vector2(x_pos*tile_size, y_pos*tile_size)
            if ttype is None:
                continue
            if ttype == "terrain":
                eng.Entity([self.terrain], 
                    pygame.Surface((tile_size, tile_size)),
                    position)
            if ttype == "player":
                Player([self.player], position=position)
            if ttype == "win":
                w = eng.Entity([self.wins], 
                    pygame.Surface((tile_size, tile_size)),
                    position)
                w.image.fill((255, 215, 0))
            if ttype == "coin":
                Coin([self.coins], position=position)

    def unload(self) -> None:
        self.player.empty()
        self.coins.empty()
        self.terrain.empty()
        self.wins.empty()

    def process_collisions(self) -> None:
        cCol, coins = self.player.sprite.collide(self.coins)
        wCol, wins = self.player.sprite.collide(self.wins)
        if cCol:
            for c in coins:
                c: Coin
                c.remove(self.coins)
                self.scene_manager.player_coins += 1
                self.coinsGathered += 1
        if wCol:
            self.scene_manager.change_to_next_level(self.level_id)


    def update(self) -> None:
        self.coins.update()
        self.player.sprite.move_x()
        self.player.sprite.collide_x(self.terrain)
        self.player.sprite.move_y()
        self.player.sprite.collide_y(self.terrain)
        
        self.process_collisions()

    def draw(self) -> None:
        self.surface.fill((255, 255, 255))
        self.terrain.draw(self.surface)
        self.wins.draw(self.surface)
        # self.coins.draw(self.surface)
        for c in self.coins.sprites():
            c.render(self.surface)
        self.player.draw(self.surface)
        if not eng.Globals().DEBUG:
            return
        pygame.draw.rect(self.surface, (255, 0, 0), self.player.sprite.rect, 1)
        for t in self.terrain.sprites():
            pygame.draw.rect(self.surface, (255, 0, 0), t.rect, 1)
        for c in self.coins.sprites():
            pygame.draw.rect(self.surface, (255, 0, 0), c.rect, 1)
    


# class LevelOne(BaseLevelScene):
#     def __init__(self, manager: eng.SceneManager) -> None:
#         super().__init__(manager)
#         self.player.add(Player(position=pygame.math.Vector2(50, 50)))
#         self.terrain.add(eng.Entity(position=pygame.math.Vector2(150, 50)))
#         self.coins.add(Coin(position=pygame.math.Vector2(300, 300)))
