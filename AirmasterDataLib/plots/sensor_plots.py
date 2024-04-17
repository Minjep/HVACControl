"""
File to plot the sensor data from the data folder
"""
from ..loadData import load_and_plot

import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime
    
def plot_sensor_data_unix(ax,sensor_data, sensor_name):
    X=sensor_data["unix time"]
    # X=[datetime.datetime.fromtimestamp(Xep[i]) for i in range(len(Xep))]
    Y=sensor_data["values"]
    ax.plot(X,Y, label=sensor_name)
     
    #ax.set_xticklabels(X, rotation=45) 
    ax.legend(loc="upper right") 
def plot_sensortype_list(data,tele_map, reqested_sensors,title):
    # extract the sensor data
    _,ax=plt.subplots(len(reqested_sensors),1,sharex=True)
    for i in range(len(reqested_sensors)):
        sensor=load_and_plot.extract_sensor_data(data, reqested_sensors[i])

        load_and_plot.plot_sensor_data(ax[i],sensor, load_and_plot.translate_code(tele_map,reqested_sensors[i]))
        # set linked x-axis
    plt.xticks(rotation=45, ha='right')
    plt.suptitle(title)
    plt.tight_layout()

def plot_sensortype_list_unix(data, tele_map,reqested_sensors,title):
    # extract the sensor data
    _,ax=plt.subplots(len(reqested_sensors),1,sharex=True)
    sensor={}
    sensor["unix time"] = data['unix time']
    for i in range(len(reqested_sensors)):
        sensor['values']=data[reqested_sensors[i]]
        plot_sensor_data_unix(ax[i],sensor, load_and_plot.translate_code(tele_map,reqested_sensors[i]))
        # set linked x-axis
    unix_times = data['unix time']
    start_time = min(unix_times) // 3600 * 3600  # Round to the nearest hour
    end_time = max(unix_times) // 3600 * 3600 + 3600  # Round to the nearest hour and add an hour
    x_ticks = np.arange(start_time, end_time, 3600*24)  # Tick every 8'th hour

    # Convert Unix time to datetime for better readability
    date_ticks = [datetime.fromtimestamp(ts).strftime("%H:%M:%S - %d/%m/%Y") for ts in x_ticks]

    # Set the custom ticks and labels
    plt.xticks(x_ticks, date_ticks)
    plt.xticks(rotation=45) 
    plt.suptitle(title)
    plt.tight_layout()
        
def plotAllSensorData_unix(data, tele_map):
    # plot the sensor data
    reqested_sensors=["rqf","rqt","op_mode","msm_state"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Requested values and states")
    print("Requested values and states")
    # heat related measurements
    reqested_sensors=["ech_1_pct","ech_2_pct","hvac_pct"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Heat related values")
    print("Heat related values")
    # Temperature related measurements
    reqested_sensors=["t_ai","t_ar","t_ae","t_ao"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Temperature related values")
    print("Temperature related values")
    # internal temperature related measurements
    reqested_sensors=["t_aop","t_aio","t_aii","t_vto","t_vti"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Internal temperature related values")
    print("Internal temperature related values")
    # fan related measurements
    reqested_sensors=["fan_sup_1_pct","fan_ext_1_pct"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Fan related values")
    print("Fan related values")
    # humidity related measurements
    reqested_sensors=["rh_ai","rh_ar","rh_ae","rh_ao"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Humidity related values")
    print("Humidity related values")
    # CO2 related measurements
    reqested_sensors=["co2_ai","co2_ar","co2_ae","co2_ao"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"CO2 related values")
    print("CO2 related values")
    # power related measurements
    reqested_sensors=["damper_recirc_in_pos","damper_bypass_pos"] #,"trt"
    plot_sensortype_list(data,tele_map,reqested_sensors,"damper position") # and target room temperature
    print("damper position and target room temperature")
    
def main():
    # set the path to the folder where the data is stored
    current_directory = os.getcwd()
    relative_path_to_file = "../../data-2/data-2"
    folderPath = os.path.join(current_directory, relative_path_to_file)
    filename=folderPath+r"/404000113/404000113.pkl"
    data=load_and_plot.load_data(filename)
    teledata=load_and_plot.load_telemetry()
    tele_map=load_and_plot.translate_telemetry(teledata)
    # print the sensor names
    load_and_plot.print_sensor_names(data,tele_map)
    
    plt.plot(data['rqf']['timestamps'],data['rqf']['values'])
    plt.xlabel("Unix time")
    plt.ylabel("Requested flow in percent")
    plt.title("Requested flow")
    # plot the sensor data
    reqested_sensors=["rqf","rqt"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Requested values")
   
    # heat related measurements
    reqested_sensors=["ech_1_pct","hp_pct","hvac_pct"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Heat related values")
    # Temperature related measurements
    reqested_sensors=["t_ai","t_ar","t_ae","t_ao"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Temperature related values")
    # internal temperature related measurements
    reqested_sensors=["t_aop","t_aio","t_aii","t_vto","t_vti"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Internal temperature related values")
    # humidity related measurements
    reqested_sensors=["rh_ai","rh_ar","rh_ae","rh_ao"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Humidity related values")
    # CO2 related measurements
    reqested_sensors=["co2_ai","co2_ar","co2_ae","co2_ao"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"CO2 related values")
    # power related measurements
    reqested_sensors=["fan_sup_pm_1_p_act","fan_ext_pm_1_p_act","hpm_pm_p_act","fan_sup_1_pwr","fan_ext_1_pwr"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Power related values")
    # fan related measurements
    reqested_sensors=["fan_sup_flow","fan_ext_flow"]
    plot_sensortype_list(data,tele_map,reqested_sensors,"Fan related values")
    plt.show()

if __name__ == "__main__":
    main()
    