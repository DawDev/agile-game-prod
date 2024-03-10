import pygame
from dataclasses import dataclass

from .event_manager import EventManager

@dataclass
class UIOptions:
    font_name: str = pygame.font.get_default_font()
    font_size: int = 16
    text_color: tuple[int, int, int] = (10, 10, 10)
    text_padding: int = 5
    antialias: bool = False
    draw_background: bool = True
    background_color: tuple[int, int, int] = (245, 245, 245)
    draw_border: bool = False
    border_color: tuple[int, int, int] = (235, 235, 235)
    border_width: int = 2
    border_radius: int = -1
    border_radia: tuple = (-1, -1, -1, -1)
    hover_darken_percentage: float = 0.1
    _font: pygame.Font | None = None

    def get_font(self) -> pygame.Font:
        if self._font is None:
            self._font = pygame.Font(self.font_name, self.font_size)
        return self._font
    
    def update_font(self) -> None:
        self._font = pygame.Font(self.font_name, self.font_size)

    def get_darkened(self, color: tuple[int, int, int]) -> None:
        darkened = tuple(c * (1 - self.hover_darken_percentage) for c in color)
        return darkened
    
    def get_bg_color(self, darkened: bool) -> tuple[int, int, int]:
        color = self.background_color if not darkened else self.get_darkened(self.background_color)
        return color
    
    def get_border_color(self, darkened: bool) -> tuple[int, int, int]:
        color = self.border_color if not darkened else self.get_darkened(self.border_color)
        return color
    
    def get_text_color(self, darkened: bool) -> tuple[int, int, int]:
        color = self.text_color if not darkened else self.get_darkened(self.text_color)
        return color


class Button:
    def __init__(self, rect: pygame.Rect, options: UIOptions, text: str) -> None:
        self.options: UIOptions = options
        self.rect: pygame.Rect = rect
        self.text: str = text
        self.options.update_font()
        self.hovered: bool = False
    
    def render_text(self) -> tuple[pygame.Surface, pygame.Rect]:
        text: pygame.Surface = self.options.get_font().render(
            self.text, 
            self.options.antialias, 
            self.options.get_text_color(self.hovered), 
            wraplength=self.rect.width - self.options.text_padding * 2
        )
        pos = text.get_rect()
        pos.center = self.rect.center
        return (text, pos)

    
    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface, 
            self.options.get_bg_color(self.hovered), 
            self.rect,
            0,
            self.options.border_radius,
            *self.options.border_radia
        )
        if self.options.draw_border:
            pygame.draw.rect(
                surface, 
                self.options.get_border_color(self.hovered), 
                self.rect,
                self.options.border_width, 
                self.options.border_radius,
                *self.options.border_radia
            )
        text, pos = self.render_text()
        # pygame.draw.rect(surface, (0, 0, 0), pos)
        surface.blit(text, pos)
    
    def update(self) -> None:
        self.hovered = self.rect.collidepoint(*pygame.mouse.get_pos())
    
    def is_clicked(self, btn: int) -> bool:
        if not self.hovered: return False
        for ev in EventManager().get_events(pygame.MOUSEBUTTONDOWN):
            ev: pygame.Event
            if ev.button == btn:
                return True
        return False


class Label:
    def __init__(self, rect: pygame.Rect, options: UIOptions, text: str) -> None:
        self.options: UIOptions = options
        self.rect: pygame.Rect = rect
        self.text: str = text
        self.options.update_font()
    
    def render_text(self) -> tuple[pygame.Surface, pygame.Rect]:
        text: pygame.Surface = self.options.get_font().render(
            self.text, 
            self.options.antialias, 
            self.options.text_color, 
            wraplength=self.rect.width - self.options.text_padding * 2
        )
        pos = text.get_rect()
        pos.center = self.rect.center
        return (text, pos)

    
    def draw(self, surface: pygame.Surface) -> None:
        if self.options.draw_background:
            pygame.draw.rect(
                surface, 
                self.options.background_color, 
                self.rect,
                0,
                self.options.border_radius,
                *self.options.border_radia
            )
        if self.options.draw_border:
            pygame.draw.rect(
                surface, 
                self.options.border_color, 
                self.rect,
                self.options.border_width, 
                self.options.border_radius,
                *self.options.border_radia
            )
        text, pos = self.render_text()
        # pygame.draw.rect(surface, (0, 0, 0), pos)
        surface.blit(text, pos)
    
    def update(self) -> None:
        pass
    