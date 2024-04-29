import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn import preprocessing
import numpy as np

from AirmasterDataLib.process.filter_data import  loadPklFile


def reward_function_one_example():
    data = loadPklFile("finalData.pkl")
    tempAirRoom = data['t_ar']
    CORoom = data['co2_ar']
    COVar = np.std(CORoom)
    tempvar = np.std(tempAirRoom)
    CO_values = np.linspace(0, 1200, 10000)  # Generate 100 evenly spaced points from -10 to 10
    Temp_values = np.linspace(21, 25, 10000)

    # Calculate the corresponding y values using the function f(x) = x^2
    temp_y_values = -((Temp_values-23)/tempvar)**2
    CO_values_addjusted = [max(x, 400) for x in CO_values]
    CO_values_addjusted = np.array(CO_values_addjusted)
    CO_y_values = -((CO_values_addjusted-400)/COVar)**2

    
    # Plot the function
    plt.figure(figsize=(6, 3))
    plt.plot(Temp_values, temp_y_values)

    # Add labels and title
    plt.xlabel('Actual room temperature [℃]')
    plt.ylabel('Reward')
    plt.title('Reward function with a requested room temperature of 23 ℃')

    plt.tight_layout()
    
    plt.figure(figsize=(6, 3))
    plt.plot(CO_values, CO_y_values)

    # Add labels and title
    plt.xlabel('Actual CO2 concentration [PPM]')
    plt.ylabel('Reward')
    plt.title('Reward function based on CO2 concentration')
    plt.tight_layout()
    plt.show()
    
    
def main():
    reward_function_one_example()
   
    
   

if __name__ == "__main__":
    
    main()