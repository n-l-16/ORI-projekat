from ReinforcementLearning.SnakeGameReinforcement import SnakeGameReinforcement
from ReinforcementLearning.qlearningAgent import ApproximateQAgent
from snake_game_GUI import SnakeGameGUI

def new_game(display, is_training):
    agent = ApproximateQAgent()
    game = SnakeGameReinforcement(is_training)
    game.run_game(agent)
    return game

def run_agent(number_of_game, number_of_training):
    zero_number = 0
    one_number = 0
    two_number = 0
    tree_number = 0
    else_number = 0
    for i in range(number_of_game):
        is_training = i < number_of_training
        if(is_training):
            display = None
        else:
            display = SnakeGameGUI()
        game = new_game(display, is_training)
        # print("game ", game)
        print(i)
        print(game.score)
        if game.score > 3:
            print("USPEO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            else_number += 1
        if game.score == 0:
            zero_number += 1
        if game.score == 1:
            one_number += 1
        if game.score == 2:
            two_number += 1
        if game.score == 3:
            tree_number += 1
        print("NULA: ", zero_number, " JEDAN: ", one_number, " DVA: ", two_number, " TRI: ", tree_number, " OSTALO: ", else_number)
