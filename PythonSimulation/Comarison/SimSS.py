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
        
        self.y_LQR = np.array(  [[0],
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
            self.x_vent = self.A_vent.dot(self.x_vent) + self.B_vent.dot(u)
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


class LQR_Controller:
    def __init__(self): 
        self.x_recirc_est = np.array([[0],
                                      [0]])
        
        self.A_recirc = np.array([[810.5, 8.8], 
                                  [48.0, 879.8]]) * 1e-3
        
        self.B_recirc = np.array([[-1.2, -0.1, -0.2, 0.0, -1.1, -2.2],
                                  [0.478, 0.066, 1.306, -0.10, 0.91, 0]]) * 1e-3
        
        self.C_recirc = np.array([[-60.7, -1.8],
                                  [-2711,-3222.3]])
        
        self.C_recirc_inv = np.array([[-0.0169, 0.0000],
                                      [0.0142, -0.0003]])
        
        self.K_recirc = np.array([[-49.8, -2.355],
                                  [-3.25,-0.153],
                                  [-5.97, -0.255],
                                  [-2.66, 0.12],
                                  [-474.89, -22.305],
                                  [0, 0]])
        self.L_recirc = np.array([[0.0014192,0], 
                                  [0.033,-0.000204]]) 
    
        self.x_vent_est = np.array([[0],
                                    [0]])
    
        self.A_vent = np.array([[913.3, -78.6], 
                                [288.0, 144.6]]) * 1e-3
        
        self.B_vent = np.array([[-0.7, -0.3, 0.3, -0.2, -5.5, -5.2],
                                [1.5, 0.3, -0.1, -0.8, 31.6, -0.9]]) * 1e-3
        
        self.C_vent = np.array([[-31.3, 0.4],
                                [-1141.8, 755.0]])
        
        self.C_vent_inv = np.array([[-0.0326, 0.0000],
                                    [-0.0493, 0.0014]])
        
        self.L_vent = np.array([[-0.019322, 0.000001], 
                                [-0.0165, 0.0001]]) 
        
        self.K_vent = np.array([[-429, 23.915],
                                  [-172.15, 9.5906],
                                  [174.2, -9.7021],
                                  [-578.64, 32.2],
                                  [-20.622, 6.2327],
                                  [0, 0]])
        
        self.outputs_est = np.array([[0],
                                     [0]])
        
        self.inputs = np.array([[0],
                                [0],
                                [0],
                                [0],
                                [0],
                                [0]])
        
        self.outputs = np.array([[0],
                                 [0]])
        
        self.references = np.array([[20], 
                                    [500]])
        # Calculate A_cl for recirculation system
        A_cl_recirc = self.A_recirc - self.B_recirc @ self.K_recirc
        A_cl_vent = self.A_vent - self.B_vent @ self.K_vent

        # Calculate N_bar for recirculation system using pseudoinverse
                
        self.N_dash_vent =  np.array([[19.698, -9.14511],
                               [7.902, -0.058279],
                               [-7.9965, 0.058992],
                               [26.596, -0.19618],
                               [-0.25564, 0.034129],
                               [0, 0]])
        self.N_dash_ref =  np.array([[1.08,0],
                               [0.0702,0],
                               [0.112,0],
                               [-0.054,0],
                               [10.19,0],
                               [0,0]])
        self.N_dash_vent = np.linalg.pinv(self.C_vent @ np.linalg.inv(A_cl_vent) @ self.B_vent)
        self.N_dash_ref = np.linalg.pinv(self.C_recirc @ np.linalg.inv(A_cl_recirc) @ self.B_recirc)

        self.damper_recirc_state = 0 # 0 = ventilation, 1=recirculation
        
        self.T_cool = 0
        self.co2_high = 0
        self.T_ao = 0
        self.T_heat = 0
        self.co2_low=0
        self.airmaster_state=2
        
    def set_current_damper_recirc_state(self):
        """
        Updates the damper recirculation state based on current CO2 levels, temperature,
        and the outdoor air temperature.

        Adjusts the CO2 thresholds based on the current temperature output. Switches
        between ventilation and recirculation modes depending on the CO2 levels and
        temperature conditions.
        """
        alpha = 1 + min(4, abs(self.outputs[0] - self.references[0])) / 4

        
        self.co2_low = alpha * 600
        self.co2_high = alpha * 900
        if self.damper_recirc_state == 1: 
            if((self.outputs[1]>self.co2_high) or (self.outputs[0]>self.T_cool and self.T_ao <(self.outputs[0]-0.5)) or (self.outputs[0]<self.T_heat and self.T_ao>(self.outputs[0]+0.5))):
                self.damper_recirc_state = 0
                print("**********Changing to ventilation mode")
        else: 
            if(self.outputs[1]<self.co2_low or (self.outputs[0] > self.T_cool and self.T_ao>(self.outputs[0]+0.5)) or (self.outputs[0]<self.T_heat and self.T_ao<(self.outputs[0]-0.5))):
                self.damper_recirc_state = 1
                print("***********Changing to recirc mode")
        return self.damper_recirc_state

    def estimate_next_state(self):
        """
        Estimates the next state of the system after receiving a response from the simulation.

        Depending on the current damper recirculation state, it updates the estimated state
        variables for either ventilation or recirculation mode.
        """
        if self.damper_recirc_state == 0: #ventilation
            self.x_vent_est = self.A_vent.dot(self.x_vent_est) + self.B_vent.dot(self.inputs)+self.L_vent.dot(-self.C_vent.dot(self.x_vent_est)+self.outputs)
        else: #recirculation
            self.x_recirc_est = self.A_recirc.dot(self.x_recirc_est) + self.B_recirc.dot(self.inputs)+self.L_recirc.dot(-self.C_recirc.dot(self.x_recirc_est)+self.outputs)
        
    def state_resetting(self):
        """
        Resets the state estimates after calculating inputs and receiving the simulated response
        corresponding to the inputs.

        This function ensures that the first state estimate corresponds to the current time and the
        second state estimate is for one timestep into the future.
        """
        if self.damper_recirc_state == 0: #ventilation
            self.outputs_est = self.C_vent.dot(self.x_vent_est)
            self.x_recirc_est = self.C_recirc_inv.dot(self.outputs_est)
            self.x_recirc_est = self.A_recirc.dot(self.x_recirc_est)+self.B_recirc.dot(self.inputs)+self.L_recirc.dot(self.C_recirc.dot(self.x_recirc_est)-self.outputs)
        else: #recirculation
            self.outputs_est = self.C_recirc.dot(self.x_recirc_est)
            self.x_vent_est = self.C_vent_inv.dot(self.outputs_est)
            self.x_vent_est = self.A_vent.dot(self.x_vent_est)+self.B_vent.dot(self.inputs)+self.L_vent.dot(self.C_vent.dot(self.x_vent_est)-self.outputs)
            
        
    def calculate_inputs(self):
        """
        Calculates the control inputs based on the current state estimates and references.

        Depending on the current damper recirculation state, it computes the control inputs
        for either ventilation or recirculation mode.
        """
        if self.damper_recirc_state == 0: #ventilation
            self.inputs = -self.K_vent.dot(self.x_vent_est) + self.N_dash_vent.dot(self.references)
        else: #ventilation
            self.inputs = -self.K_recirc.dot(self.x_recirc_est) + self.N_dash_ref.dot(self.references)
        print("Inputs before constraint")
        print(f"{self.inputs}")
        for input in [0,1,2,4]: #Fsup(t) Qech1(t) Qech2(t) Dbypass(t)
            if self.inputs[input] < 0:
                self.inputs[input] = 0
            elif self.inputs[input] > 100:
                self.inputs[input] = 100
        if self.inputs[0]<30:
            self.inputs[0]=30
        #  Qhp(t)
        if self.inputs[3] < -100:
            self.inputs[3] = -100
        elif self.inputs[3] > 100:
            self.inputs[3] = 100
            
        return self.inputs[0:5]
            


    def initialize_variables(self,temp_ref, co2_ref,temp_init,co2_init,t_ao):
        """
        Initializes the reference values, initial outputs, and outdoor air temperature.

        Parameters:
            temp_ref (float): Reference temperature.
            co2_ref (float): Reference CO2 level.
            temp_init (float): Initial temperature.
            co2_init (float): Initial CO2 level.
            t_ao (float): Outdoor air temperature.
        """
        self.references[0] = temp_ref
        self.references[1] = co2_ref
        self.T_cool = self.references[0] + 1
        self.T_heat = self.references[0] - 1
        self.outputs[0] = temp_init
        self.outputs[1] = co2_init    
        self.T_ao = t_ao
        self.inputs[5] = self.T_ao
         

if __name__ == "__main__":
    #inital u and state
    start_temp=20
    start_co2=1000
    y=np.array([[start_temp],[start_co2]])
    are_we_in_recirc=False
    t_ao=15

    RL=ReinforcementLearning("Q.npy",t_ao)
    env=simulate_model()
    env.set_variables(start_temp,start_co2,t_ao)



    # Initialize an empty list to store y values
    y_data = []
    power_data = []
    u_RL_l=[]
    u_LQR_l=[]

    y_data_LQR = []
    rc_state_RL=[]
    rc_state_LQR=[]


    env_LQR=simulate_model()
    env_LQR.set_variables(start_temp,start_co2,t_ao)
    LQR = LQR_Controller()
    LQR.initialize_variables(23,400,start_temp,start_co2,t_ao)
    disttemp=26
    distco2=1000
    # Loop to generate and store y values
    for i in range(0, 100):
        
        u, are_we_in_recirc = RL.get_actions(y)
        rc_state_RL.append(are_we_in_recirc)


        print(RL.output_to_Q_row(y),",",RL.find_optimal_action_index(y))

        if (i ==40):
            env.x_recirc=env.C_recirc_inv.dot(np.array([[disttemp],[distco2]]))
            env.x_vent=env.C_vent_inv.dot(np.array([[disttemp],[distco2]]))
            env_LQR.x_recirc=env_LQR.C_recirc_inv.dot(np.array([[disttemp],[distco2]]))
            env_LQR.x_vent=env_LQR.C_vent_inv.dot(np.array([[disttemp],[distco2]]))

        y = env.get_next_state(are_we_in_recirc, u) 
        
        # Append the y value to the list
        y_data.append(y)
        u_RL_l.append(u)
        
        
       
        are_we_in_recirc_LQR = LQR.set_current_damper_recirc_state()
        rc_state_LQR.append(are_we_in_recirc_LQR)
        u_LQR = LQR.calculate_inputs()
        u_LQR_l.append(u_LQR)
        y_LQR = env_LQR.get_next_state(are_we_in_recirc_LQR, u_LQR) 
        LQR.outputs = y_LQR
        LQR.estimate_next_state()

        LQR.state_resetting()
        
        
        y_data_LQR.append(y_LQR)
        
        
        
        
    y_data_LQR = np.array(y_data_LQR)
    y_data_RL = np.array(y_data)


t_ar_LQR=y_data_LQR[:,0]
t_ar_RL=y_data_RL[:,0]

co2_LQR=y_data_LQR[:,1]
co2_RL=y_data_RL[:,1]

t_set=y_data_LQR[:,0]*0+23
time=np.linspace(0,len(t_ar_LQR)*15,len(t_ar_LQR)+1)
time=time[0:-1]
print(time)


# Define settle criteria
settle_percentage = 0.02
temperature_setpoint = t_ar_LQR[38]
co2_setpoint = co2_LQR[38]

# Calculate settle thresholds
temp_upper_threshold_lqr = temperature_setpoint * (1 + settle_percentage)
temp_lower_threshold_lqr = temperature_setpoint * (1 - settle_percentage)
temp_upper_threshold_rl = t_ar_RL[38] * (1 + settle_percentage)
temp_lower_threshold_rl = t_ar_RL[38] * (1 - settle_percentage)
co2_upper_threshold = co2_setpoint * (1 + settle_percentage)
co2_lower_threshold = co2_setpoint * (1 - settle_percentage)

# Function to calculate settle time
def calculate_settle_time(data, upper_threshold, lower_threshold):
    for i in range(len(data)):
        if np.all(data[i:i+3] >= lower_threshold) and np.all(data[i:i+3] <= upper_threshold):
            return time[i]
    return None

# Calculate settle times
settle_time_temp_LQR = calculate_settle_time(t_ar_LQR, temp_upper_threshold_lqr, temp_lower_threshold_lqr)
settle_time_temp_RL = calculate_settle_time(t_ar_RL, temp_upper_threshold_rl, temp_lower_threshold_rl)
settle_time_co2_LQR = calculate_settle_time(co2_LQR, co2_upper_threshold, co2_lower_threshold)
settle_time_co2_RL = calculate_settle_time(co2_RL, co2_upper_threshold, co2_lower_threshold)


print(settle_time_temp_LQR)
print(settle_time_temp_RL)
plt.figure(figsize=(10, 6))
plt.plot(time,t_ar_LQR,label="LQR-control")
plt.plot(time,t_ar_RL,label="RL-control")
plt.plot(time,t_set,color="red",label="Setpoint")
plt.vlines(15*40,ymin=0,ymax=40,linestyles="--",color="grey",label="Disturbance")
plt.axvline(settle_time_temp_LQR, color='blue', linestyle=':', label=f"LQR Settle Time: {round(settle_time_temp_LQR)} min ")
plt.axvline(settle_time_temp_RL, color='purple', linestyle=':', label=f"RL Settle Time: {round(settle_time_temp_RL)} min ")
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlabel("Time[Minutes]",fontsize=11)
plt.ylabel("Temperature[°C]",fontsize=11)
plt.xlim(0,1000)
plt.ylim(18.9,36.1)
plt.title("Room temperature comparison on state space model", fontsize=14)
plt.tight_layout()
plt.savefig("ss_room_temperature_comparison.png")


plt.figure(figsize=(10, 6))
plt.plot(time,co2_LQR,label="LQR-control")
plt.plot(time,co2_RL,label="RL-control")
plt.vlines(15*40,ymin=0,ymax=1500,linestyles="--",color="grey",label="Disturbance")
plt.axvline(settle_time_co2_LQR, color='blue', linestyle=':', label=f"LQR Settle Time: {round(settle_time_co2_LQR)} min ")
plt.axvline(settle_time_co2_RL, color='purple', linestyle=':', label=f"RL Settle Time {round(settle_time_co2_RL)} min ")
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0,1000)
plt.ylim(300,1500)
plt.legend(loc='best')

plt.xlabel("Time[Minutes]",fontsize=11)
plt.ylabel("CO2 concentration[ppm]",fontsize=11)
plt.title("Room CO2 concentration comparison on state space model", fontsize=14)
plt.tight_layout()
plt.savefig("ss_co2_concentration_comparison.png")


plt.figure(figsize=(10, 6))
plt.plot(time, rc_state_LQR, label="LQR-control")
plt.plot(time, rc_state_RL, label="RL-control")
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0,1000)
plt.yticks(ticks=range(2), labels=["Ventilation","Recircilation"])
plt.ylim(-0.5,1.5)
plt.title("RC State comparison on state space model", fontsize=14)
plt.xlabel("Time[Minutes]",fontsize=11)
plt.savefig("ss_rc_state_comparison.png")

plt.tight_layout()
u_RL_l=np.array(u_RL_l)
u_LQR_l=np.array(u_LQR_l)

powerkw_RL = (u_RL_l[:,0] * 150 / 100 + u_RL_l[:,0] * 150 / 100 +
                        u_RL_l[:,1] * 1150 / 100 + u_RL_l[:,2] * 1150 / 100 +
                        abs(u_RL_l[:,3]) * 2000 / 100) / 1000

powerkw_LQR = (u_LQR_l[:,0] * 150 / 100 + u_LQR_l[:,0] * 150 / 100 +
                        u_LQR_l[:,1] * 1150 / 100 + u_LQR_l[:,2] * 1150 / 100 +
                        abs(u_LQR_l[:,3]) * 2000 / 100) / 1000

time_diff_RL = np.diff(time, prepend=0) / 4
time_diff_LQR = np.diff(time, prepend=0) / 4

# Calculate energy for each time interval
energy_kWh_RL = powerkw_RL.T * time_diff_RL
energy_kWh_LQR = powerkw_LQR.T * time_diff_LQR

# Calculate cumulative energy
cumulative_energy_kWh_RL= np.cumsum(energy_kWh_RL)
cumulative_energy_kWh_LQR= np.cumsum(energy_kWh_LQR)

plt.figure(figsize=(10, 6))
plt.plot(time, powerkw_LQR, label="LQR-control")
plt.plot(time, powerkw_RL, label="RL-control")
plt.xlabel("Time [Minutes]",fontsize=11)
plt.ylabel("Total Power Consumption [kW]",fontsize=11)
plt.title("Estimated total power consumption over time on state space model", fontsize=14)
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 1000)
plt.ylim(0, 6)
plt.tight_layout()
plt.savefig("ss_total_power_consumption.png")



plt.figure(figsize=(10, 6))
plt.plot(time, cumulative_energy_kWh_LQR, label="LQR-control")
plt.plot(time, cumulative_energy_kWh_RL, label="RL-control")
plt.xlabel("Time [Minutes]",fontsize=11)
plt.ylabel("Cumulative Energy Consumption [kWh]",fontsize=11)
plt.title("Estimated cumulative energy consumption over time on state space model", fontsize=14)
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 1000)
plt.tight_layout()
plt.savefig("ss_cumulative_energy_consumption.png")


# Plotting actuators
plt.figure(figsize=(10, 6))
plt.plot(time, u_RL_l[:,1], label="ECH 1 %")
plt.plot(time, u_RL_l[:,2], label="ECH 2 %")
plt.plot(time, u_RL_l[:,3], label="HVAC %")
plt.plot(time,  u_RL_l[:,4], label="Bypass %")
plt.plot(time, u_RL_l[:,0], label="RQF")
plt.xlabel("Time [Minutes]",fontsize=11)
plt.ylabel("Percentage [%]",fontsize=11)
plt.title("RL-control Actuator Percentages Over Time", fontsize=14)
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 1000)
plt.tight_layout()
plt.savefig("ss_rl_control_actuator_percentages.png")




# Plotting actuators
plt.figure(figsize=(10, 6))
plt.plot(time, u_LQR_l[:,1], label="ECH 1 %")
plt.plot(time, u_LQR_l[:,2], label="ECH 2 %")
plt.plot(time, u_LQR_l[:,3], label="HVAC %")
plt.plot(time, u_LQR_l[:,4], label="Bypass %")
plt.plot(time, u_LQR_l[:,0], label="RQF")
plt.xlabel("Time [Minutes]",fontsize=11)
plt.ylabel("Percentage [%]",fontsize=11)
plt.title("LQR-control Actuator Percentages Over Time", fontsize=14)
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 1000)
plt.tight_layout()
plt.savefig("ss_LQR_control_actuator_percentages.png")

plt.show()

