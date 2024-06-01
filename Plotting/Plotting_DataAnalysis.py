from AirmasterDataLib.process import filter_data as FND
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta, timezone
import pandas as pd
import numpy as np
from AirmasterDataLib.loadData import load_and_plot


def rqf_org(data):
    realtime=[]
    variable = 'rqf' 
    dataStart = 49
    dataEnd = 100
    for i in range(len(data[variable]['timestamps'])):
        temp = FND.convertUnixToRealTime(data[variable]['timestamps'][i])
        realtime.append(temp) 
    
    #plt.scatter(realtime[dataStart:dataEnd],data['rqf']['values'][dataStart:dataEnd])
    plt.scatter(data[variable]['timestamps'][dataStart:dataEnd],data[variable]['values'][dataStart:dataEnd],s=15)
    
    unix_times = data[variable]['timestamps'][dataStart:dataEnd]
    start_time = min(unix_times) // 3600 * 3600  # Round to the nearest hour
    end_time = max(unix_times) // 3600 * 3600 + 3600  # Round to the nearest hour and add an hour
    x_ticks = np.arange(start_time, end_time, 3600/2)  # Tick every 30 minute

    # Convert Unix time to datetime for better readability
    date_ticks = [datetime.fromtimestamp(ts).strftime("%H:%M:%S - %d/%m/%Y") for ts in x_ticks]

    # Set the custom ticks and labels
    plt.xticks(x_ticks, date_ticks)
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
    
    #plt.xticks(data['rqf']['timestamps'][dataStart:dataEnd],rotation=90)
    plt.xlabel("Time")
    plt.ylabel("Requested flow in percent")
    plt.title("Requested flow")
    plt.tight_layout()
    
def rqf_missing_data_points(data,dataOrg):
    # Define the datetime string
    start_time = "00:01:00 - 16/02/2024"
    end_time = "23:59:00 - 16/02/2024"

    # Convert the datetime string to a datetime object
    datetime_obj_start = datetime.strptime(start_time, "%H:%M:%S - %d/%m/%Y")
    datetime_obj_end = datetime.strptime(end_time, "%H:%M:%S - %d/%m/%Y")

    # Convert the datetime object to Unix timestamp
    start_time_unix = datetime_obj_start.timestamp()
    end_time_unix = datetime_obj_end.timestamp()
    
    filtered_data = data['rqf'][(data['rqf']['unix time'] >= start_time_unix) & (data['rqf']['unix time'] <= end_time_unix)]

    plt.plot(filtered_data['unix time'], filtered_data['values'],'C0')  # Replace 'your_data_column' with your actual data column
    plt.scatter(dataOrg['rqf']['timestamps'][49:100],dataOrg['rqf']['values'][49:100],color='C1',s=15 ,zorder=2)
    

    unix_times = data['rqf']['unix time'][(data['rqf']['unix time'] >= start_time_unix) & (data['rqf']['unix time'] <= end_time_unix)]
    start_time = min(unix_times) // 3600 * 3600  # Round to the nearest hour
    end_time = max(unix_times) // 3600 * 3600 + 3600  # Round to the nearest hour and add an hour
    x_ticks = np.arange(start_time, end_time, 3600)  # Tick every hour

    # Convert Unix time to datetime for better readability
    date_ticks = [datetime.fromtimestamp(ts).strftime("%H:%M:%S - %d/%m/%Y") for ts in x_ticks]

    # Set the custom ticks and labels
    plt.xticks(x_ticks, date_ticks)
    plt.xticks(rotation=90)  
    
    plt.xlabel("Time")
    plt.ylabel("Requested flow in percent")
    plt.title("Requested flow")
    plt.tight_layout()
    
def t_ao_all_data(data):
    start_time = "00:01:00 - 21/02/2024"
    end_time = "23:59:00 - 28/02/2024"

    # Convert the datetime string to a datetime object
    datetime_obj_start = datetime.strptime(start_time, "%H:%M:%S - %d/%m/%Y")
    datetime_obj_end = datetime.strptime(end_time, "%H:%M:%S - %d/%m/%Y")

    # Convert the datetime object to Unix timestamp
    start_time_unix = datetime_obj_start.timestamp()
    end_time_unix = datetime_obj_end.timestamp()
    
    
    
    
    
    filtered_data = data['t_ao'][(data['t_ao']['unix time'] >= start_time_unix) & (data['t_ao']['unix time'] <= end_time_unix)]
    
    
    
    plt.plot(filtered_data['unix time'][::60], filtered_data['values'][::60])  # Replace 'your_data_column' with your actual data column
    data_to_be_conditioned = pd.to_datetime(filtered_data['real time'], format='%H:%M:%S - %d/%m/%Y')
    condition_to_color = (
        (data_to_be_conditioned.dt.hour < 5) |
        (data_to_be_conditioned.dt.hour >= 17) |
        (data_to_be_conditioned.dt.dayofweek >= 5)
    )

    # Plot each colored segment separately
    plt.fill_between(filtered_data['unix time'], filtered_data['values'], where=condition_to_color, color='red', alpha=0.5)
    
    unix_times = filtered_data['unix time']
    start_time = min(unix_times) // 3600 * 3600  # Round to the nearest hour
    end_time = max(unix_times) // 3600 * 3600 + 3600  # Round to the nearest hour and add an hour
    x_ticks = np.arange(start_time, end_time, 3600*8)  # Tick every 8'th hour

    # Convert Unix time to datetime for better readability
    date_ticks = [datetime.fromtimestamp(ts).strftime("%H:%M:%S - %d/%m/%Y") for ts in x_ticks]

    # Set the custom ticks and labels
    plt.xticks(x_ticks, date_ticks)
    plt.xticks(rotation=90)  
    plt.xlabel("Time")
    plt.ylabel("Temperature outside [°C]")
    plt.title("Temperature outside over time")
    plt.tight_layout()
    
def t_ao_only_day_data(data,data_all):
    start_time = "05:30:00 - 21/02/2024"
    end_time = "15:00:00 - 28/02/2024"

    # Convert the datetime string to a datetime object
    datetime_obj_start = datetime.strptime(start_time, "%H:%M:%S - %d/%m/%Y")
    datetime_obj_end = datetime.strptime(end_time, "%H:%M:%S - %d/%m/%Y")

    # Convert the datetime object to Unix timestamp
    start_time_unix = datetime_obj_start.timestamp()
    end_time_unix = datetime_obj_end.timestamp()
    
    filtered_data = data['t_ao'][(data['t_ao']['unix time'] >= start_time_unix) & (data['t_ao']['unix time'] <= end_time_unix)]
    filtered_data_all = data_all['t_ao'][(data_all['t_ao']['unix time'] >= start_time_unix) & (data_all['t_ao']['unix time'] <= end_time_unix)]

    # plt.plot(filtered_data['unix time'], filtered_data['values'])  
    data_to_be_conditioned = pd.to_datetime(filtered_data_all['real time'], format='%H:%M:%S - %d/%m/%Y')
    condition_to_color = (
        (data_to_be_conditioned.dt.time < pd.to_datetime('05:30:00').time())|
        (data_to_be_conditioned.dt.time > pd.to_datetime('17:00:00').time()) |
        (data_to_be_conditioned.dt.dayofweek >= 5)
    )
    condition_to_color=~condition_to_color
    
    condition_switch=[0]
    for i in range(1,len(condition_to_color)):
        if condition_to_color.iloc[i] != condition_to_color.iloc[i-1]:
            condition_switch.append(i)
            
    
    

    # Plot each group of consecutive segments separately
    for i in range(1,int((len(condition_switch)+1)/2)):
        plt.plot(filtered_data_all['unix time'][condition_switch[i*2-2]:condition_switch[i*2-1]],filtered_data_all['values'][condition_switch[i*2-2]:condition_switch[i*2-1]], color='C0')
    plt.plot(filtered_data_all['unix time'][condition_switch[-1]:],filtered_data_all['values'][condition_switch[-1]:], color='C0')
    unix_times = filtered_data['unix time']
    start_time = min(unix_times) // 3600 * 3600  # Round to the nearest hour
    end_time = max(unix_times) // 3600 * 3600 + 3600  # Round to the nearest hour and add an hour
    x_ticks = np.arange(start_time, end_time, 3600*8)  # Tick every 8'th hour

    # Convert Unix time to datetime for better readability
    date_ticks = [datetime.fromtimestamp(ts).strftime("%H:%M:%S - %d/%m/%Y") for ts in x_ticks]

    # Set the custom ticks and labels
    plt.xticks(x_ticks, date_ticks)
    plt.xticks(rotation=90) 
    plt.ylim(0, 10) 
    plt.xlabel("Time")
    plt.ylabel("Temperature outside [°C]")
    plt.title("Temperature outside over time")
    plt.tight_layout()

def illustrate_start_time_issue(data,data_cropped,columnsToShow,tele_map):
    # Create a figure and two subplots
    fig, axs = plt.subplots(1, 2)
    start_time = "22:00:00 - 14/02/2024"
    end_time = "10:00:00 - 15/02/2024"
    datetime_obj_start = datetime.strptime(start_time, "%H:%M:%S - %d/%m/%Y")
    datetime_obj_end = datetime.strptime(end_time, "%H:%M:%S - %d/%m/%Y")
    start_time_unix = datetime_obj_start.timestamp()
    end_time_unix = datetime_obj_end.timestamp()
    filtered_data_cropped = data_cropped[(data_cropped['unix time'] >= start_time_unix) & (data_cropped['unix time'] <= end_time_unix)]
    for key in data.keys():
        if key in columnsToShow:
            filtered_data = data[key][(data[key]['unix time'] >= start_time_unix) & (data[key]['unix time'] <= end_time_unix)]

            # Plot data on the first subplot
            axs[0].plot(filtered_data['unix time'][::60], filtered_data['values'][::60], label=load_and_plot.translate_code(tele_map,key)) 
            
            
            # Plot data on the second subplot
            axs[1].plot(filtered_data_cropped['unix time'][::60], filtered_data_cropped[key][::60],label=load_and_plot.translate_code(tele_map,key))
            
    unix_times = np.arange(start_time_unix, end_time_unix + 1)
    start_time = min(unix_times) // 3600 * 3600  # Round to the nearest hour
    end_time = max(unix_times) // 3600 * 3600 + 3600  # Round to the nearest hour and add an hour
    x_ticks = np.arange(start_time, end_time, 3600)  # Tick every hour
    

    # Adjust layout to prevent overlapping
    date_ticks = [datetime.fromtimestamp(ts).strftime("%H:%M:%S - %d/%m/%Y") for ts in x_ticks]

    axs[0].set_xticks(x_ticks, date_ticks)
    axs[0].set_xticklabels(date_ticks, rotation=90)
    axs[0].set_title('Raw data')
    axs[0].set_xlabel('time', fontsize='large')
    axs[0].set_ylabel('values', fontsize='large')
    axs[0].set_ylim(0, 140)
    axs[0].legend(loc="upper right",fontsize='small')
    
   
    axs[1].set_xticks(x_ticks, date_ticks)
    axs[1].set_xticklabels(date_ticks, rotation=90) 
    axs[1].set_title('Aligned data')
    axs[1].set_xlabel('time', fontsize='large')
    axs[1].set_ylabel('values', fontsize='large')
    axs[1].set_ylim(0, 140)
    axs[1].legend(loc="upper right",fontsize='small')
    
    plt.tight_layout()
    
if __name__ == "__main__":    
    dataOrg, tele_map = FND.getData()
    #rqf_org(dataOrg)
    dataFilledMissingDataPoints = FND.loadPklFile("processedData.pkl")
    # #rqf_missing_data_points(dataFilledMissingDataPoints,dataOrg)
    # #t_ao_all_data(dataFilledMissingDataPoints)
    # #dataDay = FND.loadPklFile("dayTimeData.pkl")
    # #t_ao_only_day_data(dataDay,dataFilledMissingDataPoints)
    dataCropped = FND.loadPklFile('croppedData.pkl')
    columnsToShow = ['rqf','t_ao','t_ar']
    illustrate_start_time_issue(dataFilledMissingDataPoints,dataCropped,columnsToShow,tele_map)
    
    plt.show()
    
    #print("123")