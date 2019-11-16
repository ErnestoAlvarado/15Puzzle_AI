# This file will handle all the updates on the grid when the player or AI is playing

import pygame
import random

# initialize pygame
pygame.init()

# path  names for tile set
tile_path = 'Assets//Number_Blocks_01//'
tile_name = 'Number_Blocks_01_Set_1_128x128_'


class LoadAssets:
    """ This class will load in all the assets needed for the game """

    def __init__(self):
        self.tiles = []

        for i in range(1, 9):
            tile_sprite = pygame.image.load(tile_path + tile_name + str(i) + '.png')
            self.tiles.append(tile_sprite)
        print(self.tiles)

    def load_images(self, index):
        return self.tiles[index]


class Tile(pygame.sprite.Sprite):
    """ Container used to hold individual tiles """

    def __init__(self, tile_sprite, x, y):
        # initialize parent Sprite constructor
        pygame.sprite.Sprite.__init__(self)

        # create surface for tile
        # background color set to white
        self.image = pygame.Surface([64, 64])

        # load in tile image
        self.image = tile_sprite.convert_alpha()

        # grab rectangle object that holds tile sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, x, y):
        # update x and y coordinate when a tile moves
        self.rect.x = x
        self.rect.y = y


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

        # create list to hold all tiles
        self.tile_list = pygame.sprite.Group()
        self.assets = LoadAssets()

        self.draw_board()
        self.draw_tiles(size, grid_array)
        con = True
        clock = pygame.time.Clock()

        while con:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    con = False

            pygame.display.flip()
            self.tile_list.draw(self.screen)
            clock.tick(60)

    def move_square(self):
        raise NotImplementedError

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

    def draw_tiles(self, size, grid_array):
        # draw tiles in correct location
        x = self.border_width
        y = self.border_width

        # go through 2-D array and draw tile based on arrangement
        for i in range(size):
            for j in range(size):
                tile_number = grid_array[i][j]
                if tile_number != 0:
                    self.tile_list.add(Tile(self.assets.load_images(tile_number - 1), x, y))
                x += 128 + self.border_width
            y += 128 + self.border_width
            x = self.border_width

    def reset(self):
        raise NotImplementedError


class Grid:
    """ This class will create a 2-D array to handle the tiles """

    def __init__(self, size):
        # create a 2-D array to hold the tiles
        self.grid_size = size * size
        self.grid = [[0]*size for _ in range(size)]
        self.goal_grid = [[0]*size for _ in range(size)]

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
        self.shuffle(size)

    def move_square(self, tile_number):
        raise NotImplementedError

    def search_empty_square(self):
        raise NotImplementedError

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

        # fill 2-D array with tiles that have been shuffled
        for i in range(size):
            for j in range(size):
                self.grid[i][j] = tile_list[c]
                c += 1

    def check_goal_state(self):
        return self.grid == self.goal_grid

    def get_copy(self):
        return self.grid.copy()


if __name__ == '__main__':
    g = Grid(3)
    DrawGrid(3, g.get_copy())
