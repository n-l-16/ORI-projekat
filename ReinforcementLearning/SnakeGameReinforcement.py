import time

import pygame
from snake_game_GUI import SnakeGameGUI, Color

speed = 10

class SnakeGameReinforcement(SnakeGameGUI):
    def __init__(self, is_training):
        SnakeGameGUI.__init__(self)
        self.visualization_active = is_training
        self.last_state = None
        self.last_action = None
        self.episode = 0.0
        self.state = self.get_state()
        self.move_history = []

    def run_game(self, agent):
        # self.food = self.rand_food()
        if not self.visualization_active:
            pygame.init()
            font = pygame.font.SysFont("monospace", 40)
            self.draw_board()
            pygame.display.update()
            exit_game_sign = False
        if not agent:
            pass
        else:
            agent.registerInitialState(self.state)
            while self.game_active:
                obs = agent.observationFunction(self.state, self.food, self.height, self.width)#proveri za state
                action = agent.getAction(obs)
                if action is None:
                    self.game_active = False
                    break
                self.update_vel(action)
                self.update_state()
                if not self.visualization_active:
                    time.sleep(1.0 / speed)
                    self.draw_board()
                    pygame.display.update()
                self.move_history.append(action)
                self.state = self.get_successor(action)
            print("GOTOVA PARTIJA")

            if not self.visualization_active:
                label = font.render("Game Over!", True, Color.RED)
                self.SCREEN.blit(label, (self.WIDTH + 10, 50))
                pygame.display.update()

                # da prozor ostane upaljen i kad se igra zavrsi
                while not exit_game_sign:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit_game_sign = True

                # pygame.quit()
            pygame.quit()

    def get_successor(self, action):
        next_snake = self.state[1].copy()
        next_snake = next_snake[:-1]
        next_head = self.get_next_position(action, self.state[0])
        next_snake.insert(0, next_head)
        next_state = (next_head, next_snake, action, self.score, self.food, self.height, self.width)
        return next_state
