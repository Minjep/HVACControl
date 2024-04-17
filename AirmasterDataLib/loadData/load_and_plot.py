# Script to load variables from Airmaster and plot them

import numpy as np
import matplotlib.pyplot as plt
import pickle
import json
import datetime
import os
import pandas as pd
from datetime import datetime, timedelta, timezone
from AirmasterDataLib.config import get_dataset_file, get_telemetry_file

def load_data(filename=None):
    if filename is None:
        filename = get_dataset_file()
        print(filename)
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data
def print_sensor_names(data,tele_map):
    for key in data.keys():
        if key in tele_map:
            print(f"key:{key} name:{translate_code(tele_map,key)}")
def extract_sensor_data(data, sensor_name):
    return data[sensor_name]
def plot_sensor_data(ax,sensor_data, sensor_name):
    Xep=sensor_data["timestamps"]
    X=[datetime.fromtimestamp(Xep[i]) for i in range(len(Xep))]
    Y=sensor_data["values"]
    ax.plot(X,Y,"o-", label=sensor_name)
    #ax.set_xticklabels(X, rotation=45) 
    ax.legend(loc="upper right") 
def load_telemetry():
    # Load the telemetry data from the file
    with open(get_telemetry_file()) as f:
        data = json.load(f)
    return data
def translate_telemetry(tele_data):
    # Create a hashmap between the telemetry name and the code
    telemetry_map = {}
    # create a map between the telemetry name and the code
    for telemetry in tele_data:
        if 'code' in telemetry:
            telemetry_map[telemetry['code']] = telemetry['name']
    return telemetry_map
def translate_code(telemetry_map, code):
    # Translate the code to the telemetry name
    return telemetry_map[code]




def main():
    current_directory = os.getcwd()
    relative_path_to_file = "../../data-2/data-2"
    folderPath = os.path.join(current_directory, relative_path_to_file)
    filename=folderPath+r"/404000113/404000113.pkl"
    data=load_data(filename)
    teledata=load_telemetry()
    tele_map=translate_telemetry(teledata)
    print_sensor_names(data,tele_map)
    dataToBeConverted = {}
    for key in data.keys():
        if key in tele_map:
            dataName = key
            ExtractedData = extract_sensor_data(data, dataName)
            dataValues = ExtractedData['values']
            unixTime = ExtractedData['timestamps']
            unixStart = min(unixTime)
            unixEnd = max(unixTime)
            unixTimeExpanded = np.arange(1, unixEnd - unixStart + 2) + unixStart-1
            rowList = []
            meassureIndex = 0
            for index in range(len(unixTimeExpanded)):
                # Convert Unix time to datetime object
                utc_datetime = datetime.utcfromtimestamp(unixTimeExpanded[index])

                # Add UTC+1 offset
                utc_plus_one = utc_datetime.replace(tzinfo=timezone.utc) + timedelta(hours=1)

                # Convert to desired format
                formatted_date = utc_plus_one.strftime("%H:%M:%S - %d/%m/%Y")
                if unixTimeExpanded[index] == unixTime[meassureIndex+1]:
                    meassureIndex = meassureIndex + 1
                # Construct dictionary and append to array1
                row = {'unix time': unixTimeExpanded[index], 'real time': formatted_date, 'values': dataValues[meassureIndex]}
                rowList.append(row)

            dataToBeConverted[key] = pd.DataFrame(rowList)
            print(key)
    # Pad lists to the same length
    with open('processedData.pkl', 'wb') as f:
        pickle.dump(dataToBeConverted, f)
            

            
if __name__ == "__main__":

    main()