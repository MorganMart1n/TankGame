import math
import pygame as game
import random as rand

game.init()
tank = None
path = "C:\\Users\\Morgan\\OneDrive - Robert Gordon University\\Documents\\University\\Computing Math\\TankGame\\images\\tank.png"

mapSizeX = 900
mapSizeY = 500
WINDOW = game.display.set_mode((mapSizeX,mapSizeY))
FULLBLUE =(100,100,255)
FULLWHITE=(255,255,255)
scale = 20
tankX = 250
tankY = tankX
updatedtankX = tankX
updatedtankY = tankY
bound = 10
left = False
right = True
bullets=[]
randX = rand.random()* mapSizeX + 1
randY = rand.random()* mapSizeY + 1
veloctiy = 5
tankSizeX = 200
tankSizeY = 100
cursor = None
upTraj = -0.1
downTraj = 0.1
endPoint = 0.0
def collision():
    if tankX >= randX - bound and tankX <= randX + bound and tankY >= randY - bound and tankY <= randY + bound:
      game.quit()
def draw_tank():
    global tank
    tank = game.image.load(path).convert_alpha()
    tank = game.transform.scale(tank,(tankSizeX,tankSizeY))
    WINDOW.blit(tank,(tankX, tankY))
    return tank



running = True
while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
            
    collision()
    cursor = game.mouse.get_pos()
       
    # print(cursor)
    keys = game.key.get_pressed()

    if event.type == game.KEYDOWN:
        if event.key == game.K_RIGHT:     
          tankX += veloctiy
          updatedtankX += veloctiy
          right = True
        #   print(updatedtankX)
    if event.type == game.KEYDOWN:      
        if event.key == game.K_LEFT:     
           tankX -= veloctiy
           updatedtankX -= veloctiy
           left = True
        #    print(updatedtankX)
    if event.type == game.KEYDOWN:  
     if event.type == game.MOUSEBUTTONDOWN:
        print("clicked")
        game.draw.circle(WINDOW, FULLBLUE,(cursor[0],cursor[1]),scale,0)
    
    if event.type == game.KEYDOWN:  
     if event.key == game.K_UP:
            upTraj += 0.1
    if event.type == game.KEYDOWN:  
     if event.key == game.K_DOWN:
            downTraj -= 20

    
    arcX = tankX + 25
    
    arcY = tankY + 50

    center = tankX+ 50
    game.display.set_caption('Tank Game')
    WINDOW.fill(FULLWHITE)
    draw_tank()
    game.draw.arc(WINDOW, FULLBLUE, (arcX,arcY,tankX, tankY * upTraj + downTraj), 0, math.pi /2, 1)
    game.draw.circle(WINDOW, FULLBLUE,(randX,randY),scale,0)
    game.display.update()
    game.time.Clock().tick(60)