import pygame
from source import setup, constans
from source import tools


# 加载管卡页面信息   以及 关卡的数据
class Info:
    def __init__(self, state):  # state 接受是哪个页面
        self.state = state
        self.map_data = setup.MAP_DATA
        self.trap_data = setup.TRAP_DATA

        self.text = None
        self.level_number()

        self.Level_font = setup.Level_font
        self.Other_font = setup.Other_font

        self.load_screen_info()

    # 判断关卡 并 加载资源
    def level_number(self):
        constans.LEVEL_NUMBER += 1
        self.text = "第" + str(constans.LEVEL_NUMBER) + '关'
        # 初始化陷阱
        setup.set_up_trap()
        for name in self.map_data:
            if self.map_data[name]['number'] == constans.LEVEL_NUMBER:
                constans.MAP = self.map_data[name]['map']
                constans.PLAYER_BUFF = self.map_data[name]['buff']
                tools.modify_json('source/data/maps/memory.json', "level_number", constans.LEVEL_NUMBER)


                # 读取陷阱信息
                for trap_name in self.trap_data[name]:
                    for trap in self.trap_data[name][trap_name]:
                        trap = str(trap)
                        constans.TRAP_XY[trap_name].append(self.trap_data[name][trap_name][trap]['trap_xy'])
                        print(self.trap_data[name][trap_name][trap]['trap_xy'])
                        constans.TRAP_TRACK[trap_name].append(self.trap_data[name][trap_name][trap]['trap_track'])
                        print(self.trap_data[name][trap_name][trap]['trap_track'])

    # 加载文字信息
    def load_screen_info(self):
        self.Level_text = self.Level_font.render(self.text, True, (255, 255, 255))
        self.Level_rect = self.Level_text.get_rect()
        self.Level_rect.center = (100, 100)

    # 渲染
    def draw(self, surface):
        if self.state == 'load_screen':
            surface.blit(self.Level_text, self.Level_rect)


# 主页面文字信息
class main_menu_info:
    def __init__(self):
        self.Main_menu_font = setup.Main_menu_font
        self.load_screen_info()

    # 加载文字信息
    def load_screen_info(self):
        if constans.LEVEL_NUMBER != 0:
            self.continue_game = self.Main_menu_font.render("继续游戏", True, (0, 0, 0))
            self.continue_game_rect = self.continue_game.get_rect()
            self.continue_game_rect.center = (400, 280)

        self.new_game = self.Main_menu_font.render("新游戏", True, (0, 0, 0))
        self.new_game_rect = self.new_game.get_rect()
        self.new_game_rect.center = (380, 340)

        self.about = self.Main_menu_font.render("关于", True, (0, 0, 0))
        self.about_rect = self.about.get_rect()
        self.about_rect.center = (357, 400)

        self.quit = self.Main_menu_font.render("退出游戏", True, (0, 0, 0))
        self.quit_rect = self.quit.get_rect()
        self.quit_rect.center = (400, 460)

    def draw(self, surface):
        if constans.LEVEL_NUMBER != 0:
            surface.blit(self.continue_game, self.continue_game_rect)
        surface.blit(self.new_game, self.new_game_rect)
        surface.blit(self.about, self.about_rect)
        surface.blit(self.quit, self.quit_rect)


# 暂停界面信息
class pause_screen_info:
    def __init__(self):
        self.Main_menu_font = setup.Main_menu_font
        self.load_screen_info()

    def load_screen_info(self):
        self.return_home = self.Main_menu_font.render("返回主界面", True, (0, 0, 0))
        self.return_home_rect = self.return_home.get_rect()
        self.return_home_rect.center = (420, 300)

        self.save_load_rect(self.return_home_rect, 'return_home')

        self.up_level = self.Main_menu_font.render("上一关", True, (0, 0, 0))
        self.up_level_rect = self.up_level.get_rect()
        self.up_level_rect.center = (280, 400)

        self.save_load_rect(self.up_level_rect, "up_level")

        self.down_level = self.Main_menu_font.render("下一关", True, (0, 0, 0))
        self.down_level_rect = self.down_level.get_rect()
        self.down_level_rect.center = (580, 400)

        self.save_load_rect(self.down_level_rect, "down_level")

        print(constans.LOAD_SCREEN_RECT)

    # 保存控件位置
    def save_load_rect(self, kongjian, name):
        list_ = []
        list_.append(kongjian.x)
        list_.append(kongjian.y)
        list_.append(kongjian.right)
        list_.append(kongjian.bottom)
        constans.LOAD_SCREEN_RECT[name] = list_

    def draw(self, surface):
        surface.blit(self.return_home, self.return_home_rect)
        surface.blit(self.up_level, self.up_level_rect)
        surface.blit(self.down_level, self.down_level_rect)
