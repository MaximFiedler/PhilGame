import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("PhilGame")
pygame_icon = pygame.image.load('resources/logo.png')
pygame.display.set_icon(pygame_icon)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
font_iq = pygame.font.Font(None, 50)
font_big = pygame.font.Font(None, 100)

surface_sky = pygame.image.load("resources/elements/sky.png")
surface_damage = pygame.image.load("resources/elements/damage.png")
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

legirio_pos_y = 400
legirio_pos_x = 1100

gameover = False

phil_x_pos = 100

gameover_text = font_big.render("Game over!", False, "White")

speed_mult = 1.05

base_slowUpdateInterval = 10

damage_anim_delay = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if iq <= 0: gameover = True
    keys = pygame.key.get_pressed()

    # ON GAMEOVER
    if gameover:
        score_gameover = font_iq.render("Score: " + str(score), False, "White")
        screen.blit(surface_gameover, (0, 0))
        screen.blit(gameover_text, (310, 70))
        screen.blit(score_gameover, (430, 150))
        surface_respawn_text = font.render("Press R to respawn", False, "White")
        screen.blit(surface_respawn_text, (20, 20))

        # ON SPACE RESPAWN
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            gameover = False
            score = 0
            iq = 10
            legirio_pos_x = 1200
            speed_mult = 1.05
            damage_anim_delay = 0

        pygame.display.update()
        clock.tick(60)
        continue

    speed_mult += 0.0005
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]: speed_mult += 0.0005

    # ON JUMP
    if keys[pygame.K_SPACE] and phil_y_pos >= 260 and not keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        jumping = True
    if jumping:
        if phil_y_pos > -300:
            if phil_x_pos < 970: phil_x_pos += 10
            phil_y_pos -= 20
        else:
            jumping = False
    else:
        if phil_x_pos > 100 and not phil_y_pos < 260: phil_x_pos -= 7
        if phil_y_pos < 260:
            phil_y_pos += 10

    # MOVE GROUND
    ground_x_pos -= 4.5 * speed_mult
    if ground_x_pos < 0:
        ground_x_pos = 1000

    # MOVE LEGIRIO
    legirio_pos_x -= 3.5 * speed_mult
    if legirio_pos_x < 0 - random.uniform(50, 3000):
        legirio_pos_x = 2000
        legirio_pos_y += random.uniform(-100, 100)
        if legirio_pos_y > 700: legirio_pos_y = 500
        if legirio_pos_y < 300: legirio_pos_y = 500

    screen.blit(surface_sky, (0, 0))
    screen.blit(surface_ground, (ground_x_pos, 400))
    screen.blit(surface_ground, (ground_x_pos - 1000, 400))

    slowUpdateInterval = max(base_slowUpdateInterval / speed_mult, 1)

    slowUpdate += 1
    if slowUpdate > slowUpdateInterval:
        slowUpdate = 0

    if slowUpdate == 0:
        score += 1
        if not jumping: phil_anim_state += 1
        if phil_anim_state > 9:
            phil_anim_state = 0

    surface_text = font.render("Score: " + str(score), False, "White")
    surface_iq = font_iq.render("IQ: " + str(iq), False, "Gray")
    fly_pos = 0
    # Phil
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        surface_phil = pygame.image.load("resources/elements/animations/phil/fly.png")
        fly_pos = 200
    else:
        surface_phil = pygame.image.load("resources/elements/animations/phil/frame_0" + str(phil_anim_state) + ".gif")
    screen.blit(surface_phil, (phil_x_pos, phil_y_pos + fly_pos))
    screen.blit(surface_text, (20, 20))
    screen.blit(surface_iq, (phil_x_pos + 60, phil_y_pos - 50 + fly_pos))
    surface_legirio = pygame.image.load("resources/elements/legirio.png")
    screen.blit(surface_legirio, (legirio_pos_x, legirio_pos_y))

    # CHECK IF surface_legirio HAS COLLIDED WITH THE surface_phil
    legirio_rect = surface_legirio.get_rect()
    legirio_rect.topleft = (legirio_pos_x, legirio_pos_y)

    phil_rect = surface_phil.get_rect()
    phil_rect.topleft = (phil_x_pos, phil_y_pos + fly_pos)

    damage_anim_delay -= 1

    # If phil collided with Legirio
    if legirio_rect.colliderect(phil_rect):
        damage_anim_delay = 5
        legirio_pos_x = 2000
        legirio_pos_y += random.uniform(-100, 100)
        if legirio_pos_y > 500: legirio_pos_y = 400
        if legirio_pos_y < 200: legirio_pos_y = 400
        iq -= 1

    if damage_anim_delay > 0:
        screen.blit(surface_damage, (0, 0))

    pygame.display.update()
    clock.tick(60)
