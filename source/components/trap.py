import pygame
from source import tools, setup


# 齿轮陷阱
class trap_gear(pygame.sprite.Sprite):
    def __init__(self, x, y, name, resize):
        pygame.sprite.Sprite.__init__(self)
        self.resize = resize
        self.frames = []
        self.frame_index = 0
        self.frame_rects = [(72, 8, 50, 50), (128, 8, 50, 50), (189, 8, 50, 50), (251, 8, 50, 50)]
        self.load_frames()
        # 创建精灵
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.center = self.rect.center

        # 计时器
        self.timer = 0

        self.name = name

    # 加载陷阱齿轮图像
    def load_frames(self):
        self.sheet = setup.GRAPHIC['main']
        for frame_rect in self.frame_rects:
            self.frames.append(tools.get_image(self.sheet, *frame_rect, (255, 255, 255), self.resize))

    def gear_1(self):
        frames = []
        for frame_rect in self.frame_rects:
            frames.append(tools.get_image(self.sheet, *frame_rect, (255, 255, 255), 3))
        self.frames = frames
        # 改变完尺寸后得重新放入精灵族

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def update(self):
        self.current_time = pygame.time.get_ticks()
        frame_durations = [200, 200, 200, 200]

        if self.timer == 0:
            self.timer = self.current_time
        elif self.current_time - self.timer > frame_durations[self.frame_index]:
            self.frame_index += 1
            self.frame_index %= len(frame_durations)
            self.timer = self.current_time

        self.image = self.frames[self.frame_index]


# 地刺陷阱
class Ground_thorn_trap(pygame.sprite.Sprite):
    def __init__(self, x, y, name, resize, way):
        pygame.sprite.Sprite.__init__(self)
        self.resize = resize
        self.x = x
        self.y = y
        self.name = name
        self.way = way
        self.frames = []
        self.frame_index = 0
        self.frame_rects = [(75, 63, 50, 35)]

        self.load_frames()

        # 创建精灵类
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # 计时器
        self.timer = 0

    # 加载地刺陷阱 图像
    def load_frames(self):
        self.sheet = setup.GRAPHIC['main']
        for frame_rect in self.frame_rects:
            self.frames.append(tools.get_image(self.sheet, *frame_rect, (255, 255, 255), self.resize))

    def update(self):
        # 动态效果
        # self.current_time = pygame.time.get_ticks()
        # frame_durations = [200, 200, 200, 200]
        #
        # if self.timer == 0:
        #     self.timer = self.current_time
        # elif self.timer - self.current_time > frame_durations[self.frame_index]:
        #     self.frame_index += 1
        #     self.frame_index %= len(frame_durations)
        #     self.timer = self.current_time

        self.image = self.frames[self.frame_index]
        self.image_rota()

    def image_rota(self):
        if self.way == "up":
            pass
        elif self.way == 'down':
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.way == 'left':
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.way == 'right':
            self.image = pygame.transform.rotate(self.image, -90)


# 墙体移动
class Wall_trap(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.name = name
        self.frames = []
        self.frame_index = 0
        self.frame_rects = [(746, 9, 50, 50)]

        self.load_frames()

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # 计时器
        self.timer = 0

    # 加载墙面的图片
    def load_frames(self):
        self.sheet = setup.GRAPHIC['main']
        for frame_rect in self.frame_rects:
            image = tools.get_image(self.sheet, *frame_rect, (255, 255, 255), 1)
            ground_image = pygame.transform.scale(image, (50, 52))
            self.frames.append(ground_image)

    def wall_1(self, way):
        speed = 10
        if way == 1:  # 上
            self.rect.y -= speed
        elif way == 2:  # 下
            self.rect.y += speed
        elif way == 3:  # 左
            self.rect.x -= speed
        elif way == 4:  # 右
            self.rect.x += speed

    def update(self):
        self.image = self.frames[self.frame_index]


# 尖刺陷阱
class janci_trap(pygame.sprite.Sprite):
    def __init__(self, x, y, name, resize, way):
        pygame.sprite.Sprite.__init__(self)
        self.resize = resize
        self.way = way
        self.frames = []
        self.frame_index = 0
        self.frame_rects = [(10, 197, 19, 61)]
        self.load_frames()
        # 创建精灵
        self.image = self.frames[self.frame_index]
        # 旋转图片
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.center = self.rect.center

        # 计时器
        self.timer = 0

        self.name = name

    # 加载尖刺陷阱图像
    def load_frames(self):
        self.sheet = setup.GRAPHIC['main']
        for frame_rect in self.frame_rects:
            self.frames.append(tools.get_image(self.sheet, *frame_rect, (255, 255, 255), 1))

    def janci_1(self):
        speed = 10
        if self.way == 'up':
            self.rect.y -= speed
        elif self.way == 'down':
            self.rect.y += speed
        elif self.way == 'left':
            self.rect.x -= speed
        elif self.way == 'right':
            self.rect.x += speed

    def update(self):
        # self.current_time = pygame.time.get_ticks()
        # frame_durations = [200, 200, 200, 200]
        #
        # if self.timer == 0:
        #     self.timer = self.current_time
        # elif self.current_time - self.timer > frame_durations[self.frame_index]:
        #     self.frame_index += 1
        #     self.frame_index %= len(frame_durations)
        #     self.timer = self.current_time

        self.image = self.frames[self.frame_index]
        self.image_rota()

    def image_rota(self):
        if self.way == 'up':
            pass
        elif self.way == 'down':
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.way == 'left':
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.way == 'right':
            self.image = pygame.transform.rotate(self.image, 90)
