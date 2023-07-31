import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("A pygame lol")
pygame_icon = pygame.image.load('resources/logo.png')
pygame.display.set_icon(pygame_icon)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
font_iq = pygame.font.Font(None, 50)
font_big = pygame.font.Font(None, 100)

surface_sky = pygame.image.load("resources/elements/sky.png")
surface_gameover = pygame.image.load("resources/elements/gameover.png")
surface_ground = pygame.image.load("resources/elements/ground.png")
surface_phil = pygame.image.load("resources/elements/animations/phil/frame_00.gif")
ground_x_pos = 1000
phil_y_pos = 260
jumping = False

import random

iq = 10

phil_anim_state = 0

slowUpdate = 0

score = 0

legirio_pos_y = 100
legirio_pos_x = 1100

gameover = False

gameover_text = font_big.render("Game over! (Press space to continue)", False, "White")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if iq <= 0: gameover = True

    # ON GAMEOVER
    if gameover:
        score_gameover = font_iq.render("Score: " + str(score), False, "White")
        screen.blit(surface_gameover, (0, 0))
        screen.blit(gameover_text, (310, 70))
        screen.blit(score_gameover, (430, 150))


        # ON SPACE RESPAWN
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_r] and phil_y_pos >= 260:
            gameover = False
            score = 0
            iq = 10
            legirio_pos_x = 1200

        pygame.display.update()
        clock.tick(60)
        continue

    # ON JUMP
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and phil_y_pos >= 260:
        jumping = True
    if jumping:
        if phil_y_pos > 30:
            phil_y_pos -= 15
        else:
            jumping = False
    else:
        if phil_y_pos < 260:
            phil_y_pos += 6

    # MOVE GROUND
    ground_x_pos -= 8
    if ground_x_pos < 0:
        ground_x_pos = 1000


    # MOVE LEGIRIO
    legirio_pos_x -= 5
    if legirio_pos_x < 0 - random.uniform(50, 3000):
        legirio_pos_x = 1200
        legirio_pos_y += random.uniform(-100, 200)
        if legirio_pos_y > 400: legirio_pos_y = 100
        if legirio_pos_y < 20: legirio_pos_y = 100

    screen.blit(surface_sky, (0, 0))
    screen.blit(surface_ground, (ground_x_pos, 400))
    screen.blit(surface_ground, (ground_x_pos - 1000, 400))

    slowUpdate += 2
    if slowUpdate > 4:
        slowUpdate = 0

    if slowUpdate == 4:
        score += 1
        if not jumping: phil_anim_state += 1
    if phil_anim_state > 9:
        phil_anim_state = 0

    surface_text = font.render("Score: " + str(score), False, "White")
    surface_iq = font_iq.render("IQ: " + str(iq), False, "Gray")

    # Phil
    surface_phil = pygame.image.load("resources/elements/animations/phil/frame_0" + str(phil_anim_state) + ".gif")
    screen.blit(surface_phil, (100, phil_y_pos))
    screen.blit(surface_text, (20, 20))
    screen.blit(surface_iq, (160, phil_y_pos - 50))
    surface_legirio = pygame.image.load("resources/elements/legirio.png")
    screen.blit(surface_legirio, (legirio_pos_x, legirio_pos_y))

    # CHECK IF surface_legirio HAS COLLIDED WITH THE surface_phil
    legirio_rect = surface_legirio.get_rect()
    legirio_rect.topleft = (legirio_pos_x, legirio_pos_y)

    phil_rect = surface_phil.get_rect()
    phil_rect.topleft = (100, phil_y_pos)
    if legirio_rect.colliderect(phil_rect):
        legirio_pos_x = 1200
        iq -= 1

    pygame.display.update()
    clock.tick(60)
