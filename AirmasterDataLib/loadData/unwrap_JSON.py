"""
File to unwrap the JSON files from Airmaster and save them as pickle files and csv files
"""

import matplotlib.pyplot as plt
import datetime
import json
import os
import sys
import pickle
def jsonlist_to_dict(jsonFiles: list) -> dict:
    """
    Loop through all the json files and create a dictionary with the serial number as the key and a subdictionary as the value.

    Parameters:
    ----------
    jsonFiles: list
        A list of all the json files in the folder.

    Returns:
    -------
    dict
        A dictionary with the serial number as the key and a subdictionary as the value.
    """
    GiantDict = {}
    # create a subdictionary for each serial number in the json files
    for file in jsonFiles:
        serialNumber = file.split("_")[0]
        if serialNumber not in GiantDict:
            GiantDict[serialNumber] = {}
            # create a list of all the json files for each serial number
            GiantDict[serialNumber]["Files"] = []
            # also create a list of all the "from" values for each serial number
            GiantDict[serialNumber]["From"] = []
        GiantDict[serialNumber]["Files"].append(file)
    return GiantDict

def sort_dict(GiantDict: dict,folderPath:str) -> dict:
    """
    Sort the files by the "from" value and concatenate the data. 


    Parameters:
    ----------
    GiantDict: dict
        A dictionary with the serial number as the key and a subdictionary as the value.
    
    Returns:
    -------
    dict
        A dictionary with the serial number as the key and a subdictionary as the value.
    """
    for serialNumber in GiantDict:  
        # loop all files and sort by the key "from"
        for file in GiantDict[serialNumber]["Files"]:
            data=json.load(open(folderPath + "\\" + file))
            # Check if the key "from" exists in the json file
            if "from" in data:
                GiantDict[serialNumber]["From"].append(data["from"])
        # now sort the files by the "from" value
        GiantDict[serialNumber]["SortedFiles"] = [x for _,x in sorted(zip(GiantDict[serialNumber]["From"],GiantDict[serialNumber]["Files"]))]

            
    # now loop  all the sorted files for each serial number and concatenate the data
    for serialNumber in GiantDict:
        for file in GiantDict[serialNumber]["SortedFiles"]:
            data=json.load(open(folderPath + "\\" + file))
            if "results" in data:
                # loop dicts in results 
                for sensor in data["results"]:
                    if sensor["timestamps"] == []:
                        continue
                    if sensor["name"] not in GiantDict[serialNumber]:
                        GiantDict[serialNumber][sensor["name"]] = {}
                        GiantDict[serialNumber][sensor["name"]]["timestamps"] = []
                        GiantDict[serialNumber][sensor["name"]]["values"] = []
                    GiantDict[serialNumber][sensor["name"]]["timestamps"].extend(sensor["timestamps"])
                    GiantDict[serialNumber][sensor["name"]]["values"].extend(sensor["values"])
    return GiantDict
def save_as_pickle(GiantDict: dict, folderPath: str):
    """
    Save the dictionary as a pickle file and save each sensor as a csv file in the folder.

    Parameters:
    ----------
    returns: bool
        True if the function runs without errors.
    """
    try:
        for serialNumber in GiantDict:
            # create a folder for each serial number
            if not os.path.exists(folderPath + "\\" + serialNumber):
                os.mkdir(folderPath + "\\" + serialNumber)
            # save each serial number as a pickle file
            with open(folderPath + "\\" + serialNumber + "\\" + serialNumber + ".pkl", 'wb') as handle:
                pickle.dump(GiantDict[serialNumber], handle, protocol=pickle.HIGHEST_PROTOCOL)
        
            # save each sensor as a csv file in the folder
            for sensor in GiantDict[serialNumber]:
                if sensor == "Files" or sensor == "From" or sensor == "SortedFiles":
                    continue
                with open(folderPath + "\\" + serialNumber + "\\" + sensor + ".csv", 'w') as file:
                    for i in range(len(GiantDict[serialNumber][sensor]["timestamps"])):
                        file.write(str(GiantDict[serialNumber][sensor]["timestamps"][i]) + "," + str(GiantDict[serialNumber][sensor]["values"][i]) + "\n")
    except Exception as e:
        print("Error: ", e)
        return False    
    return True

def load_raw_dataset_from_path(folderPath: str) -> dict:
    """
    This function loads the dataset from the given path and returns it as a dictionary.

    Parameters:
    ----------
    folderPath: str
        The path to the folder containing the dataset.

    Returns:
    -------
    dict
        The dataset as a dictionary.
    
    """

    # list all files in folder
    jsonFiles=os.listdir(folderPath)
    # Keep only the json files
    jsonFiles = [file for file in jsonFiles if file.endswith(".json")]

    # create a dictionary with the serial number as the key and a subdictionary as the value
    GiantDict = jsonlist_to_dict(jsonFiles)
   
    # sort the files by the "from" value and concatenate the data
    GiantDict = sort_dict(GiantDict,folderPath)
    # save the dictionary as a pickle file and save each sensor as a csv file in the folder
    save_as_pickle(GiantDict, folderPath)

    return GiantDict

def load_dataset_from_serial_number(serialNumber: str,folderPath:str) -> dict:
    """
    This function loads the dataset from the given serial number and returns it as a dictionary.

    Parameters:
    ----------
    serialNumber: str
        The serial number of the dataset.

    Returns:
    -------
    dict
        The dataset as a dictionary.
    
    """
    try:
        with open(folderPath + "\\" + serialNumber + "\\" + serialNumber + ".pkl", 'rb') as handle:
            GiantDict = pickle.load(handle)
    except Exception as e:
        print("Error: ", e)
        return False
    return GiantDict


def main():
    """
    Main function to run the program.
        """
    folderPathJakob=r"/Users/jakob/Library/CloudStorage/OneDrive-AalborgUniversitet/8. Semester Shared work/data_45"
    folderPathJeppe=r"C:\Users\jeppe\OneDrive - Aalborg Universitet\8. Semester Shared work\data_45"
    folderPath=folderPathJeppe

    readRaw=1
    if readRaw:
        folderPath = sys.argv[1]
        load_raw_dataset_from_path(folderPath)
    else:
        folderPath = sys.argv[1]
        serialNumber = sys.argv[2]
        load_dataset_from_serial_number(serialNumber,folderPath)
    return True


if __name__ == "__main__":
    main()