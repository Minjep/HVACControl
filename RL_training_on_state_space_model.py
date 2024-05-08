import numpy as np
import random

def reward_function(temperature_room:float,CO2_room:float):
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

def simModel(xR:np.array,xV:np.array,u:np.array,recirc:bool):
    AR = np.array([[810.5, 8.8], [48.0, 879.8]]) * 1e-3
    BR = np.array([[-1.2, -0.1, -0.2, 0.0, -1.1, -2.2],
                [0.5, 0.1, 1.3, -0.1, 0.9, 1.8]]) * 1e-3
    CR = np.array([[-60.7, -1.8],
                [-2711.0, -3222.3]])
    AV = np.array([[913.3, -78.6], [288.0, 144.6]]) * 1e-3
    BV = np.array([[-0.7, -0.3, 0.3, -0.2, -5.5, -5.2],
                [1.5, 0.3, -0.1, -0.8, 31.6, -0.9]]) * 1e-3
    CV = np.array([[-31.3, 0.4],
                [-1141.8, 755.0]])
    
    
    xk1R=AR.dot(xR)+BR.dot(u)
    yR=CR.dot(xV)

    xk1V=AV.dot(xV)+BV.dot(u)
    yV=CV.dot(xV)

    
    if recirc==True:
        return xk1R,xk1V,yR
    else:
        return xk1R,xk1V,yV

def output_to_Q_row(Y, tempRoomSteps, co2RoomSteps,tempOutSteps,tempOut):
    """
    Converts the output Y to an index for the Q-matrix, accounting for out-of-range values.
    
    Parameters:
    - Y: np.array, expected to contain [temperature, CO2 level]
    - tempRoomSteps: int, number of discrete steps for temperature
    - co2RoomSteps: int, number of discrete steps for CO2
    
    Returns:
    - int, index for the Q-matrix
    """
    # Define arbitrary ranges for temperature and CO2 (adjust based on real-world data)
    temp_min, temp_max = 21.5, 24.5  # Example range for temperature
    co2_min, co2_max = 600, 1000  # Example range for CO2
    tempOut_min, tempOut_max = 0, 20 # Example range for output temperature

    # Calculate the range size for each step
    temp_step_size = (temp_max - temp_min) / (tempRoomSteps - 2)
    co2_step_size = (co2_max - co2_min) / (co2RoomSteps - 2)
    tempOut_step_size = (tempOut_max - tempOut_min) / (tempOutSteps - 2)

    # Determine the index for output temperature
    if tempOut <= tempOut_min:
        tempOut_index = 0
    elif tempOut >= tempOut_max:
        tempOut_index = tempOutSteps - 1
    else:
        tempOut_index = int((tempOut - tempOut_min) // tempOut_step_size) + 1

    # Determine the index for temperature
    if Y[0, 0] <= temp_min:
        temp_index = 0
    elif Y[0, 0] >= temp_max:
        temp_index = tempRoomSteps - 1
    else:
        temp_index = int((Y[0, 0] - temp_min) // temp_step_size) + 1

    # Determine the index for CO2
    if Y[1, 0] <= co2_min:
        co2_index = 0
    elif Y[1, 0] >= co2_max:
        co2_index = co2RoomSteps - 1
    else:
        co2_index = int((Y[1, 0] - co2_min) // co2_step_size) + 1

    # Calculate the Q-matrix index
    q_index = (temp_index * co2RoomSteps * tempOutSteps) + (co2_index * tempOutSteps) + tempOut_index

    return q_index

def choose_Action(Q_matrix:np.array,epsilon:float,row:int,number_of_actions:int,fanSteps:int,ech1Steps:int,ech2Steps:int,hpSteps:int,bypassSteps:int,statesSteps:int):
    random_number = random.random()

    if (random_number<epsilon):
        print("choosing random action")
        action_index = find_random_action(number_of_actions)
    else: 
        print("choosing optimal action")
        action_index = find_optimal_action(Q_matrix,row)
        
    actions = convert_action_index_to_actions(action_index,fanSteps,ech1Steps,ech2Steps,hpSteps,bypassSteps,statesSteps)
    return actions

def find_optimal_action(Q_matrix:np.array,row:int):


    # Access the row in the Q-matrix.
    row_values = Q_matrix[row]

    # Find the index of the maximum entry in this row.
    max_action_index = np.argmax(row_values)

    return max_action_index

def find_random_action(number_of_actions:int):
    """
    Select a random action index.
    
    Parameters:
        number_of_actions (int): Total number of actions available.
    
    Returns:
        int: Randomly selected action index.
    """
    random_integer = random.randint(0, number_of_actions-1)
    return random_integer

def convert_action_index_to_actions(index:int,fanSteps,ech1Steps,ech2Steps,hpSteps,bypassSteps,statesSteps):
    fan_min, fan_max = 0, 100  # Assuming these are indices for fan settings
    ech_min, ech_max = 0, 100  # Assuming these are indices for economizer settings
    hp_min, hp_max = -100, 100    # Assuming these are indices for heat pump settings
    bypass_min, bypass_max = 0, 100  # Assuming these are indices for bypass settings
    recirc_min, recirc_max = 0, 100  # State settings, assuming binary or two distinct states

    # Calculate the step sizes for each variable
    fan_step_size = (fan_max - fan_min) / (fanSteps - 1)
    ech1_step_size = (ech_max - ech_min) / (ech1Steps - 1)
    ech2_step_size = (ech_max - ech_min) / (ech2Steps - 1)
    hp_step_size = (hp_max - hp_min) / (hpSteps - 1)
    bypass_step_size = (bypass_max - bypass_min) / (bypassSteps - 1)
    recirc_step_size = (recirc_max - recirc_min) / (statesSteps - 1)

    fan_step=index//(ech1Steps*ech2Steps*hpSteps*bypassSteps*statesSteps)
    remainder=index%(ech1Steps*ech2Steps*hpSteps*bypassSteps*statesSteps)
    ech1_step=index//(ech2Steps*hpSteps*bypassSteps*statesSteps)
    remainder=index%(ech2Steps*hpSteps*bypassSteps*statesSteps)
    ech2_step=remainder//(hpSteps*bypassSteps*statesSteps)
    remainder=remainder%(hpSteps*bypassSteps*statesSteps)
    hp_step=remainder//(bypassSteps*statesSteps)
    remainder=remainder%(bypassSteps*statesSteps)
    bypass_step=remainder//(statesSteps)
    recirc_step=remainder%(statesSteps)

    recirc_action=recirc_step*recirc_step_size
    bypass_action=bypass_step*bypass_step_size
    hp_action=hp_step*hp_step_size
    ech1_action=ech1_step*ech1_step_size
    ech2_action=ech2_step*ech2_step_size
    fan_action=fan_step*fan_step_size

    return fan_action,ech1_action,ech2_action,hp_action,bypass_action,recirc_action





    

def update_Q(Q:np.array, state_index:int, action_index:int, rewards:np.array, next_state_index:int, discount_factor:float, learning_rate:float):
    # Q-learning update rule
    rewards = sum(rewards)
    best_next_action = np.argmax(Q[next_state_index])
    td_target = rewards + discount_factor * Q[next_state_index][best_next_action]
    td_error = td_target - Q[state_index][action_index]
    Q[state_index][action_index] += learning_rate * td_error
    return Q

if __name__ == "__main__":
    X_recirc=np.array([[0,0],[0,0]],float)
    X_vent=np.array([[0,0],[0,0]],float)
    Y=np.array([[0],[0]],float)

    fanSteps=5
    ech1Steps=5
    ech2Steps=5
    hpSteps=5
    bypassSteps=5
    statesSteps=2

    numberOfActions=fanSteps*ech1Steps*ech2Steps*hpSteps*bypassSteps*statesSteps

    tempOutSteps=5
    tempRoomSteps=5
    co2RoomSteps=5

    numberOfStates=tempRoomSteps*co2RoomSteps*tempOutSteps


    Q=np.zeros((numberOfStates,numberOfActions),float)

    for i in range(0,10):
        U = np.random.rand(6, 1)

        X_recirc,X_vent,Y=simModel(X_recirc,X_vent,U,True)

        q_row = output_to_Q_row(Y, tempRoomSteps, co2RoomSteps,tempOutSteps,0)

        actions=choose_Action(Q,1,q_row,numberOfActions,fanSteps,ech1Steps,ech2Steps,hpSteps,bypassSteps,statesSteps)
