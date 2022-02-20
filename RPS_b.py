# This didn't work...

import numpy as np

state_space = 3
action_space = 3

#q_table = np.random.uniform(low = 0, high = 3, size = (state_space, action_space))
q_table = np.ones((state_space, action_space))
q_table *= 1/3

total_reward, reward = 0, 0
avg_rewards_list = []

avg_reward = 0

tags = ['Rock', 'Paper', 'Scissors']

loses_to = {
    '0': 1, #rock loses to paper
    '1': 2, # paper loses to scissors
    '2': 0 # Scissors loses to rock
}

RPS_TO_INT = {
    'R': 0,
    'P': 1,
    'S': 2
}

INT_TO_RPS = {v: k for k, v in RPS_TO_INT.items()}

ALPHA = 0.8
GAMMA = 0.2
EPSILON = 0.8
epsilon = EPSILON
MIN_EPSILON = 0
REDUCTION = (EPSILON - MIN_EPSILON) / 10000

def player(prev_play, opponent_history = []):
    global epsilon, q_table
    if not prev_play:
        q_table, epsilon = reset_vars()
        prev_play = 'S'
    opponent_history.append(prev_play)
    #if len(opponent_history) == 2000:
    #    q_table, epsilon = reset_vars()
    #    opponent_history = []
    action = 0
    prev_play = RPS_TO_INT[prev_play]
    if np.random.random() < 1 - round(epsilon, 2):
        action = np.argmax(q_table[prev_play])
    else:
        action = np.random.randint(0, action_space)
    
    if epsilon > MIN_EPSILON:
        epsilon -= REDUCTION 
    
    reward = get_reward(prev_play, action)
    #print(q_table)
    q_table = update_q_table(q_table, prev_play, action, reward, ALPHA, GAMMA)
    #print(q_table)
    this_action = np.argmax(q_table[prev_play])
    return INT_TO_RPS[action]

def update_q_table(q_table, state, action, reward, alpha, gamma):
    delta = alpha * (reward + gamma * np.max(q_table[action]) - q_table[state, action])
    q_table[state, action] += delta
    return q_table

def get_reward(prev_play, player_play):
    reward = 0
    result = get_result(prev_play, player_play)
    if result == 'WIN':
        reward = 2
    elif result == 'LOSE':
        reward = -1
    return reward

def get_result(prev_play, player_play):
    if prev_play == player_play:
        result = 'DRAW'
    elif loses_to[str(player_play)] == prev_play:
        result = 'LOSE'
    else:
        result = 'WIN'
    
    return result

def reset_vars():
    q_table = np.ones((state_space, action_space))
    q_table *= 1/3
    return q_table, EPSILON
    #return np.random.uniform(low = 0, high = 2, size = (state_space, action_space)), EPSILON