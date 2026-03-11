import models.pet as pet
import random
import const.constants as constants
from services import exporter

# function for the json db so the data will be saved and pulled out of the db
# this db will help me save the pets object even if the web is restarting
def to_dict(my_pet: pet.Pet):
    return {
        "name": my_pet.name,
        "type": my_pet.type,
        "hunger": my_pet.hunger,
        "energy": my_pet.energy,
        "happiness": my_pet.happiness,
        "general_rate": my_pet.general_rate,
        "points": my_pet.points        
    }

def from_dict(data):
    my_pet = pet.Pet(data["name"], data.get("type", "Unknown"))
    my_pet.hunger = data.get("hunger", 0)
    my_pet.energy = data.get("energy", 100)
    my_pet.happiness = data.get("happiness", 100)
    my_pet.points = data.get("points", 0)
    return my_pet


# functions for the flask app:
def flask_action(my_pet: pet.Pet, action, param):
    happened = False
    if action == "eat":
        happened = flask_eat(my_pet, param)
        
    elif action == "sleep":
        happened = flask_sleep(my_pet, param)

    elif action == "play":
        happened = flask_play(my_pet, param)

    elif action == "getpoints":
        happened = flask_getpoints(my_pet,param)

    exporter.call_sample_by_action(my_pet.samples_file, my_pet, action)
    return happened


def flask_eat(my_pet: pet.Pet, food_name):
    """
    Eats food by the name of the food from the menu.
    :param food_name: str
    :return: bool (True if success)
    """
    for food in constants.FOOD_MENU:
        if food[0] == food_name:
            my_pet.hunger = my_pet.in_range(food[1], my_pet.hunger, pet.OPERATION.MINUS)
            my_pet.energy = my_pet.in_range(food[1], my_pet.energy, pet.OPERATION.PLUS)
            my_pet.points += pet.EAT_POINTS
            text_msg = f"{my_pet.name} ate {food[0]}"
            my_pet.end_of_action(text_msg)
            return True
    return False
    

def flask_sleep(my_pet: pet.Pet, hours):
    """
    sleep by the value sleep hours.
    :param hours: str
    :return: bool (True if success)
    """
    my_pet.energy = my_pet.in_range(pet.SLEEP_ENERGY_POINTS * hours, my_pet.energy, pet.OPERATION.PLUS)
    my_pet.hunger = my_pet.in_range(pet.SLEEP_HUNGER_POINTS * hours, my_pet.hunger, pet.OPERATION.PLUS)
    my_pet.points += pet.SLEEP_POINTS
    text_msg = f"{my_pet.name} sleep {hours} hours"        
    my_pet.end_of_action(text_msg)
    return True
    
def flask_play(my_pet: pet.Pet, game_name):
    """
    play a game by the name of the game from the menu.
    :param game_name: str
    :return: bool (True if success)
    """
    for game in constants.GAMES_MENU:
        if game[0] == game_name:
            my_pet.happiness = my_pet.in_range(game[1], my_pet.happiness, pet.OPERATION.PLUS)
            my_pet.energy = my_pet.in_range(pet.PLAY_ENERGY_POINTS, my_pet.energy, pet.OPERATION.MINUS)
            my_pet.points += pet.PLAY_POINTS
            text_msg = f"{my_pet.name} is playing {game[0]}"
            my_pet.end_of_action(text_msg)
            return True
    return False
    
def flask_getpoints(my_pet: pet.Pet, guess):
    my_pet.rand_num = random.randint(pet.FREE_POINTS_MIN, pet.FREE_POINTS_MAX)

    if guess == my_pet.rand_num:
        my_pet.points += my_pet.rand_num

    my_pet.energy = my_pet.in_range(pet.PLAY_ENERGY_POINTS, my_pet.energy, pet.OPERATION.MINUS)
    text_msg = f"{my_pet.name} play the free points game"
    my_pet.end_of_action(text_msg)


    return guess == my_pet.rand_num

