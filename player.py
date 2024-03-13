import pygame
from pygame.math import Vector2
from pygame.locals import *
import engine as eng


class Player(eng.Entity):
    SIZE: int = 24
    def __init__(self, 
        groups: tuple[pygame.sprite.Group] = (), 
        image: pygame.Surface=pygame.transform.scale(pygame.image.load("./assets/player.png"), (SIZE*0.8333, SIZE)), 
        position: Vector2=Vector2(0, 0)) -> None:
        super().__init__(groups, image, position)
    
        self.y_velocity: float = 0.0
        self.SPEED: int = 200
        self.MAX_FALL_SPEED = 500
        self.JUMP_FORCE = 525
        self.frame_x_vel: float = 0.0
        self.GRAVITY: float = 30
        self.grounded: bool = False

    def move_x(self) -> None:
        keys = pygame.key.get_pressed()
        dt: float = eng.Globals().DELTA_TIME
        x_delta: float = 0

        if keys[K_d] or keys[K_RIGHT]:
            x_delta += 1
        if keys[K_a] or keys[K_LEFT]:
            x_delta -= 1
        self.rect.x += x_delta * dt * self.SPEED
        self.frame_x_vel = x_delta * dt * self.SPEED

    def collide_x(self, group) -> None:
        for ent in group.sprites():
            ent: pygame.sprite.Sprite
            if self.rect.colliderect(ent.rect):
                if self.frame_x_vel > 0:
                    self.rect.right = ent.rect.left
                if self.frame_x_vel < 0:
                    self.rect.left = ent.rect.right

    def move_y(self) -> None:
        keys = pygame.key.get_just_pressed()
        dt: float = eng.Globals().DELTA_TIME

        if (keys[K_w] or keys[K_UP]) and self.grounded:
            self.y_velocity = -self.JUMP_FORCE

        if self.y_velocity > self.MAX_FALL_SPEED:
            self.y_velocity = self.MAX_FALL_SPEED
        
        # if not self.grounded:
        self.y_velocity += self.GRAVITY
        self.rect.y += self.y_velocity * dt
    
    def collide_y(self, group) -> None:
        grounded = False
        for ent in group.sprites():
            ent: pygame.sprite.Sprite
            if self.rect.colliderect(ent.rect):
                if self.y_velocity > 0:
                    self.rect.bottom = ent.rect.top
                    grounded = True
                    self.y_velocity = 0
                if self.y_velocity < 0:
                    self.y_velocity = 0
                    self.rect.top = ent.rect.bottom

            rct = (self.rect.left-3, self.rect.bottom, self.rect.width+3, 3)
            if ent.rect.colliderect(rct):
                grounded = True
        self.grounded = grounded
    
    def collide(self, group) -> tuple[bool, list[eng.Entity]]:
        collided = []
        for ent in group.sprites():
            ent: pygame.sprite.Sprite
            if self.rect.colliderect(ent.rect):
                collided.append(ent)
        return (len(collided) != 0, collided)