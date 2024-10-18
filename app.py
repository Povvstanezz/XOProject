import pygame
import pygame.draw_py

from GameGrid import GameGrid

pygame.init()

screen = pygame.display.set_mode((640,480))

bgcolor = (179, 180, 181)
screen.fill(bgcolor)
tiles = (3,3)

# grid_surface = pygame.Surface(screen.get_size())
# grid_surface.fill(bgcolor)

run = True
count = 1

# Создаем Surfaces

grid = GameGrid(tiles=(tiles), grid_size=(400,400))
grid_surface = pygame.Surface((450,450))
grid_surface.fill(bgcolor)

cursor_surface = pygame.Surface((grid.STEP_SIZE_X, grid.STEP_SIZE_Y))
#Surfaces list
surface_list = [screen, grid_surface, cursor_surface]

# Создаем диагональ
# делаем ее зависимой от количества клеток - (tiles)

left_diag = grid.get_line(0, 0, (tiles[0] - 1), (tiles[1] - 1))
right_diag = grid.get_line((tiles[0] - 1), 0, 0, (tiles[1] - 1))

DRAW_DATA = grid.update()

def surfaces_update():
    main_surface = screen
    main_surface.blit(grid_surface, (50,50))
    grid_surface.fill(bgcolor)
    cursor_marker = DRAW_DATA['cursor_marker']
    x1 = cursor_marker[0][0] - 1
    x2 = cursor_marker[0][1] - 1
    grid_surface.blit(cursor_surface, (x1,x2))      
    pass

def draw_data():
    data_list = DRAW_DATA['tiles_grid_data']
    lines_list = DRAW_DATA['lines']
    cursor_marker = DRAW_DATA['cursor_marker']

    # Отрисовываем данные
    for x in range(len(data_list)):
        for y in range(len(data_list[x])):
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
    # pygame.draw.polygon(cursor_surface, (120,120,102), (0,0), (0,0))
    cursor_surface.fill((100,100,100))

    surfaces_update()    
    pass

def draw_HV_lines(tile):
    horizontal_line = grid.get_line(0, tile[1], (tiles[0] -1), tile[1])
    vertical_line = grid.get_line(tile[0], 0, tile[0], (tiles[0] - 1))
    return horizontal_line, vertical_line

# def select_tiles():
#     data = DRAW_DATA['selected_tiles']
#     for tile in data:
#         pygame.draw.polygon(grid_surface, (120, 129, 159), (tile[0],tile[1],tile[2],tile[3]))

# def draw_cursor():
#     pygame.draw.polygon(grid_surface, (120,120,102), DRAW_DATA['cursor_marker'])


# def draw_data():
#     data_list = DRAW_DATA['tiles_grid_data']
    
#     for x in range(len(data_list)):
#         for y in range(len(data_list[x])):
#             pos = grid.norm_tiles_coord(x,y)
#             if data_list[x][y] == 'X':
#                 pygame.draw.line(grid_surface,(170,0,0),pos[0], pos[2], 5)
#                 pygame.draw.line(grid_surface,(170,0,0),pos[1], pos[3], 5)

#             if data_list[x][y] == '0':
#                 pygame.draw.circle(grid_surface, (0, 0, 170), (pos[0][0] + grid.STEP_SIZE_X / 2, pos[0][1] + grid.STEP_SIZE_Y / 2), ((grid.STEP_SIZE_Y / 2) - 3), 5)
#     pass

# def draw_lines(lines):
#     for coord in lines:
#         x1,y1,x2,y2 = coord
#         pygame.draw.line(grid_surface, (0,0,0), (x1, y1), (x2, y2), 1)

# run = True
# count = 1

# Создаем диагональ
# делаем ее зависимой от количества клеток - (tiles)
# left_diag = grid.get_line(0, 0, (tiles[0] - 1), (tiles[1] - 1))
# right_diag = grid.get_line((tiles[0] - 1), 0, 0, (tiles[1] - 1))

# получаем горизонтальную и вертикальную линию исходя из нажатой клетки - (tile)

                                  
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        draw_data()

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
            
            norm_X, norm_Y = DRAW_DATA['cursor']
            norm_X, norm_Y = grid.validate_pos(norm_X, norm_Y)
            cursor_marker = grid.norm_tiles_coord(norm_X, norm_Y)
            grid.set_cursor_pos(norm_X, norm_Y)
            grid.set_cursor_marker(cursor_marker)
           
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = [mouse_pos[0]-50, mouse_pos[1]-50]
            tile = grid.get_cursor(mouse_pos)
            data = '0' if count % 2 == 0 else "X"
            grid.mark_pos(tile[0], tile[1], data)

            if grid.check_line(left_diag, data):
                print('Win')

            if grid.check_line(right_diag, data):
                print('Win')
                
            hor_line, ver_line = draw_HV_lines(tile) #функция получения гор. и вер. линий
            if grid.check_line(hor_line, data):
                print('Win')
            
            if grid.check_line(ver_line, data):
                print('Win')
            count +=1
            

    grid.update()
    # draw_cursor()
    pygame.display.update()