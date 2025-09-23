# 主菜单文件
import pygame
from .. import setup
from .. import run_, tools
from source import constans
from source.components import info


class MainMenu:
    def __init__(self):
        self.area_index = None
        self.info = info.main_menu_info()

        self.setup_background()
        self.setup_player()
        self.setup_cursor()

        self.finished = False  # 状态机
        self.next = "load_screen"

    # 初始化背景
    def setup_background(self):
        self.background = setup.GRAPHIC['background']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, setup.C.SCREEN_SIZE)

        self.viewport = setup.SCREEN.get_rect()

        self.cation = tools.get_image(setup.GRAPHIC['main'], 11, 12, 51, 79, (255, 255, 255), 1)

    def setup_player(self):
        pass

    def setup_cursor(self):
        self.cursor = pygame.sprite.Sprite()
        # 光标（门）
        self.cursor.image = tools.get_image(setup.GRAPHIC['main'], 11, 12, 51, 79, (255, 255, 255), 0.8)
        rect = self.cursor.image.get_rect()
        if constans.LEVEL_NUMBER != 0:
            rect.x, rect.y = 280, 260
            self.area_index = 0
        else:
            rect.x, rect.y = 280, 320
            self.area_index = 1
        self.cursor.rect = rect

        self.cursor.state = self.area_index  # 状态机

    def update_cursor(self, event_key):
        area = [260, 320, 380, 440]
        if event_key == pygame.K_w:
            if constans.LEVEL_NUMBER != 0:
                if self.area_index > 0:
                    self.area_index -= 1
            else:
                if self.area_index > 1:  # 防止进入0
                    self.area_index -= 1
            self.cursor.state = self.area_index
            self.cursor.rect.y = area[self.area_index]
        elif event_key == pygame.K_s:
            if self.area_index < 3:
                self.area_index += 1
            self.cursor.state = self.area_index
            self.cursor.rect.y = area[self.area_index]
        elif event_key == pygame.K_RETURN:
            if self.cursor.state == 0:
                self.finished = True
                constans.MAIN_MENU_FLAGE = False
                constans.LEVEL_NUMBER -= 1
            elif self.cursor.state == 1:
                self.finished = True
                constans.MAIN_MENU_FLAGE = False
            elif self.cursor.state == 2:
                print(2)
            elif self.cursor.state == 3:
                print(3)

    def update(self, surface, keys):

        surface.blit(self.background, self.viewport)
        self.info.draw(surface)
        surface.blit(self.cation, (445, 100))
        surface.blit(self.cursor.image, self.cursor.rect)
