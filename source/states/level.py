import json
import os
import pygame
from pygame import surface

from source import constans, track
from source.components import player, trap, door
from source import setup, run_, tools


class Level:
    # 地面对象列表
    GROUND_LIST = []
    # 地面精灵族
    GROUND_ITEMS_GROUP = pygame.sprite.Group()

    # 陷阱精灵族
    TRAP_ITEMS_GROUP = pygame.sprite.Group()

    # 各类陷阱列表
    TRAP_GEAR_LIST = []
    TRAP_DICI_LIST = []
    TRAP_JANCI_LIST = []

    def __init__(self):

        # 初始化类列表
        Level.GROUND_LIST = []
        Level.TRAP_GEAR_LIST = []
        Level.TRAP_DICI_LIST = []
        Level.TRAP_JANCI_LIST = []

        # 清空精灵族
        Level.GROUND_ITEMS_GROUP.empty()
        Level.TRAP_ITEMS_GROUP.empty()

        # 关卡状态标志
        self.finished = False  # 关卡是否结束
        self.next = 'load_screen'  # 下一个状态
        self.ground_number = 0  # 地面编号计数器
        self.trap_number = 0  # 陷阱编号计数器
        self.map = constans.MAP  # 地图数据

        # 初始化玩家、门和轨迹检测
        self.setup_player_door()
        # 加载地图
        self.load_map()

        # 复活计时器
        self.back_life_timer = 0

    # 加载地图
    def load_map(self):
        wall_x = 0  # 墙块x坐标
        wall_y = 0  # 墙块y坐标
        # 遍历地图数据
        for y in self.map:
            for x in y:
                # 墙块(地面)
                if x == 1:
                    self.ground_number += 1
                    # 加载路面并放入列表
                    self.setup_ground(wall_x, wall_y)
                # 玩家起始位置
                elif x == 10:
                    self.player.rect.x = wall_x
                    self.player.rect.y = wall_y + 1
                # 门位置
                elif x == 100:
                    self.door.rect.x = wall_x
                    self.door.rect.y = wall_y - 12

                wall_x += 50  # 每个地块宽度为50像素
            wall_x = 0  # 换行重置x坐标
            wall_y += 50  # 每个地块高度为50像素

        # 加载陷阱
        self.load_trap()

    # 加载陷阱
    def load_trap(self):
        # 加载齿轮陷阱
        for trap_xy in constans.TRAP_XY['gear_trap']:
            self.setup_gear_trap(x=trap_xy[0], y=trap_xy[1], resize=trap_xy[2])
        self.trap_number = 0

        # 加载地刺陷阱
        for trap_xy in constans.TRAP_XY['Ground_thorn_trap']:
            self.setup_dici_trap(x=trap_xy[0], y=trap_xy[1], resize=trap_xy[2], way=trap_xy[3])
        self.trap_number = 0

        # 加载尖刺陷阱
        for trap_xy in constans.TRAP_XY['janci_trap']:
            self.setup_janci_trap(x=trap_xy[0], y=trap_xy[1], resize=trap_xy[2], way=trap_xy[3])

    # ------------------------------------------------------------------------------------------
    # todo  这里待优化
    # 初始化 尖刺陷阱 并放入列表
    def setup_janci_trap(self, x, y, resize, way):
        janci_trap_number = "jianci_trap_" + str(self.trap_number)
        janci_trap = trap.janci_trap(x, y, janci_trap_number, resize, way)
        Level.TRAP_JANCI_LIST.append(janci_trap)
        Level.TRAP_ITEMS_GROUP.add(janci_trap)

        self.trap_number += 1

    # 初始化 地刺陷阱 并放入列表和精灵组
    def setup_dici_trap(self, x, y, resize, way):
        di_trap_number = "dici_trap_" + str(self.trap_number)
        dici_trap = trap.Ground_thorn_trap(x, y, di_trap_number, resize, way)
        Level.TRAP_DICI_LIST.append(dici_trap)
        Level.TRAP_ITEMS_GROUP.add(dici_trap)
        self.trap_number += 1

    # 初始化 齿轮陷阱 并放入列表和精灵组
    def setup_gear_trap(self, x, y, resize):
        gear_trap_name = "gear_trap_" + str(self.trap_number)
        gear_trap = trap.trap_gear(x, y, gear_trap_name, resize)
        Level.TRAP_GEAR_LIST.append(gear_trap)
        Level.TRAP_ITEMS_GROUP.add(gear_trap)
        self.trap_number += 1

    # 初始化路面并放入列表和精灵组
    def setup_ground(self, x, y):
        ground_name = "ground_" + str(self.ground_number)
        ground = trap.Wall_trap(x, y, ground_name)
        Level.GROUND_LIST.append(ground)
        Level.GROUND_ITEMS_GROUP.add(ground)

    # ----------------------------------------------------------------------------------

    # 初始化玩家 和 门 和 碰撞检测
    def setup_player_door(self):
        self.player = player.Player("GZJ")  # 创建玩家对象
        self.door = door.Door("door")  # 创建门对象
        self.track_check = track.Track()  # 创建轨迹检测对象

    def update(self, surface, keys):
        # TODO 暂时的进入下一关的代码
        # 游戏成功 进入下一关
        if keys[pygame.K_DOWN] or constans.button_down == 2:
            self.finished = True
            # 恢复默认值
            constans.button_down = -1

        # 检查玩家是否到达门前
        self.player_check_door()

        # 游戏失败 重新这一关
        if keys[pygame.K_LEFT] or self.player.dead_timer > 5000:
            self.player.dead_timer = 0

            self.finished = True
            # 直接重新进入这一关， 不需要加载界面
            self.next = "level"
            if constans.LEVEL_NUMBER > 0:
                constans.LEVEL_NUMBER -= 1

            # 复活
            self.player.back_life_player()
        # 返回上一关
        if keys[pygame.K_UP] or constans.button_down == 1:
            self.finished = True
            # 恢复默认值
            constans.button_down = -1
            if constans.LEVEL_NUMBER != 1:
                constans.LEVEL_NUMBER -= 2
            else:
                constans.LEVEL_NUMBER = 0

        # 更新玩家状态
        self.player.update(keys)
        # 更新玩家位置
        self.update_player_position()
        # 绘制游戏画面
        self.draw(surface)

    # 判断玩家是否到达了门前 是否可以进入下一关
    def player_check_door(self):
        if (self.player.rect.left >= self.door.rect.left and
                self.player.rect.right <= self.door.rect.right and
                self.player.rect.top >= self.door.rect.top and
                self.player.rect.bottom <= self.door.rect.bottom):
            self.finished = True
            # 恢复默认值
            constans.button_down = -1

    # 更新玩家位置（移动）
    def update_player_position(self):
        # x方向移动
        self.player.rect.x += self.player.x_vel
        self.check_x_collision()

        # y方向移动
        self.player.rect.y += self.player.y_vel
        self.check_y_collision()

        # 陷阱启位置检测
        self.track_check.check_trap(self.player.rect)

        # 人物与陷阱的碰撞检测
        self.check_player_trap()
        # 检测是否掉出屏幕， 掉出屏幕死亡
        self.check_in_screen()

    # 检测是否掉出屏幕， 掉出屏幕死亡
    def check_in_screen(self):
        if (self.player.rect.x < 0 or
                self.player.rect.x > constans.SCREEN_W or
                self.player.rect.y < 0 or self.player.rect.y > constans.SCREEN_H):
            self.player.dead_player()

    # 检测是否碰到陷阱
    def check_player_trap(self):
        for trap in Level.TRAP_ITEMS_GROUP:
            trap_item = pygame.sprite.collide_mask(self.player, trap)
            if trap_item:
                self.player.dead_player()
                break

    # 检测x方向是否碰撞
    def check_x_collision(self):
        ground_item = pygame.sprite.spritecollideany(self.player, Level.GROUND_ITEMS_GROUP)
        if ground_item:
            self.adjust_player_x(ground_item)

    # 检测y方向是否碰撞
    def check_y_collision(self):
        ground_item = pygame.sprite.spritecollideany(self.player, Level.GROUND_ITEMS_GROUP)
        if ground_item:
            self.adjust_player_y(ground_item)

        # 检测是否一会会掉落
        self.check_will_fall(self.player)

    # 判断 x 方向 是 才能够左边还是右边 碰撞
    def adjust_player_x(self, sprite):
        if self.player.rect.x < sprite.rect.left:
            self.player.rect.right = sprite.rect.left
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_vel = 0

    # 判断 y 方向 是 才能够上边还是下边 碰撞
    def adjust_player_y(self, sprite):
        # downwards
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.y_vel = 0
            self.player.rect.bottom = sprite.rect.top
            self.player.state = 'run'
        #  upwards
        else:
            self.player.y_vel = 7
            self.player.rect.top = sprite.rect.bottom
            self.player.state = 'fall'

    def check_will_fall(self, sprite):
        sprite.rect.y += 1
        collided = pygame.sprite.spritecollideany(sprite, Level.GROUND_ITEMS_GROUP)
        if not collided and sprite.state != "jump":
            sprite.state = "fall"
        sprite.rect.y -= 1

    # 渲染
    def draw(self, surface):
        # 填充白色背景
        surface.fill((255, 255, 255))
        # 绘制地图
        self.draw_map(surface)
        # 绘制门
        surface.blit(self.door.image, self.door.rect)
        # 绘制玩家
        surface.blit(self.player.image, self.player.rect)

    # 画路面 以及 陷阱等
    def draw_map(self, surface):
        # 绘制地面
        for ground in Level.GROUND_LIST:
            surface.blit(ground.image, ground.rect)
        # 绘制齿轮陷阱
        for trap in Level.TRAP_GEAR_LIST:
            trap.update()
            surface.blit(trap.image, trap.rect)
        # 绘制地刺陷阱
        for trap in Level.TRAP_DICI_LIST:
            trap.update()
            surface.blit(trap.image, trap.rect)
        # 绘制尖刺陷阱
        for trap in Level.TRAP_JANCI_LIST:
            trap.update()
            surface.blit(trap.image, trap.rect)
