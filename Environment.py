from displayGrid import Grid
from mdp import MarkovDecisionProcess
from valueIteration import ValueIterationAgent
from QLearningAgent import QLearning
import itertools
from util import Actions
import time
import collections as co
import json
import random
import pickle


class PuzzleEnvironment:
    """ This file will keep track of the environment and make
        necessary calls to grid class to update puzzle
    """

    def __init__(self):
        # create initial random playable grid
        self.grid = Grid(3)
        self.mdp = MarkovDecisionProcess(self.grid.get_copy())

        # initialize value iteration agent and q-learning agent
        self.value_iteration_agent = ValueIterationAgent(self.mdp)
        self.q_agent = QLearning()

        # transition gets reward of 1 if we reach goal state
        self.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

        # number of episodes used to train agent
        self.episodes = 100
        self.reward = -1

        self.action = Actions()
        # create list with all possible states
        self.grid_list = []
        grid = self.grid.get_copy()

        for i in range(0, 3):
            for j in range(0, 3):
                self.grid_list.append(grid[i][j])
        self.all_states = list(itertools.permutations(self.grid_list))

    def test_inverse(self):
        solve = self.grid.is_solvable()
        while not solve:
            self.grid.shuffle(3)
            solve = self.grid.is_solvable()

    def write_to_file(self, values):
        with open('Qvalues', 'wb') as file:
            pickle.dump(values, file)

    def train(self):

        total_actions = 0

        # train for 10 episodes and observe result
        for i in range(0, 1000):
            converge = False
            # a random starting point will be chosen
            # only constraint will be that the random state must have even number of inversions
            state = random.choice(self.all_states)

            state_list = self.action.convert_to_list(state)

            valid = False
            while not valid:
                if self.action.is_solvable(state_list) and state_list[-1][-1] == 0:
                    valid = True
                else:
                    state_list = self.action.convert_to_list(random.choice(self.all_states))

            state = self.action.flatten(state_list)

            print("Grid in training: ", state_list)
            while not converge:

                # get the current best action for current state
                action = self.q_agent.get_action(state)

                # convert tuple into list to attempt to move tile
                grid = self.action.convert_to_list(state)
                grid_list = self.action.try_action(grid, action)

                # convert list into tuple to show next state
                next_state = self.action.flatten(grid_list)

                self.q_agent.update_values(state, action, next_state, self.reward)

                state = next_state
                total_actions += 1
                if state == self.goal_state:
                    converge = True

            values = self.q_agent.show_values()
            print("Done with episode: ", i)

        # save contents of value matrix to file in case of error
        self.write_to_file(values)

    def find_solution(self):
        # load Q values
        with open('Qvalues', 'rb') as file:
            values = pickle.load(file)

        agent = QLearning(values)

        val = agent.show_values()

        for (s, a) in val:
            if val[(s, a)] > 0:
                print("prev state: ", (s,a))
                print("Found a good value", val[(s, a)])
        # before attempting to find solution, check if puzzle configuration is solvable
        # if number of inverses is even, then it can be solved, otherwise make new puzzle
        self.test_inverse()

        average = []

        # solve 100 puzzles
        for i in range(0, 10):
            print("Solving: ", self.grid.get_copy())
            while not self.grid.check_goal_state():
                # turn grid into tuple to check for best action
                current_state = self.action.flatten(self.grid.get_copy())

                # get action with highest value from our q_value list
                best_action = agent.get_action(current_state)

                # apply action to current grid
                self.grid.try_action(best_action)

            print("Move count: ", self.grid.get_num_moves())
            average.append(self.grid.get_num_moves())
            print("Final puzzle: ", self.grid.get_copy())
            self.grid.shuffle(3)
            self.test_inverse()

        sum = 0
        for moves in average:
            sum += moves
        print("average: ", sum / len(average))

    def solvePuzzle(self):
        # create copy of grid after it is randomly shuffled
        s = self.grid.get_copy()

        # create two lists that will be used to solve the 8 puzzle
        g_set = set([])
        r_set = set([])

        # iterate from 1 to 8 and attempt to solve the 8 puzzle
        for i in range(1, 9):
            g_set = set([i])
            r_set = set([x for x in range(1, i+1)])

            # perform value iteration
            self.value_iteration_agent.value_iteration()
            values = self.value_iteration_agent.getValue((0, 0))

            while values == 0:
                g_set.add(max(r_set))
                r_set.remove(max(r_set))

                # perform value iteration again
                self.value_iteration_agent.value_iteration()
                values = self.value_iteration_agent.getValue((0, 0))

            # solve puzzle for g(i)_set and r(i)_set
