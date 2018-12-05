import pygame as pg
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2
import math

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        # print(hits)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width /2.0
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width /2.0
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # print hits
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.0
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2.0
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0,0)
        self.path = []
        self.player_speed = PLAYER_SPEED
        self.rot_speed = 0
        self.rot = 0
        self.index = 0

    # def get_keys(self):
    #     self.rot_speed = 0
    #     self.vel = vec(0, 0)
    #     keys = pg.key.get_pressed()
    #     if keys[pg.K_LEFT] or keys[pg.K_a]:
    #         self.rot_speed = PLAYER_ROT_SPEED
    #     if keys[pg.K_RIGHT] or keys[pg.K_d]:
    #         self.rot_speed = -PLAYER_ROT_SPEED
    #     if keys[pg.K_UP] or keys[pg.K_w]:
    #         self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
    #     if keys[pg.K_DOWN] or keys[pg.K_s]:
    #         self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)

    def distance(self, dest):
        distance = math.sqrt((dest.x - self.pos.x)**2 + (dest.y - self.pos.y)**2)
        return distance

    def update(self):
        # list_points = self.path
        # # print list_points
        # immediate_point = None
        # path_min = math.sqrt((self.game.flag.pos.x - self.pos.x)**2 + (self.game.flag.pos.y - self.pos.y)**2)
        # for point in list_points:
        #     distance = math.sqrt((point[0] - self.pos.x)**2 + (point[1] - self.pos.y)**2)
        #     if distance <= path_min:
        #         path_min = distance
        #         immediate_point = point
        # print self.path
        self.rot = (self.path[self.index] - self.pos).angle_to(vec(1,0))%360
        # print self.rot
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        distance = self.distance(self.path[self.index])
        self.move(distance)
        if distance <= 20:
            self.index +=1
            if self.index == len(self.path):
                self.index -= 1
                self.player_speed = 0
        # change_car_speed


    def move(self, distance):
        if distance < 30:
            self.acc = vec(self.player_speed/2,0).rotate(-self.rot)
        else:
            self.acc = vec(self.player_speed,0).rotate(-self.rot)
        self.acc += self.vel*-1
        self.vel += self.acc*self.game.dt
        self.pos += self.vel*self.game.dt + self.acc*self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.stones,'y')
        # self.rect.center = self.hit_rect.center
        self.rect.center = self.pos



class Stone(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.stones
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.stone_img
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y)


class Flag(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.flag_img
        self.rect = game.flag_img.get_rect()
        self.pos = vec(x ,y)
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center


class Traffic_light(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x,y,w,h)
        self.image = pg.Surface((w,h))
        self.image.fill(LIGHTGREY)
        self.pos = vec(x ,y)
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.light_status = None


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x,y,w,h)
        self.x = x
        self.y = y
        self.rect.x = x 
        self.rect.y = y