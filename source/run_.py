# 工具和游戏主控
import os
import pygame
import random
from source import constans
import json
from source.states import load_screen, level, pause_screen
from source.states import main_menu, load_screen, level


# 游戏主控
class Game:
    def __init__(self):
        """
        初始化游戏控制器
        """
        self.screen = pygame.display.get_surface()  # 获取显示表面
        self.clock = pygame.time.Clock()  # 创建时钟对象的控制频率

        self.keys = pygame.key.get_pressed()  # 获取当前的按键状态

        self.pause_screen = pause_screen.Pause_screen()  # 暂停界面实例

        self.state_dict = None  # 状态字典，存储不同游戏状态
        self.state = main_menu.MainMenu()  # 当前游戏状态， 默认围为主菜单
        self.pause = False  # 暂停状态
        self.return_home_flage = False  # 返回主菜单标志

    def run(self):
        """
        游戏主循环
        """
        while True:
            # 鼠标事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()  # 退出游戏
                elif event.type == pygame.KEYDOWN:
                    # 判断是否在主页面
                    flage = constans.MAIN_MENU_FLAGE
                    if flage == True:
                        self.state.update_cursor(event.key)  # 更新光标
                    # --------------------------------------#

                    self.keys = pygame.key.get_pressed()

                    # 暂停
                    if event.key == pygame.K_ESCAPE and flage == False:
                        self.pause = not self.pause
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()  # 更新按键状态
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.pause_mouse_event(event)  # pause界面的鼠标检测和功能

            # 如果没有暂停则更新游戏状态
            if not self.pause:
                self.update()

            # 如果暂停则显示暂停界面
            if self.pause:
                # pause界面的鼠标检测
                self.pause_screen.update(self.screen)

            pygame.display.update()  # 更新显示
            self.clock.tick(60)  # 控制帧率为60fps


    def update(self):
        """
        更新游戏状态
        """
        # 如果当前状态完全且不需要返回主菜单
        if self.state.finished and self.return_home_flage == False:
            next_state = self.state.next  # 获取下一个状态s

            # 根据下一个状态创建对应的状态字典
            if next_state == 'load_screen':
                self.state_dict = {
                    "load_screen": load_screen.LoadScreen(),
                }
            elif next_state == 'level':
                self.state_dict = {
                    "level": level.Level(),
                }

            self.state.finished = False  # 重置当前状态完成标志
            self.state = self.state_dict[next_state]  # 切换到下一个状态

        elif self.state.finished and self.return_home_flage == True:
            self.state.finished = False
            self.return_home_flage = False
            self.state = main_menu.MainMenu()

        self.state.update(self.screen, self.keys)

    # pause界面的鼠标检测和功能
    def pause_mouse_event(self, event):
        """
        处理暂停界面的鼠标事件
        :param event: 鼠标事件
        """
        if event.button == 1:  # 左键点击
            mouse_x, mouse_y = pygame.mouse.get_pos()  # 获取鼠标位置

            if (constans.LOAD_SCREEN_RECT['return_home'][0] < mouse_x < constans.LOAD_SCREEN_RECT['return_home'][2] and
                    constans.LOAD_SCREEN_RECT['return_home'][1] < mouse_y < constans.LOAD_SCREEN_RECT['return_home'][
                        3]):
                self.pause = not self.pause  # 取消暂停
                # 返回主界面
                self.return_home_flage = True  # 设置返回主菜单标志
                self.state.finished = True  # 标记当前状态完成
                constans.MAIN_MENU_FLAGE = True  # 设置主菜单标志
            elif (constans.LOAD_SCREEN_RECT['up_level'][0] < mouse_x < constans.LOAD_SCREEN_RECT['up_level'][2] and
                  constans.LOAD_SCREEN_RECT['up_level'][1] < mouse_y < constans.LOAD_SCREEN_RECT['up_level'][3]):
                constans.button_down = 1  # 设置按钮状态
                self.pause = not self.pause  # 取消暂停

            # 检测是否点击了"下一级"按钮
            elif (constans.LOAD_SCREEN_RECT['down_level'][0] < mouse_x < constans.LOAD_SCREEN_RECT['down_level'][2] and
                  constans.LOAD_SCREEN_RECT['down_level'][1] < mouse_y < constans.LOAD_SCREEN_RECT['down_level'][3]):
                constans.button_down = 2  # 设置按钮状态
                self.pause = not self.pause  # 取消暂停
