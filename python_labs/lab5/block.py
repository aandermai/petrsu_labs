import random, pygame
from settings import *

RULD = "urdl"  # направления


class Block:
    def __init__(self, screen, position: list, block_type: int) -> None:
        self.position = position

        self.screen = screen

        self.is_activated = 0
        self.block_type = block_type

        self.facing_offset = random.randint(0, 3)
        self.facing = (
            RULD[self.facing_offset] + RULD[(self.facing_offset + self.block_type) % 4]
        )

    def rotate(self):
        self.facing_offset += 1

        if self.facing_offset == 4:
            self.facing_offset = 0

        self.facing = (
            RULD[self.facing_offset] + RULD[(self.facing_offset + self.block_type) % 4]
        )

        self.draw()

    def draw(self):
        r = pygame.Rect(*self.position, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(self.screen, BLOCK_COLOR, r)

        if self.block_type == STRAIGHT:
            if self.facing_offset % 2 == 0:
                start_pos = (self.position[0] + (BLOCK_SIZE // 2), self.position[1])
                end_pos = (
                    self.position[0] + (BLOCK_SIZE // 2),
                    self.position[1] + BLOCK_SIZE - 1,
                )
            else:
                start_pos = (self.position[0], self.position[1] + (BLOCK_SIZE // 2))
                end_pos = (
                    self.position[0] + BLOCK_SIZE - 1,
                    self.position[1] + (BLOCK_SIZE // 2),
                )
            if self.is_activated == 1:
                pygame.draw.line(
                    self.screen, ACTIVATED_COLOR, start_pos, end_pos, WIRE_SIZE
                )
            else:
                pygame.draw.line(
                    self.screen, NON_ACTIVATED_COLOR, start_pos, end_pos, WIRE_SIZE
                )

        else:
            mid_pos = (
                self.position[0] + (BLOCK_SIZE // 2),
                self.position[1] + (BLOCK_SIZE // 2),
            )

            match self.facing_offset:
                case 0:
                    start_pos = (mid_pos[0], mid_pos[1] - (BLOCK_SIZE // 2))
                    end_pos = (mid_pos[0] + (BLOCK_SIZE // 2) - 1, mid_pos[1])
                    mid_pos = (mid_pos[0], mid_pos[1])
                case 1:
                    start_pos = (mid_pos[0] + (BLOCK_SIZE // 2) - 1, mid_pos[1])
                    end_pos = (mid_pos[0], mid_pos[1] + (BLOCK_SIZE // 2) - 1)
                case 2:
                    start_pos = (mid_pos[0], mid_pos[1] + (BLOCK_SIZE // 2) - 1)
                    end_pos = (mid_pos[0] - (BLOCK_SIZE // 2), mid_pos[1])
                case 3:
                    start_pos = (mid_pos[0] - (BLOCK_SIZE // 2), mid_pos[1])
                    end_pos = (mid_pos[0], mid_pos[1] - (BLOCK_SIZE // 2))
            if self.is_activated == 1:
                pygame.draw.circle(
                    self.screen, ACTIVATED_COLOR, mid_pos, WIRE_SIZE // 2
                )
                pygame.draw.lines(
                    self.screen,
                    ACTIVATED_COLOR,
                    False,
                    [start_pos, mid_pos, end_pos],
                    WIRE_SIZE,
                )
            else:
                pygame.draw.circle(
                    self.screen, NON_ACTIVATED_COLOR, mid_pos, WIRE_SIZE // 2
                )
                pygame.draw.lines(
                    self.screen,
                    NON_ACTIVATED_COLOR,
                    False,
                    [start_pos, mid_pos, end_pos],
                    WIRE_SIZE,
                )
