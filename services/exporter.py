import os
import time
import json
from enum import Enum
import models.pet as pet
from const import constants


MONITORING_DATA_DIR = os.path.join(constants.BASE_DIR, "monitoring_data")


# convert the data to a dict from the json db
def load_metrics_data(file_name):
    # composes the file path by the dir and the file name
    file_path = os.path.join(MONITORING_DATA_DIR, file_name)
    # read the data from the json file 
    try:
        with open(file_path, "r") as file:
            content = file.read().strip()

            if not content:
                return {}

            return json.loads(content)

    except FileNotFoundError:
        return {}

    
# save the dict back to the json db
def save_metrics_data(file_name, metrics_dict):
    # composes the file path by the dir and the file name
    file_path = os.path.join(MONITORING_DATA_DIR, file_name)

    # load the data from the dict to the json file
    with open(file_path, "w") as file:
        json.dump(metrics_dict, file, indent=4)


# add new sample to the metrics data file
def new_sample_to_metrics_data(file_name, category, action_time, value):
    # load the data from the json db to a dict
    all_samples_data = load_metrics_data(file_name)
    # add the new sample 
    category_samples = all_samples_data.get(category, {}) 
    category_samples[action_time] = value
    all_samples_data[category] = category_samples
    # save the new data
    save_metrics_data(file_name, all_samples_data)

def call_sample_by_action(file_name, my_pet: pet.Pet, action):
    action_time = time.asctime()
    if action == "eat":
        new_sample_to_metrics_data(file_name, "eat", action_time, 1)
        new_sample_to_metrics_data(file_name, "hunger", action_time, my_pet.hunger)
        new_sample_to_metrics_data(file_name, "energy", action_time, my_pet.energy)
    
    elif action == "sleep":
        new_sample_to_metrics_data(file_name, "sleep", action_time, 1)
        new_sample_to_metrics_data(file_name, "hunger", action_time, my_pet.hunger)
        new_sample_to_metrics_data(file_name, "energy", action_time, my_pet.energy)

    elif action == "play":
        new_sample_to_metrics_data(file_name, "play", action_time, 1)
        new_sample_to_metrics_data(file_name, "happiness", action_time, my_pet.happiness)
        new_sample_to_metrics_data(file_name, "energy", action_time, my_pet.energy)

    elif action == "getpoints":
        new_sample_to_metrics_data(file_name, "getpoints", action_time, 1)
        new_sample_to_metrics_data(file_name, "energy", action_time, my_pet.energy)

    new_sample_to_metrics_data(file_name, "points", action_time, my_pet.points)
    new_sample_to_metrics_data(file_name, "general_rate", action_time, my_pet.general_rate)


