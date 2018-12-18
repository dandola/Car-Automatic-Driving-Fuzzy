import pygame as pg
from settings import *
from tilemap import collide_hit_rect
import math
from XLTTM import cal_steering, cal_speed
from XLTTM import cal_speed_stone_left, cal_speed_stone_right
from XLTTM import cal_steering_right, cal_steering_left
import numpy as np

vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
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
        self.rect.x = x
        self.rect.y = y
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
        self.closest_stone = None

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
            # print wall["wall"].id, axis_x, axis_y, wall["wall"].width, wall["wall"].height
            if axis_x <= wall["wall"].width/2.0:
                list_expected_walls.append({"wall": wall["wall"], "distance": axis_y - wall["wall"].height/2.0})
            elif axis_y <= wall["wall"].height/2.0:
                list_expected_walls.append({"wall": wall["wall"], "distance": axis_x - wall["wall"].width/2.0})
            else:
                continue
        if len(list_expected_walls) >= 2:
            left = right = None
            list_expected_walls.sort()
            rot0 = (list_expected_walls[0]["wall"].pos - self.pos).angle_to(vec(self.path[self.index] - self.pos))
            rot1 = (list_expected_walls[1]["wall"].pos - self.pos).angle_to(vec(self.path[self.index] - self.pos))
            if rot0%360 > 0 and rot0%360 < 180:
                left = list_expected_walls[0]
            else:
                right = list_expected_walls[0]
            if rot1%360 > 180 and rot1%360 < 360:
                right = list_expected_walls[1]
            else:
                left = list_expected_walls[1]
            return left["distance"], right["distance"]
        else:
            return 0.5, 0.5
    
    def get_distance_traffic(self):
        axis_x = math.fabs(self.pos.x - self.game.traffic_light.x)
        axis_y = math.fabs(self.pos.y - self.game.traffic_light.y)
        if axis_x <= self.game.traffic_light.width/2.0 and axis_y > self.game.traffic_light.height/2.0:
            return axis_y - self.game.traffic_light.height/2.0 - self.rect.w/2.0
        elif axis_y <= self.game.traffic_light.height/2.0 and axis_x > self.game.traffic_light.width/2.0:
             return axis_x - self.game.traffic_light.width/2.0 - self.rect.w/2.0
        elif axis_y <= self.game.traffic_light.height/2.0 and axis_x <= self.game.traffic_light.width/2.0:
            return 0
        else:
            return axis_x - self.game.traffic_light.width/2.0 - self.rect.w/2.0

    def get_min_distance_stone(self, dest):
        distance_two_stones = 200
        angle = (dest - self.pos).angle_to(dest - self.pos)
        list_stones = []
        closest_stone = None
        min = self.distance(dest)
        for stone in self.game.stones:
            rot_stone = (stone.pos - self.pos).angle_to(dest - self.pos)
            distance = self.distance(stone) -  stone.rect.w/2.0 - self.rect.w/2.0
            if distance >= 100:
                continue
            if math.fabs(angle - rot_stone) < 90:
                list_stones.append({"stone": stone, "distance": distance})
                if distance <= min:
                    min = distance
                    closest_stone = stone
        if len(list_stones) >= 2:
            list_stones.sort()
            stone1 = list_stones[0]
            stone2 = list_stones[1]
            rot1 = (stone1["stone"].pos - self.pos).angle_to(dest - self.pos)
            rot2 = (stone2["stone"].pos - self.pos).angle_to(dest - self.pos)
            if rot1*rot2 < 0:
                axis_x = math.fabs(stone1["stone"].pos.x - stone2["stone"].pos.x) - stone1["stone"].rect.w
                axis_y = math.fabs(stone1["stone"].pos.y - stone2["stone"].pos.y) - stone1["stone"].rect.h
                distance_two_stones = max(axis_x, axis_y)
                print axis_x, axis_y

        if min == self.distance(dest):
            min = 200
        return closest_stone, min, distance_two_stones




    def get_deviation(self, deviation1, deviation2):
        deviation = None
        if deviation1 == None:
            if deviation2 == None:
                deviation  = 0.5
            else:
                deviation  = deviation2
        else:
            if deviation2 == None:
                deviation = deviation1
            else:
                if(deviation1 < 0.5 and deviation2 < 0.5):
                    deviation  = min(deviation1, deviation2)
                elif deviation1 > 0.5 and deviation2 > 0.5:
                    deviation  = max(deviation1,deviation2)
                elif deviation2 == 0.5:
                    deviation  = deviation1
                else:
                    deviation  = deviation2
        return deviation

    def get_velocity(self, vel1, vel2):
        vel = None
        if vel1 == None:
            if vel2 == None:
                vel = 1
            else:
                vel = vel2
        else:
            if vel2 == None:
                vel = vel1
            else:
                vel = min(vel1, vel2)
        return vel


    def update(self):
        distance_two_stones = nearest_stone = None
        distance_stone = None
        deviation = vel = None
        deviation2 = deviation1 = None
        vel2 = vel1 = None
        left_right_stone = None
        # print self.rot
        status_light = self.game.traffic_light.light_status
        left_wall, right_wall = self.get_distance_walls()
        sum = left_wall + right_wall
        dev = left_wall*1.0/(right_wall + left_wall)
        distance_traffic_light = self.get_distance_traffic()
        nearest_stone, distance_stone, distance_two_stones = self.get_min_distance_stone(self.path[self.index])
        if distance_two_stones >= 50:
            distance_two_stones = 200

        if nearest_stone:
            self.closest_stone = nearest_stone
            angle_car_stone = (self.closest_stone.pos - self.pos).angle_to(self.path[self.index] - self.pos)
            distance_car_stone = self.distance(self.closest_stone)
            height = round(distance_car_stone*round(math.sin(math.radians(angle_car_stone)),2),2)
            left = WIDTH_PATH/2 - height - self.closest_stone.rect.w/2.0
            right = WIDTH_PATH - left - self.closest_stone.rect.w
            if left > right:
                left_right_stone ="right"
            else:
                left_right_stone ="left"
        deviation1 = cal_steering(dev)
        vel1 = cal_speed(status_light, distance_traffic_light, dev)
        if left_right_stone == "left":
            deviation2 =  cal_steering_left(dev, distance_stone)
            vel2 = cal_speed_stone_left( dev, distance_stone, distance_two_stones/4.0)
        elif left_right_stone == "right":
            deviation2 =  cal_steering_right(dev, distance_stone)
            vel2 = cal_speed_stone_right( dev, distance_stone, distance_two_stones/4.0)
        else:
            deviation2 = None
            vel2 = None

        vel = self.get_velocity(vel1, vel2)
        deviation = self.get_deviation(deviation1, deviation2)
        # --> vel, deviation
        self.player_speed = vel*100
        angle = (math.asin(math.fabs((deviation - 0.5)/0.5)))*180/math.pi
        # print angle
        if deviation > 0.5:
            self.rot = (self.path[self.index] - self.pos).angle_to(vec(1,0)) + angle*(-1)
        else:
            self.rot = (self.path[self.index] - self.pos).angle_to(vec(1,0)) + angle
        if self.player_speed >= 5:
            self.image = pg.transform.rotate(self.game.player_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect.center = self.pos
        distance = self.distance(self.path[self.index])
        self.move(distance)
        if distance <= 30:
            self.index +=1
            if self.index == len(self.path)-1:
                self.rot = (self.path[self.index] - self.pos).angle_to(vec(1,0))
                self.image = pg.transform.rotate(self.game.player_img, self.rot)
                self.rect = self.image.get_rect()
                self.rect.center = self.pos

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
        collide_with_walls(self, self.game.walls,'y')
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

class Stone(pg.sprite.Sprite):
    def __init__(self, game,id, x, y, w, h):
        self.groups = game.all_sprites, game.stones
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.id = id
        self.image = game.stone_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(self.rect.x + self.rect.w/2.0,self.rect.y + self.rect.h/2.0)
        self.x = self.rect.x + self.rect.w/2.0
        self.y = self.rect.y + self.rect.h/2.0
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, id, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.id = id
        self.rect = pg.Rect(x,y,w,h)
        self.x = x + w/2.0
        self.y = y + h/2.0
        self.pos = vec(self.x, self.y)
        self.rect.x = x 
        self.rect.y = y
        self.width = w
        self.height = h


