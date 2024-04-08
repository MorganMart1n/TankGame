import math
import pygame as game

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

# Score Variables
score = 0
font = game.font.SysFont('Arial', 24)

# Set up tank barrel coordinates
barrelX = tankX + tankSizeX / 2 + math.cos(shellArc) * 30
barrelY = tankY + tankSizeY / 2 - math.sin(shellArc) * 30


running = True
while running:
    WINDOW.fill(WHITE)
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False

    # Key Events
    keys = game.key.get_pressed()
    if keys[game.K_RIGHT]:
        tankX += tankVelocity
    if keys[game.K_LEFT]:
        tankX -= tankVelocity
    if keys[game.K_UP]:
        shellArc += 0.1
    if keys[game.K_DOWN]:
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

    # Render Target 
    game.draw.circle(WINDOW, RED, (targetX, targetY), targetRadius)

    # Render Score
    score_text = font.render("Score: " + str(score), True, FULLBLUE)
    WINDOW.blit(score_text, (10, 10))  # Draw score in top-left

    game.display.update()
    game.time.Clock().tick(60)

game.quit()