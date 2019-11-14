# This file will handle all the updates on the grid when the player or AI is playing

import pygame

# initialize pygame
pygame.init()


class LoadAssets:
    """ This class will load in all the assets needed for the game """

    def load_images(self):
        raise NotImplementedError

class DrawGrid:
    """ This class will create the playable grid, and update the squares when the player
        makes a move, or the AI
    """

    def __init__(self):
        raise NotImplementedError

    def move_square(self):
        raise NotImplementedError

    def draw_board(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError


class Grid:
    """ This class will create a 2-D array to handle the tiles """

    def __init__(self):
        raise NotImplementedError

    def move_square(self):
        raise NotImplementedError

    def search_empty_square(self):
        raise NotImplementedError

    def shuffle(self):
        raise NotImplementedError

