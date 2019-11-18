
class Directions:

    # set up directions the AI will be able to take
    Right = 'Right'
    Left = 'Left'
    Down = 'Down'
    Up = 'Up'
    Nothing = 'Nothing'


class Actions:

    def __init__(self):
        self.directions = {Directions.Right: (0, 1), Directions.Left: (0, -1), Directions.Up: (-1, 0),
                           Directions.Down: (1, 0), Directions.Nothing: (0, 0)}

    def get_actions(self, grid, tile_number):
        possible_actions = []

        length = len(grid[0])

        # go through grid and determine which actions a tile can take
        for i in range(length):
            for j in range(length):
                if grid[i][j] == tile_number:
                    for action, (x, y) in self.directions.items():
                        if (0 <= x + i <= length - 1) and (0 <= y + j <= length - 1):
                            if grid[i + x][j + y] == 0:
                                possible_actions.append((action, (x, y)))
                            elif action == 'Nothing':
                                possible_actions.append((action, (x, y)))

        return possible_actions
