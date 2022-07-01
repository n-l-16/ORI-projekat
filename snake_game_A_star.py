import csv
import time

from PriorityQueue import PriorityQueueWithFunction
from snake_game_GUI import SnakeGameGUI, Color
import pygame
import random
rand = random.Random()

statistic_files = {

    "h1_heuristic" : "a_star_scores_h1.csv",
    "h2_heuristic" : "a_star_scores_h2.csv",
    "h4_heuristic" : "a_star_scores_h4.csv",
    "h3_heuristic" : "a_star_scores_h3.csv"

}


class SnakeGameAStar(SnakeGameGUI):

    def __init__(self):
        super().__init__()


    def heuristic(self, head):
        x = self.food[0] - head[0]
        y = self.food[1] - head[1]
        heuristic = abs(x) + abs(y)
        # if self.is_blind_row(head):
        #     heuristic += 100
        # return np.sqrt(x ** 2 + y ** 2)  # heuristika h1
        return heuristic # heuristika h2


    def get_direction_from_event(self, event):
        direction = self.dir
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
                direction = self.dir
        return direction


    def run_game(self, player_ai=None):
        self.score = 0
        speed = 70
        direction = self.dir
        pygame.init()
        font = pygame.font.SysFont("monospace", 40)
        self.draw_board()
        pygame.display.update()
        exit_game_sign = False

        while exit_game_sign is False and self.game_active is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game_sign = True

                direction = self.get_direction_from_event(event)
                if direction not in self.directions:
                    self.game_active = False
                    break

            if self.game_active :
                if player_ai is not None:
                    directions = player_ai()
                    if len(directions) != 0:
                        for dir in directions:
                            self.update_vel(dir)
                            self.update_state()
                            if not self.game_active:
                                break
                            self.draw_board()
                            pygame.display.update()
                            time.sleep(1.0 / speed)
                    else:
                        self.game_active = False


        label = font.render("Game Over!", True, Color.RED)
        self.SCREEN.blit(label, (self.WIDTH + 10, 50))
        pygame.display.update()

        #da prozor ostane upaljen i kad se igra zavrsi
        while not exit_game_sign:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game_sign = True

        pygame.quit()
        return self.score

    def run_with_write(self, iteration):
        f = open(statistic_files["h3_heuristic"], 'a')
        writer = csv.writer(f)
        score = self.run_game(self.aStarSearch)
        writer.writerow([iteration, score])

    def aStarSearch(self):
        cost = lambda path: self.getCostOfActions() + self.heuristic(path[-1][0])
        priorityQueue = PriorityQueueWithFunction(cost)
        return self.generalSearch( priorityQueue)


    def generalSearch(self, data_structure):
        visited = []
        path = list()
        data_structure.push([self.get_start_state()])

        while not data_structure.isEmpty():
            path = data_structure.pop()
            current_head = path[-1][0]
            current_state = path[-1]

            if self.is_goal_state(current_state):
                return [state[2] for state in path][1:]

            if current_head not in visited:
                visited.append(current_head)

            for successor in self.get_successors(current_state):
                if successor[0] not in visited: #glava
                    successorPath = path[:]
                    successorPath.append(successor)
                    data_structure.push(successorPath)
        return []
