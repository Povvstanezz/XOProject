class GameGrid:

    def __init__(self, surface_size=(300,300), tiles=(10,10), grid_size=(200,200)):
        self.SURFACE_SIZE = None
        self.GRID_SIZE = None
        self.LINES = None
        self.STEP_SIZE_X = None
        self.STEP_SIZE_Y = None
        self.START_X = None
        self.START_Y = None
        self.COORD_LINES_X = list()
        self.COORD_LINES_Y = list()
        self.TILES_COORD_LIST = list()
        self.SELECTED_TILES = list()
        self.CURSOR = [0,0]
        self.CURSOR_MARKER = list()
        self.GRID_DATA = dict()
        self.TILES = tiles
        self.GRID_SIZE = grid_size
        self.SURFACE_SIZE = surface_size
        self.TILES_DATA_LIST = list()

        self.clear_tiles_data_list()
        self.grid_calculate()   
        self.get_cursor(self.CURSOR)
        self.update()
        pass
    
    def clear_tiles_data_list(self):
        # (10, 10)
        for col in range(self.TILES[1]):
            x_list = ['empty' for i in range(self.TILES[0])]
            self.TILES_DATA_LIST.append(x_list)


    def grid_calculate(self):
        self.LINES = (self.TILES[0] + 1 , self.TILES[1] + 1)
        self.STEP_SIZE_X = self.GRID_SIZE[0]/(self.TILES[0])
        self.STEP_SIZE_Y = self.GRID_SIZE[1]/(self.TILES[1])

        grid_size_x, grid_size_y = self.GRID_SIZE

        self.START_X = self.SURFACE_SIZE[0]/2 - grid_size_x/2
        self.START_Y = self.SURFACE_SIZE[1]/2 - grid_size_y/2

        st_x, st_y = self.START_X, self.START_Y

        #Calculate lines
        for line in range(self.LINES[0]):
            self.COORD_LINES_X.append([st_x, self.START_Y, st_x , self.START_Y + grid_size_y])
            st_x += self.STEP_SIZE_X

        for line in range(self.LINES[1]):
            self.COORD_LINES_Y.append([self.START_X, st_y, self.START_X + grid_size_x, st_y])
            st_y += self.STEP_SIZE_Y

        #Calculate tiles
        coord_list = []
        coord_list_x = []

        for line_x in self.COORD_LINES_X[:-1]:
            x = line_x[0]
            for line_y in self.COORD_LINES_Y[:-1]:
                y = line_y[1]
                coord_list_x.append( [[x+1, y + 1],
                        [x + self.STEP_SIZE_X - 1, y + 1],
                        [x + self.STEP_SIZE_X - 1, y + self.STEP_SIZE_Y - 1],
                        [x + 1, y + self.STEP_SIZE_Y - 1]])

            coord_list.append(coord_list_x)
            coord_list_x = []

        self.TILES_COORD_LIST = coord_list

    def get_lines(self):
        lines_data = self.COORD_LINES_X + self.COORD_LINES_Y
        return lines_data
    
    def get_lines_x(self):
        return self.COORD_LINES_X
    
    def get_lines_y(self):
        return self.COORD_LINES_Y
    
    def get_tiles(self):
        tiles_data = self.TILES_COORD_LIST
        return self.TILES_COORD_LIST
    
    
    def get_line(self, start_x, start_y, end_x, end_y):
        tiles_list = [[start_x, start_y]]

        start_x, start_y = self.validate_pos(start_x, start_y)
        end_x, end_y = self.validate_pos(end_x, end_y)
        loop = True

        while loop:

            dir_x = -1 if start_x > end_x else 1
            dir_y = -1 if start_y > end_y else 1

            if start_x != end_x:
                start_x += dir_x

            if start_y != end_y:
                    start_y += dir_y

            if start_x == end_x and start_y == end_y:
                loop = False

            tiles_list.append([start_x, start_y])

            # self.SELECTED_TILES.append(self.norm_tiles_coord(start_x, start_y))

        return tiles_list


    def validate_pos(self, x,y):
        if x >= self.TILES[0]:
            x = self.TILES[0]-1
        elif x < 0:
            x = 0

        if y >= self.TILES[1]:
            y = self.TILES[1]-1
        elif y < 0:
            y = 0
        
        return x,y        

    def norm_tiles_coord(self, x,y):
        tiles = self.get_tiles()
        tile = tiles[x][y]
        return tile
    
    def set_cursor_pos(self, x,y):
        self.CURSOR = [x, y]

    def set_cursor_marker(self, tile):
        self.CURSOR_MARKER = tile
    
    def get_cursor(self, pos):
        x, y = pos
        lines_x = self.get_lines_x()
        lines_y = self.get_lines_y()
        loc_x, loc_y = 0,0

        for line_y in lines_y[:-1]:
            if y > line_y[1] and y > lines_y[0][1]:
                loc_y = lines_y.index(line_y)

        for line_x in lines_x[:-1]:
            if x > line_x[0] and x > lines_x[0][0]:
                loc_x = lines_x.index(line_x)

        self.CURSOR = [loc_x, loc_y]
        tiles = self.get_tiles()

        self.CURSOR_MARKER = tiles[loc_x][loc_y]
        return [loc_x, loc_y]
    
    def select_tile(self, x,y):
        tiles = self.get_tiles()
        if tiles[x][y] in self.SELECTED_TILES:
            pass
        else:
            self.CURSOR_TILE[0](tiles[x][y])

    def mark_pos(self, x, y, data):
        x,y = self.validate_pos(x,y)
        if self.TILES_DATA_LIST[x][y] != 'empty':
            pass
        else:
            self.TILES_DATA_LIST[x][y] = data
    
    def get_tiles_data(self):
        return self.TILES_DATA_LIST

    def select_grid_tile(self):
        x, y = self.CURSOR
        tile = self.norm_tiles_coord(x ,y)
        if tile in self.SELECTED_TILES:
            self.SELECTED_TILES.remove(tile)
        else:
            self.SELECTED_TILES.append(tile)
        pass
    

    # Проверяем позиции на data
    # Если все позиции в tiles с одной data то возвращает True иначе False
    def check_line(self, tiles, data):
        count = 0
        for tile in tiles:
            if self.TILES_DATA_LIST[tile[0]][tile[1]] == data:
                continue
            else:
                return False

        return True
        
    def update(self):
        self.GRID_DATA.update({'lines': self.COORD_LINES_X + self.COORD_LINES_Y})
        self.GRID_DATA.update({'cursor': self.CURSOR})
        self.GRID_DATA.update({'cursor_marker': self.CURSOR_MARKER})
        self.GRID_DATA.update({'selected_tiles': self.SELECTED_TILES})
        self.GRID_DATA.update({'tiles_grid_data': self.TILES_DATA_LIST})

        return self.GRID_DATA
    
    def __str__(self):
        return f'Grid data: TILES={self.TILES}, GRID_SIZE={self.GRID_SIZE}'
    
if __name__ == '__main__':
    grid = GameGrid()
    grid.update()