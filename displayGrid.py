# This file will handle all the updates on the grid when the player or AI is playing

import pygame
import random
import util

# initialize pygame
pygame.init()

# path  names for tile set
tile_path = 'Assets//Number_Blocks_01//'
tile_name = 'Number_Blocks_01_Set_1_128x128_'


class LoadAssets:
    """ This class will load in all the assets needed for the game """

    def __init__(self):
        self.tiles = []
        self.tiles.append(pygame.image.load(tile_path + 'Empty_Block_128x128.png'))

        for i in range(1, 9):
            tile_sprite = pygame.image.load(tile_path + tile_name + str(i) + '.png')
            self.tiles.append(tile_sprite)

    def load_images(self, index):
        return self.tiles[index]


class Tile(pygame.sprite.Sprite):
    """ Container used to hold individual tiles """

    def __init__(self, tile_sprite, x, y, num):
        # initialize parent Sprite constructor
        pygame.sprite.Sprite.__init__(self)

        # keep track of number assigned to this tile
        self.number = num

        # create surface for tile
        self.image = pygame.Surface([64, 64])

        # load in tile image
        self.image = tile_sprite.convert_alpha()

        # grab rectangle object that holds tile sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, x, y):
        # update x and y coordinate when a tile moves

        diff_x = self.rect.x - x
        diff_y = self.rect.y - y

        if diff_x < 0 or diff_x > 0 or diff_y < 0 or diff_y > 0:
            if diff_x < 0:
                self.rect = self.rect.move(1, 0)
                diff_x += 1
            elif diff_x > 0:
                self.rect = self.rect.move(-1, 0)
                diff_x += -1
            elif diff_y < 0:
                self.rect = self.rect.move(0, 1)
                diff_y += 1
            elif diff_y > 0:
                self.rect = self.rect.move(0, -1)
                diff_y += -1

    def get_number(self):
        return self.number

    def get_coord(self):
        return self.rect.x, self.rect.y


# function used to create window to show grid
def window(width, height):
    # create a window based on the number of tiles that will be used
    screen = pygame.display.set_mode([width, height])
    screen.fill((255, 255, 255))
    return screen


class DrawGrid:
    """ This class will create the playable grid, and update the squares when the player
        makes a move, or the AI
    """

    def __init__(self, size, grid_array):
        # create screen
        self.border_width = 5
        self.screen_width = size * 128 + self.border_width * 4
        self.screen_height = self.screen_width + (self.screen_width // self.border_width)
        self.screen = window(self.screen_width, self.screen_height)
        self.screen.fill((255, 255, 255))

        # create list to hold all tiles
        self.tile_list = pygame.sprite.Group()
        self.assets = LoadAssets()
        self.grid = grid_array

        # create grid along with the border and load in the tiles
        self.draw_board()
        self.draw_tiles(size)
        self.tile_list.draw(self.screen)

    def move_square(self, tile_number, grid):

        # tile and empty and used to represent
        # the tile that is about to be moved and the empty space
        tile = self.find_tile(tile_number)
        empty = self.find_tile(0)

        # get the coordinates of the tile that was clicked on along with the empty space
        empty_x, empty_y = empty.get_coord()
        tx, ty = tile.get_coord()

        # continue to move the tile until it is now where the empty space was located
        # empty tile will move in the opposite direction to fill in space of the tile that was moved
        while tile.get_coord() != (empty_x, empty_y):
            delay = pygame.time.get_ticks() / 1000
            while delay > 0:
                delay -= 1
                tile.move(empty_x, empty_y)
                empty.move(tx, ty)
                self.update_grid(grid)

    def find_tile(self, tile_number):
        # return reference to tile you are searching for
        for tile in self.tile_list:
            if tile.get_number() == tile_number:
                return tile

    def update_grid(self, grid):
        # this will be called when a tile is moved successfully
        # when a tile is moved, refresh the screen and load all assets again
        self.screen.fill((255, 255, 255))
        self.draw_board()
        self.tile_list.draw(self.screen)

    def check_collision(self, mouse_x, mouse_y):
        # determine which tile was clicked on
        for tile in self.tile_list:
            if tile.rect.collidepoint((mouse_x, mouse_y)):
                return tile.get_number()

    def draw_board(self):
        # create the borders of the grid
        top_border = (0, 0, self.screen_width, self.border_width)
        left_border = (0, 0, self.border_width, self.screen_width)
        right_border = (self.screen_width - self.border_width, 0, self.border_width, self.screen_width)
        bottom_border = (0, self.screen_width - self.border_width, self.screen_width, self.border_width)

        pygame.draw.rect(self.screen, (150, 150, 150), top_border)
        pygame.draw.rect(self.screen, (150, 150, 150), right_border)
        pygame.draw.rect(self.screen, (150, 150, 150), bottom_border)
        pygame.draw.rect(self.screen, (150, 150, 150), left_border)

    def draw_tiles(self, size):
        # draw tiles in correct location
        x = self.border_width
        y = self.border_width

        # go through 2-D array and draw tile based on arrangement
        # each tile is of size 128, so that is added to the x-coordinate of each tile
        for i in range(size):
            for j in range(size):
                tile_number = self.grid[i][j]
                self.tile_list.add(Tile(self.assets.load_images(tile_number), x, y, tile_number))
                x += 128 + self.border_width
            y += 128 + self.border_width
            x = self.border_width


class Grid:
    """ This class will create a 2-D array to handle the tiles """

    def __init__(self, size, *args):
        # create a 2-D array to hold the tiles
        self.grid_size = size * size
        self.grid = [[0]*size for _ in range(size)]
        self.goal_grid = [[0]*size for _ in range(size)]

        # variable to keep track of number of moves made
        self.moves_count = 0

        # create list of tiles based on size of grid
        self.tiles = [i for i in range(1, self.grid_size)]
        copy_tiles = self.tiles.copy()
        copy_tiles.append(0)
        num = 0

        # fill 2-D array with win condition
        for i in range(size):
            for j in range(size):
                self.goal_grid[i][j] = copy_tiles[num]
                num += 1

        # randomly shuffle tiles
        if len(args) == 1:
            self.grid = args[0]
        else:
            self.shuffle(size)
        self.tile_actions = util.Actions()

    def move_square(self, tile_number):
        tile_moved = False

        # check if the tile can be moved
        possible_action = self.tile_actions.get_actions(self.grid, tile_number)

        action, (x, y) = possible_action[0]

        if action != 'Nothing':
            i, j = self.get_index(tile_number)
            self.grid[i][j] = 0
            self.grid[i + x][j + y] = tile_number
            self.moves_count += 1
            tile_moved = True

        return tile_moved

    def try_action(self, action):

        (x, y) = self.tile_actions.get_action_value(action)
        length = 3

        # attempt to move tile in the direction of the action
        for i in range(0, 3):
            for j in range(0, 3):
                if (0 <= x + i <= length - 1) and (0 <= y + j <= length - 1):
                    if self.grid[i + x][j + y] == 0:
                        tile = self.grid[i][j]
                        self.grid[i][j] = 0
                        self.grid[i+x][j+y] = tile
                        self.moves_count += 1

    def get_index(self, tile_number):
        # return current index of tile
        for i in range(len(self.grid[0])):
            for j in range(len(self.grid[0])):
                if tile_number == self.grid[i][j]:
                    return i, j

    def get_tile(self, tile_index):
        # return tile value located in tile_index tuple
        (x, y) = tile_index
        return self.grid[x][y]

    def shuffle(self, size):
        # randomly shuffle tiles and ensure that goal state is not reached accidentally
        tile_list = self.tiles.copy()
        random.shuffle(tile_list)

        # add a 0 to the end of list to indicate empty space
        tile_list.append(0)
        c = 0

        self.moves_count = 0
        # fill 2-D array with tiles that have been shuffled
        for i in range(size):
            for j in range(size):
                self.grid[i][j] = tile_list[c]
                c += 1

    def is_solvable(self):
        inversions = 0

        # count the number of inversions to determine if the current
        # puzzle configuration can be solve
        # a puzzle can be solved if it has even number of inversions
        flatten_grid = self.tile_actions.flatten(self.grid.copy())

        index = 0
        for i in range(0,9):
            for j in range(index, 9):
                if flatten_grid[index] > flatten_grid[j] and flatten_grid[j] != 0:
                    inversions += 1
            index += 1

        return inversions % 2 == 0

    def custom_gird(self, grid):
        # manually change grid for testing purposes
        self.grid = grid

    def check_goal_state(self):
        return self.grid == self.goal_grid

    def get_copy(self):
        return self.grid.copy()

    def get_num_moves(self):
        return self.moves_count


