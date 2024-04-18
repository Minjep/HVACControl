from ..loadData import load_and_plot
from AirmasterDataLib.config import get_dataset_file
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta, timezone
import pickle
import pandas as pd
import numpy as np
import json
from scipy import stats

def getData():
    data=load_and_plot.load_data()
    teledata=load_and_plot.load_telemetry()
    tele_map=load_and_plot.translate_telemetry(teledata)
    return data, tele_map

def convertUnixToRealTime(unixTime):
    utc_datetime = datetime.utcfromtimestamp(unixTime)
    utc_plus_one = utc_datetime.replace(tzinfo=timezone.utc) + timedelta(hours=1)
    formatted_date = utc_plus_one.strftime("%H:%M:%S - %d/%m/%Y")
    return formatted_date

def convertUnixTimeAndFillMissingData(data,tele_map,columnsToBeRemoved,makeFile=False):
    print('processData')
    dataToBeConverted = {}
    for key in data.keys():
        if key in tele_map and key not in columnsToBeRemoved:
            dataName = key
            ExtractedData = load_and_plot.extract_sensor_data(data, dataName)
            dataValues = ExtractedData['values']
            unixTime = ExtractedData['timestamps']
            
            unixStart = min(unixTime)
            unixEnd = max(unixTime)
            unixTimeExpanded = np.arange(1, unixEnd - unixStart + 2) + unixStart-1
            rowList = []
            meassureIndex = 0 
            
            for index in range(len(unixTimeExpanded)):
                formatted_date = convertUnixToRealTime(unixTimeExpanded[index])
                #This is to make zero order hold on the missing data
                if unixTimeExpanded[index] >= unixTime[meassureIndex+1]:
                    meassureIndex = meassureIndex + 1  
                # Construct dictionary and append to array1
                row = {'unix time': unixTimeExpanded[index], 'real time': formatted_date, 'values': dataValues[meassureIndex]}
                rowList.append(row)
            dataToBeConverted[key] = pd.DataFrame(rowList)
            print(key)
            
    if makeFile:
        makePklFile(dataToBeConverted,'processedData.pkl')
    return dataToBeConverted

def makePklFile(dataToBeConverted,fileName):
    with open(fileName, 'wb') as f:
        pickle.dump(dataToBeConverted, f)
            
def loadPklFile(filename):
    if filename.endswith(".pkl"):  
        with open(filename, 'rb') as f:
            data = pickle.load(f)
    else:
        filename = filename + ".pkl"
        with open(filename, 'rb') as f:
            data = pickle.load(f)
    return data

def adjustResolution(data,resolution):
    print('adjustResolution')
    dataToBeConvereted = data[::60]
    makePklFile(dataToBeConvereted,'resolution'+str(resolution)+'Data.pkl')

def removeNightAndWeekend(data,makeFile=False):
    print('removeNightData')
    real_time_format = pd.to_datetime(data['real time'], format='%H:%M:%S - %d/%m/%Y')
    time_format = real_time_format.dt.time
    start_time = pd.Timestamp('05:30:00').time()
    end_time = pd.Timestamp('17:00:00').time()
    time_mask = (time_format >= start_time) & (time_format <= end_time)
    weekday_mask = real_time_format.dt.weekday.isin(range(0, 5))
    day_time_data = time_mask & weekday_mask
    data = data[day_time_data]
    data = data.reset_index(drop=True)
        
    if makeFile:
        makePklFile(data,'dayTimeData.pkl')
    return data       

def adjustStartEndTime(data,makeFile=False):
    print('adjustStartEndTime')
    firstSharedTime = 0
    lastSharedTime = 10000000000
    dataToBeConverted={}
    firstTime = 10000000000
    for key in data.keys():
        unixTime = data[key]['unix time']
        if unixTime[0] < firstTime:
            firstTime = unixTime[0]
    
    for key in data.keys():
        if key in ['damper_bypass_pos','ech_2_pct']:
            end_timestamp = data[key]['unix time'][0]-1
            desired_realtime={}
            unix_timestamp_list = list(range(firstTime, end_timestamp + 1))
            desired_realtime = [convertUnixToRealTime(timestamp) for timestamp in unix_timestamp_list]
            # for timestampIndex in range(len(unix_timestamp_list)):
            #     desired_realtime[timestampIndex] = convertUnixToRealTime(unix_timestamp_list[timestampIndex])

            desired_values = [0] * len(unix_timestamp_list)

            desired_df = pd.DataFrame({'unix time': unix_timestamp_list,'real time': desired_realtime ,'values': desired_values})

            # Concatenate the original DataFrame with the desired DataFrame
            data[key] = pd.concat([desired_df, data[key]]).reset_index(drop=True)

    
    for key in data.keys():
        unixTime = data[key]['unix time']
        if unixTime[0] > firstSharedTime:
            firstSharedTime = unixTime[0]
        if unixTime[len(unixTime)-1] < lastSharedTime:
            lastSharedTime = unixTime[len(unixTime)-1]
    for key, df in data.items():
        # Find the index range where 'unix time' falls within the desired range
        mask = (df['unix time'] >= firstSharedTime) & (df['unix time'] <= lastSharedTime)
        desired_data = df[mask]

        # Assign the desired data to the dictionary
        dataToBeConverted[key] = desired_data.copy()

        # Reset index if needed
        dataToBeConverted[key].reset_index(drop=True, inplace=True)
    
    merged_df = pd.DataFrame()
    for key, df in dataToBeConverted.items():
        # Extract 'unix time', 'real time', and 'values' columns
        df_subset = df[['unix time', 'real time', 'values']]
        # Rename the 'values' column to the key name
        df_subset = df_subset.rename(columns={'values': key})
        
        # Merge the subset DataFrame with the merged DataFrame
        if merged_df.empty:
            merged_df = df_subset
        else:
            merged_df = pd.merge(merged_df, df_subset, on=['unix time', 'real time'], how='outer')
    
    if makeFile:
        makePklFile(merged_df,'croppedData.pkl')
    return merged_df
         
def fifften_minute_intervals(df):
    # Convert 'real time' to datetime if it's not already
    df['real time'] = pd.to_datetime(df['real time'], format='%H:%M:%S - %d/%m/%Y')

    # Set 'real time' as the index
    df.set_index('real time', inplace=True)

    # Create a dictionary to hold shifted DataFrames
    new_df = {}

    for i in range(900):  # 15 minutes = 15 * 60 = 900 seconds
        shifted_df = df.shift(freq=f'-{i}s').resample('15T').first()
        new_df[i] = shifted_df
        print(i)
        
    for offset_value, df in new_df.items():
        df.to_csv(f'fifften_minute_interval_csv_data/offset_{offset_value}_data.csv')
        print(offset_value)

def detect_and_filter_outliers(data, var_to_be_detected=[],threshold=3.5,makeFile=True):
    outlier_indices={}
    for var in var_to_be_detected:
        z_scores = np.abs(stats.zscore(data[var]))
        outlier_indices[var] = np.where(z_scores > threshold)[0]
        print(var +": " + str(len(outlier_indices[var])))
        for i in range(len(outlier_indices[var])):
            data[var].iloc[outlier_indices[var][i]] = data[var].iloc[outlier_indices[var][i]-1] 
    if makeFile:
        makePklFile(data,'finalData.pkl')
    return data
         

def dataframe_to_csv(data):
    path_name = load_and_plot.get_dataset_file()
    
    
    parts = path_name.split('/')
    HVAC_unit = parts[-1]
    HVAC_unit_without_extension = HVAC_unit.rstrip('.pkl')
    filename = "processed_full_resolution_" + HVAC_unit_without_extension + ".csv"
    
    data.to_csv(filename, index=False) 