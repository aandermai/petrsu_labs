from settings import *
from block import Block

def restart_game(screen):
    position = [BLOCK_MARGIN, BLOCK_MARGIN + 100]
    FIELD = []
    for _ in range(FIELD_SIZE):
        FIELD.append([])
        for j in range(FIELD_SIZE):
            if j == 0 or j == FIELD_SIZE - 1:
                block_type = CORNER
            else:
                block_type = STRAIGHT

            FIELD[-1].append(Block(screen, position.copy(), block_type))
            FIELD[-1][-1].draw()

            position[0] += BLOCK_SIZE + BLOCK_MARGIN

        position[0] = BLOCK_MARGIN
        position[1] += BLOCK_SIZE + BLOCK_MARGIN

    FIELD[0][0].rotate = lambda: None
    FIELD[0][0].facing_offset = 0
    FIELD[0][0].facing = "ur"
    FIELD[0][0].is_activated = 1
    FIELD[0][0].draw()
    return FIELD