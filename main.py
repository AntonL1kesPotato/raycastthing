import pygame
import math
from map import mapp
import numpy as np
from player import Playr
from globalvar import scrH, scrW
from editor import Edit

pygame.init()
screen_size = (scrW, scrH)
 
#win = pygame.display.set_mode(screen_size)
win = pygame.display.set_mode((scrW,scrH))
pygame.display.set_caption("Raytracing")

clock = pygame.time.Clock()
clr = 0
TileNumX = 10
TileNumY = 10
tick =0
Map = mapp()
Player = Playr()
font = pygame.font.SysFont("Arial" , 18 , bold = True)
running = True
Editor = Edit(win)
from ray import Renderer
Render = Renderer(win)
EDITMODE = True
Fullscreen = True
var = 0
    
def fps_counter():
        fps = str(int(clock.get_fps()))
        fps_t = font.render(fps , 1, pygame.Color("RED"))
        win.blit(fps_t,(0,0))

while running:
    keys = pygame.key.get_pressed()
    deltaTime = clock.tick(int(clock.get_fps()))/1000


    Player.GetInput(1)
    Render.Player = Player
    if keys[pygame.K_SPACE]:
         Render.FOV = math.radians(60)
    else:
         Render.FOV = math.radians(90)
    back = Render.Render(1)
    #(back)
    
    surf = pygame.surfarray.make_surface(back*255) 
    win.blit(surf, (0,0))
    
    if EDITMODE:
          Editor.rays = Render.rays 
          if Fullscreen:
             Editor.DrawFullScreen(var)
          else: 
             Editor.Draw()
          Editor.map = Map
          Render.Map = Map
          Player.ChangeMap(Map)
          Render.debugRendr()


          if keys[pygame.K_0]:
            print("1: Save current map")
            print("2: Load map")
            print("3: Make new map")

          if keys[pygame.K_1]:
             Map.SaveMap()

          if keys[pygame.K_2]:
             loadedmap = input("which map")
             Map.LoadMap(int(loadedmap))

          if keys[pygame.K_3]:
             size = input("what size")
             Map.MakeMap(int(size), int(size))
          
          if keys[pygame.K_UP]:
              Editor.Zoom(1.5)
          elif keys[pygame.K_DOWN]:
              Editor.Zoom(0.7)

             

    fps_counter()
    pygame.display.update()
    
    
    clock.tick(60)
    tick += 1
    var = 0
    for event in pygame.event.get():
          if event.type == pygame.QUIT:
               running = False
          if event.type == pygame.MOUSEBUTTONDOWN:
               if event.button == 4:
                    var = 1
               elif event.button == 5:
                    var = -1

 
pygame.quit()


'''
-sprites (ennemis, objets)
-éditeur de niveaux
-optimization
-plafond et sol textured
-correction de bugs (fisheye par exemple)
-réecrire un peu le code (longeur des murs,  résolution)

facultatifs: (
-armes simples
-portes
)

'''