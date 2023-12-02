import pygame
import sys
import random
import numpy
import time


def change_pos(y, x):
    global rad_c_p
    # global d_pos_else
    global d_pos_same
    d_ver = 0
    for a in range(y - rad_c_p, y + rad_c_p + 1):
        for b in range(x - rad_c_p, x + rad_c_p + 1):
            if (a >= 0 and b >= 0) and (a < ROWS and b < COLS):
                if df[a][b] == 2:
                    d_ver += d_pos_same
                elif df[a][b] == 3:
                    d_ver -= d_pos_same
    return d_ver


def create_field_u(ver_civ, ver_enemy):
    global COLS, ROWS, max_score
    for i in range(ROWS):
        for j in range(COLS):
            ver_g = 1 - (ver_enemy + ver_civ)
            ver_c_e = ver_g + ver_civ + change_pos(i, j)
            # if ver_c_e < ver_g or ver_c_e > 1:
            #     raise Exception(ver_g, ver_c_e)
            rand = random.random()
            if ver_g < rand < ver_c_e:
                df[i][j] = 2
            elif rand > ver_c_e:
                df[i][j] = 3
                max_score += 1


def draw_field():
    screen.fill((0, 0, 0))
    global TOP_MARGIN
    grid = []
    for row in range(ROWS):
        grid.append([])
        for col in range(COLS):
            rect = pygame.Rect(col * (CELL_SIZE + MARGIN), row * (CELL_SIZE + MARGIN) + TOP_MARGIN, CELL_SIZE, CELL_SIZE)
            grid[row].append(rect)

    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, s[df[row, col]], grid[row][col])
            pygame.draw.rect(screen, s[0], grid[row][col], 1)

    f1 = pygame.font.Font(None, 40)
    try:
        text1 = f1.render(f'Счёт: {score}/{max_score}  {int(score / max_score * 100)} %', 1, (255, 255, 255))
    except:
        text1 = f1.render(f'Счёт: {score}/{0}  {int(score / 1 * 100)} %', 1, (255, 255, 255))
    screen.blit(text1, TEXT_PLACE)

    rect = pygame.Rect(N_G_B_P[0], N_G_B_P[1], N_G_B_P[2], N_G_B_P[3])
    pygame.draw.rect(screen, COLOR_NGB, rect)
    pygame.display.flip()


def boom(r, x, y):
    global score
    global df
    for a in range(y - r, y + r + 1):
        for b in range(x - r, x + r + 1):
            if a >= 0 and b >= 0 and a < ROWS and b < COLS:
                if df[a, b] == 2:
                    score -= sc_min
                elif df[a, b] == 3:
                    score += sc_plus
                df[a, b] = 4
                boomed.append((y, x))


def animation():
    pass


ROWS = 170
COLS = ROWS
CELL_SIZE = 5
MARGIN = 0
TOP_MARGIN = 50
TEXT_PLACE = (110, 20)
N_G_B_P = [2, 2, 100, 40]
COLOR_NGB = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((ROWS * (CELL_SIZE + MARGIN), COLS * (CELL_SIZE + MARGIN) + TOP_MARGIN))
pygame.display.set_caption("BOOM")

pos_civ = 0.3
pos_enemy = pos_civ
d_pos_same = 0.045
# d_pos_else = 0.03
rad_c_p = 2

score = 0
max_score = 0
sc_min = 1
sc_plus = 1

boomed = []
s = [(0, 0, 0), (0, 153, 0), (0, 0, 255), (153, 0, 0), (102, 102, 102)]
space = 0
field = 1
civilians = 2
enemy = 3
destroyed = 4

df = numpy.ones((ROWS, COLS), int)
create_field_u(pos_civ, pos_enemy)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] > TOP_MARGIN:
            rand = random.randint(2, 5)
            pos = event.pos
            x_c, y_c = pos[0] // (CELL_SIZE + MARGIN), (pos[1] - TOP_MARGIN) // (CELL_SIZE + MARGIN)
            if df[y_c][x_c] != 4:
                boom(rand, x_c, y_c)
                print(boomed)
        elif event.type == pygame.MOUSEBUTTONDOWN and (N_G_B_P[0] <= event.pos[0] <= N_G_B_P[2] + N_G_B_P[0] and N_G_B_P[1] <= event.pos[1] <= N_G_B_P[3] + N_G_B_P[1]) or event.type == pygame.MOUSEWHEEL:
            df = numpy.ones((ROWS, COLS), int)
            max_score = 0
            score = 0
            create_field_u(pos_civ, pos_enemy)
    draw_field()


