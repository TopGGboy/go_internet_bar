# 游戏初始启动向

import pygame
from source import constans as C
from source import run_, tools

pygame.init()
SCREEN = pygame.display.set_mode((C.SCREEN_W, C.SCREEN_H))

GRAPHIC = tools.load_graphics('resources/graphics')

MAP_DATA = tools.load_map_data('map.json')
TRAP_DATA = tools.load_map_data('trap.json')

Level_font = pygame.font.Font('./resources/font/font_1.ttf', 50)
Other_font = pygame.font.Font('./resources/font/font_1.ttf', 30)

Main_menu_font = pygame.font.Font('./resources/font/font_1.ttf', 40)


# 初始化陷阱
def set_up_trap():
    # 陷阱位置
    C.TRAP_XY = {'gear_trap': [], 'Ground_thorn_trap': [], 'wall_trap': [], 'janci_trap': []}
    # 陷阱触发位置
    C.TRAP_TRACK = {'gear_trap': [], 'Ground_thorn_trap': [], 'wall_trap': [], 'janci_trap': []}
