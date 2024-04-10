import math
import pygame as game
import random

def initialize_game():
    # Initialize the game window
    game.init()
    mapSizeX = 900
    mapSizeY = 600
    WINDOW = game.display.set_mode((mapSizeX, mapSizeY))
    game.display.set_caption("Tank Game")
    return WINDOW, mapSizeX, mapSizeY

def load_tank_image(path, tankSizeX, tankSizeY):
    # Load and resize the tank image
    tank = game.image.load(path).convert_alpha()
    tank = game.transform.scale(tank, (tankSizeX, tankSizeY))
    return tank

def handle_key_events(keys, tankX, tankY, tankVelocity, tankSizeX, mapSizeX, shellArc):
    # Handle key events for tank movement and shell arc adjustment
    if keys[game.K_RIGHT] and tankX + tankVelocity + tankSizeX <= mapSizeX:
        tankX += tankVelocity
    if keys[game.K_LEFT] and tankX - tankVelocity >= 0:
        tankX -= tankVelocity
    if keys[game.K_UP] and shellArc < 1.5:
        shellArc += 0.1
    if keys[game.K_DOWN] and shellArc > 0:
        shellArc -= 0.1
    return tankX, tankY, shellArc

def calculate_barrel_position(tankX, tankSizeX, tankY, tankSizeY, shellArc):
    # Calculate the position of the barrel based on tank position and shell arc
    barrelX = tankX + tankSizeX / 2 + math.cos(shellArc) * 30
    barrelY = tankY + tankSizeY / 2 - math.sin(shellArc) * 30
    return barrelX, barrelY

def handle_fire_event(keys, tankX, tankY, tankSizeX, tankSizeY, shellArc, shellVelocity, shellVelocityX, shellVelocityY, shellTime, tankShellX, tankShellY, gravity):
    # Handle the fire event when spacebar is pressed
    if keys[game.K_SPACE]:
        tankShellX = tankX + tankSizeX / 2
        tankShellY = tankY + tankSizeY / 2
        shellVelocityX = shellVelocity * math.cos(shellArc) * 2.5
        shellVelocityY = -shellVelocity * math.sin(shellArc)
        shellTime = 0
    return tankShellX, tankShellY, shellVelocityX, shellVelocityY, shellTime

def handle_shell_movement(shellTime, maxShellTime, tankShellX, tankShellY, shellVelocityX, shellVelocityY, gravity):
    # Handle the movement of the shell
    if shellTime < maxShellTime:
        shellTime += 1
        tankShellX += shellVelocityX
        tankShellY += shellVelocityY + 0.5 * gravity * shellTime ** 2
    else:
        tankShellX = 0
        tankShellY = 0
    return shellTime, tankShellX, tankShellY

def handle_collision_detection(tankShellX, tankShellY, targetX, targetY, tankShellSize, targetRadius, score, level, scorePerLevel, mapSizeX, mapSizeY):
    # Handle collision detection between the shell and the target
    distance_to_target = math.sqrt((tankShellX - targetX) ** 2 + (tankShellY - targetY) ** 2)
    if distance_to_target <= tankShellSize + targetRadius:
        score += 1
        tankShellX = 9999
        tankShellY = 9999
        shellTime = 0
        targetX, targetY = move_target(mapSizeX, mapSizeY, targetRadius, targetX, targetY)
        if score % scorePerLevel == 0 and targetRadius >= 10:
            level += 1
            targetRadius -= 5 
    return tankShellX, tankShellY, score, level, targetRadius, targetX, targetY

def check_game_over(score, WINDOW, mapSizeX, mapSizeY, WHITE, RED, font):
    # Check if the game is over (score reaches a certain threshold)
    if score >= 25:
        WINDOW.fill(WHITE)
        winning_message = font.render("Congratulations! You have completed the game!", True, RED)
        winning_rect = winning_message.get_rect(center=(mapSizeX / 2, mapSizeY / 2))
        WINDOW.blit(winning_message, winning_rect)
        game.display.update()
        game.time.delay(5000)
        return True
    return False

def render_game(WINDOW, WHITE, tank, tankX, tankY, tankSizeX, tankSizeY, barrelX, barrelY, FULLBLUE, tankShellX, tankShellY, tankShellSize, targetX, targetY, targetRadius, RED, score, level, font):
    # Render the game window with all the game elements
    WINDOW.fill(WHITE)
    WINDOW.blit(tank, (tankX, tankY))
    game.draw.line(WINDOW, FULLBLUE, (tankX + tankSizeX / 2, tankY + tankSizeY / 2), (barrelX, barrelY), 5)
    game.draw.circle(WINDOW, FULLBLUE, (int(tankShellX), int(tankShellY)), tankShellSize)
    game.draw.circle(WINDOW, RED, (targetX, targetY), targetRadius)
    score_text = font.render("Score: " + str(score), True, FULLBLUE)
    level_text = font.render("Level: " + str(level), True, FULLBLUE)
    WINDOW.blit(score_text, (10, 10))
    WINDOW.blit(level_text, (10, 40))
    game.display.update()
    game.time.Clock().tick(60)

def move_target(mapSizeX, mapSizeY, targetRadius, targetX, targetY):
    # Move the target to a random position within the game window
    max_target_height = mapSizeY - 175  

    targetX = random.randint(mapSizeX / 6, mapSizeX - targetRadius) 
    targetY = random.randint(max_target_height, mapSizeY - targetRadius)

    return targetX, targetY

def main():
    # Main game loop
    WINDOW, mapSizeX, mapSizeY = initialize_game()
    path = "images\\tank.png"
    WHITE = (255, 255, 255)
    FULLBLUE = (100, 100, 255)
    RED = (255, 0, 0)
    tankSizeX = 200
    tankSizeY = 100
    tankX = mapSizeX // 2 - tankSizeX // 2
    tankY = mapSizeY - tankSizeY
    tankVelocity = 10
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
    targetX = mapSizeX - 200
    targetY = mapSizeY - 100
    targetRadius = 30
    score = 0
    level = 1
    scorePerLevel = 5
    font = game.font.SysFont('Arial', 24)
    tank = load_tank_image(path, tankSizeX, tankSizeY)
    running = True
    while running:
        WINDOW.fill(WHITE)
        for event in game.event.get():
            if event.type == game.QUIT:
                running = False
        keys = game.key.get_pressed()
        tankX, tankY, shellArc = handle_key_events(keys, tankX, tankY, tankVelocity, tankSizeX, mapSizeX, shellArc)
        barrelX, barrelY = calculate_barrel_position(tankX, tankSizeX, tankY, tankSizeY, shellArc)
        tankShellX, tankShellY, shellVelocityX, shellVelocityY, shellTime = handle_fire_event(keys, tankX, tankY, tankSizeX, tankSizeY, shellArc, shellVelocity, shellVelocityX, shellVelocityY, shellTime, tankShellX, tankShellY, gravity)
        shellTime, tankShellX, tankShellY = handle_shell_movement(shellTime, maxShellTime, tankShellX, tankShellY, shellVelocityX, shellVelocityY, gravity)
        tankShellX, tankShellY, score, level, targetRadius, targetX, targetY = handle_collision_detection(tankShellX, tankShellY, targetX, targetY, tankShellSize, targetRadius, score, level, scorePerLevel, mapSizeX, mapSizeY)
        if check_game_over(score, WINDOW, mapSizeX, mapSizeY, WHITE, RED, font):
            break
        render_game(WINDOW, WHITE, tank, tankX, tankY, tankSizeX, tankSizeY, barrelX, barrelY, FULLBLUE, tankShellX, tankShellY, tankShellSize, targetX, targetY, targetRadius, RED, score, level, font)
    game.quit()

if __name__ == "__main__":
    main()