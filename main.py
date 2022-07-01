from snake_game_A_star import SnakeGameAStar
from score_visualization.visualization import  *

class Color:
    GREEN = '\033[92m'
    END_GREEN = '\033[0m'
    BOLD = '\033[1m'
    BOLD_END = '\033[0m'


def run_a_star_algorithm(iteration=None):
    snake_game = SnakeGameAStar()
    snake_game.run_with_write(iteration) #ako hocemo upisivanje u fajl
    #snake_game.run_game(snake_game.aStarSearch)


def run_with_writing():
    for i in range(100):
        run_a_star_algorithm(i)
    plot_a_star_score('a_star_scores_h3.csv')


def run_reinforcement_learning():
    pass


def choose_algorithm():
    print("\n" + Color.GREEN + Color.BOLD + "Choose the algorithm for snake game" + Color.BOLD_END + Color.END_GREEN)
    print("1. --> A*  algorithm")
    print("2. --> Reinforcement learning")
    choice = ""
    while choice not in ["1", "2"]:
        choice = input(">>> ")
        if choice == "1":
            #plot_a_star_score('a_star_scores_h4.csv')
            run_with_writing()
        elif choice == "2":
            run_reinforcement_learning()
        else:
            choice = input("Choose only between 1 ond 2")



if __name__ == "__main__":
    choose_algorithm()