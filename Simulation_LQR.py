from numba import jit
import numpy as np
import random
import csv
import os
from multiprocessing import Pool
import time

class LQR_Controller:
    def __init__(self): 
        self.x_recirc_est = np.array([[0, 0],
                                      [0, 0]])
        
        self.A_recirc = np.array([[810.5, 8.8], 
                                  [48.0, 879.8]]) * 1e-3
        
        self.B_recirc = np.array([[-1.2, -0.1, -0.2, 0.0, -1.1, -2.2],
                                  [0.5, 0.1, 1.3, -0.1, 0.9, 1.8]]) * 1e-3
        
        self.C_recirc = np.array([[-60.7, -1.8],
                                  [-2711.0, -3222.3]])
        
        self.C_recirc_inv = np.array([[-0.0169, 0.0000],
                                      [0.0142, -0.0003]])
        
        self.K_recirc = ([[-429, 23.915],
                          [-172.15, 9.5906],
                          [174.2, -9.7021],
                          [-578.64, 32.2],
                          [-20.622, 6.2327],
                          [0, 0]])
        self.L_recirc = np.array([[-0.022602, -9.3051*1e-05], 
                                  [-0.016509, 0.00019963]]) 
    
        self.x_vent_est = np.array([[0, 0],
                                    [0, 0]])
    
        self.A_vent = np.array([[913.3, -78.6], 
                                [288.0, 144.6]]) * 1e-3
        
        self.B_vent = np.array([[-0.7, -0.3, 0.3, -0.2, -5.5, -5.2],
                                [1.5, 0.3, -0.1, -0.8, 31.6, -0.9]]) * 1e-3
        
        self.C_vent = np.array([[-31.3, 0.4],
                                [-1141.8, 755.0]])
        
        self.C_vent_inv = np.array([[-0.0326, 0.0000],
                                    [-0.0493, 0.0014]])
        
        self.L_vent = np.array([[0, 0], 
                                [0, 0]]) 
        
        self.K_vent = ([[0, 0],
                        [0, 0],
                        [0, 0],
                        [0, 0],
                        [0, 0],
                        [0, 0]])
        
        self.outputs_est = ([[0],
                             [0]])
        
        self.inputs = ([[0],
                        [0],
                        [0],
                        [0],
                        [0],
                        [0]])
        
        self.outputs = ([[0],
                         [0]])
        
        self.references = np.array([[0], 
                                    [0]])
        
        self.N_dash =  np.array([[0, 0],
                                 [0, 0]])
        
        self.damper_recirc_state = 0 # 0 = ventilation, 1=recirculation
        
        self.T_cool = 0
        self.co2_high = 0
        self.T_ao = 0
        self.T_heat = 0
        self.co2_low=0
        self.airmaster_state=2
        
    def set_current_damper_recirc_state(self):
        alpha = 1 + min(4, (self.outputs[0] - self.references[0])) / 4
        self.co2_low = alpha * 600
        self.co2_high = alpha * 900
        if self.damper_recirc_state == 0: #ventilation
            if(self.outputs[1]>self.co2_high or (self.outputs[0]>self.T_cool and self.T_ao <(self.outputs[0]-0.5)) or (self.outputs[0]<self.T_heat and self.T_ao>(self.outputs[0]+0.5))):
                self.damper_recirc_state = 1
        else: #recirculation
            if(self.outputs[1]<self.co2_low or (self.outputs[0] > self.T_cool and self.T_ao>(self.outputs[0]+0.5)) or (self.outputs[0]<self.T_heat and self.T_ao<(self.outputs[0]-0.5))):
                self.damper_recirc_state = 0
        
        

    def estimate_next_state(self):
        """have to be rund of the respons from the simulataion
        """
        if self.damper_recirc_state == 0: #ventilation
            self.x_vent_est = self.A_vent*self.x_vent_est + self.B_vent*self.inputs+self.L_vent*(self.C_vent*self.x_vent_est-self.outputs)
        else: #recirculation
            self.x_recirc_est = self.A_recirc*self.x_recirc_est + self.B_recirc*self.inputs+self.L_recirc*(self.C_recirc*self.x_recirc_est-self.outputs)
        
    def state_resetting(self):
        """This function have to be run after calculate_input and the simuleted respons corresponding the the inputs 
        Because the first self.x_xxxx_est is corresponding to the current time but the second is for one timestep
        into the future.
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
        if self.damper_recirc_state == 0: #ventilation
            self.inputs = self.K_vent*self.x_vent_est + self.N_dash * self.references
        else: #ventilation
            self.inputs = self.K_recirc*self.x_recirc_est + self.N_dash * self.references

    def initialize_variables(self,temp_ref, co2_ref,temp_init,co2_init,t_ao):
        self.references[0] = temp_ref
        self.references[1] = co2_ref
        self.T_cool = self.references[0] + 1
        self.T_heat = self.references[0] - 1
        self.outputs[0] = temp_init
        self.outputs[1] = co2_init    
        self.T_ao = t_ao
        




if __name__ == "__main__":
    env = LQR_Controller()
    env.initialize_variables(20,500,20,500,10)
    while(1): #main loop
        env.set_current_damper_recirc_state()
        env.estimate_next_state()
        env.calculate_inputs()
        """Send inputs to simulation
        return new outputs
        """
        env.state_resetting()