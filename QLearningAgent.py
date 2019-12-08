import util
import random
import collections as co


class QLearning:

    def __init__(self, *args):
        self.alpha = 0.2
        self.epsilon = 0.5
        self.gamma = 0.8
        self.grid_list = []
        self.action = util.Actions()
        self.q_values = co.Counter()

        if len(args) == 1:
            self.q_values = args[0]

    def get_q_value(self, state, action):
        # check if we have seen current state
        if self.q_values[(state, action)] == 0:
            return 0
        else:
            return self.q_values[(state, action)]

    def compute_value_from_q_value(self, state):

        state_list = self.action.convert_to_list(state)
        possible_actions = self.action.get_all_actions(state_list)
        max_action = []

        if len(possible_actions) == 0:
            return 0
        else:
            for action in possible_actions:
                max_action.append(self.get_q_value(state, action))

            max_value = max(max_action)

            return max_value

    def compute_action_from_q_value(self, state):
        # get a list of all the actions the agent can take
        # this does not consider actions that are illegal
        legal_actions = self.action.get_legal_actions()

        # compute the list of possible actions
        possible_actions = self.action.get_all_actions(self.action.convert_to_list(state))

        # create a counter object to store possible actions
        best_action = co.Counter()

        if len(possible_actions) == 0:
            return 'Nothing'

        else:
            # find best action for current state
            for action in possible_actions:
                best_action[state, action] = self.get_q_value(state, action)

            action_value = []

            for action in best_action:
                # check to see if current action is the best action available
                if best_action[action] == best_action[max(best_action)]:
                    action_value.append(action)

            (current_state, action) = random.choice(action_value)

        return action

    def get_action(self, state):
        possible_actions = self.action.get_all_actions(self.action.convert_to_list(state))

        # if we have reached a goal state, then there is nothing left to do
        if util.flipCoin(self.epsilon) and possible_actions != []:
            return random.choice(possible_actions)
        else:
            return self.compute_action_from_q_value(state)

    def update_values(self, state, action, next_state, reward):
        # update values after transition
        current_value = self.q_values[(state, action)]

        current_reward = 0
        # check if current state reaches goal state with taking action
        # if goal state is reached, then add reward to value, else subtract 1
        if next_state == (1, 2, 3, 4, 5, 6, 7, 8, 0):
            current_reward = 1

        self.q_values[(state, action)] = (current_value * (1 - self.alpha)) + (self.alpha * (current_reward + self.compute_value_from_q_value(next_state)))

    def get_policy(self, state):
        return self.compute_action_from_q_value(state)

    def get_value(self, state):
        return self.compute_value_from_q_value(state)

    def show_values(self):
        return self.q_values
