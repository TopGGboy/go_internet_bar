import pygame
from source import setup, tools


class Door(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.frames = []
        self.frame_index = 0
        self.frame_rects = [(11, 12, 51, 79)]

        self.load_frames()

        # 创建精灵类
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

        # 计时器
        self.timer = 0
        # 是否通过
        self.finish = False

    # 加载门的图片
    def load_frames(self):
        self.sheet = setup.GRAPHIC['main']
        for frame_rect in self.frame_rects:
            self.frames.append(tools.get_image(self.sheet, *frame_rect, (255, 255, 255), 1))

    def update(self):
        #  动态效果
        # self.current_time = pygame.time.get_ticks()
        # frame_durations = [200, 200, 200, 200]
        #
        # if self.timer == 0:
        #     self.timer = self.current_time
        # elif self.timer < self.current_time + frame_durations[self.frame_index]:
        #     self.frame_index += 1
        #     self.frame_index %= len(self.frames)
        #     self.timer = self.current_time

        self.image = self.frames[self.frame_index]
