from source import tools

# 全局量

SCREEN_W, SCREEN_H = 800, 600
SCREEN_SIZE = (SCREEN_W, SCREEN_H)

MAIN_MENU_FLAGE = True

LEVEL_NUMBER = tools.load_map_data("memory.json")['level_number']

# 地图
MAP = None
# 玩家状态
PLAYER_BUFF = None
# 陷阱位置
TRAP_XY = {'gear_trap': [], 'Ground_thorn_trap': [], 'wall_trap': [], 'janci_trap': []}
# 陷阱触发位
TRAP_TRACK = {'gear_trap': [], 'Ground_thorn_trap': [], 'wall_trap': [], 'janci_trap': []}

# 暂停界面控件位置
LOAD_SCREEN_RECT = {"return_home": None, "up_level": None, "down_level": None}

# 鼠标点击切换关卡的变量
button_down = -1
