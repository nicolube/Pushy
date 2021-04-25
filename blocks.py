from enum import Enum
import pygame
from os import path

textures = {
    1: "wall.png",
    2: "box.png",
    3: "red_ball.png",
    4: "yellow_ball.png",
    5: "blue_ball.png",
    9: "red_goal.png",
    10: "yellow_goal.png",
    11: "blue_goal.png",
    12: "house.png",
    99: "pushy.png"
}

def loadTextures():
    global textures
    for k, v in textures.items():
        p = path.join("textures", v)
        textures[k] = pygame.image.load(p).convert_alpha()

class BlockProperties(Enum):
    SOLID = 0
    MOVEABLE = 1
    BALL = 2
    DYE = 3
    GOAL = 4


class Blocks(Enum):
    PB = BlockProperties
    VOID        = [ 0, 0, []] # Texture ID, Layer, Properties
    WALL        = [ 1, 1, [PB.SOLID]]
    BOX         = [ 2, 1, [PB.MOVEABLE]]
    RED_BALL    = [ 3, 1, [PB.MOVEABLE, PB.BALL]]
    YELLOW_BALL  = [ 4, 1, [PB.MOVEABLE, PB.BALL]]
    BLUE_BALL   = [ 5, 1, [PB.MOVEABLE, PB.BALL]]
    RED_DYE     = [ 6, 0, [PB.DYE]]
    YELLOW_DYE   = [ 7, 0, [PB.DYE]]
    BLUE_DYE    = [ 8, 0, [PB.DYE]]
    RED_GOAL    = [ 9, 0, [PB.MOVEABLE, PB.GOAL]]
    YELLOW_GOAL  = [10, 0, [PB.MOVEABLE, PB.GOAL]]
    BLUE_GOAL   = [11, 0, [PB.MOVEABLE, PB.GOAL]]
    HOUSE       = [12, 0, []]
    PLAYER1     = [98, 1, []]
    PLAYER      = [99, 1, []]