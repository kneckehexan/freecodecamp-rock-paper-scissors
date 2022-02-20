# Found somewhere, beats the game almost 100%, not using it

from anyio import open_process
import numpy as np

ideal_response = {
    'R': 'P',
    'P': 'S',
    'S': 'R'
}

my_moves = ['R'] # Where to store my own moves
opponent_history = [] # The opponents actual moves
opponent_guess = ['', '', '', '']
strategy = [0, 0, 0, 0]
strategy_guess = ['', '', '', '']
my_play_order = {}
opponent_play_order = {}

def player(prev_play):
    if prev_play in ['R', 'P', 'S']:
        opponent_history.append(prev_play)
        for i in range(0,4):
            if opponent_guess[i] == prev_play:
                strategy[i] += 1
    else:
        reset()
    
    # Figure out what the opponents guess will be
    # Do that based om my previous move
    # Counter the opponents guess with ideal response

    myLastTen = my_moves[-10:]
    if len(myLastTen) > 0:
        myFrequentMoves = max(set(myLastTen), key = myLastTen.count)
        opponent_guess[0] = ideal_response[myFrequentMoves]
        strategy_guess[0] = ideal_response[opponent_guess[0]]
        
    if len(my_moves) > 0:
        myLastPlay = my_moves[-1]
        opponent_guess[1] = ideal_response[myLastPlay]
        strategy_guess[1] = ideal_response[opponent_guess[1]]

    if len(opponent_history) >= 3:
        opponent_guess[2] = predict_move(opponent_history, 3, opponent_play_order)
        strategy_guess[2] = ideal_response[opponent_guess[2]]

    if len(my_moves) >= 2:
        opponent_guess[3] = ideal_response[predict_move(my_moves, 2, my_play_order)]
        strategy_guess[3] = ideal_response[opponent_guess[3]]

    best_strat = np.argmax(strategy)
    guess = strategy_guess[best_strat]
    if guess == '':
        guess = 'S'
    my_moves.append(guess)
    return guess

def predict_move(history, n, play_order):
    if ''.join(history[-n:]) in play_order.keys():
        play_order[''.join(history[-n:])] += 1
    else:
        play_order[''.join(history[-n:])] = 1
    possible = [''.join(history[-(n - 1):]) + k for k in ['R','S', 'P']]
    for pm in possible:
        if not pm in play_order.keys():
            play_order[pm] = 0
    predict = max(possible, key = lambda key: play_order[key])
    return predict[-1]

def reset():
    global opponent_history, my_moves, opponent_guess, strategy_guess, strategy, opponent_play_order, my_play_order
    opponent_history.clear()
    opponent_guess = ['', '', '', '']
    strategy_guess = ['', '', '', '']
    strategy = [0, 0, 0, 0]
    my_moves = ['R']
    opponent_play_order = {}
    my_play_order = {}