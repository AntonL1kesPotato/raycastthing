from math import radians, sin, cos, floor
#from pygame import key, K_j, K_i, K_k, K_l
from map import mapp
import pygame
class Playr():
    def __init__(self):
        self.XPos = 300
        self.YPos = 300
        self.dir = -90
        self.Speed = 8
        self.RotationSpeed = 8
        self.mapy = mapp()

    def ChangeMap(self, newmap):
        self.mapy = newmap
    def MoveX(self, speed):
        
        diff = sin(radians(self.dir)) * speed
        self.XPos += diff

    def MoveY(self, speed):
        
        diff = cos(radians(self.dir)) * speed

        self.YPos += diff

    def GetCollision(self, collider): 
        x = collider[0]
        y = collider[1]   
        return self.mapy.Tiles[floor(y/self.mapy.GridSize)][floor(x/self.mapy.GridSize)]
    
    def GetInput(self, dt):
        keys = pygame.key.get_pressed()
        
        
        if keys[pygame.K_j]: #left
            self.dir -= self.RotationSpeed * dt
            self.dir %= 360

        if keys[pygame.K_l]: #right
            self.dir += self.RotationSpeed * dt
            self.dir %= 360

        if keys[pygame.K_i]: #forward
            self.Speed = 8 * dt

        elif keys[pygame.K_k]:  #backward
            self.Speed = -8 * dt
        else:
            self.Speed *= 0.8 * dt
        
        self.MoveX(self.Speed)
        if self.GetCollision([self.XPos, self.YPos]) != 0: self.MoveX(-self.Speed)
        
        self.MoveY(self.Speed)
        if self.GetCollision([self.XPos, self.YPos]) != 0: self.MoveY(-self.Speed)
        

        
