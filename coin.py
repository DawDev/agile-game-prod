import pygame
from pygame.math import Vector2
from pygame.locals import *
import engine as eng
import math


class Coin(eng.Entity):
    SIZE: int = 50
    def __init__(self, 
        groups: tuple[pygame.sprite.Group] = (), 
        image: pygame.Surface=pygame.transform.scale(pygame.image.load("./assets/coin.png"), (SIZE, SIZE)), 
        position: Vector2=Vector2(0, 0)) -> None:
        super().__init__(groups, image, position)
        self.y_offset: float = 0.0
        self.y_offset_mult: float = 20
        self.y_offset_curve: list[float] = []

        for i in range(0, 30):
            self.y_offset_curve.append(i/30)
        for i in range(30).__reversed__():
            self.y_offset_curve.append(i/30)

        self.y_offset_t: int = 0
        self.animation_speed: float = 50
        self.t_delta_per_sec: float = self.animation_speed / len(self.y_offset_curve)

    def update(self) -> None:
        self.y_offset_t += self.t_delta_per_sec * eng.Globals().DELTA_TIME

        curve_ind = min(math.floor(self.y_offset_t * len(self.y_offset_curve)), len(self.y_offset_curve)-1)
        
        if self.y_offset_t >= 1:
            self.y_offset_t = 0
        self.y_offset = -self.y_offset_curve[curve_ind] * self.y_offset_mult
    
    def render(self, surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y + self.y_offset))
