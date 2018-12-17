import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (110, 110, 110)

GREEN = (48, 255, 2)
HIGH_GREEN = (0,60,0)

RED = (255, 0, 0)
HIGH_RED = (100,0,0)

YELLOW = (254, 251, 2)
HIGH_YELLOW = (144, 144, 60)

BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WIDTH_PATH = 128


WALL_IMG ='tileGreen_39.png'
STONE_IMG = 'stone.png'
FLAG_IMG = 'flag4.png'

# Player settings
PLAYER_SPEED = 100.0
PLAYER_ROT_SPEED = 250.0
PLAYER_IMG = 'car4.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 32, 32)