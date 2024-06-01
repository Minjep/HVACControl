import numpy as np
import matplotlib.pyplot as plt

class simulate_model:
    def __init__(self): 
        self.x_recirc = np.array([[0, 0],
                                      [0, 0]])
        
        self.A_recirc = np.array([[810.5, 8.8], 
                                  [48.0, 879.8]]) * 1e-3
        
        self.B_recirc = np.array([[-1.2, -0.1, -0.2, 0.0, -1.1, -2.2],
                                  [0.5, 0.1, 1.3, -0.1, 0.9, 1.8]]) * 1e-3
        
        self.C_recirc = np.array([[-60.7, -1.8],
                                  [-2711.0, -3222.3]])
        
        self.C_recirc_inv = np.array([[-0.0169, 0.0000],
                                      [0.0142, -0.0003]])
    
        self.x_vent = np.array([[0, 0],
                                    [0, 0]])
    
        self.A_vent = np.array([[913.3, -78.6], 
                                [288.0, 144.6]]) * 1e-3
        
        self.B_vent = np.array([[-0.7, -0.3, 0.3, -0.2, -5.5, -5.2],
                                [1.5, 0.3, -0.1, -0.8, 31.6, -0.9]]) * 1e-3
        
        self.C_vent = np.array([[-31.3, 0.4],
                                [-1141.8, 755.0]])
        
        self.C_vent_inv = np.array([[-0.0326, 0.0000],
                                    [-0.0493, 0.0014]])
        
        
        self.y = np.array(  [[0],
                            [0]])
        
    def get_next_state(self,in_recirc_state:bool,u):
        """
        Estimates the next state of the system after receiving a response from the simulation.

        Depending on the current damper recirculation state, it updates the estimated state
        variables for either ventilation or recirculation mode.
        """
        u = np.vstack((u, [[self.T_ao]]))

        if in_recirc_state:
            self.y = self.C_recirc.dot(self.x_recirc)
            if self.y[1, 0] < 400:
                self.y[1, 0] = 400
                self.x_recirc = self.C_recirc_inv.dot(self.y)
            self.x_recirc = self.A_recirc.dot(self.x_recirc) + self.B_recirc.dot(u)
            self.x_vent = self.C_vent_inv.dot(self.y)
            self.x_vent = self.C_vent.dot(self.x_vent) + self.B_vent.dot(u)
        else:
            self.y = self.C_vent.dot(self.x_vent)
            if self.y[1, 0] < 400:
                self.y[1, 0] = 400
                self.x_vent = self.C_vent_inv.dot(self.y)
            self.x_vent = self.A_vent.dot(self.x_vent) + self.B_vent.dot(u)
            self.x_recirc = self.C_recirc_inv.dot(self.y)
            self.x_recirc = self.A_recirc.dot(self.x_recirc) + self.B_recirc.dot(u)
        return self.y

    def set_variables(self,temp_value:float,co2_value:float,t_ao:float):
        """
        Initializes the reference values, initial outputs, and outdoor air temperature.

        Parameters:
            temp_ref (float): Reference temperature.
            co2_ref (float): Reference CO2 level.
            temp_init (float): Initial temperature.
            co2_init (float): Initial CO2 level.
            t_ao (float): Outdoor air temperature.
        """
        self.y[0,0] = temp_value
        self.y[1,0] = co2_value

        self.x_vent = self.C_vent_inv.dot(self.y)
        self.x_recirc = self.C_recirc_inv.dot(self.y)

        self.T_ao = t_ao
        
class ReinforcementLearning:
    def __init__(self, file_path_for_q_table,t_ao:float):
        """
        Initialize the reinforcement learning class by loading the Q-table from the specified file path.
        
        Parameters:
        - file_path: str, path to the numpy file containing the Q-table
        """
        self.q_table = self.load_q_table(file_path_for_q_table)
        self.T_ao=t_ao

        self.fanSteps=5
        self.ech1Steps=5
        self.ech2Steps=5
        self.hpSteps=5
        self.bypassSteps=5
        self.statesSteps=2
        
        self.tempOutSteps=5
        self.tempRoomSteps=5
        self.co2RoomSteps=5

    def load_q_table(self, file_path):
        """
        Load the Q-table from a numpy file.
        
        Parameters:
        - file_path: str, path to the numpy file containing the Q-table
        
        Returns:
        - q_table: numpy array, loaded Q-table
        """
        try:
            q_table = np.load(file_path)
            print(f"Q-table successfully loaded from {file_path}")
        except Exception as e:
            print(f"An error occurred while loading the Q-table: {e}")
            q_table = None
        return q_table
    
    def find_optimal_action_index(self,Y):
        # Access the row in the Q-matrix.
        row=self.output_to_Q_row(Y)
        
        row_values = self.q_table[row]

        # Find the index of the maximum entry in this row.
        max_action_index = np.argmax(row_values)

        return max_action_index

    def get_actions(self,Y):
        
        index=self.find_optimal_action_index(Y)

        fanSteps=self.fanSteps
        ech1Steps=self.ech1Steps
        ech2Steps=self.ech2Steps
        hpSteps=self.hpSteps
        bypassSteps=self.bypassSteps
        statesSteps=self.statesSteps

        fan_min, fan_max = 30, 100  # Assuming these are indices for fan settings
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
        ech1_step=remainder//(ech2Steps*hpSteps*bypassSteps*statesSteps)
        remainder=remainder%(ech2Steps*hpSteps*bypassSteps*statesSteps)
        ech2_step=remainder//(hpSteps*bypassSteps*statesSteps)
        remainder=remainder%(hpSteps*bypassSteps*statesSteps)
        hp_step=remainder//(bypassSteps*statesSteps)
        remainder=remainder%(bypassSteps*statesSteps)
        bypass_step=remainder//(statesSteps)
        recirc_step=remainder%(statesSteps)

        recirc_action=recirc_min+recirc_step*recirc_step_size
        bypass_action=bypass_min+bypass_step*bypass_step_size
        hp_action=hp_min+hp_step*hp_step_size
        ech1_action=ech_min+ech1_step*ech1_step_size
        ech2_action=ech_min+ech2_step*ech2_step_size
        fan_action=fan_min+fan_step*fan_step_size

        u = np.array([[fan_action], [ech1_action], [ech2_action], [hp_action], [bypass_action]])

        if recirc_action==0:
            recirc_state=True
        else:
            recirc_state=False

        return u,recirc_state

    def output_to_Q_row(self,Y):
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
        temp_step_size = (temp_max - temp_min) / (self.tempRoomSteps - 2)
        co2_step_size = (co2_max - co2_min) / (self.co2RoomSteps - 2)
        tempOut_step_size = (tempOut_max - tempOut_min) / (self.tempOutSteps - 2)

        # Determine the index for output temperature
        if self.T_ao <= tempOut_min:
            tempOut_index = 0
        elif self.T_ao >= tempOut_max:
            tempOut_index = self.tempOutSteps - 1
        else:
            tempOut_index = int((self.T_ao - tempOut_min) // tempOut_step_size) + 1

        # Determine the index for temperature
        if Y[0, 0] <= temp_min:
            temp_index = 0
        elif Y[0, 0] >= temp_max:
            temp_index = self.tempRoomSteps - 1
        else:
            temp_index = int((Y[0, 0] - temp_min) // temp_step_size) + 1

        # Determine the index for CO2
        if Y[1, 0] <= co2_min:
            co2_index = 0
        elif Y[1, 0] >= co2_max:
            co2_index = self.co2RoomSteps - 1
        else:
            co2_index = int((Y[1, 0] - co2_min) // co2_step_size) + 1

        # Calculate the Q-matrix index
        q_index = (temp_index * self.co2RoomSteps * self.tempOutSteps) + (co2_index * self.tempOutSteps) + tempOut_index

        return q_index

def calculate_total_energy_consumption(Fans,Q_ech1,Q_ech2,Q_hp):
    total_energy_consumption=Fans*150/100+Fans*150/100+Q_ech1*1150/100+Q_ech2*1150/100+abs(Q_hp)*2000/100
    
    return total_energy_consumption

if __name__ == "__main__":
    #inital u and state
    start_temp=10
    start_co2=1000
    y=np.array([[start_temp],[start_co2]])
    are_we_in_recirc=False
    t_ao=-5

    RL=ReinforcementLearning("C:/Users/overg/Downloads/rl/Q.npy",t_ao)
    env=simulate_model()
    env.set_variables(start_temp,start_co2,t_ao)


    # Initialize an empty list to store y values
    y_data = []
    power_data = []

    # Loop to generate and store y values
    for i in range(1, 100):
        u, are_we_in_recirc = RL.get_actions(y)
        y = env.get_next_state(are_we_in_recirc, u) 

        print(RL.output_to_Q_row(y),",",RL.find_optimal_action_index(y))

        power=calculate_total_energy_consumption(u[0,0],u[1,0],u[2,0],u[3,0])
        
        power_data.append(power)
        # Append the y value to the list
        y_data.append(y)

    # Convert the list to a numpy array if y values are numerical
    y_data = np.array(y_data)

    # Plot the y data
    # Extract the components to plot separately
    y_component_1 = y_data[:, 0, 0]
    y_component_2 = y_data[:, 1, 0]

    # Plot the y data components
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(y_component_1)
    plt.xlabel('Iteration')
    plt.ylabel('t_ar')
    plt.title('t_ar over iterations')

    plt.subplot(1, 2, 2)
    plt.plot(y_component_2)
    plt.xlabel('Iteration')
    plt.ylabel('co2_ar')
    plt.title('co2_ar over iterations')

    plt.tight_layout()
    plt.show()

    plt.figure()
    plt.plot(power_data)
    plt.xlabel('Iteration')
    plt.ylabel('Watt')
    plt.title('Power over iteration')

    plt.tight_layout()
    plt.show()

    print("")