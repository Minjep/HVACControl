import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from AirmasterDataLib.process.filter_data import  loadPklFile

def reward_function(temperature_room,CO2_room):
    
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
    states = {'temperature_room': 0,  'co2_room': 0,  'temperature_outside' : 0 ,'time_of_day': 0}
    actions = {'req_inlet_temperature': 0,  'req_inlet_flow': 0,  'recirc_damper_pos': 0}
    return np.zeros((num_states, num_actions)),states,actions
   
    

def convert_actions_to_values(actions):
    action_values = {'req_inlet_temperature_values': 0,  'req_inlet_flow_values': 0,  'recirc_damper_pos_values': 0}
    
    action_values['req_inlet_temperature_values'] = actions['req_inlet_temperature']*0.5+16
    action_values['req_inlet_flow_values'] = actions['req_inlet_flow']*10+30
    action_values['recirc_damper_pos_values'] = actions['recirc_damper_pos']*100
    
    return action_values

def convert_values_to_states(values):
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
    # Q-learning update rule
    reward = sum(reward)
    best_next_action = np.argmax(Q[next_state])
    td_target = reward + discount_factor * Q[next_state][best_next_action]
    td_error = td_target - Q[state_index][action_index]
    Q[state_index][action_index] += learning_rate * td_error
    

    
    
def main():
    num_temp_room_states = 20
    num_co2_room_states = 14
    num_temp_outside_states = 27
    num_time_of_day_states = 12
   
    number_of_states = num_temp_room_states*num_co2_room_states*num_time_of_day_states*num_temp_outside_states
    
    num_req_inlet_temp_actions = 29
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
    
    action_values = convert_actions_to_values(actions)
    

    


    reward_function(1,21)
   
    
   

if __name__ == "__main__":
    
    main()