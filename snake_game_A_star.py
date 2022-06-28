from snake_game_GUI import SnakeGameGUI
import pygame
import time
import random
import numpy as np
rand = random.Random()


class SnakeGameAStar(SnakeGameGUI):

    def __init__(self, headless_mode=False):
        super().__init__(headless_mode)
        self.path2food = []
        self.food_found = False
        self.not_explored = []
        self.explored = []
        self.parents = dict()

    def check_food(self, position):
        if self.food[0] == position[0] and self.food[1] == position[1]:
            return True
        return False

    def heuristic(self, head):
        # sqrt food distance
        x = self.food[0] - head[0]
        y = self.food[1] - head[1]
        return np.sqrt(x ** 2 + y ** 2)

    def get_head(self, temp_head, move):
        new_head_x = temp_head[0] + move[0]
        new_head_y = temp_head[1] + move[1]
        new_head = [new_head_x, new_head_y]
        return new_head

    def get_safe_moves(self, current_head=None):
        moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        if current_head is None:
            current_head_orig = self.head.copy()
        else:
            current_head_orig = current_head.copy()

        moves = self.remove_unsafe_moves(moves, current_head_orig)
        return moves

    def remove_unsafe_moves(self, moves, current_head_orig):
        unsafe_moves = []

        for move in moves:
            next_head_position = self.get_head(current_head_orig, move)

            if self.is_collision(next_head_position):
                unsafe_moves.append(move)
            # if current_head[0] < 0 or current_head[0] >= self.height:
            #
            # elif current_head[1] < 0 or current_head[1] >= self.width:
            #     unsafe_moves.append(move)
            # elif current_head in self.snake:
            #     unsafe_moves.append(move)

        for move in unsafe_moves:
            moves.remove(move)

        return moves

    def a_star_explore_node(self, unexplored_position):
        self.explored.append(unexplored_position)
        moves = self.get_safe_moves(unexplored_position)

        for move in moves:
            new_head = self.get_head(unexplored_position, move)
            heuristic = self.heuristic(new_head)

            if str(new_head) not in self.parents.keys():
                self.parents[str(new_head)] = unexplored_position

            if new_head in self.explored:
                continue

            if self.check_food(new_head):
                self.food_found = True
                return

            if [heuristic, new_head] not in self.not_explored:
                self.not_explored.append([heuristic, new_head])
                self.not_explored.sort()


    def a_star_search(self, current_head=None):
        self.clear_collections()

        if current_head is None:
            current_head = self.head.copy()

        moves = self.get_safe_moves(current_head)

        for move in moves:
            new_head = self.get_head(current_head, move)
            heuristic = self.heuristic(new_head)

            if str(new_head) not in self.parents.keys():
                self.parents[str(new_head)] = current_head #pravac iz kog je dosao potez
            if self.check_food(new_head):
                return move
            else:
                self.not_explored.append([heuristic, new_head]) #not_explored su kao sukcesori
                self.not_explored.sort() #sorita se po heuristici, najmanja heuristika je prva tj najbiza hrani

        while len(self.not_explored) > 0:
            not_explored_node = self.not_explored.pop(0)
            self.a_star_explore_node(not_explored_node[1])
            if self.food_found:
                break

        if self.food_found:  # hrana je pronadjena, treba vratiti prvi potez koji vodi ka njoj
            position = self.food
            return self.get_next_move(position, current_head)
        elif len(self.explored) > 0: #nema direktnog puta do hrane
            position = self.explored[-1]  # last point
            return self.get_next_move(position, current_head)
        else:  # nema legalnih suseda
            #pokusati pronaci resenje za ovakve slucajeve
            return rand.choice(self.directions)

    def get_next_move(self, position, current_head):
        while self.parents[str(position)] != current_head:
            position = self.parents[str(position)]
        return [position[0] - current_head[0], position[1] - current_head[1]]


    def clear_collections(self):
        self.food_found = False
        self.not_explored = []
        self.explored = []
        self.parents = dict()

    def run_game(self, player_ai=None):
        update_rate = 1
        speed = 20
        counter = 0
        direction = self.vel
        pygame.init()
        my_font = pygame.font.SysFont("monospace", 40)
        self.draw_board()
        pygame.display.update()

        exit_flag = False
        while exit_flag is False and self.game_state is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = [-1, 0]
                    elif event.key == pygame.K_DOWN:
                        direction = [1, 0]
                    elif event.key == pygame.K_LEFT:
                        direction = [0, -1]
                    elif event.key == pygame.K_RIGHT:
                        direction = [0, 1]
                    else:
                        direction = self.vel

            time.sleep(1.0 / speed)
            counter += 1
            if counter >= update_rate:
                if player_ai is not None:
                    direction = player_ai()
                self.update_vel(direction)
                self.update_state()
                counter = 0
            self.draw_board()
            pygame.display.update()

        label = my_font.render("Game Over!", True, self.RED)
        self.SCREEN.blit(label, (self.WIDTH + 10, 50))
        pygame.display.update()

        #da prozor ostane upaljen i kad se igra zavrsi
        while not exit_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True
        pygame.quit()


def main():
    snake_game = SnakeGameAStar()
    snake_game.run_game(snake_game.a_star_search)

if __name__ == "__main__":
    main()
