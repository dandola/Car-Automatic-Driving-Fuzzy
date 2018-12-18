# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 6
# Rotating Player Sprite
# Video link: https://youtu.be/5M_-cJP5rk8
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
vec = pg.math.Vector2



def draw_traffic_light(surf, x, y, col1, col2, col3):
    BAR_LENGTH = 30
    BAR_HEIGHT = 90
    fill_red = pg.Rect(x,y, 30, BAR_LENGTH)
    fill_amber = pg.Rect(x, y+30, 30, BAR_LENGTH)
    fill_green = pg.Rect(x, y+60, 30, BAR_LENGTH)

    pg.draw.ellipse(surf, col1, fill_red)
    pg.draw.ellipse(surf, col2, fill_amber)
    pg.draw.ellipse(surf, col3, fill_green)
    outline_rect = pg.Rect(x,y,BAR_LENGTH, BAR_HEIGHT)
    pg.draw.rect(surf, LIGHTGREY, outline_rect,1)

def draw_times(surf, text, size, x,y) :
    font= pg.font.Font(pg.font.match_font('arial'),size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_speed(surf, text, size, x,y) :
    font= pg.font.Font(pg.font.match_font('arial'),size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'street2.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.stone_img = pg.image.load(path.join(img_folder, STONE_IMG)).convert_alpha()
        self.flag_img = pg.image.load(path.join(img_folder, FLAG_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img,(TILESIZE,TILESIZE))



    def new(self):
        # initialize all variables and do all the setup for a new game
        self.color_light = BLACK
        self.times = 0
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.stones = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
                for object in self.map.tmxdata.objects:
                    if object.name == "point":
                        self.player.path.append(vec(object.x,object.y))
            if tile_object.name == "dest":
                self.flag = Flag(self, tile_object.x, tile_object.y)
            if tile_object.name == "stone":
                Stone(self, tile_object.id, tile_object.x, tile_object.y,tile_object.width, tile_object.height)
            if tile_object.name == "wall":
                Obstacle(self, tile_object.id ,tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "traffic_light":
                self.traffic_light = Traffic_light(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        self.player.path.append(self.flag.pos)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.draw_traffic()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)


    def draw_traffic(self):
        self.time = pg.time.get_ticks()/1000 % 10
        # print self.time
        self.times = self.time + 1
        self.color_light1 = HIGH_RED
        self.color_light2 = HIGH_YELLOW
        self.color_light3 = HIGH_GREEN
        if self.time < 4:
            self.color_light1 = RED
            self.color_light = RED
            self.traffic_light.light_status = (4 - self.time)/10.0 + 0.625
            self.color_light2 = HIGH_YELLOW
            self.color_light3 = HIGH_GREEN
        elif self.time < 8:
            self.times = self.time - 2
            self.color_light1 = HIGH_RED
            self.color_light2 = HIGH_YELLOW
            self.color_light3 = GREEN
            self.color_light = GREEN
            self.traffic_light.light_status = (8 - self.time)/10.0
        elif self.time < 10:
            self.times = self.time - 5
            self.color_light1 = HIGH_RED
            self.color_light2 = YELLOW
            self.color_light = YELLOW
            self.traffic_light.light_status = (10 - self.time)/10.0 + 0.458
            self.color_light3 = HIGH_GREEN
            

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect),1)
        draw_traffic_light(self.traffic_light.image, 0, 0, self.color_light1, self.color_light2, self.color_light3)
        # draw_traffic_light(self.screen, 500, 10, self.color_light1, self.color_light2, self.color_light3)
        draw_speed(self.screen, str("{:.0f} km/h".format(self.player.player_speed)), 32, 280, 5)
        # draw_times(self.screen, str(self.times.__int__()), 40, 680, 10)
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()