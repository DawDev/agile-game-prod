import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups: tuple[pygame.sprite.Group], 
                image: pygame.Surface = pygame.Surface((50, 50)),
                position: pygame.Vector2 = pygame.Vector2(0, 0)) -> None:
        super().__init__(groups)
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = position