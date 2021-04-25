from pygame import *
from pygame.transform import rotate
import pygame
from blocks import *
from level import Level
from config import *

def init(size):
    pygame.init()
    screen = pygame.display.set_mode(size)
    loadTextures()
    return screen

def display_level(screen, level):
    for y in range(level.level.size_y):
        for x in range(level.level.size_x):
            sBock = level.static_layer[y][x]
            dBock = level.dynamic_layer[y][x]
            if (sBock != Blocks.VOID):
                screen.blit(textures[sBock.value[0]], (x*grid_size, y*grid_size))
            if (dBock != Blocks.VOID):
                screen.blit(textures[dBock.value[0]], (x*grid_size, y*grid_size))
    if (level.win):
        image = textures[99]
        rotated_image = rotate(image, level.playerPos[2].value*90+level.winRotation)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = [grid_size*level.playerPos[i] for i in range(2)]).center)
        screen.blit(rotated_image, new_rect.topleft)
        level.winRotation += 12
        f = pygame.font.Font("Minecraft.ttf", 150)
        img = f.render('You Win!', True, "#0000F0")
        screen.blit(img, img.get_rect(center =  screen.get_rect().center))
    elif (level.playerPos != None):
        screen.blit(rotate(textures[99], level.playerPos[2].value*90), [grid_size*level.playerPos[i] for i in range(2)])