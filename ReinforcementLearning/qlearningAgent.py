from ReinforcementLearning.Agent import ReinforcementAgent
import random
from ReinforcementLearning.Features import  SimpleExtractor


class QLearningAgent(ReinforcementAgent):
    def __init__(self, epsilon=0.01, gamma=0.8, alpha=0.8, numTraining=0):
        ReinforcementAgent.__init__(self)
        self.q_value = {}

    def get_Q_value(self, state, action):
        if (state, action) in self.q_value:
            return self.q_value[(state, action)]
        else:
            return 0.0


    def compute_value_from_Q_values(self, state):
        legalActions = self.get_legal_actions(state)
        if len(legalActions) == 0:
            return 0.0

        value = []
        for action in legalActions:
            value.append(self.get_Q_value(state, action))

        return max(value)

    def compute_action_from_Q_values(self, state):
        legalActions = self.get_legal_actions(state)
        if len(legalActions) == 0:
            return None
        else:
            value = []
            for action in legalActions:
                value.append(self.get_Q_value(state, action))

            max_value = max(value)
            for action in legalActions:
                if self.get_Q_value(state, action) == max_value:
                    return action

    def get_action(self, state):
        legalActions = self.get_legal_actions(state)
        action = None

        if flip_coin(self.epsilon):
            if len(legalActions) > 0:
                action = random.choice(legalActions)
            else:
                action = self.compute_action_from_Q_values(state)
        else:
            action = self.compute_action_from_Q_values(state)
        return action

    def update(self, state, action, next_state, reward):
        self.q_value[(state, action)] = (1-self.alpha) * self.get_Q_value(state, action) + self.alpha * (reward + self.discount * self.get_value(next_state))


    def get_policy(self, state):
        return self.compute_action_from_Q_values(state)

    def get_value(self, state):
        return self.compute_value_from_Q_values(state)


def flip_coin(p):
    r = random.random()
    return r < p



class SnakeQAgent(QLearningAgent):
    def __init__(self, epsilon=0.01, gamma=0.8, alpha=0.8, numTraining=0):
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.numTraining = numTraining
        self.index = 0
        QLearningAgent.__init__(self, 0.05, 0.8, 0.2, numTraining)

    def get_action(self, state):
        action = QLearningAgent.get_action(self, state)
        self.do_action(state, action)
        return action


class ApproximateQAgent(SnakeQAgent):
    def __init__(self, epsilon=0.01, gamma=0.8, alpha=0.8, numTraining=0):
        self.featExtractor = SimpleExtractor()

        SnakeQAgent.__init__(self, 0.05, 0.8, 0.2, numTraining)
        self.weights = {"food": 10, "snake-size": 5, "walls": -1, "in-walls": -100, "in-tail": -100,
                        "distance-food": 2}

    def get_weights(self):
        return self.weights

    def get_Q_value(self, state, action):
        """
          Q(state,action) = w * featureVector
        """
        qValue = 0.0
        features = self.featExtractor.get_features(state, action)
        for key in features.keys():
            qValue += (self.weights[key] * features[key])
            # print(qValue)
        return qValue

    def update(self, state, action, next_state, reward):
        """
          Azuriranje i vrednosti iz recnika tezina
        """
        features = self.featExtractor.get_features(state, action)
        diff = self.alpha * ((reward + self.discount * self.get_value(next_state)) - self.get_Q_value(state, action))
        for feature in features.keys():
            self.weights[feature] = self.weights[feature] + diff * features[feature]
