from configparser import ConfigParser
import os

config = ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)



def get_dataset_folder():
    if get_config_key("__FOLDERPATH__") == None:
        assert False, "No path defined in use set_folder(path) to set the path of the folder containing the pkl files"
    else:
        return get_config_key("__FOLDERPATH__")
def get_dataset_file():
    if get_config_key("__pklfilepath__") == None:
        assert False, "No path defined in use set_file(filepath) to set the path of pkl files"
    else:
        return get_config_key("__pklfilepath__")

def get_telemetry_file():
    if get_config_key("__TELEMETRYFILE__") == None:
        assert False, "No path defined in use set_config_file(value,key) to set the path of the telemetry file"
    else:
        return get_config_key("__TELEMETRYFILE__")

def get_config_key(key):
    if (config.get("DEFAULT", key)!=None
        and config.get("DEFAULT", key)!=""):
        return config.get("DEFAULT", key)
    else:
        return None    

def set_folder(path):
    config.set("DEFAULT", "__FOLDERPATH__", path)
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def set_file(filepath):
    config.set("DEFAULT", "__pklfilepath__", filepath)
    print(filepath)

    with open(config_path, 'w') as configfile:
        config.write(configfile)
def set_telemetry_file(filepath):
    config.set("DEFAULT", "__TELEMETRYFILE__", filepath)
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def set_config_file(value, key):
    config.set("Defualt", value, key)
    with open(config_path, 'w') as configfile:
        config.write(configfile)