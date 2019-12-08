
class MarkovDecisionProcess:

    def __init__(self, grid):
        self.grid = grid

    def get_states(self):
        # return all states in the grid
        states = []
        length = len(self.grid[0])
        for i in range(length):
            for j in range(length):
                states.append((i, j))

        return states

    def get_reward(self, state):
        # get reward
        raise NotImplementedError

    def get_start_state(self):
        # return start state of mdp
        raise NotImplementedError

    def get_possible_actions(self, state):
        # get a list of legal actions in current state
        return []

    def is_goal_state(self, state):
        # check if current state has reached goal state
        return False
