import pygame
from pygame import Surface
from source import setup
from source.components import info


class Pause_screen:
    def __init__(self):
        """
        初始化暂停界面
        """
        self.setup_pause()  # 设置暂停界面背景图片
        self.info = info.pause_screen_info()  # 创建暂停界面信息对象

    def setup_pause(self):
        """
        设置暂停界面的背景图片
        """

        self.pause_image = setup.GRAPHIC['pause']  # 获取暂停界面背景图片
        # 将图片缩放至指定大小 (480, 300)
        self.pause_image = pygame.transform.scale(self.pause_image, (480, 300))

    def update(self, surface):
        """
        更新暂停界面（主循环调用）
        :param surface: 绘制表面
        """
        self.draw(surface)

    # 渲染
    def draw(self, surface):
        """
        绘制暂停界面
        :param surface: 绘制表面
         """
        surface.blit(self.pause_image, (190, 130))
        self.info.draw(surface)
