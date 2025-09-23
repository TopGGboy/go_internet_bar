import os
import pygame
import json
from source import constans as C


# 加载图片
def load_graphics(path, accept=('.png', '.jpg', '.bmp', '.gif')):
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name] = img
    return graphics


# 获取图片
def get_image(sheet, x, y, width, height, colorkey, scale):  # scale放大倍数
    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    return image


# 加载地图数据
def load_map_data(file_name):
    file_name = file_name
    file_path = os.path.join('source/data/maps', file_name)
    with open(file_path) as f:
        data = json.load(f)
    return data


# 修改json数据
def modify_json(filename, key, new_value):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data[key] = new_value

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
