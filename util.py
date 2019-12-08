import sys
import inspect
import heapq, random


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

    def get_action_value(self, action):
        return self.directions[action]

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

    def get_all_actions(self, grid):
        length = len(grid[0])
        legal_actions = []

        # before finding all possible actions, check if we have reached goal state
        if grid == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
            return legal_actions

        for i in range(length):
            for j in range(length):
                for action, (x, y) in self.directions.items():
                    if (0 <= x + i <= length - 1) and (0 <= y + j <= length - 1):
                        if grid[i + x][j + y] == 0 and action is not 'Nothing':
                            legal_actions.append(action)
                        elif action == 'Nothing':
                            pass

        return legal_actions

    def get_legal_actions(self):
        actions = []
        for action, (x,y) in self.directions.items():
            actions.append(action)

    def convert_to_list(self, state):
        grid = [[0] * 3 for _ in range(3)]
        index = 0

        for i in range(0, 3):
            for j in range(0, 3):
                grid[i][j] = state[index]
                index += 1

        return grid

    def try_action(self, grid, action):

        (x, y) = self.get_action_value(action)
        length = 3

        # attempt to move tile in the direction of the action
        for i in range(0, 3):
            for j in range(0, 3):
                if (0 <= x + i <= length - 1) and (0 <= y + j <= length - 1):
                    if grid[i + x][j + y] == 0:
                        tile = grid[i][j]
                        grid[i][j] = 0
                        grid[i+x][j+y] = tile

        return grid

    def flatten(self, grid):
        list = []

        for i in range(0,3):
            for j in range(0,3):
                list.append(grid[i][j])

        return tuple(list)

    def is_solvable(self, grid):
        inversions = 0

        # count the number of inversions to determine if the current
        # puzzle configuration can be solve
        # a puzzle can be solved if it has even number of inversions
        flatten_grid = self.flatten(grid)

        index = 0
        for i in range(0, 9):
            for j in range(index, 9):
                if flatten_grid[index] > flatten_grid[j] and flatten_grid[j] != 0:
                    inversions += 1
            index += 1

        return inversions % 2 == 0


class Container:
    """ This class will act as a container when calculating Q values
        It will provide a way to store Q values for the 5 possible actions
        in each state(Left, Right, Up, Down, Nothing)
    """

    def __init__(self, s):
        self.state = s
        # create a dictionary to hold values for each possible action
        self.action_list = Counter({'Up': 0, 'Down': 0, 'Left:': 0, 'Right': 0, 'Nothing': 0})

def flipCoin( p ):
    r = random.random()
    return r < p

class Counter(dict):
    """
    A counter keeps track of counts for a set of keys.

    The counter class is an extension of the standard python
    dictionary type.  It is specialized to have number values
    (integers or floats), and includes a handful of additional
    functions to ease the task of counting data.  In particular,
    all keys are defaulted to have value 0.  Using a dictionary:

    a = {}
    print a['test']

    would give an error, while the Counter class analogue:

    >>> a = Counter()
    >>> print a['test']
    0

    returns the default 0 value. Note that to reference a key
    that you know is contained in the counter,
    you can still use the dictionary syntax:

    >>> a = Counter()
    >>> a['test'] = 2
    >>> print a['test']
    2

    This is very useful for counting things without initializing their counts,
    see for example:

    >>> a['blah'] += 1
    >>> print a['blah']
    1

    The counter also includes additional functionality useful in implementing
    the classifiers for this assignment.  Two counters can be added,
    subtracted or multiplied together.  See below for details.  They can
    also be normalized and their total count and arg max can be extracted.
    """
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def incrementAll(self, keys, count):
        """
        Increments all elements of keys by the same count.

        >>> a = Counter()
        >>> a.incrementAll(['one','two', 'three'], 1)
        >>> a['one']
        1
        >>> a['two']
        1
        """
        for key in keys:
            self[key] += count

    def argMax(self):
        """
        Returns the key with the highest value.
        """
        if len(self.keys()) == 0: return None
        all = self.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def sortedKeys(self):
        """
        Returns a list of keys sorted by their values.  Keys
        with the highest values will appear first.

        >>> a = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> a['third'] = 1
        >>> a.sortedKeys()
        ['second', 'third', 'first']
        """
        sortedItems = self.items()
        compare = lambda x, y:  sign(y[1] - x[1])
        sortedItems.sort(cmp=compare)
        return [x[0] for x in sortedItems]

    def totalCount(self):
        """
        Returns the sum of counts for all keys.
        """
        return sum(self.values())

    def normalize(self):
        """
        Edits the counter such that the total count of all
        keys sums to 1.  The ratio of counts for all keys
        will remain the same. Note that normalizing an empty
        Counter will result in an error.
        """
        total = float(self.totalCount())
        if total == 0: return
        for key in self.keys():
            self[key] = self[key] / total

    def divideAll(self, divisor):
        """
        Divides all counts by divisor
        """
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor

    def copy(self):
        """
        Returns a copy of the counter
        """
        return Counter(dict.copy(self))

    def __mul__(self, y ):
        """
        Multiplying two counters gives the dot product of their vectors where
        each unique label is a vector element.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['second'] = 5
        >>> a['third'] = 1.5
        >>> a['fourth'] = 2.5
        >>> a * b
        14
        """
        sum = 0
        x = self
        if len(x) > len(y):
            x,y = y,x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        """
        Adding another counter to a counter increments the current counter
        by the values stored in the second counter.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> a += b
        >>> a['first']
        1
        """
        for key, value in y.items():
            self[key] += value

    def __add__( self, y ):
        """
        Adding two counters gives a counter with the union of all keys and
        counts of the second added to counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a + b)['first']
        1
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] + y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = y[key]
        return addend

    def __sub__( self, y ):
        """
        Subtracting a counter from another gives a counter with the union of all keys and
        counts of the second subtracted from counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a - b)['first']
        -5
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] - y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = -1 * y[key]
        return addend
