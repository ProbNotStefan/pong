import pygame
from pygame.locals import *
from ponggameassets import *
def pong0p():

    pygame.init()
    pygame.mixer.init()


    # display setup
    screen_x,screen_y = 720,450
    screen = pygame.display.set_mode((screen_x,screen_y))
    pygame.display.set_caption("Pong!")

    # game loop
    paddle1 = botpaddle(50,screen_x,screen_y)
    paddle2 = botpaddle(screen_x-50,screen_x,screen_y)
    ball1 = ball(screen_x,screen_y)
    running = True
    clock = pygame.time.Clock()
    wintext1 = wintext()
    score = scorevalue()
    scoretext1 = scoretext(score)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        paddle1.handleai(ball1)
        paddle2.handleai(ball1)
        ball1.handleevents([paddle1,paddle2],wintext1,screen,score)
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), paddle1.sprite)
        pygame.draw.rect(screen, (255, 255, 255), paddle2.sprite)
        pygame.draw.ellipse(screen,ball1.color,ball1.sprite)
        wintext1.display(screen,screen_x,screen_y,wintext1.text_value,(255,255,255))
        scoretext1.display(screen,screen_x,score)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()