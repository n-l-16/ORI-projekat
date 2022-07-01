from ReinforcementLearning.start import run_agent
from snake_game_A_star import SnakeGameAStar


class Color:
    GREEN = '\033[92m'
    END_GREEN = '\033[0m'
    BOLD = '\033[1m'
    BOLD_END = '\033[0m'



def run_a_star_algorithm():
    snake_game = SnakeGameAStar()
    snake_game.run_game(snake_game.a_star_search)


def run_reinforcement_learning():
    number_of_game = 10000
    number_of_training = 9990
    run_agent(number_of_game, number_of_training)


def choose_algorithm():
    print("\n" + Color.GREEN + Color.BOLD +  "Choose the algorithm for snake game" + Color.BOLD_END + Color.END_GREEN)
    print("1. --> A*  algorithm")
    print("2. --> Reinforcement learning")
    choice = ""
    while choice not in ["1", "2"]:
        choice = input(">>> ")
        if choice == "1":
            run_a_star_algorithm()
        elif choice == "2":
            run_reinforcement_learning()
        else:
            choice = input("Choose only between 1 ond 2")



if __name__ == "__main__":
    choose_algorithm()