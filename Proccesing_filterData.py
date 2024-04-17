import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
from AirmasterDataLib.loadData import load_data, load_telemetry, translate_telemetry
from AirmasterDataLib.process.filter_data import getData,convertUnixToRealTime, convertUnixTimeAndFillMissingData, makePklFile, loadPklFile,adjustStartEndTime,removeNightAndWeekend,detect_and_filter_outliers,adjustResolution
def create15minIntervals_csv(force=False):
    # create 15 min intervals and the other pkl files, if they do not exist
    if force or not os.path.exists('processedData'):
        print ("processedData not found, converting data to unix time and filling missing data...")
        dataOld, tele_map = getData()
        columnsToBeRemoved = ['tvoc_ai','tvoc_ar','tvoc_ae','tvoc_ao','trt']
        convertUnixTimeAndFillMissingData(dataOld,tele_map,columnsToBeRemoved,makeFile = True)
    if force or not os.path.exists('croppedData'):
        print ("croppedData not found, adjusting start and end time...")
        dataNew = loadPklFile("processedData.pkl")
        adjustStartEndTime(dataNew,makeFile = True)
    if force or not os.path.exists('dayTimeData'):
        print ("dayTimeData not found, adjusting resolution...")
        dataCrop = loadPklFile('croppedData.pkl')
        removeNightAndWeekend(dataCrop,makeFile = True)
    if force or not os.path.exists('finalData'):
        print ("finalData not found, detecting and filtering outliers...")
        dataDay = loadPklFile("dayTimeData.pkl")
        var_to_be_detected = ['rqf','rqt','t_ai','t_ar','t_ao','t_aop','t_aio','t_vti','rh_ai','rh_ar','rh_ae','rh_ao','co2_ai','co2_ar','co2_ao']
        detect_and_filter_outliers(dataDay,var_to_be_detected,4,makeFile = True) 



def main():
    create15minIntervals_csv(force=False)       

if __name__ == "__main__":
    main()
    
    
        
    
    
    
    
    
    



