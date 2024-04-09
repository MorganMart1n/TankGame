import math
import pygame as game
import random

game.init()

# System Variables
mapSizeX = 900
mapSizeY = 600
WINDOW = game.display.set_mode((mapSizeX, mapSizeY))
path = "images\\tank.png"
WHITE = (255, 255, 255)
FULLBLUE = (100, 100, 255)
RED = (255, 0, 0)
game.display.set_caption("Tank Game")

# Tank Initialized Variables
tankSizeX = 200
tankSizeY = 100
tankX = mapSizeX // 2 - tankSizeX // 2
tankY = mapSizeY - tankSizeY
tankVelocity = 10

# Tank Shell Initialized Variables
shellVelocity = 7
shellVelocityX = 0
shellVelocityY = 0
shellArc = math.pi / 4
gravity = 0.02
tankShellX = 0
tankShellY = 0
tankShellSize = 10
shellTime = 0
maxShellTime = 1000

# Load tank image
tank = game.image.load(path).convert_alpha()
tank = game.transform.scale(tank, (tankSizeX, tankSizeY))

# Target Variables
targetX = mapSizeX - 200
targetY = mapSizeY - 100
targetRadius = 30

# Score and Level Variables
score = 0
level = 1
scorePerLevel = 5
font = game.font.SysFont('Arial', 24)


# Set up tank barrel coordinates
barrelX = tankX + tankSizeX / 2 + math.cos(shellArc) * 30
barrelY = tankY + tankSizeY / 2 - math.sin(shellArc) * 30

def move_target():
    global targetX, targetY

    # Adjusted where target can spawn to make sure target can always be reached
    max_target_height = mapSizeY - 175  

    targetX = random.randint(mapSizeX / 6, mapSizeX - targetRadius) 
    targetY = random.randint(max_target_height, mapSizeY - targetRadius)


running = True
while running:
    WINDOW.fill(WHITE)
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False

    # Key Events
    keys = game.key.get_pressed()
    if keys[game.K_RIGHT] and tankX + tankVelocity + tankSizeX <= mapSizeX:  # Check right boundary
        tankX += tankVelocity
    if keys[game.K_LEFT] and tankX - tankVelocity >= 0:  # Check left boundary
        tankX -= tankVelocity
    if keys[game.K_UP] and shellArc < 1.5:
        shellArc += 0.1
    if keys[game.K_DOWN] and shellArc > 0:
        shellArc -= 0.1

     # Calculate barrel endpoint position
    barrelX = tankX + tankSizeX / 2 + math.cos(shellArc) * 30
    barrelY = tankY + tankSizeY / 2 - math.sin(shellArc) * 30 

    # Draw tank and barrel
    WINDOW.fill(WHITE)
    WINDOW.blit(tank, (tankX, tankY))
    game.draw.line(WINDOW, FULLBLUE, (tankX + tankSizeX / 2, tankY + tankSizeY / 2), (barrelX, barrelY), 5)

    # Key Fire Event
    if keys[game.K_SPACE]:
        tankShellX, tankShellY = tankX + tankSizeX /2, tankY + tankSizeY / 2
        shellVelocityX = shellVelocity * math.cos(shellArc) * 2.5
        shellVelocityY = -shellVelocity * math.sin(shellArc)
        shellTime = 0

    if shellTime < maxShellTime:
        shellTime += 1
        tankShellX += shellVelocityX
        tankShellY += shellVelocityY + 0.5 * gravity * shellTime ** 2

        # Draw tank shell
        game.draw.circle(WINDOW, FULLBLUE, (int(tankShellX), int(tankShellY)), tankShellSize)
    else:
        # Reset tank shell position
        tankShellX = 0
        tankShellY = 0

    # Collision Detection
    distance_to_target = math.sqrt((tankShellX - targetX) ** 2 + (tankShellY - targetY) ** 2)
    if distance_to_target <= tankShellSize + targetRadius:
        # Target Hit!
        score += 1
        # Move shell very far off screen, I couldn't figure out how to delete it
        tankShellX = 9999
        tankShellY = 9999
        shellTime = 0
        move_target()        
    # Increase level and decrease target size for every level complete
        if score % scorePerLevel == 0 and targetRadius >= 10:
            level += 1
            targetRadius -= 5 

    # Checks if player has won the game
    if score >= 25:
        #Clears window and displays win message
        WINDOW.fill(WHITE)
        winning_message = font.render("Congratulations! You have completed the game!", True, RED)
        winning_rect = winning_message.get_rect(center=(mapSizeX / 2, mapSizeY / 2))
        WINDOW.blit(winning_message, winning_rect)
        game.display.update()
        game.time.delay(5000) # Delays window closing and allows player to read message
        break

    # Render Target 
    game.draw.circle(WINDOW, RED, (targetX, targetY), targetRadius)

    # Render Score and Level
    score_text = font.render("Score: " + str(score), True, FULLBLUE)
    level_text = font.render("Level: " + str(level), True, FULLBLUE)
    WINDOW.blit(score_text, (10, 10))
    WINDOW.blit(level_text, (10, 40))

    game.display.update()
    game.time.Clock().tick(60)

game.quit()