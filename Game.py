import pygame as game


game.init()
WINDOW = game.display.set_mode((500,500))
FULLBLUE =(100,100,255)
FULLWHITE=(255,255,255)
x =100
y = x

veloctiy = 5
running = True
while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False

    keys = game.key.get_pressed()

    if event.type == game.KEYDOWN:
        if event.key == game.K_RIGHT:     
          x += veloctiy
        elif event.key == game.K_LEFT:     
           x -= veloctiy
        elif event.key == game.K_UP:     
            y -= veloctiy
        elif event.key == game.K_DOWN:    
            y += veloctiy




    game.display.set_caption('Tank Game')
    WINDOW.fill(FULLWHITE)
    game.draw.circle(WINDOW, FULLBLUE,(x,y),20,0)
    game.draw.circle(WINDOW, FULLBLUE,(300,250),20,0)
    game.draw.line(WINDOW, FULLBLUE,(100, 300), (375, 300), 10)
    game.display.update()
    game.time.Clock().tick(60)


