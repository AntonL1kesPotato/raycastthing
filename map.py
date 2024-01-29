from pygame import draw
import json
import os 
class mapp():
    def __init__(self):
        self.TileNumX = 10
        self.TileNumY = 10
        self.Tiles = None
        self.LoadMap(0)
        self.GridSize = 40

    def Draw(self, win):
        for x in range(self.TileNumX):
            for y in range(self.TileNumY):
                

                if self.Tiles[x][y]: clr = (255,255,255)
                else: clr = (25,25,25)
                draw.rect(win, clr, (y*self.GridSize+1, x*self.GridSize+1, self.GridSize-1, self.GridSize-1))
    
    def MakeMap(self, sizeX, sizeY):
        newmap = []

        for y in range(sizeY):

            newline = []
            for x in range(sizeX):

                if x == 0 or x == sizeX-1 or y == 0 or y == sizeY-1: 
                    newline.append(1)
                else:
                    newline.append(0)


            newmap.append(newline)
        worldNum = len(os.listdir("Maps")) 
        path = "Maps/world" + str(worldNum) + ".json"
        newfile = open(path, "w")
        json.dump(newmap, newfile)
        self.worldNum = worldNum
        return newmap
    
    def LoadMap(self, worldnum):
        path = "Maps/world" + str(worldnum) + ".json"
        map = json.load(open(path, "r"))
        self.Tiles = map
        self.worldNum = worldnum
    
    def SaveMap(self):
        path = "Maps/world" + str(self.worldNum) + ".json"
        json.dump(self.Tiles, open(path, "w"))
        
