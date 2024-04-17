"""Use this file to setup config before running"""
import os
import AirmasterDataLib.config as config
# Add personal folders to this path, do not delete any of the folders
DatasetFolders = [
    r"C:\Users\jeppe\OneDrive - Aalborg Universitet\8. Semester Shared work\data_45\404000135",
    r"C:\Users\jeppe\OneDrive - Aalborg Universitet\8. Semester Shared work\data_45\404000138",
    r"C:\Users\jeppe\OneDrive - Aalborg Universitet\8. Semester Shared work\data_45\404000140",
]
# add specific pkl files to this path
Files = [
    r"C:\Users\jeppe\OneDrive - Aalborg Universitet\8. Semester Shared work\data_45\404000135\404000135.pkl",
    r"C:\Users\jeppe\OneDrive - Aalborg Universitet\8. Semester Shared work\data_45\404000138\404000138.pkl",
    r"C:\Users\jeppe\OneDrive - Aalborg Universitet\8. Semester Shared work\data_45\404000140\404000140.pkl",
]

# add specific telemetry files to this path
TelemetryFiles = [
    r"AirmasterControl\AirMasterData\telemetry.json",
    r"AirMasterData\telemetry.json",
    r"C:\Users\jeppe\gits\HVACControl\AirMasterData\telemetry.json",
]

# Loops through the folders and loads the data to check if they are available
OptionListFolder=[]
for folder in DatasetFolders:
    if os.path.exists(folder):
        OptionListFolder.append(folder)
OptionListFiles=[]
for file in Files:
    if os.path.exists(file):
        OptionListFiles.append(file)

for file in TelemetryFiles:
    
    if os.path.exists(file):
        print(f"Telemetry file found: {file}")
        config.set_telemetry_file(file)
        break

# Show the available folders to the user and let them choose
print("Available folders:")
for i in range(len(OptionListFolder)):
    print(f"{i+1}: {OptionListFolder[i]}")
chosenFolder = int(input("Choose a folder num: "))
config.set_folder(OptionListFolder[chosenFolder-1])

# Show the available files to the user and let them choose
print("Available files:")
for i in range(len(OptionListFiles)):
    print(f"{i+1}: {OptionListFiles[i]}")
chosenFile = int(input("Choose a file num: "))
config.set_file(OptionListFiles[chosenFile-1])
