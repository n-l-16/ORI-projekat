import numpy as np
import random

rand = random.Random()


class SnakeGame:
    
    def __init__(self):
        self.game_active = True
        self.height = 10
        self.width = 10
        self.size = [self.height, self.width]
        self.board = np.zeros(self.size)
        self.score = 0
        self.head = [self.height//2, self.width//2]
        self.directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        self.dir = rand.choice(self.directions)
        self.snake = [[self.head[0] - i * self.dir[0], self.head[1] - i * self.dir[1]] for i in range(3)]
        self.food = self.rand_food()
        self.draw_initial_board()

    def draw_initial_board(self):
        for body_elem in self.snake:
            self.board[body_elem[0], body_elem[1]] = 1
        self.board[self.head[0], self.head[1]] = 2

        self.board[self.food[0], self.food[1]] = -1

    def rand_food(self):
        empty_spaces = [[i, j] for i in range(self.height) for j in range(self.width) if self.board[i, j] == 0]
        return rand.choices(empty_spaces)[0]
    
    def update_vel(self, vel):
        temp_head = [self.head[0] + vel[0], self.head[1] + vel[1]]
        if temp_head != self.snake[1]:  # make sure it's not previous body part
            self.dir = vel

    def update_state(self):
        self.head[0] += self.dir[0]
        self.head[1] += self.dir[1]

        if self.is_end_game():
            self.game_active = False
        elif self.head not in self.snake:  # ispravno pomeranje
            if self.head == self.food:  # jede hranu
                self.score += 1
                self.move_head()
                self.food = self.rand_food()
                self.board[self.food[0], self.food[1]] = -1
            else:  # obicno pomeranje
                self.move_head()
                rem = self.snake.pop()
                self.board[rem[0], rem[1]] = 0
        else:
            self.head = self.snake[0].copy()  # neispravan potez, ne pomera se zmija

    def move_head(self):
        self.snake.insert(0, self.head.copy())
        self.board[self.snake[1][0], self.snake[1][1]] = 1
        self.board[self.head[0], self.head[1]] = 2

    def is_end_game(self):
        if self.head[0] < 0 or self.head[0] >= self.height:  # udarac u zid
            return True
        elif self.head[1] < 0 or self.head[1] >= self.width:  # udarac u zid
            return True
        elif self.head in self.snake[2::]:  # udarac u svoje teleo
            return True
        return False

    def get_start_state(self):
        return self.head

    def is_goal_state(self):
        return self.head[0] == self.food[0] and self.head[1] == self.food[1]

    def get_successors(self, new_head):
        successors = []
        for direction in self.directions:
            next_position = self.get_next_position(direction, new_head)
            if not self.is_collision(next_position):
                successors.append(next_position)

        return successors

    def is_collision(self, next_position):
        if next_position[0] < 0 or next_position[0] >= self.height:
            return True
        elif next_position[1] < 0 or next_position[1] >= self.width:
            return True
        elif next_position in self.snake:

            return True
        return False

    def get_next_position(self, direction, head):
        new_head_x = head[0] + direction[0]
        new_head_y = head[1] + direction[1]
        new_head = [new_head_x, new_head_y]
        return new_head

    def getCostOfActions(self):
        return 1
