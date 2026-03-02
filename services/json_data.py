import json
from models.pet import Pet
import services.pet_service as pet_service
from const import constants
import os

DATA_FILE_DIR = os.path.join(constants.BASE_DIR, "pets_db")
DATA_FILE_PATH = os.path.join(DATA_FILE_DIR, "pets_data.json")

# save all the current data of pets
def save_pets(pets_dict):
    # dict to load to the json db
    all_pets_data = {}
    
    # get the data
    for name, pet_obj in pets_dict.items():
        all_pets_data[name] = pet_service.to_dict(pet_obj)

    # load the data from the dict to the json file
    with open(DATA_FILE_PATH, "w") as file:
        json.dump(all_pets_data, file, indent=4)


# read all the data from the json db
def load_pets():
    # read the data from the json file and convert it to the
    # if the file is not exist- return empty dict 
    try:
        with open(DATA_FILE_PATH, "r") as file:
            content = file.read().strip()
            # if there is no data return empty dict
            if not content:
                return {}
            # convert the json format data to a dict 
            data = json.loads(content)
            return {name: pet_service.from_dict(pet_data) for name, pet_data in data.items()}
    except FileNotFoundError:
        return {}