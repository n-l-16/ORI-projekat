from ReinforcementLearning.Features import raise_not_defined


class Agent:
    def __init__(self, index=0):
        self.index = index

    def get_action(self, state):
        """
        Funkcija koja vraca mogucu akciju koja zmija moze da izvrsi - Left, Right, Up, Down
        """
        raise_not_defined()


class ValueEstimationAgent(Agent):

    def __init__(self, alpha=1.0, epsilon=0.05, gamma=0.8, numTraining = 10):
        """
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes
        """
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.discount = float(gamma)
        self.numTraining = int(numTraining)


    def get_Q_value(self, state, action):
        """
        Vraca Q(state,action)
        """
        raise_not_defined()

    def get_value(self, state):
        """
        Vraca V(s) = max_{a in actions} Q(s,a)
        """
        raise_not_defined()

    def get_policy(self, state):
        raise_not_defined()

    def get_action(self, state):
        raise_not_defined()

class ReinforcementAgent(ValueEstimationAgent):

    def update(self, state, action, next_state, reward):
        """
               Funkcija u kojoj se vrednost recnika azurira
        """
        raise_not_defined()

    def get_legal_actions(self, state):
        """
          moguce akcije iz trenutnog stanja
        """
        actions = []
        for action in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            next_head = self.get_next_position(action, state[0])
            if not self.is_collision(next_head, state[1]):
                actions.append(action)
        return actions

    def get_next_position(self, direction, head):
        new_head_x = head[0] + direction[0]
        new_head_y = head[1] + direction[1]
        new_head = [new_head_x, new_head_y]
        return new_head

    def is_collision(self, next_position, snake):
        if next_position[0] < 0 or next_position[0] >= 10:
            return True
        elif next_position[1] < 0 or next_position[1] >= 10:
            return True
        elif next_position in snake[1:]:
            return True
        return False

    def observe_transition(self, state, action, next_state, delta_reward):
        self.episodeRewards += delta_reward
        self.update(state, action, next_state, delta_reward)

    def start_episode(self):
        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0

    def stop_episode(self):
        if self.episodesSoFar < self.numTraining:
            self.accumTrainRewards += self.episodeRewards
        else:
            self.accumTestRewards += self.episodeRewards
        self.episodesSoFar += 1
        if self.episodesSoFar >= self.numTraining:
            # Take off the training wheels
            self.epsilon = 0.0    # no exploration
            self.alpha = 0.0      # no learning

    def is_in_training(self):
        return self.episodesSoFar < self.numTraining

    def is_in_testing(self):
        return not self.is_in_training()

    def __init__(self, actionFn = None, numTraining=9990, epsilon=0.5, alpha=0.5, gamma=0.8):
        """
        actionFn: Function which takes a state and returns the list of legal actions

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes
        """
        if actionFn == None:
            actionFn = lambda state: state.get_legal_actions()
        self.actionFn = actionFn
        self.episodesSoFar = 0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    def set_learning_rate(self, alpha):
        self.alpha = alpha

    def set_discount(self, discount):
        self.discount = discount

    def do_action(self, state, action):
        self.lastState = state
        self.lastAction = action

    def observation_function(self, state, food, height, width):
        if not self.lastState is None:
            reward = state[3] - self.lastState[3] + self.score_change(state)
            self.observe_transition(self.lastState, self.lastAction, state, reward)
        return state

    def score_change(self, state):
        food = state[4]
        height = state[5]
        width = state[6]

        score = 0

        if state[0][0] < 0 or state[0][0] >= height:
            score += -500
        elif state[0][1] < 0 or state[0][1] >= width:
            score += -500
        elif state[0][1] in state[1][1:]:
            score += -500

        x = food[0] - state[0][0]
        y = food[1] - state[0][1]
        if abs(x) + abs(y) != 0:
            score += (1/(abs(x) + abs(y)))*50

        score += len(state[1])*10
        if x == 0 and y == 0:
            score += 30

        if state[0][0] < 1 or state[0][0] >= height-1:
            score += -5
        elif state[0][1] < 1 or state[0][1] >= width-1:
            score += -5

        return score

    def register_initial_state(self, state):
        self.start_episode()
        if self.episodesSoFar == 0:
            print('Beginning %d episodes of Training' % (self.numTraining))
