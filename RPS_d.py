# Didn't work...

# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

import numpy as np

RPS_TO_INT = {
    'R': 0,
    'P': 1,
    'S': 2
}

INT_TO_RPS = {v: k for k, v in RPS_TO_INT.items()}

BEST_GUESS = {
    'R': 'P',
    'P': 'S',
    'S': 'R'
}

# Transistion matrix with initial values set to 1/3 for all possible outcomes
T = np.ones((3, 3))
T = T * 1/3

def player(prev_play, opposition_play = [], player_play = []):
    global T
    # If no moves have been made
    if not prev_play:
        T = reset_transistion_matrix(T)
        prev_play = 'R'
    
    opposition_play.append(prev_play)
    T = update_transition_matrix(convert_opposistion_play_to_int(opposition_play), T)
    print(T)

    next_state = INT_TO_RPS[np.argmax(T[RPS_TO_INT[prev_play]])]

    # Introduce Bellman's equation

    guess = BEST_GUESS[next_state]
    player_play.append(guess)
    print('player moves:', player_play)
    print('opposition moves:', opposition_play)

    return guess


def update_transition_matrix(data, m):
    """
    Function that takes a list of opposistion data containing 'R', 'P' or 'S' and converts into a transistion matrix.
    Ref: https://stackoverflow.com/questions/46657221/generating-markov-transition-matrix-in-python/46657489
    """
    for (i, j) in zip(data, data[1:]):
        m[i][j] += 1
    
    for row in m:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]

    return m

def reset_transistion_matrix(t):
    t = np.ones((3, 3))
    t = t * 1/3
    return t

def convert_opposistion_play_to_int(data):
    data_as_int = []
    for d in data:
        data_as_int.append(RPS_TO_INT[d])
    
    return data_as_int