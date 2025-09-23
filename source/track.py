# 陷阱触发 文件
import pygame
from source import constans as C
from source.states import level


class Track:
    def __init__(self):
        self.trap = C.TRAP_TRACK

        self.gear_trap_list = level.Level.TRAP_GEAR_LIST
        self.wall_trap_lit = level.Level.GROUND_LIST
        self.janci_trap_lit = level.Level.TRAP_JANCI_LIST

        self.wall_move_flage = False
        self.wall_move_timer = 0

        self.janci_number = []
        self.janci_move_timer = 0
        self.janci_move_flage = False

    def check_trap(self, player_rect):
        self.player_rect = player_rect
        self.player_right = self.player_rect.right
        self.player_bottom = self.player_rect.bottom
        for trap_name in self.trap:
            if trap_name == 'gear_trap':
                self.track_gear(trap_name)
            elif trap_name == 'wall_trap':
                self.track_wall(trap_name)
            elif trap_name == 'janci_trap':
                self.track_janci(trap_name)

    def track_gear(self, trap_name):
        number = -1
        for trap_xy in self.trap[trap_name]:
            number += 1
            gear = self.gear_trap_list[number]
            if (trap_xy[0] + 5 >= self.player_right >= trap_xy[0] and
                    trap_xy[1] - 5 <= self.player_bottom <= trap_xy[1] + 5):
                gear.gear_1()

    def track_wall(self, trap_name):
        for trap_xy in self.trap[trap_name]:
            wall_number = C.TRAP_XY[trap_name][0]
            way = trap_xy[2]
            if ((trap_xy[0] + 5 >= self.player_right >= trap_xy[0] - 5 and
                 trap_xy[1] - 5 <= self.player_bottom <= trap_xy[1] + 5)) or self.wall_move_flage:

                self.wall_move_flage = True
                self.wall_move_timer += 1

                if (self.wall_move_timer > 100):
                    self.wall_move_flage = False

                for number in wall_number:
                    wall = self.wall_trap_lit[number]
                    wall.wall_1(way)

    def track_janci(self, trap_name):
        number = -1
        for trap_xy in self.trap[trap_name]:
            number += 1
            if not self.janci_number:
                janci = self.janci_trap_lit[number]
            elif number in self.janci_number:
                janci = self.janci_trap_lit[number]

            if ((trap_xy[0] + 5 >= self.player_right >= trap_xy[0] - 5 and
                 trap_xy[1] - 5 <= self.player_bottom <= trap_xy[1] + 5)) or self.janci_move_flage:

                self.janci_number.append(number)
                self.janci_move_timer += 1
                self.janci_move_flage = True

                if (self.janci_move_timer > 100):
                    self.janci_move_flage = False
                    self.janci_number = []
                    if self.janci_number:
                        self.janci_number.remove(number)

                janci.janci_1()
