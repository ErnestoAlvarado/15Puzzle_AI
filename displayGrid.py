# This file will handle all the updates on the grid when the player or AI is playing

import pygame
import random

# initialize pygame
pygame.init()

# window dimensions
screen_width = 900
screen_height = 700
tile_path = 'Assets//Number_Blocks_01//'


class LoadAssets:
    """ This class will load in all the assets needed for the game """

    def load_images(self):
        raise NotImplementedError


class Tile(pygame.sprite.Sprite):
    """ Container used to hold individual tiles """

    def __init__(self, tile_sprite):
        # initialize parent Sprite constructor
        pygame.sprite.Sprite.__init__(self)

        # create surface for tile
        # background color set to white
        self.image = pygame.Surface([32, 32])

        # load in tile image
        self.image = tile_sprite.convert_alpha()

        # grab rectangle object that holds tile sprite
        self.rect = self.image.get_rect()


class DrawGrid:
    """ This class will create the playable grid, and update the squares when the player
        makes a move, or the AI
    """

    def __init__(self):
        # create screen
        self.screen = pygame.display.set_mode([screen_width, screen_height])

    def move_square(self):
        raise NotImplementedError

    def draw_board(self):
        raise NotImplementedError

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


if __name__ == '__main__':
    DrawGrid()
