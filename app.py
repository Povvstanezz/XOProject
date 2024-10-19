import pygame
import pygame.draw_py

from GameGrid import GameGrid

pygame.init()

screen = pygame.display.set_mode((640,480))
bgcolor = (179, 180, 181)
screen.fill(bgcolor)
tiles = (3,3)

DRAW_DATA = grid.update()

# Создаем Surfaces

grid = GameGrid(tiles=(tiles), grid_size=(400,400))
grid_surface = pygame.Surface((450,450))
grid_surface.fill(bgcolor)
cursor_surface = pygame.Surface((grid.STEP_SIZE_X, grid.STEP_SIZE_Y))

def surfaces_update():
    main_surface = screen
    main_surface.blit(grid_surface, (50,50))
    grid_surface.fill(bgcolor)
    
    cursor_marker = DRAW_DATA['cursor_marker']
    x1 = cursor_marker[0][0] - 1
    y1 = cursor_marker[0][1] - 1
    grid_surface.blit(cursor_surface, (x1,y1))
    pass

#Всё отлично
def draw_data():
    data_list = DRAW_DATA['tiles_grid_data']
    lines_list = DRAW_DATA['lines']

    # Отрисовываем данные
    for x in range(len(data_list)):
        for y in range(len(data_list[x])):
            x, y = grid.validate_pos(x,y)
            pos = grid.norm_tiles_coord(x,y)
            if data_list[x][y] == 'X':
                pygame.draw.line(grid_surface,(170,0,0),pos[0], pos[2], 5)
                pygame.draw.line(grid_surface,(170,0,0),pos[1], pos[3], 5)

            if data_list[x][y] == '0':
                pygame.draw.circle(grid_surface, (0, 0, 170), (pos[0][0] + grid.STEP_SIZE_X / 2, pos[0][1] + grid.STEP_SIZE_Y / 2), grid.STEP_SIZE_Y / 2 - 3, 5)

    # Отрисовываем линии
    for coord in lines_list:
        x1,y1,x2,y2 = coord
        pygame.draw.line(grid_surface, (0,0,0), (x1, y1), (x2, y2), 2)

    # Отрисовываем курсор
    cursor_surface.fill((100,100,100))

    #Обновляем surfaces
    surfaces_update()    
    pass


def check(tile):
    # Получаем диагонали
    left_diag = grid.get_line(0, 0, (tiles[0] - 1), (tiles[1] - 1))
    right_diag = grid.get_line((tiles[0] - 1), 0, 0, (tiles[1] - 1))

    horizontal_line = grid.get_line(0, tile[1], (tiles[0] -1), tile[1])
    vertical_line = grid.get_line(tile[0], 0, tile[0], (tiles[0] - 1))

    #Все линии собрать в один список и проверить в цикле
    if grid.check_line(left_diag, data):
        print('Win')
        win_check(p1, p2, data)

    if grid.check_line(right_diag, data):
        print('Win')
        win_check(p1, p2, data)

    hor_line, ver_line = draw_HV_lines(tile) #функция получения гор. и вер. линий
    if grid.check_line(hor_line, data):
        print('Win')
        win_check(p1, p2, data)

    if grid.check_line(ver_line, data):
        print('Win')
        win_check(p1, p2, data)
    pass

# Этот функционал в Check
def draw_HV_lines(tile):
    horizontal_line = grid.get_line(0, tile[1], (tiles[0] -1), tile[1])
    vertical_line = grid.get_line(tile[0], 0, tile[0], (tiles[0] - 1))
    return horizontal_line, vertical_line


run = True
count = 1

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = [mouse_pos[0]-50, mouse_pos[1]-50]
            grid.get_cursor(mouse_pos)
        
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
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = [mouse_pos[0]-50, mouse_pos[1]-50]
            tile = grid.get_cursor(mouse_pos)

            data = '0' if count % 2 == 0 else "X"
            if not grid.mark_pos(tile[0], tile[1], data):
                count += 1

            count +=1

    grid.update()
    draw_data()
    pygame.display.update()
