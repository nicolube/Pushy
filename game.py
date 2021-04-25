from level import *

levels = [
    Level(file="levels/1.dat"),
    Level(file="levels/2.dat"),
    Level(file="levels/3.dat"),
    Level(file="levels/4.dat"),
    Level(file="levels/5.dat"),
    Level(file="levels/6.dat"),
    Level(file="levels/7.dat"),
    Level(file="levels/8.dat"),
    Level(file="levels/9.dat"),
    Level(file="levels/10.dat"),
    ]

current_level = 0
level_instance = None

def resetLevel(level_id=current_level):
    global level_instance, levels,current_level
    current_level = level_id
    level_instance = LevelInstance(levels[level_id])

def press_key_event(button):
    if current_level != None:
        if button == pygame.K_UP:
            level_instance.up()
        elif button == pygame.K_DOWN:
            level_instance.down()
        elif button == pygame.K_RIGHT:
            level_instance.right()
        elif button == pygame.K_LEFT:
            level_instance.left()
        elif button == pygame.K_RETURN:
            if level_instance.win:
                resetLevel(current_level+1)

def press_mouse_event(button, position):
    print(position)