# This file will handle all the logic for the 15 puzzle game

import pygame
import displayGrid as dp


class Game:
    """ This class will handle the game loop """

    def __init__(self, grid_size):

        self.grid = dp.Grid(grid_size)
        self.display = dp.DrawGrid(grid_size, self.grid.get_copy())

    def run(self):
        con = True
        clock = pygame.time.Clock()

        # game loop
        while con:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    con = False
                # when mouse is clicked, check coordinates to see if a tile was clicked
                if pygame.mouse.get_pressed()[0]:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()
                    tile = self.display.check_collision(mouse_x, mouse_y)

                    # attempt to move a tile when clicked
                    if tile != 0 and tile is not None:
                        # if a tile was moved successfully, update move counter, and check if we won
                        if self.grid.move_square(tile):
                            print("updated grid: ", self.grid.get_copy())
                            print("Moves: ", self.grid.get_num_moves())
                            self.display.move_square(tile, self.grid.get_copy())
                            if self.grid.check_goal_state():
                                pygame.QUIT

            pygame.display.flip()
            clock.tick(60)


if __name__ == '__main__':
    game = Game(3)
    game.run()
