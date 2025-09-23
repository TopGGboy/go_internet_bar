import pygame
from pygame import Surface
from source import setup
from source.components import info


class Pause_screen:
    def __init__(self):
        self.setup_pause()
        self.info = info.pause_screen_info()

    def setup_pause(self):
        self.pause_image = setup.GRAPHIC['pause']
        self.pause_image = pygame.transform.scale(self.pause_image, (480, 300))

    def update(self, surface):
        self.draw(surface)

    # 渲染
    def draw(self, surface):
        surface.blit(self.pause_image, (190, 130))
        self.info.draw(surface)
