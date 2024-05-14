import paho.mqtt.client as mqtt
import json
import time
import random
import numpy as np
import numpy as np
from datetime import datetime, timedelta
import pickle
class MQTTController:
    def __init__(self, client_id, host, port):
        self.client = mqtt.Client(
            client_id=client_id,
            clean_session=True,
            userdata=None,
            protocol=mqtt.MQTTv311,
            transport="tcp"
        )
        self.host = host
        self.port = port
        self.t_ar = None
        self.co2_count= None
        self.current_values=None


    def connect(self):
        self.client.connect(self.host, self.port)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe(self, topic):
        def on_message(client, userdata, msg):
            if "t_ar" in msg.payload.decode():
                #print(f"Received `{type(msg.payload.decode())}` from `{msg.topic}` topic")
                self.current_values = json.loads(msg.payload.decode())
                self.t_ar = self.current_values["t_ar"]
            
        self.client.subscribe(topic)
        self.client.on_message = on_message

    def publish(self, topic, value):
        topic_body = {"id": random.randint(0, 1000), "value": value}
        payload = json.dumps(topic_body, indent=1)
        result = self.client.publish(topic, payload)

    def set_override_mode(self, bool_on_off):
        self.publish("control_override/enable", bool_on_off)
        time.sleep(1)

    def set_override_flow(self, flow_value):
        self.publish("control_override/flow", flow_value)

    def set_state(self, state_value):
        self.publish("control_override/rc_state", state_value)

    def set_override_inlet_temp(self, temp_value):
        self.publish("control_override/inlet_temp", temp_value)

class ReinforcementLearningEnvironment:
    def __init__(self):
        # Initialize all simulation parameters
        self.num_temp_room_states = 3
        self.num_co2_room_states = 3
        self.num_temp_outside_states = 20
        self.num_time_of_day_states = 1  # Usually 12, but not influencing the simulation in this setup
        self.number_of_states = (self.num_temp_room_states * self.num_co2_room_states *
                                 self.num_time_of_day_states * self.num_temp_outside_states)

        self.num_req_inlet_temp_actions = 3
        self.num_req_inlet_flow_actions = 3
        self.num_recirc_damp_actions = 2
        self.number_of_actions = (self.num_req_inlet_temp_actions * self.num_req_inlet_flow_actions *
                                  self.num_recirc_damp_actions)

        self.userdefined_requested_room_temperature = 23
        self.epsilon = 1  # Exploration rate
        self.discount_factor =0.9
        self.learning_rate=1
        self.xi = 0.9999
        self.firstLogTime=0
        self.loginterval=120

        # Initialize Q-table and state-action mappings
        self.Q_table, self.states, self.actions = self.initialize_variables(self.number_of_states, self.number_of_actions)

    def initialize_variables(self, num_states, num_actions, t_ao):
        temp_outside_stepsize = 2
        temp_outside_min = -8
        temp_outside_max = 28
        t_ao_state = max(0, min((t_ao - temp_outside_min) // temp_outside_stepsize, (temp_outside_max - temp_outside_min) // temp_outside_stepsize))
        states = {'temperature_room': 0, 'co2_room': 0, 'temperature_outside': t_ao_state, 'time_of_day': 0}
        actions = {'req_inlet_temperature': 0, 'req_inlet_flow': 0, 'recirc_damper_pos': 0}
        Q_table = np.zeros((num_states, num_actions))
        return Q_table, states, actions

    def reward_function(self, temperature_room:float, CO2_room:float,total_energy_consumption: float):
        temperature_variance = 0.272
        CO2_variance = 151.375
        requested_room_temperature = 23
        CO2_average_concentration_outside = 400

        temperature_reward = -((temperature_room - requested_room_temperature) / temperature_variance) ** 2
        CO2_adjusted = max(CO2_average_concentration_outside, CO2_room)
        CO2_reward = -((CO2_adjusted - CO2_average_concentration_outside) / CO2_variance) ** 2
        
        power_reward=-(total_energy_consumption*9/4600)

        return [temperature_reward, CO2_reward,power_reward]
    
    def calculate_total_energy_consumption(Fans,Q_ech1,Q_ech2,Q_hp):
        total_energy_consumption=Fans*150/100+Fans*150/100+Q_ech1*1150/100+Q_ech2*1150/100+abs(Q_hp)*2000/100
        return total_energy_consumption
    def convert_actions_to_values(self, actions):
        
        action_values = {
            'req_inlet_temperature_values': actions['req_inlet_temperature'] * 2 + 21,
            'req_inlet_flow_values': actions['req_inlet_flow'] * 35 + 30,
            'recirc_damper_pos_values': actions['recirc_damper_pos'] * 100
        }
        return action_values

    def convert_values_to_states(self, values):
        states = {'temperature_room': 0, 'co2_room': 0, 'temperature_outside': 0, 'time_of_day': 0}
        intervals = [
            (float('-inf'), 22.5), (22.5, 23.5), (23.5, float('inf'))
        ]
        for i, (lower, upper) in enumerate(intervals):
            if lower <= values['temperature_room_value'] < upper:
                states['temperature_room'] = i

        if values['co2_room_value'] < 600:
            states['co2_room']=0
        elif values['co2_room_value'] < 900:
            states['co2_room']=1
        else:
            states['co2_room']=2
        
        temp_outside_stepsize = 2
        temp_outside_min = -8
        temp_outside_max = 28
        states['temperature_outside'] = max(0, min((values['temperature_outside_value'] - temp_outside_min) // temp_outside_stepsize, (temp_outside_max - temp_outside_min) // temp_outside_stepsize))

        return states

    def get_Q_index(self, states, actions):
        state_index = (states['temperature_outside'] * self.num_temp_room_states * self.num_co2_room_states  * self.num_time_of_day_states +
                       states['temperature_room'] * self.num_co2_room_states * self.num_time_of_day_states +
                        states['co2_room']) #* self.num_time_of_day_states +states['time_of_day']
                        
        

        action_index = (actions['req_inlet_temperature'] * self.num_req_inlet_flow_actions * self.num_recirc_damp_actions +
                        actions['req_inlet_flow'] * self.num_recirc_damp_actions +
                        actions['recirc_damper_pos'])

        return state_index, action_index

    def update_Q(self, state_index, action_index, reward, next_state_index:int):
        best_next_action = np.argmax(self.Q_table[next_state_index])
        rewardsSum=sum(reward)
        print(f"Rewarded:           {rewardsSum}\n\n")
        td_target = rewardsSum + self.discount_factor * self.Q_table[next_state_index][best_next_action]
        td_error = td_target - self.Q_table[state_index][action_index]
        self.Q_table[state_index][action_index] += self.learning_rate * td_error
        self.epsilon = self.epsilon*self.xi
        self.learning_rate = self.learning_rate*self.xi
    def get_Q_row(self, states):
        state_index = (states['temperature_outside'] * self.num_temp_room_states * self.num_co2_room_states  * self.num_time_of_day_states +
                       states['temperature_room'] * self.num_co2_room_states * self.num_time_of_day_states +
                        states['co2_room']) #* self.num_time_of_day_states +states['time_of_day']
        return int(state_index)
    def convert_action_index_to_actions(self, action_index):
        req_inlet_temperature = action_index // (self.num_req_inlet_flow_actions * self.num_recirc_damp_actions)
        remainder = action_index % (self.num_req_inlet_flow_actions * self.num_recirc_damp_actions)
        req_inlet_flow = remainder // self.num_recirc_damp_actions
        recirc_damper_pos = remainder % self.num_recirc_damp_actions
        actions = {
            'req_inlet_temperature': req_inlet_temperature,
            'req_inlet_flow': req_inlet_flow,
            'recirc_damper_pos': recirc_damper_pos
        }
        return actions
    def choose_Action(self, states):
        """
        Choose an action based on the epsilon-greedy strategy.

        Parameters:
            states (dict): Dictionary containing current state information, as keys to state indices.

        Returns:
            dict: Dictionary of actions with actual values: inlet temperature action, inlet flow action, recirc damper bypass position.
        """
        random_number = random.random()
        print(f"Random number for action decision: {random_number}")

        if random_number < self.epsilon:
            print("Choosing random action")
            action_index = self.find_random_action()
        else:
            print("Choosing optimal action")
            action_index = self.find_optimal_action(states)
        
        actions = self.convert_action_index_to_actions(action_index)
        return actions

    def find_optimal_action(self, states):
        """
        Identify the optimal action for the current state based on the Q-values from the class's Q-table.
        
        Parameters:
            states (dict): Dictionary containing current states, with keys corresponding to state variables.
        
        Returns:
            int: The index of the optimal action.
        """
        # Calculate the row in the Q-table for the given states using a class method
        Q_row = self.get_Q_row(states)

        # Access the row in the Q-table
        row_values = self.Q_table[Q_row]

        # Find the index of the maximum value in this row, which corresponds to the optimal action
        max_action_index = np.argmax(row_values)
        return max_action_index

    def find_random_action(self):
        """
        Select a random action index based on the total number of actions available from the class attribute.
        
        Returns:
            int: Randomly selected action index.
        """
        # Use the class's attribute `number_of_actions` to determine the range of possible actions
        random_integer = random.randint(0, self.number_of_actions - 1)
        return random_integer
        
    def set_airmaster_sim_state(self,requested_inlet_temperature:float,recirc_damp:int):
        """convert states and action in reinforcement learning, to a state in the Airmaster simulation tool

        Args:
            requested_room_temperature (float): user defined prefered room temperature
            requested_inlet_temperature (float): inlet temperature given from an action by the agent
            recirc_damp (int): whether the system should be in ventilation (recirc_damp=0) or recirculation (recirc_damp=100)

        Returns:
            int: the state that should be given to the airmaster simulation tool
        """
        if recirc_damp == 0:
            if requested_inlet_temperature<self.userdefined_requested_room_temperature :
                airmaster_state = 6#ventilation_cooling 
            else:
                airmaster_state = 4#ventilation_heating
        else:
            if requested_inlet_temperature<self.userdefined_requested_room_temperature :
                airmaster_state = 5#recirculation_cooling 
            else:
                airmaster_state = 3#recirculation_heating
        return airmaster_state
    def saveQToFile(self):
        with open('Q.pkl','wb') as f:
            print("Saving Q table")
            pickle.dump(self.Q_table, f)


    def checkForSave(self):
        if (time.time()>(self.firstLogTime+self.loginterval)):
            self.saveQToFile()
            self.firstLogTime=time.time()


if __name__ == "__main__":
    controller = MQTTController(client_id="BetterCtrl", host="localhost", port=1883)
    controller.connect()
    controller.subscribe("tel/all_values")
    
    controller.set_override_mode(True)
    controller.set_state(3)
    controller.set_override_flow(87.0)
    controller.set_override_inlet_temp(38.0)



    env = ReinforcementLearningEnvironment()
    for i in range(env.Q_table.shape[0]):
            env.Q_table[i, :] = i

    for i in range(env.Q_table.shape[1]):
        env.Q_table[:, i] = env.Q_table[:, i] + i

    # Assign a test action for demonstration
    for key in env.actions.keys():
        env.actions[key] = 1

    # Update the Q-table with dummy values
    env.update_Q(1, 1, [1], 1, 0.9, 0.1)

    # Dummy state values for demonstration
    state_values = {'temperature_room_value': 22.5, 'co2_room_value': 390, 'temperature_outside_value': 15}
    states = env.convert_values_to_states(state_values)
    print("State:", states)

    # Choose an action based on current state
    action = env.choose_Action(states)
    print("Action selected:", action)

    # Dummy call to reward function, assumes it exists
    print("Reward for action:", env.reward_function(22, 450))

    print("Simulation complete")



    

    
    time.sleep(100)  # Keep connection alive for updates
    controller.disconnect()

