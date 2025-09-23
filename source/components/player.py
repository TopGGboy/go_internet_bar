import json
import os

import pygame

from source import constans as C
from .. import run_, setup, tools


class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.load_data()
        self.setup_states()
        self.setup_velocitis()
        self.seup_timers()
        self.load_images()

    # 加载玩家数据
    def load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('source/data/player', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)

    # 主角状态
    def setup_states(self):
        self.state = 'stand'
        self.face_right = True
        self.dead = False
        self.can_jump = True
        self.dead_timer = 0

    # 设置速度
    def setup_velocitis(self):
        self.x_vel = 0
        self.y_vel = 0

        self.gravity = C.PLAYER_BUFF['gravity']

    # 设置计时器
    def seup_timers(self):
        self.walking_time = 0

    # 主角造型
    def load_images(self):
        sheet = setup.GRAPHIC["main"]
        frame_rects = self.player_data['image_frames']

        self.right_run_frames = []
        self.left_run_frames = []
        self.up_frames = []
        self.stand = []

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                right_image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'], frame_rect['width'],
                                              frame_rect['height'], (255, 255, 255), C.PLAYER_BUFF['measure'])
                left_image = pygame.transform.flip(right_image, True, False)
                if group == 'right_run':
                    self.right_run_frames.append(right_image)
                    self.left_run_frames.append(left_image)
                if group == 'up':
                    self.up_frames.append(right_image)
                if group == 'stand':
                    self.stand.append(right_image)

        self.frame_index = 0
        self.frames = self.stand
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        print(self.rect)

    def update(self, keys):
        if self.dead == True:
            self.dead_timer = pygame.time.get_ticks()

        self.current_time = pygame.time.get_ticks()
        self.handle_states(keys)

    def handle_states(self, keys):
        # 是否可以跳跃
        self.can_jump_or_not(keys)

        if self.state == 'stand':
            self.stand_state(keys)
        if self.state == 'run':
            self.run_state(keys)
        if self.state == 'jump':
            self.jump_state(keys)
        if self.state == 'fall':
            self.fall_state(keys)

        self.update_image()

    def update_image(self):
        if self.state == 'jump':
            self.image = self.up_frames[0]
        elif self.state == 'stand':
            self.image = self.stand[0]
        elif self.state == 'run':
            if self.face_right:
                self.image = self.right_run_frames[self.frame_index]
            else:
                self.image = self.left_run_frames[self.frame_index]

    def can_jump_or_not(self, keys):
        if not keys[pygame.K_SPACE]:
            self.can_jump = True

    def stand_state(self, keys):
        self.frame_index = 0
        self.x_vel = 0
        self.y_vel = 0
        if keys[pygame.K_d]:
            self.state = 'run'
            self.face_right = True
            self.frames = self.right_run_frames
        elif keys[pygame.K_a]:
            self.state = 'run'
            self.face_right = False
            self.frames = self.left_run_frames

        if keys[pygame.K_SPACE] and self.can_jump:
            self.state = 'jump'
            self.y_vel = -C.PLAYER_BUFF['tall']
            self.frames = self.up_frames

    def run_state(self, keys):
        if self.current_time - self.walking_time > 100:
            if self.frame_index < len(self.frames) - 1:
                self.frame_index += 1
            else:
                self.frame_index = 0
            self.walking_time = self.current_time

        if keys[pygame.K_d]:
            self.face_right = True
            self.x_vel = C.PLAYER_BUFF['x_vel']
        elif keys[pygame.K_a]:
            self.face_right = False
            self.x_vel = -C.PLAYER_BUFF['x_vel']
        else:
            self.x_vel = 0
            self.state = 'stand'

        if keys[pygame.K_SPACE] and self.can_jump:
            self.state = 'jump'
            self.y_vel = -C.PLAYER_BUFF['tall']  # 移动时跳跃高度
            self.frames = self.up_frames

    def jump_state(self, keys):
        self.can_jump = False
        self.y_vel += self.gravity - 0.2

        if self.y_vel >= 0:
            self.state = 'fall'

        if keys[pygame.K_a]:
            self.x_vel = -C.PLAYER_BUFF['x_vel']
        if keys[pygame.K_d]:
            self.x_vel = C.PLAYER_BUFF['x_vel']

        # 小跳
        if not keys[pygame.K_SPACE]:
            self.state = 'fall'

    def fall_state(self, keys):
        self.y_vel = C.PLAYER_BUFF['gravity']

        if keys[pygame.K_a]:
            self.x_vel = -C.PLAYER_BUFF['x_vel']
        elif keys[pygame.K_d]:
            self.x_vel = C.PLAYER_BUFF['x_vel']

    # 主角死亡
    def dead_player(self):
        print("死亡")
        self.dead = True
        self.rect.x = 1000
        self.rect.y = 1000

    # 主角复活
    def back_life_player(self):
        print("复活啦")
