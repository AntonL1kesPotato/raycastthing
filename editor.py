import pygame
from map import mapp
from globalvar import scrH,scrW
import os
class Edit():
    def __init__(self, win) -> None:
        self.map = mapp()
        self.win = win
        self.tileSize = 10
        self.rays  = []
        self.colors = {
            0: [255,255,255],
            1: [0,255,0],
            2: [255,0,0],
            3: [255,255,0]
        }
        self.chosentext = 1
        self.font = pygame.font.SysFont("Calibri" , 18 , bold = True)
        self.textures = self.LoadImages()

    def LoadImages(self):
        ret = []
        for img in os.listdir("Texture"):
            ret.append(pygame.transform.scale(pygame.image.load("Texture/" + str(img)).convert(), (self.tileSize, self.tileSize))   )
        return ret

    def Zoom(self, mult):
        self.tileSize *= mult
        self.textures = self.LoadImages()

    def DrawFullScreen(self, scrwheel):
        self.chosentext += scrwheel
        self.chosentext = max(0, self.chosentext)

        for y in range(int(scrH / self.tileSize)-1):

            for x in range(int(scrW/ self.tileSize)-1):


                if x >= len(self.map.Tiles) or  y >= len(self.map.Tiles): break
                mouse = pygame.mouse.get_pos()
                mouseDown = pygame.mouse.get_pressed()

                if int(mouse[0]/self.tileSize) == x and int(mouse[1]/self.tileSize) == y:
                    color = (100,100,100)
                    if mouseDown[0]:
                        self.map.Tiles[y][x] = 0
                    elif mouseDown[2]:
                        self.map.Tiles[y][x] = self.chosentext

                #pygame.draw.rect(self.win, color, (x * self.tileSize+1, y * self.tileSize-1, self.tileSize, self.tileSize))
                
                if self.map.Tiles[y][x] != 0 :
                    self.win.blit(self.textures[self.map.Tiles[y][x]], (x * self.tileSize, y * self.tileSize, self.tileSize, self.tileSize))
                else:
                    pygame.draw.rect(self.win, (0,0,0), (x * self.tileSize, y * self.tileSize, self.tileSize, self.tileSize))
        
        
        txt = str(self.chosentext)
        txt = self.font.render(txt , 1, pygame.Color("WHITE"))
        self.win.blit(txt, (int(scrW/1.2), int(scrH/8)))
        
    def Draw(self):
        mouse = pygame.mouse.get_pos()
        mouseDown = pygame.mouse.get_pressed()

        for x in range(self.map.TileNumX):

            for y in range(self.map.TileNumY):

                if int(mouse[0]/self.tileSize) == x and int(mouse[1]/self.tileSize) == y:
                    color = (100,100,100)
                    if mouseDown[0]:
                        self.map.Tiles[y][x] = 0
                    elif mouseDown[2]:
                        self.map.Tiles[y][x] = 1
                else:
                    color = self.colors[self.map.Tiles[y][x]]

                pygame.draw.rect(self.win, color, (x * self.tileSize+1, y * self.tileSize-1, self.tileSize, self.tileSize))
        
        #for i in range(len(self.rays)-2):
        #    pygame.draw.line(self.win, (255,0,0), (self.rays[0] * self.tileSize, self.rays[1] * self.tileSize) , (self.rays[i+2][0] * self.tileSize, self.rays[i+2][1] * self.tileSize))
        
        return self.map
        