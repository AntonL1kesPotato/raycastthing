from globalvar import scrW, scrH
import math
from map import mapp
import pygame as py
import numpy as np
from PIL import Image
import os
from ennemy import Sprite
from numba import njit
@njit
def fast():
                y = 0
                for x in range(1000):
                    y += 1
@njit
def resetframe():
    return np.zeros((int(scrW), int(scrH), 3))
@njit
def drawall(realdrawStart, lineH, offset, texture, buff, times, realen, tX, i, RES, step, tileID):
        if realdrawStart < 0: 
            drawY = -1
        else:
            drawY = realdrawStart + offset
        for y in range(times):
                drawX = i * RES
                drawY += 1
                dX = int(min(max(0, drawX), scrW-1))
                dY = int(min(max(0, drawY), scrH-1))
                if realdrawStart < 0: 
                    tY = int((y -realdrawStart ) * step) % realen
                else:
                     tY = int((y) * step) % realen
                for x in range(RES):
                    buff[dX+x][dY] = texture[tileID][tY][tX]/255
                
                if drawY >= realdrawStart + lineH + offset:
                    return buff
        return buff


@njit
def FloorCast(buffer, texture, pdir, px, py, dv, RES):
    
        
    halfvres = int(scrH/2)
    for i in range(int(scrW/RES)):

        scrX = i*RES - scrW/2 
        angle = math.degrees(math.atan(scrX / dv))
        Dir = pdir + angle

        sin, cos, cos2 = math.sin(math.radians(Dir)), math.cos(math.radians(Dir)), math.cos(math.radians(Dir) - math.radians(pdir))
        for j in range(halfvres):

            dist = halfvres / (halfvres - j)/cos2
            x = (px + (sin * dist)) 
            y = (py + (cos * dist)) 
            xx, yy = int((x - int(x))*10) , int((y - int(y))*10)
            buffer[i*RES][halfvres*2-j-1] = texture[0][xx][yy]/255
       
class Renderer():

    def __init__(self, win):
        self.Player = None
        self.Map = mapp()
        self.win = win
        self.zoom = 1
        self.RES = 2
        self.textures = []
        #self.img = py.transform.scale_by(py.image.load("brik.png").convert_alpha(), 0.25)
        self.screenbuffer = []
        self.ybuffer = []
        self.clock = py.time.Clock()
        self.divider = 30
        self.FOV = math.radians(90)
        self.SIZE = 40
        self.enemy = Sprite(win)
        self.dv = scrW/2 / math.tan(self.FOV/2)
        self.rays = []
        self.debugDraw = []
        self.doorhit = 0
        self.initbuff = np.zeros((int(scrW), int(scrH), 3))
        
        self.LoadImages()
        
    def LoadImages(self):
        for img in os.listdir("Texture"):
             self.textures.append(np.asarray(Image.open("Texture/" + str(img))))

    def spritestuff(self, camdir):
        sprX = 2
        sprY = 4
       
        distX = sprX - self.Player.XPos/self.SIZE
        distY = sprY - self.Player.YPos/self.SIZE

        vx = (distX*math.cos(camdir)) - (distY*math.sin(camdir)) 
        vy = ((distX*math.sin(camdir)) + (distY*math.cos(camdir)))
        height = (self.dv / vy)/100
        #height = self.dv / dist
        imgsize = self.img.get_width()
        if height > 10: height = 10
        if not(height < 0):

            newimg = py.transform.scale(self.img, (imgsize*height, imgsize*height))
            center = newimg.get_width()/4
            posX = vx * (self.dv / vy) + scrW/2 - center
            self.win.blit(newimg, (posX, scrH/2 - center))

    def FOVUpdate(self, newFOV):
        self.FOV = newFOV
        self.dv = scrW/2 / math.tan(self.FOV/2)

             
    def RayCast(self, dir, origin, tick):
            
            Distance = 0
            alreadyChecked = False
            vertHit = None
            step = py.Vector2()
            nextTile = py.Vector2()
            RayDir = py.Vector2(math.sin(dir)+ 0.00000001 , math.cos(dir)+ 0.00000001)
            rayStepSize = py.Vector2(math.sqrt(1 + (RayDir.y/RayDir.x)**2), math.sqrt(1 + (RayDir.x/RayDir.y)**2)) 
            tileCheck = py.Vector2(int(origin.x), int(origin.y))
            
            if RayDir.x > 0:
                nextTile.x = (float(tileCheck.x + 1) - origin.x) * rayStepSize.x
                step.x = 1
            else:
                nextTile.x = (origin.x - float(tileCheck.x)) * rayStepSize.x
                step.x = -1

            if RayDir.y > 0:
                nextTile.y = (float(tileCheck.y + 1) - origin.y) * rayStepSize.y
                step.y = 1
            else:
                nextTile.y = (origin.y - float(tileCheck.y)) * rayStepSize.y
                step.y = -1
            
            
            while  self.Map.Tiles[int(tileCheck.y)][int(tileCheck.x)] == 0:

                if nextTile.y > nextTile.x:
                    tileCheck.x += step.x
                    Distance = nextTile.x
                    nextTile.x += rayStepSize.x
                    vertHit = False

                else:
                    tileCheck.y += step.y
                    Distance = nextTile.y
                    nextTile.y += rayStepSize.y
                    vertHit = True

                if self.Map.Tiles[int(tileCheck.y)][int(tileCheck.x)] == 200 and not(alreadyChecked):

                        if vertHit: 
                            Distance += rayStepSize.y/2
                        else:
                            Distance += rayStepSize.x/2
                        self.doorhit = vertHit
                        currTileX = origin.x + Distance * math.sin(dir)
                        currTileY = origin.y + Distance * math.cos(dir)
                        currTileX = min(max(0, currTileX), 10)
                        currTileY = min(max(0, currTileY), 10)
                        
                        
                        
                        if int(currTileX) == tileCheck.x and int(currTileY) == tileCheck.y:
                            return Distance, vertHit, self.Map.Tiles[int(tileCheck.y)][int(tileCheck.x)]
                        else:
                            alreadyChecked = True
                    
                    

            return Distance, vertHit, self.Map.Tiles[int(tileCheck.y)][int(tileCheck.x)]

    def debugRendr(self):
        
        for f in self.debugDraw:
                py.draw.line(self.win, (100,0,0), (f[0]*10, f[1]*10), (f[2]*10, f[3]*10))
        self.debugDraw = []

    


    def Render(self, tick):
        
        self.buffer = self.initbuff
        FloorCast(self.buffer, self.textures, self.Player.dir, (self.Player.XPos/self.SIZE), (self.Player.YPos/self.SIZE), self.dv, self.RES)
        PlayerPos = py.Vector2(self.Player.XPos/self.SIZE, self.Player.YPos/self.SIZE)
        self.rays = [PlayerPos.x, PlayerPos.y]
        self.yoffset = 0
        self.initbuff = resetframe()
        for i in range(math.ceil(scrW/self.RES)):
            scrX = i*self.RES - scrW/2
            Dir = self.Player.dir + math.degrees(math.atan(scrX / self.dv))
            RayDist, verticalHit, tileID = self.RayCast(math.radians(Dir), PlayerPos, i)

            if i == 0:
                 mindir = Dir
            if i == math.ceil(scrW/self.RES)-1:
                 maxdir = Dir
            
            heightMult = 1
            CameraDist = RayDist * math.cos(math.radians(Dir) - math.radians(self.Player.dir)) + 0.00000001
            LineHeight = (self.dv/CameraDist)
            intersect = py.Vector2(PlayerPos.x + RayDist * math.sin(math.radians(Dir)), PlayerPos.y + RayDist * math.cos(math.radians(Dir)))
            realen = len(self.textures[tileID])

            step = realen/LineHeight
            self.rays.append(intersect)
            
            drawStart = -LineHeight / 2 + scrH / 2 - ((realen*heightMult-realen)/step)

            brightness =  (RayDist**self.RES/500)
            if brightness < 25: brightness = 25
            if brightness > 255: brightness = 255
            
            if not verticalHit: 
                x = int((intersect.y - int(intersect.y))*realen)
            else:
                x = int((intersect.x - int(intersect.x))*realen)
                
            self.buffer = drawall(drawStart, LineHeight, self.yoffset, self.textures, self.buffer, scrH, realen, x, i, self.RES, step, tileID)
            
        return self.buffer
    
        #self.enemy.draw(PlayerPos.x, PlayerPos.y, math.radians(self.Player.dir), (i / (scrW / self.FOV / self.RES)))
        
    