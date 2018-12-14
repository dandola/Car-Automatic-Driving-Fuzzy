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
        self.angle = 0
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

    def get_distance_walls(self):
        list_expected_walls = []
        list_walls = []
        for wall in self.game.walls:
            axis_x = math.fabs(wall.x - self.pos.x)
            axis_y = math.fabs(wall.y - self.pos.y)
            distance = math.sqrt(axis_x**2 + axis_y**2)
            list_walls.append({"wall": wall, "distance": distance})
        list_walls.sort()
        walls = list_walls[:4]
        for wall in walls:
            axis_x = math.fabs(wall["wall"].x - self.pos.x)
            axis_y = math.fabs(wall["wall"].y - self.pos.y)
            if axis_x <= wall["wall"].width/2.0:
                list_expected_walls.append({"wall": wall["wall"], "distance": axis_y - wall["wall"].height/2.0})
            elif axis_y <= wall["wall"].height/2.0:
                list_expected_walls.append({"wall": wall["wall"], "distance": axis_x - wall["wall"].width/2.0})
            else:
                continue
        if len(list_expected_walls) >= 2:
            list_expected_walls.sort()
            return list_expected_walls[0]["distance"], list_expected_walls[1]["distance"]
        else:
            return 0.5, 0.5
    
    def get_distance_traffic(self):
        axis_x = math.fabs(self.pos.x - self.game.traffic_light.x)
        axis_y = math.fabs(self.pos.y - self.game.traffic_light.y)
        if axis_x <= self.game.traffic_light.width/2.0 and axis_y > self.game.traffic_light.height/2.0:
            return axis_y - self.game.traffic_light.height/2.0
        elif axis_y <= self.game.traffic_light.height/2.0 and axis_x > self.game.traffic_light.width/2.0:
             return axis_x - self.game.traffic_light.width/2.0
        elif axis_y <= self.game.traffic_light.height/2.0 and axis_x <= self.game.traffic_light.width/2.0:
            return 0
        else:
            return math.sqrt((self.pos.x - self.game.traffic_light.x)**2 + (self.game.traffic_light.y - self.pos.y)**2)

    def update(self):
        #status traffic light
        status_light = self.game.traffic_light.light_status
        #distance between walls and car
        wall1, wall2 = self.get_distance_walls()
        #distance between traffic light and car
        distance_traffic_light = self.get_distance_traffic()
        sum = wall1 + wall2
        # print "distance between two wall: ", round(wall1*1.0/sum,3), round(wall2*1.0/sum,3)
        self.rot = (self.path[self.index] - self.pos).angle_to(vec(1,0))%360
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
    # def change_speed_traffic(self):
        


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


class Stone(pg.sprite.Sprite):
    def __init__(self, game,id, x, y, w, h):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.id = id
        self.image = game.stone_img
        self.rect = game.flag_img.get_rect()
        self.pos = vec(x ,y)
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = pg.Rect(x,y,w,h)
        self.hit_rect.center = self.rect.center


class Traffic_light(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.width = w 
        self.height = h 
        self.rect = pg.Rect(x,y,w,h)
        self.image = pg.Surface((w,h))
        self.image.fill(LIGHTGREY)
        self.pos = vec(x + w/2.0,y + h/2.0)
        self.rect.x = x
        self.rect.y = y 
        self.x = x + w/2.0
        self.y = y + h/2.0
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.light_status = None

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, id, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.id = id
        self.rect = pg.Rect(x,y,w,h)
        self.x = x + w/2.0
        self.y = y + h/2.0
        self.rect.x = x 
        self.rect.y = y
        self.width = w
        self.height = h


