import pygame
from pong0p import pong0p
from pong1p import pong1p
from pong2p import pong2p

pygame.init()

screen_x,screen_y = 720,450
screen = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption("Pong!")

white = (255,255,255)
red = (255,55,55)

font = pygame.font.Font(None, 36)

button_width = 200
button_height = 50
button_padding = 20

button1 = pygame.Rect((screen_x - button_width) // 2, 100, button_width, button_height)
button2 = pygame.Rect((screen_x - button_width) // 2, 200, button_width, button_height)
button3 = pygame.Rect((screen_x - button_width) // 2, 300, button_width, button_height)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button1.collidepoint(mouse_pos):
                pygame.quit()
                pong0p()
            elif button2.collidepoint(mouse_pos):
                pygame.quit()
                pong1p()
            elif button3.collidepoint(mouse_pos):
                pygame.quit()
                pong2p()

    screen.fill((0,0,0))
    pygame.draw.rect(screen, red, button1)
    pygame.draw.rect(screen, red, button2)
    pygame.draw.rect(screen, red, button3)

    text1 = font.render("0 Player", True, white)
    text2 = font.render("1 Player", True, white)
    text3 = font.render("2 Player", True, white)

    screen.blit(text1, (button1.x + button_width // 2 - text1.get_width() // 2, button1.y + button_height // 2 - text1.get_height() // 2))
    screen.blit(text2, (button2.x + button_width // 2 - text2.get_width() // 2, button2.y + button_height // 2 - text2.get_height() // 2))
    screen.blit(text3, (button3.x + button_width // 2 - text3.get_width() // 2, button3.y + button_height // 2 - text3.get_height() // 2))

    pygame.display.flip()

pygame.quit()