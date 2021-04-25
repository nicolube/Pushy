import pygame
from pygame.transform import rotate
import blocks
import level
import graphics
import game
from config import *

import sys

game.resetLevel(0)

screen = graphics.init(game.levels[0].get_size())

is_running = True
clock = pygame.time.Clock()
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            game.press_key_event(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.press_mouse_event(event.button, pygame.mouse.get_pos())
    screen.fill(pygame.Color('#FFFFFF'))
    graphics.display_level(screen, game.level_instance)
    pygame.display.update()
    clock.tick(60)
   