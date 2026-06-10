import pygame, sys, game_control, layout_control, time
from tkinter import messagebox

from settings import *

pygame.init()
screen = pygame.display.set_mode(
    (
        BLOCK_SIZE * FIELD_SIZE + (FIELD_SIZE + 1) * BLOCK_MARGIN,
        BLOCK_SIZE * FIELD_SIZE + (FIELD_SIZE + 1) * BLOCK_MARGIN + 100,
    )
)

font = pygame.font.SysFont(None, 136)

pygame.display.set_caption("Light'em up!")


def start_game():
    FIELD = game_control.restart_game(screen)

    layout_control.check_layout(FIELD)
    time_start_game = time.time()
    time_stop_game = time_start_game + TIME_STOP
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                column = pos[0] // (BLOCK_SIZE + BLOCK_MARGIN)
                row = (pos[1] - 100) // (BLOCK_SIZE + BLOCK_MARGIN)

                FIELD[row][column].rotate()

                layout_control.clear_all(FIELD)
                layout_control.check_layout(FIELD)

        pygame.display.flip()
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_SIZE, 100))
        timer_text = font.render(
            str(int(time_stop_game - time.time() + 1)), False, (255, 255, 255)
        )
        screen.blit(timer_text, (SCREEN_SIZE // 2 - 40, 10))

        pygame.time.Clock().tick(10)
        if (
            FIELD[-1][0].facing == "rd"
            and FIELD_SIZE % 2 == 0
            and FIELD[-1][0].is_activated == 1
        ):
            return True
        if (
            FIELD[-1][-1].facing == "dl"
            and FIELD_SIZE % 2 == 1
            and FIELD[-1][-1].is_activated == 1
        ):
            return True

        if time.time() - time_start_game > TIME_STOP:
            return False


if __name__ == "__main__":
    while True:
        is_win = start_game()
        if is_win:
            messagebox.showinfo("Неплох", "Неплох")
        else:
            messagebox.showinfo("Плох", "Плох")
