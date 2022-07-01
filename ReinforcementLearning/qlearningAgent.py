from ReinforcementLearning.Agent import ReinforcementAgent
import random
from ReinforcementLearning.Features import  SimpleExtractor


class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, epsilon=0.01, gamma=0.8, alpha=0.8, numTraining=0):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self)
        self.q_value = {}
        #[koordinata] : [vrednost, vrednost, vrednost, vrednost] ---('north', 'west', 'south', 'east')

        "*** YOUR CODE HERE ***"

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        if (state, action) in self.q_value:
            return self.q_value[(state, action)]
        else:
            return 0.0


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:
            return 0.0

        value = []
        for action in legalActions:
            value.append(self.getQValue(state, action))

        return max(value)

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:
            return None
        else:
            value = []
            for action in legalActions:
                value.append(self.getQValue(state, action))

            max_value = max(value)
            for action in legalActions:
                if self.getQValue(state, action) == max_value:
                    return action

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob) true/false
          HINT: To pick randomly from a list, use random.choice(list)
        """
        #TREBA DA MI VRATI NAPRED, LEVO ILI DESNO
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None

        if flip_coin(self.epsilon):
            if len(legalActions) > 0:
                action = random.choice(legalActions)
            else:
                action = self.computeActionFromQValues(state)
        else:
            action = self.computeActionFromQValues(state)

        "*** YOUR CODE HERE ***"

        return action

    def update(self, state, action, next_state, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #ovde vidi za next state treba da se mapira lepo u listi
        # OVO RACUNA PROCENU KOLIKO JE DOBAR TAJ POTEZ STATE, AKCIJA = BROJ
        #STATE SADZI TABELU TRENUTNU I SCORE
        self.q_value[(state, action)] = (1-self.alpha)*self.getQValue(state, action)+self.alpha*(reward + self.discount * self.getValue(next_state))


    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


def flip_coin(p):
    r = random.random()
    return r < p



class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.01, gamma=0.8, alpha=0.8, numTraining=0):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.numTraining = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, 0.05, 0.8, 0.2, numTraining)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, epsilon=0.01, gamma=0.8, alpha=0.8, numTraining=0):
        self.featExtractor = SimpleExtractor()

        PacmanQAgent.__init__(self, 0.05, 0.8, 0.2, numTraining)
        # self.weights = {"food": 100, "snake-size": 100, "walls": 250, "in-walls": 500, "in-tail": 300, "distance-food": 100}
        self.weights = {"food": 10, "snake-size": 5, "walls": -1, "in-walls": -100, "in-tail": -100,
                        "distance-food": 2}

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        qValue = 0.0
        features = self.featExtractor.getFeatures(state, action)
        for key in features.keys():
            qValue += (self.weights[key] * features[key])
            # print(qValue)
        return qValue

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        features = self.featExtractor.getFeatures(state, action)
        # print(reward)
        diff = self.alpha * ((reward + self.discount * self.getValue(nextState)) - self.getQValue(state, action))
        # print(diff)
        for feature in features.keys():
            self.weights[feature] = self.weights[feature] + diff * features[feature]
