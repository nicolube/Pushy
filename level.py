from blocks import *
from config import *
from enum import Enum

class Direction(Enum):
    NORTH = 0
    EAST = 3
    SOUTH = 2
    WEST = 1

blockMap = {
    "W": Blocks.WALL,
    "#": Blocks.BOX,
    "r": Blocks.RED_BALL,
    "y": Blocks.YELLOW_BALL,
    "b": Blocks.BLUE_BALL,
    "R": Blocks.RED_DYE,
    "Y": Blocks.YELLOW_DYE,
    "B": Blocks.BLUE_DYE,
    "a": Blocks.RED_GOAL,
    "d": Blocks.YELLOW_GOAL,
    "c": Blocks.BLUE_GOAL,
    "H": Blocks.HOUSE,
    "p": Blocks.PLAYER1,
    "P": Blocks.PLAYER
}

class Level:
    size_x = 0
    size_y = 0

    playerPos = None
    player1Pos = None

    static_layer = []
    dynamic_layer = []

    balls = 0    

    def __init__(self, size = None, file=None):
        if (size != None):
            self.size_x = size[0]
            self.size_y = size[1]
        if (file != None):
            self.load(file)

    def load(self, file):
        with open(file, mode="r") as f:
            print("Load level:", file)
            lines = f.readlines()
            level_iterator = iter(lines)
            config = next(level_iterator).split(':')
            self.size_x = int(config[0])
            self.size_y = int(config[1])
            self.static_layer = [[Blocks.VOID]*self.size_x for i in range(self.size_y)]
            self.dynamic_layer = [[Blocks.VOID]*self.size_x for i in range(self.size_y)]
            
            for y in range(self.size_y):
                line = next(level_iterator, None)
                if line == None:
                    break
                x = 0
                for s in line:
                    if s in blockMap.keys():
                        block_data = blockMap[s]
                        if block_data.value[1] == 0:
                            self.static_layer[y][x] = block_data
                            print("layer", block_data)
                        elif block_data.value[1] == 1:
                            if block_data == Blocks.PLAYER:
                                self.playerPos = [x, y]
                            elif block_data == Blocks.PLAYER1:
                                self.player1Pos = [x, y]
                            else:
                                self.dynamic_layer[y][x] = block_data
                                if BlockProperties.BALL in block_data.value[2]:
                                    self.balls += 1
                    x += 1
    def get_size(self):
        return (self.size_x*grid_size, self.size_y*grid_size)

class LevelInstance:
    level = None

    playerPos = None
    player1Pos = None

    static_layer = []
    dynamic_layer = []

    locked = False
    win = False
    winRotation = 0
    
    balls = 0

    def __init__(self, level):
        self.level = level
        self.playerPos = level.playerPos
        self.player1Pos = level.player1Pos
        self.static_layer =level.static_layer
        self.dynamic_layer = level.dynamic_layer
        if self.playerPos !=None:
            self.playerPos.append(Direction.NORTH)
        if self.player1Pos !=None:
            self.player1Pos.append(Direction.NORTH)
        self.balls = level.balls

    def up(self, pId=0):
        if self.locked: return
        self.playerPos[2] = Direction.NORTH
        self.__move(pId)
    def down(self, pId=0):
        if self.locked: return
        self.playerPos[2] = Direction.SOUTH
        self.__move(pId)
    def left(self, pId=0):
        if self.locked: return
        self.playerPos[2] = Direction.WEST
        self.__move(pId)
    def right(self, pId=0):
        if self.locked: return
        self.playerPos[2] = Direction.EAST
        self.__move(pId)
    
    def __move(self, pId):
        direction = None
        position = None
        if (pId == 0):
            position = self.playerPos
            direction = self.playerPos[2]
        elif (pId == 1):
            position = self.player1Pos
            direction = self.player1Pos[2]
        targetPos = self.__getTargetPos(position, direction)
        dTargetBlock = self.dynamic_layer[targetPos[1]][targetPos[0]]
        sTargetBlock = self.static_layer[targetPos[1]][targetPos[0]]
        properties = dTargetBlock.value[2]
        if BlockProperties.SOLID in properties:
            return
        elif BlockProperties.MOVEABLE in properties:
            if not self.__moveEntity(targetPos, direction, dTargetBlock):
                return
        if sTargetBlock == Blocks.HOUSE:
            self.__checkWin()
        if (pId == 0):
            self.playerPos = targetPos
        elif (pId == 1):
            self.player1Pos = targetPos
    
    def __checkWin(self):
        if (self.balls > 0):
            return
        self.locked = True
        self.win = True

    def __moveEntity(self, position, direction, current_block):
        targetPos = self.__getTargetPos(position, direction)
        current_block = self.dynamic_layer[position[1]][position[0]] 
        dTargetBlock = self.dynamic_layer[targetPos[1]][targetPos[0]]
        sTargetBlock = self.static_layer[targetPos[1]][targetPos[0]]
        if (dTargetBlock != Blocks.VOID):
            return False
        dProperties = current_block.value[2]
        sProperties = sTargetBlock.value[2]
        if BlockProperties.BALL in dProperties and BlockProperties.GOAL in sProperties:
            if sTargetBlock.name.split('_')[0] != current_block.name.split('_')[0]:
                return False
            self.dynamic_layer[position[1]][position[0]] = Blocks.VOID
            self.balls -= 1
            return True
        self.dynamic_layer[targetPos[1]][targetPos[0]] = current_block
        self.dynamic_layer[position[1]][position[0]] = dTargetBlock
        return True

    def __getTargetPos(self, pos, direction):
        pos = pos.copy()
        if direction == Direction.NORTH:
            pos[1] -= 1
        if direction == Direction.EAST:
            pos[0] += 1
        if direction == Direction.SOUTH:
            pos[1] += 1
        if direction == Direction.WEST:
            pos[0] -= 1
        return pos

