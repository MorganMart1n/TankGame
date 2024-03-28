import math
import pygame as game
import random as rand
import numpy as np
game.init()

#System Variables
mapSizeX = 900
mapSizeY = 600
WINDOW = game.display.set_mode((mapSizeX, mapSizeY))
path = "C:\\Users\\Morgan\\OneDrive - Robert Gordon University\\Documents\\University\\Computing Math\\TankGame\\images\\tank.png"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FULLBLUE = (100, 100, 255)
game.display.set_caption("Tank Game")
#Tank Shell Initalised Variables
shellW = 5
shellH = 10
shellVelocity = 7
isFired = "READY!"
tankShellX = 0
tankShellY = 0
tankShellSize = 10
Shells = []

#Tank Initalised Variables
tankSizeX = 200
tankSizeY = 100
tankX = mapSizeX // 2 - tankSizeX // 2
tankY = mapSizeY - tankSizeY
tankVelocity = 10
lineX = tankX + tankSizeX - shellW -25
lineY = tankY + 52

# def maxLine():

#Sets the tank image to a maluable player object
def initalise_tank():
    global tank
    tank = game.image.load(path).convert_alpha()
    tank = game.transform.scale(tank, (tankSizeX, tankSizeY))
    WINDOW.blit(tank, (tankX, tankY))
    return tank
#Initalises the tank shell
def tankShell(X, Y):
    game.draw.circle(WINDOW, FULLBLUE, (X, Y), tankShellSize, 3)

running = True
while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False

#Key Events
    if event.type == game.KEYDOWN:
        if event.key == game.K_RIGHT:     
          tankX += tankVelocity 
          right = True

    if event.type == game.KEYDOWN:      
        if event.key == game.K_LEFT:     
           tankX -= tankVelocity
           left = True
#Key Fire Event
    if event.type == game.KEYDOWN:
            if event.key == game.K_BACKSPACE:
                if isFired == "READY!":
                    print("Tank is loaded")
                    isFired = "FIRE!"
                    print("Tank Fired")
                    #Sets the shell x,y to approprite position of tank barrel
                    tankShellX = cursor[0]
                    tankShellY = cursor[1]
    #Fires shell in constant x Velocity
    if isFired == "FIRE!":
        tankShellX += shellVelocity 
        #Checks if out of bounds to reset the Shell State and Pos
        if tankShellX >= mapSizeX:
            isFired = "READY!"  
    cursor = game.mouse.get_pos()

#Trying to to add a maximum for the line length for arrow aiming    
    # if cursor[0] >= 600 or cursor[0] <= 460 :
    #     cursorX = game.mouse.set_cursor([520,cursor[1]])
    #     cursorY = game.mouse.set_cursor([cursor[0],520])
        
    # print(lineX)
    WINDOW.fill(WHITE)
    #Calls the Initalised tank
    initalise_tank()
    #Calles the initalised tankShell
    if isFired == "FIRE!":
        tankShell(tankShellX, tankShellY)
    game.draw.line(WINDOW, FULLBLUE,(lineX, lineY),cursor,5)
    game.display.update()
    game.time.Clock().tick(60)

game.quit()
