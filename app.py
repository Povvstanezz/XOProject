import pygame
import pygame.draw_py
import random


from GameGrid import GameGrid
from gui import Button

pygame.init()

screen = pygame.display.set_mode((640,480))
bgcolor = (179, 180, 181)
screen.fill(bgcolor)
tiles = (3,3)

# Создаем Surfaces
grid = GameGrid(tiles=(tiles), grid_size=(400,400))
DRAW_DATA = grid.update()
grid_surface = pygame.Surface((401,401))
grid_surface.fill(bgcolor)
cursor_surface = pygame.Surface((grid.STEP_SIZE_X, grid.STEP_SIZE_Y))

start_game_screen_surface = pygame.Surface(screen.get_size())
start_game_screen_surface.fill((100, 100, 100))
btn_surface = Button().get_button_surface()
btn = Button()
btn_start_pos = screen.get_size()[0]/2-btn_surface.get_size()[0]/2, screen.get_size()[1]/2-btn_surface.get_size()[1]/2
# btn_size = btn.get_size()

# btn_end_pos = btn_start_pos[0] + btn_size[0], btn_start_pos[1] + btn_size[1]

def surfaces_update():
    main_surface = screen
    main_surface.blit(grid_surface, (50,50))
    grid_surface.fill(bgcolor)
    cursor_marker = DRAW_DATA['cursor_marker']
    x1 = cursor_marker[0][0] - 1
    y1 = cursor_marker[0][1] - 1
    grid_surface.blit(cursor_surface, (x1,y1))
    screen.blit(start_game_screen_surface, (0,0))
    start_game_screen_surface.blit(btn_surface, btn_start_pos)
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


def delete_duplicates(input_list):
    unique_list = list()
    for data in input_list:
        if data not in unique_list:
            unique_list.append(data)
    return unique_list


def check(tile, data):
    # Получаем диагонали
    left_diag = grid.get_line(0, 0, (tiles[0] - 1), (tiles[1] - 1))
    right_diag = grid.get_line((tiles[0] - 1), 0, 0, (tiles[1] - 1))

    horizontal_line = grid.get_line(0, tile[1], (tiles[0] - 1), tile[1])
    vertical_line = grid.get_line(tile[0], 0, tile[0], (tiles[0] - 1))

    #Все линии собрать в один список и проверить в цикле
    line_list = []

    line_list.append(right_diag)
    line_list.append(left_diag)
    line_list.append(horizontal_line)
    line_list.append(vertical_line)

    line_list = delete_duplicates(line_list)

    for line in line_list:
        if grid.check_line(line, data):
            print(f'Win: {line}')
            return True
    
    pass

# Двигаем курсор клавишами
def move_cursor(x,y):
    x, y = grid.validate_pos(x, y)
    cursor_marker = grid.norm_tiles_coord(x, y)
    grid.set_cursor_pos(x, y)
    grid.set_cursor_marker(cursor_marker)
    pass

# Получаем список игроков
def get_players():
    player_data = ['X','0']
    # Берем рандомное число 0 или 1 для первого игрока
    dice = random.randint(0, 1)

    # Вычисляем для второго игрока
    # Если для первого 1 то для второго 0 и наоборот

    if dice > 0:
        dice2 = dice - 1
    else:
        dice2 = dice + 1

    # Записываем все в список [['player1, 'X'], ['player2', '0']]

    game_list = [['player1', player_data[dice]],['player2', player_data[dice2]]]
    return game_list

# Получаем список с данными игроков(Возможно нужно убрать отсюда)
players = get_players()
player_index = 0

#Выполняем при выигрыше

def win_game(player):
    print(f'Player:{player[0]} Win game!')
    pass

#Ход игрока
def player_turn(pos):    
    # Отмечаем позицию
    global player_index

    mark = grid.mark_pos(pos[0],pos[1], players[player_index][1])

    if check(pos, players[player_index][1]):
        win_game(players[player_index])

    if mark:
        if player_index == 1:
            player_index -= 1
        else:
            player_index += 1
    pass

run = True
win = False
game_state = False


def get_start_game_screen():
    surfaces_update()
    print('!')

if not game_state:
    get_start_game_screen()
    
start_game = False

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
                move_cursor(norm_X - 1, norm_Y)
            elif event.key == pygame.K_RIGHT:
                move_cursor(norm_X + 1, norm_Y)
            elif event.key == pygame.K_UP:
                move_cursor(norm_X, norm_Y - 1)
            elif event.key == pygame.K_DOWN:
                move_cursor(norm_X,norm_Y + 1)
            elif event.key == pygame.K_SPACE:
                pass
           
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = [mouse_pos[0]-50, mouse_pos[1]-50]
            tile = grid.get_cursor(mouse_pos)

            if not win:
                player_turn(tile)
            
            mouse_pos = pygame.mouse.get_pos()
    
            start_game = btn.on_mouse_motion(btn_start_pos, mouse_pos)
            if start_game:
                print(True)
 

    draw_data()
    grid.update()       
    pygame.display.update()