import pygame as pg
import math
from globalvar import scrH, scrW
class Sprite():
    def __init__(self, window):
        self.x = 0
        self.y = 0
        #self.image = pg.image.load("cat.jpg").convert()
        self.win = window
        self.scrH = window.get_height()
        self.scrW = window.get_width()

    def draw(self, playerX, playerY, dir, angleGap):
        dx, dy = self.x - playerX, self.y - playerY
        Distance = math.sqrt(dx**2 + dy**2)
        newimg = pg.transform.scale(self.image, (self.image.get_height()/Distance, self.image.get_height()/Distance))

        
        theta = math.atan2(dy, dx)
        
        gamma = theta - dir #player angle est en radians

        #if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
        #    gamma += DOUBLE_PI
        

        #spritePosX = current_ray * (self.scrW // 90) - half_projected_height ##SCALE = resX // NUM_RAYS
        #self.win.blit(newimg, (spritePosX, 200))