import pygame
import sys
import random
import numpy



def change_pos(y, x, w):
    global rad_c_p
    global d_pos_else
    global d_pos_same
    d_pos = 0
    for a in range(y - rad_c_p, y + rad_c_p + 1):
        for b in range(x - rad_c_p, x + rad_c_p + 1):
            if (a >= 0 and b >= 0) and (a < ROWS and b < COLS):
                if df[a][b] == w:
                    d_pos += d_pos_same
                elif df[a][b] in [2, 3]:
                    d_pos -= d_pos_else



    return d_pos


def create_field_u(pos_civ, pos_enemy):
    global COLS, ROWS, max_score
    for i in range(ROWS):
        for j in range(COLS):
            pos1 = pos_civ + change_pos(i, j, 2)
            pos2 = pos_enemy + change_pos(i, j, 3)
            rand = random.random()
            if rand < pos1:
                df[i][j] = 2
                max_score += 1
            elif rand < pos2 + pos1:
                df[i][j] = 3


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
    text1 = f1.render(f'Счёт: {score}/{max_score}  {int(score / max_score * 100)} %', 1, (255, 255, 255))
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


ROWS = 25
COLS = ROWS
CELL_SIZE = 25
MARGIN = 1
TOP_MARGIN = 50
TEXT_PLACE = (110, 20)
N_G_B_P = [2, 2, 100, 40]
COLOR_NGB = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((ROWS * (CELL_SIZE + MARGIN), COLS * (CELL_SIZE + MARGIN) + TOP_MARGIN))
pygame.display.set_caption("BOOM")

pos_civ = 0.15
pos_enemy = pos_civ
d_pos_same = 0.05
d_pos_else = 0.01
rad_c_p = 2

score = 0
max_score = 0
sc_min = 1
sc_plus = 1

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
            rand = random.randint(0, 4)
            pos = event.pos
            x_c, y_c = pos[0] // (CELL_SIZE + MARGIN), (pos[1] - TOP_MARGIN) // (CELL_SIZE + MARGIN)
            boom(rand, x_c, y_c)
        elif event.type == pygame.MOUSEBUTTONDOWN and (N_G_B_P[0] <= event.pos[0] <= N_G_B_P[2] + N_G_B_P[0] and N_G_B_P[1] <= event.pos[1] <= N_G_B_P[3] + N_G_B_P[1]):
            df = numpy.ones((ROWS, COLS), int)
            max_score = 0
            score = 0
            create_field_u(pos_civ, pos_enemy)

    draw_field()


