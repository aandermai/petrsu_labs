from settings import *


# получение вектора перемещения в зависимости от направления
def get_vector(facing: str) -> list:
    match facing:
        case "u":
            return [-1, 0]
        case "r":
            return [0, 1]
        case "d":
            return [1, 0]
        case "l":
            return [0, -1]


# проверка и активация проводов
def check_layout(FIELD, facing="r", x=0, y=0):
    offset = get_vector(facing)  # вычисление смещения вектора

    x += offset[0]
    y += offset[1]

    if 0 <= x < FIELD_SIZE and 0 <= y < FIELD_SIZE:
        if MIRRORED[facing] in FIELD[x][y].facing:
            FIELD[x][y].is_activated = 1
            FIELD[x][y].draw()
            check_layout(
                FIELD,
                FIELD[x][y].facing[1 - FIELD[x][y].facing.index(MIRRORED[facing])],
                x,
                y,
            )


# очистка игрового поля, деактивируя все блоки, кроме начального
def clear_all(FIELD):
    for i in range(FIELD_SIZE):
        for j in range(FIELD_SIZE):
            if i == 0 and j == 0:
                continue
            FIELD[i][j].is_activated = 0
            FIELD[i][j].draw()
