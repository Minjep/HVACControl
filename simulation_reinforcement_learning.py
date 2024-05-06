import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from AirmasterDataLib.process.filter_data import  loadPklFile

def reward_function(temperature_room,CO2_room):
    """
    Calculate rewards based on deviation of room temperature and CO2 level from their desired thresholds.
    
    Parameters:
        temperature_room (float): The current temperature in the room.
        CO2_room (float): The current CO2 concentration in the room.

    Returns:
        list: Contains two float values representing the reward for temperature and CO2 level.
    """
    
    temperature_variance = 0.272 #baseret på airmaster data
    CO2_variance = 151.375 #baseret på airmaster data
    requested_room_temperature = 23 
    CO2_average_concentration_outside = 400  
    
    temperature_reward = -((temperature_room-requested_room_temperature)/temperature_variance)**2
    
    CO2_adjusted = max(CO2_average_concentration_outside,(CO2_room))
    CO2_reward = -((CO2_adjusted-CO2_average_concentration_outside)/CO2_variance)**2
    
    rewards = [temperature_reward,CO2_reward]
    
    return rewards


    

def initialize_variables(num_states, num_actions):
    """
    Initialize the Q-table and state-action mappings.
    
    Parameters:
        num_states (int): Total number of states in the Q-table.
        num_actions (int): Total number of actions in the Q-table.
    
    Returns:
        tuple: A tuple containing the initialized Q-table (numpy array), states dictionary, and actions dictionary.
    """
    states = {'temperature_room': 0,  'co2_room': 0,  'temperature_outside' : 0 ,'time_of_day': 0}
    actions = {'req_inlet_temperature': 0,  'req_inlet_flow': 0,  'recirc_damper_pos': 0}
    return np.zeros((num_states, num_actions)),states,actions
   
    

def convert_actions_to_values(actions):
    """
    Convert action indices to real-world values based on predefined scales.
    
    Parameters:
        actions (dict): Dictionary of action indices.
    
    Returns:
        dict: Dictionary of action values calculated from the indices.
    """
    action_values = {'req_inlet_temperature_values': 0,  'req_inlet_flow_values': 0,  'recirc_damper_pos_values': 0}
    
    action_values['req_inlet_temperature_values'] = actions['req_inlet_temperature']*0.5+16
    action_values['req_inlet_flow_values'] = actions['req_inlet_flow']*10+30
    action_values['recirc_damper_pos_values'] = actions['recirc_damper_pos']*100
    
    return action_values

def convert_values_to_states(values):
    """
    Map continuous or real-world value ranges into discrete state indices.
    
    Parameters:
        values (dict): Dictionary of real-world values.
    
    Returns:
        dict: Dictionary of state indices.
    """
    states = {'temperature_room': 0,  'co2_room': 0,'temperature_outside':0 , 'time_of_day': 0}
    
    
    #Get temp room states
    intervals = [
        (float('-inf'), 21.5),
        (21.5, 21.8),
        (21.8, 22.1),
        (22.1, 22.3),
        (22.3, 22.5),
        (22.5, 22.6),
        (22.6, 22.7),
        (22.7, 22.8),
        (22.8, 22.9),
        (22.9, 23),
        (23, 23.1),
        (23.1, 23.2),
        (23.2, 23.3),
        (23.3, 23.4),
        (23.4, 23.5),
        (23.5, 23.7),
        (23.7, 23.9),
        (23.9, 24.2),
        (24.2, 24.5),
        (24.5, float('inf'))
    ]

    for i, (lower, upper) in enumerate(intervals):
        if lower <= values['temperature_room_value'] < upper:
             states['temperature_room'] = i
    
    #Get co2 room state
    co2_room_min = 400
    co2_room_max = 1000
    co2_room_stepsize = 50
    if values['co2_room_value'] < co2_room_min:
        states['co2_room'] = 0  # Below the minimum value
    elif values['co2_room_value'] >= co2_room_max:
        states['co2_room'] = (co2_room_max - co2_room_min) // co2_room_stepsize + 1  # Above the maximum value
    else:
        states['co2_room'] = (values['co2_room_value'] - co2_room_min) // co2_room_stepsize + 1
        
    #get temp air outside state
    if values['temperature_outside_value'] < -20:
        states['temperature_outside'] = 0  # Below the minimum value
    elif values['temperature_outside_value'] >= 30:
        states['temperature_outside'] = (30 - (-20)) // 2 + 1  # Above the maximum value
    else:
        states['temperature_outside'] = (values['temperature_outside_value'] - (-20)) // 2 + 1


    #Get time of day state
    min_time = "05:00:00"
    max_time = "17:00:00"
    min_time = datetime.strptime(min_time, '%H:%M:%S')
    max_time = datetime.strptime(max_time, '%H:%M:%S')
    time = datetime.strptime(values['time_of_day_values'], '%H:%M:%S')

    time_difference = time - min_time
    states['time_of_day'] = (time_difference.seconds // 3600)
    
    return states

    
def get_Q_index(states, num_states_2, num_states_3,num_states_4,actions,num_action_2,num_action_3):
    """
    Compute the indices in the Q-table for given states and actions.
    
    Parameters:
        states (dict): Dictionary containing current states.
        num_states_2 (int): Total number of secondary states.
        num_states_3 (int): Total number of tertiary states.
        num_states_4 (int): Total number of quaternary states.
        actions (dict): Dictionary containing current actions.
        num_action_2 (int): Total number of secondary actions.
        num_action_3 (int): Total number of tertiary actions.

    Returns:
        list: Indices in the Q-table for the current state and action.
    """
    state_index = (states['temperature_room'] ) * (num_states_2 * num_states_3 * num_states_4) + \
            (states['co2_room'] ) * (num_states_4 * num_states_3) + \
            (states['temperature_outside'] ) * num_states_4 + \
             (states['time_of_day'])   
            
    action_index = (actions['req_inlet_temperature'] ) * (num_action_2 * num_action_3) + \
            (actions['req_inlet_flow'] ) * num_action_3 + \
            (actions['recirc_damper_pos'] )
            
    Q_index = [state_index,action_index]
    return Q_index

 
def update_Q(Q, state_index, action_index, reward, next_state, discount_factor, learning_rate):
    """
    Update the Q-value based on the reward received and the highest Q-value of the next state.
    
    Parameters:
        Q (numpy.ndarray): The Q-table.
        state_index (int): Index for the current state.
        action_index (int): Index for the current action.
        reward (float): Reward received.
        next_state (int): Index for the next state.
        discount_factor (float): Discount factor for future rewards.
        learning_rate (float): Learning rate.
    """
    # Q-learning update rule
    reward = sum(reward)
    best_next_action = np.argmax(Q[next_state])
    td_target = reward + discount_factor * Q[next_state][best_next_action]
    td_error = td_target - Q[state_index][action_index]
    Q[state_index][action_index] += learning_rate * td_error
    
def get_Q_row(states, num_states_2, num_states_3,num_states_4):
    """
    Retrieve the row index in the Q-table for the given states.
    
    Parameters:
        states (dict): Current state information.
        num_states_2 (int): Total number of secondary states.
        num_states_3 (int): Total number of tertiary states.
        num_states_4 (int): Total number of quaternary states.
    
    Returns:
        int: Index of the Q-table row corresponding to the given states.
    """
    state_index = (states['temperature_room'] ) * (num_states_2 * num_states_3 * num_states_4) + \
            (states['co2_room'] ) * (num_states_4 * num_states_3) + \
            (states['temperature_outside'] ) * num_states_4 + \
             (states['time_of_day'])   

    Q_row = state_index
    return Q_row

def choose_Action(Q_matrix,epsilon,states, num_states_2, num_states_3,num_states_4,number_of_actions):
    """
    Choose an action based on the epsilon-greedy strategy.
    
    Parameters:
        Q_matrix (numpy.ndarray): The Q-table.
        epsilon (float): Probability threshold for choosing a random action.
        states (dict): Current state information.
        num_states_2 (int): Total number of secondary states.
        num_states_3 (int): Total number of tertiary states.
        num_states_4 (int): Total number of quaternary states.
        number_of_actions (int): Total number of actions available.
    
    Returns:
        int: The chosen action index.
    """
    random_number = random.random()
    print(random_number)

    if (random_number<epsilon):
        print("choosing random action")
        return find_random_action(number_of_actions)
    else: 
        print("choosing optimal action")
        return find_optimal_action(Q_matrix,states, num_states_2, num_states_3,num_states_4)

def find_optimal_action(Q_matrix,states, num_states_2, num_states_3,num_states_4):
    """
    Identify the optimal action for the current state based on the Q-values.
    
    Parameters:
        Q_matrix (numpy.ndarray): The Q-table.
        states (dict): Current state information.
        num_states_2 (int): Total number of secondary states.
        num_states_3 (int): Total number of tertiary states.
        num_states_4 (int): Total number of quaternary states.
    
    Returns:
        int: The index of the optimal action.
    """
    Q_row=get_Q_row(states, num_states_2, num_states_3,num_states_4)

    # Access the row in the Q-matrix.
    row_values = Q_matrix[Q_row]

    # Find the index of the maximum entry in this row.
    max_action_index = np.argmax(row_values)

    return max_action_index

def find_random_action(number_of_actions):
    """
    Select a random action index.
    
    Parameters:
        number_of_actions (int): Total number of actions available.
    
    Returns:
        int: Randomly selected action index.
    """
    random_integer = random.randint(0, number_of_actions-1)
    return random_integer
    
    
def main():
    num_temp_room_states = 20
    num_co2_room_states = 14
    num_temp_outside_states = 27
    num_time_of_day_states = 12
   
    number_of_states = num_temp_room_states*num_co2_room_states*num_time_of_day_states*num_temp_outside_states
    
    num_req_inlet_temp_actions = 21
    num_req_inlet_flow_actions = 8
    num_recirc_damp_actions = 2
    number_of_actions = num_req_inlet_temp_actions*num_req_inlet_flow_actions*num_recirc_damp_actions 
    
    
    Q_table,states,actions = initialize_variables(number_of_states,number_of_actions)
    
    for i in range(Q_table.shape[0]):
        Q_table[i,:] = i
        
    for i in range(Q_table.shape[1]):
        Q_table[:,i] = Q_table[:,i]+i 
    
    for key in actions.keys(): actions[key] = 1
    
    update_Q(Q_table,1,1,1,1,1,1)
    
    state_values = {'temperature_room_value': 0,  'co2_room_value': 390,  'time_of_day_values': "05:30:00"}
    states = convert_values_to_states(state_values)
    print("State:", states)

    Q_index = get_Q_index(states, num_co2_room_states, num_time_of_day_states,actions,num_req_inlet_flow_actions,num_recirc_damp_actions)

    


    reward_function(1,21)
    print("done")
   
    
   

if __name__ == "__main__":
    num_temp_room_states = 20
    num_co2_room_states = 14
    num_temp_outside_states = 27
    num_time_of_day_states = 12
   
    number_of_states = num_temp_room_states*num_co2_room_states*num_time_of_day_states*num_temp_outside_states
    
    num_req_inlet_temp_actions = 21
    num_req_inlet_flow_actions = 8
    num_recirc_damp_actions = 2
    number_of_actions = num_req_inlet_temp_actions*num_req_inlet_flow_actions*num_recirc_damp_actions #21 requested inlet temperature, 8 requested inlet flow, 2 recirc damper position
    Q,states,actions = initialize_variables(number_of_states,number_of_actions)

    state_values = {'temperature_room_value': 0,  'co2_room_value': 390,  'time_of_day_values': "05:30:00",'temperature_outside_value':-100}
    states = convert_values_to_states(state_values)
    print("State:", states)

    for i in range(Q.shape[0]):
        Q[i,:] = i
        
    for i in range(Q.shape[1]):
        Q[:,i] = Q[:,i]+i 
    
    action=choose_Action(Q,0,states, num_co2_room_states, num_temp_room_states,num_temp_outside_states,number_of_actions)
    print("done")