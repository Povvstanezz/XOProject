import pygame
import pygame.draw_py

from GameGrid import GameGrid

pygame.init()

screen = pygame.display.set_mode((640,480))
bgcolor = (179, 180, 181)
tiles = (5, 5)

grid_surface = pygame.Surface(screen.get_size())
grid_surface.fill(bgcolor)

grid = GameGrid(screen.get_size(), (tiles), (400,400))

DRAW_DATA = grid.update()

def draw_lines(lines):
    for coord in lines:
        x1,y1,x2,y2 = coord
        pygame.draw.line(grid_surface, (0,0,0), (x1, y1), (x2, y2), 1)

def select_tiles():
    data = DRAW_DATA['selected_tiles']
    for tile in data:
        pygame.draw.polygon(grid_surface, (120, 129, 159), (tile[0],tile[1],tile[2],tile[3]))

def draw_cursor():
    pygame.draw.polygon(grid_surface, (120,120,102), DRAW_DATA['cursor_marker'])


def draw_data():
    data_list = DRAW_DATA['tiles_grid_data']
    
    for x in range(len(data_list)):
        for y in range(len(data_list[x])):
            pos = grid.norm_tiles_coord(x,y)
            if data_list[x][y] == 'X':
                pygame.draw.line(grid_surface,(170,0,0),pos[0], pos[2], 5)
                pygame.draw.line(grid_surface,(170,0,0),pos[1], pos[3], 5)

            if data_list[x][y] == '0':
                pygame.draw.circle(grid_surface, (0, 0, 170), (pos[0][0] + grid.STEP_SIZE_X / 2, pos[0][1] + grid.STEP_SIZE_Y / 2), ((grid.STEP_SIZE_Y / 2) - 3), 5)
    pass


run = True
count = 1
# Создаем диагональ
diag = grid.get_line(0,0,9,9)

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        draw_lines(DRAW_DATA['lines'])
        select_tiles()
        screen.blit(grid_surface, (0,0))
        grid_surface.fill(bgcolor)
        draw_data()




        

        if event.type == pygame.MOUSEMOTION:
            grid.get_cursor(pygame.mouse.get_pos())

        norm_X, norm_Y = DRAW_DATA['cursor']

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                norm_X -= 1
            elif event.key == pygame.K_RIGHT:
                norm_X += 1
            elif event.key == pygame.K_UP:
                norm_Y -= 1
            elif event.key == pygame.K_DOWN:
                norm_Y += 1
            elif event.key == pygame.K_SPACE:
                pass

            norm_X, norm_Y = grid.validate_pos(norm_X, norm_Y)
            cursor_marker = grid.norm_tiles_coord(norm_X, norm_Y)
            grid.set_cursor_pos(norm_X, norm_Y)
            grid.set_cursor_marker(cursor_marker)
           
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            tile = grid.get_cursor(pygame.mouse.get_pos())

            data = '0' if count % 2 == 0 else "X"
            grid.mark_pos(tile[0], tile[1], data)

            if grid.check_line(diag, data):
                print('Win')
            else:
                print('More')
            count +=1

    grid.update()
    draw_cursor()
    pygame.display.update()