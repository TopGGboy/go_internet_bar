# 主菜单文件
import pygame
from .. import setup
from .. import run_, tools
from source import constans
from source.components import info


class MainMenu:
    def __init__(self):
        """
        初始化主菜单状态
        """
        self.area_index = None  # 当前光标选中的菜单项索引
        self.info = info.main_menu_info()  # 创建主菜单信息对象，用于显示文字

        self.setup_background()  # 设置背景
        self.setup_player()  # 设置玩家（当前为空)
        self.setup_cursor()  # 设置光标

        self.finished = False  # 状态机
        self.next = "load_screen"

    # 初始化背景
    def setup_background(self):
        """
        设置主菜单背景图片
        """

        self.background = setup.GRAPHIC['background']  # 获取背景图片
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, setup.C.SCREEN_SIZE)  # 缩放到屏幕大小

        self.viewport = setup.SCREEN.get_rect()  # 获取屏幕矩形区域

        # 获取装饰用的门图片
        self.cation = tools.get_image(setup.GRAPHIC['main'], 11, 12, 51, 79, (255, 255, 255), 1)

    def setup_player(self):
        """
        设置玩家（主菜单中未使用）
        """
        pass

    def setup_cursor(self):
        """
        设置光标（用于菜单选择）
        """
        self.cursor = pygame.sprite.Sprite()
        # 光标（门）
        self.cursor.image = tools.get_image(setup.GRAPHIC['main'], 11, 12, 51, 79, (255, 255, 255), 0.8)
        rect = self.cursor.image.get_rect()

        # 根据是否有已保存的游戏进度设置光标初始位置
        if constans.LEVEL_NUMBER != 0:
            rect.x, rect.y = 280, 260
            self.area_index = 0  # 有存档时，默认选择"继续游戏"
        else:
            rect.x, rect.y = 280, 320
            self.area_index = 1  # 无存档时，默认选择"新游戏"
        self.cursor.rect = rect

        self.cursor.state = self.area_index  # 设置光标状态

    def update_cursor(self, event_key):
        """
        更新光标位置（处理键盘输入）
        :param event_key: 按下的键盘按键
        """
        area = [260, 320, 380, 440]  # 菜单项的Y坐标列表
        if event_key == pygame.K_w:  # 向上移动光标
            # 根据是否有存档决定是否可以选中第一个选项
            if constans.LEVEL_NUMBER != 0:
                if self.area_index > 0:
                    self.area_index -= 1
            else:
                if self.area_index > 1:  # 防止进入0（无存档时不能选择"继续游戏"）
                    self.area_index -= 1
            self.cursor.state = self.area_index
            self.cursor.rect.y = area[self.area_index]
        elif event_key == pygame.K_s:  # 向下移动光标
            if self.area_index < 3:  # 最多只能移动到第4个选项
                self.area_index += 1
            self.cursor.state = self.area_index
            self.cursor.rect.y = area[self.area_index]
        elif event_key == pygame.K_RETURN:  # 回车键确认选择
            if self.cursor.state == 0:  # 选择"继续游戏"
                self.finished = True  # 标记当前状态完成
                constans.MAIN_MENU_FLAGE = False  # 设置不在主菜单状态
                constans.LEVEL_NUMBER -= 1  # 回到上一关
            elif self.cursor.state == 1:  # 选择"新游戏"
                self.finished = True
                constans.MAIN_MENU_FLAGE = False
            elif self.cursor.state == 2:  # 选择"关于"
                print(2)
            elif self.cursor.state == 3:  # 选择"退出游戏"
                print(3)

    def update(self, surface, keys):
        """
        更新主菜单画面
        :param surface: 绘制表面
        :param keys: 键盘按键状态
        """

        surface.blit(self.background, self.viewport)  # 绘制背景
        self.info.draw(surface)  # 绘制菜单文字信息
        surface.blit(self.cation, (445, 100))  # 绘制装饰图片
        surface.blit(self.cursor.image, self.cursor.rect)  # 绘制光标
