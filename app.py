import pygame

from GameGrid import GameGrid

pygame.init()

screen = pygame.display.set_mode((640,480))
bgcolor = (207, 235, 52)
tiles = (10, 10)

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
        pygame.draw.polygon(grid_surface, (120, 129, 159), (tile[0],tile[1],tile[2], tile[3]))

def draw_cursor():
    pygame.draw.polygon(grid_surface, (120,120,102), DRAW_DATA['cursor_marker'])

run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        draw_lines(DRAW_DATA['lines'])
        select_tiles()
        screen.blit(grid_surface, (0,0))
        grid_surface.fill(bgcolor)

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
                grid.select_grid_tile()
            elif event.key == pygame.K_LSHIFT:
                grid.get_line(0,0,9,0)
                grid.get_line(0,0,0,9)
                grid.get_line(0,0,9,9)
                grid.get_line(9,0,9,9)
                grid.get_line(0,9,9,0)

            
            norm_X, norm_Y = grid.validate_pos(norm_X, norm_Y)
            cursor_marker = grid.norm_tiles_coord(norm_X, norm_Y)
            grid.set_cursor_pos(norm_X, norm_Y)
            grid.set_cursor_marker(cursor_marker)
    
    grid.update()
    draw_cursor()
    pygame.display.update()