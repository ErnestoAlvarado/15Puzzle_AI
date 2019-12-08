import mdp
import util


class ValueIterationAgent:

    def __init__(self, mdp, discount=0.5, iterations=10):
        # init value iteration agent

        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()

    def value_iteration(self):
        # set iteration counter to 0
        current_iteration = 0

        while current_iteration < self.iterations:
            # get states from mdp
            states = self.mdp.get_states()
            current_values = util.Counter()

            print(states)

            # go through each possible state and perform value iteration
            for s in states:
                # check if we have reached a terminal state
                if not self.mdp.is_goal_state(s):
                    action_values = util.Counter()
                    possible_actions = self.mdp.get_possible_actions(s)

                    for action in possible_actions:
                        action_values[action] = self.computeQValueFromValues(s, action)

                        current_values[s] = max(action_values.values())

            current_iteration += 1
            self.values = current_values.copy()

    def getValue(self, state):
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        transition_states = self.mdp.getTransitionStatesAndProbs(state, action)

        q_value = 0

        for (result_state, value) in transition_states:
            q_value += value * (self.mdp.getReward(state, action, result_state)
                                + (self.discount * self.values[result_state]))

        return q_value

    def computeActionFromValues(self, state):
        if self.mdp.is_goal_state(state):
            return None
        else:
            best_action = util.Counter()
            possible_actions = self.mdp.get_possible_actions(state)

            if len(possible_actions) == 0:
                return None

            for action in possible_actions:
                best_action[action] = self.computeQValueFromValues(state, action)

            return best_action.argMax()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
