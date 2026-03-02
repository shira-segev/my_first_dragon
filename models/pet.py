import random
from dataclasses import dataclass, field
from enum import Enum
import const.constants as constants
import time
import os

OPERATION = Enum('Operation', [('PLUS', 1), ('MINUS', 2)])

# Maximum and minimum allowed values for pet stats
MAX_VALUE = 100
MIN_VALUE = 0

# Sleep effect constants
SLEEP_ENERGY_POINTS = 10
SLEEP_HUNGER_POINTS = 5
SLEEP_HOURS_RANGE = [f"{i + 1}" for i in range(10)]
SLEEP_EXPLANATION = """For every hour of sleep you will receive 10 energy points and 5 hunger points will increase.\n
Your maximum energy is 100, no matter how many hours you sleep."""

VEGAN_HUNGER_POINTS = 10
PASTRY_HUNGER_POINTS = 20
PROTEIN_HUNGER_POINTS = 30

# Energy reduction after playing
PLAY_ENERGY_POINTS = 10

# Happiness change in free points game
FREE_POINTS_HAPPINESS_POINTS = 20

# guess points constans
FREE_POINTS_MAX = 10
FREE_POINTS_MIN = 1

# Points rewarded per action
SLEEP_POINTS = 5
EAT_POINTS = 10
PLAY_POINTS = 20

SAMPLES_FILE = "samples_example"
MONITORING_DATA_DIR = os.path.join(constants.BASE_DIR, "monitoring_data")
LOG_FILES_DIR = os.path.join(constants.BASE_DIR, "log_files")


class Pet:
    """
    Represents a virtual pet with hunger, happiness, energy and points.
    Provides actions such as eat, sleep, play and free_points.
    """

    def __init__(self, pet_name: str, pet_type: str):
        """
        Initializes a new Pet object.

        :param pet_name: str - Name of the pet.
        :param pet_type: str - Type/species of the pet.
        :return: None
        """
        self.name = pet_name
        self.type = pet_type
        self.hunger: int = MIN_VALUE 
        self.happiness: int = MAX_VALUE
        self.energy: int = MAX_VALUE
        self.points: int = MIN_VALUE
        self.log_file: str = f"{self.name}_log_file"
        self.samples_file:str = self.create_samples_file()
        self.general_rate: int = self.general_rate_calc()
        self.rand_num: int = 0

    def general_rate_calc(self):
        """
        Calculates the general average rate of the pet
        based on happiness, hunger and energy.

        :param: None
        :return: float - Average value of happiness, hunger and energy.
        """
        return round(float((self.happiness + (MAX_VALUE - self.hunger) + self.energy) / 3), 2)
    

    def create_samples_file(self):
        # give the samples file a name by the pet name
        sample_file_name = f"{self.name}_samples.json"

        # composes the file path by the dir and the file name
        samples_file_path = os.path.join(MONITORING_DATA_DIR, sample_file_name)
        samples_example_path = os.path.join(MONITORING_DATA_DIR, SAMPLES_FILE)

        with open(samples_example_path, "r") as file:
            template = file.read().strip()

        if not os.path.exists(samples_file_path):
            with open(samples_file_path, "w") as file:
                file.write(template)

        return sample_file_name


    def write_to_log_file(self, action_data):
        file_path = os.path.join(LOG_FILES_DIR, self.log_file)

        data = f"""Time: {time.asctime()}
        Action: {action_data}
        Metrics:
            happiness- {self.happiness}
            hungry- {self.hunger}
            energy- {self.energy}
            points- {self.points}
            general rate- {self.general_rate}\n"""

        # write the data to it
        with open(file_path, 'a') as file:
            file.writelines(data)


    def display(self, text_msg: str):
        """
        Displays a message and the current status of the pet.

        :param text_msg: str - Message describing the action performed.
        :return: None
        """
        print(text_msg)
        print(f"""current pet's status: hunger- {self.hunger}. happiness- {self.happiness}. energy- {self.energy}.
               POINTS = {self.points}. GENERAL_RATE = {self.general_rate}""")

    # def add_to_history(self, text_msg: str):
    #     """
    #     Adds an action message to the pet's history list.

    #     :param text_msg: str - Action description to store.
    #     :return: None
    #     """
    #     self.history.append(text_msg)

    def end_of_action(self, text_msg: str):
        """
        Performs end-of-action updates:
        recalculates general rate, displays status, and saves history.

        :param text_msg: str - Description of the action performed.
        :return: None
        """
        self.general_rate = self.general_rate_calc()
        self.display(text_msg)
        self.write_to_log_file(text_msg)

    def in_range(self, change_amount: int, current: int, operation: OPERATION):
        """
        Ensures a stat remains between 0 and 100 after change.

        :param change_amount: int - Amount to increase or decrease.
        :param current: int - Current stat value.
        :param action: str - "plus" to increase, otherwise decrease.
        :return: int - Updated stat value within allowed range (0–100).
        """
        if operation == OPERATION.PLUS:
            new_value = current + change_amount

        elif operation == OPERATION.MINUS:
            new_value = current - change_amount

        if new_value > MAX_VALUE:
            new_value = MAX_VALUE
        elif new_value < MIN_VALUE:
            new_value = MIN_VALUE

        return new_value

    def show_food_menu(self):
        """
        Displays the food menu and allows user to choose food.

        :param: None
        :return: tuple - Selected food item (name, points, category).
        """
        menu_str = ""
        food_num = 1
        for item in constants.FOOD_MENU:
            menu_str += f"{food_num}. {item[0]}: -{item[1]} Hunger points +{item[1]} energy points \n"
            food_num += 1
        print(menu_str)
        return menu_str
    

    def choose_food(self):
        valid = False
        while not valid:
            choice = input("what would you like to eat? enter the food number")
            
            try:
                choice = int(choice)   
            except ValueError:
                print("Please enter a valid number.")
                continue
            
            if choice > 0 and choice <= len(constants.FOOD_MENU):
                valid = True
                return constants.FOOD_MENU[choice -1]
            else:
                print("No such a food. Try again...")

    def eat(self):
        """
        Feeds the pet using selected food.
        Updates hunger, energy and points.

        :param: None
        :return: None
        """
        self.show_food_menu()
        food = self.choose_food()
        self.hunger = self.in_range(food[1], self.hunger, OPERATION.MINUS)
        self.energy = self.in_range(food[1], self.energy, OPERATION.PLUS)
        self.points += EAT_POINTS
        text_msg = f"{self.name} ate {food[0]}"
        self.end_of_action(text_msg)

    def sleep_explanation(self):
        print(constants.SLEEP_EXPLANATION)
        return constants.SLEEP_EXPLANATION

    def sleep_hours(self):
        hours = 0
        while hours <= 0:
            input_hours = input("How many sleep hours would you like to have? ")
            
            try:
                input_hours = int(input_hours)
                if input_hours <= 0:
                    print("Please enter a positive number.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue

            hours = input_hours
        return hours

    def sleep(self):
        """
        Lets the pet sleep for a number of hours.
        Increases energy and hunger based on sleep hours.

        :param: None
        :return: None
        """
        self.sleep_explanation()
        hours = self.sleep_hours()
        self.energy = self.in_range(SLEEP_ENERGY_POINTS * hours, self.energy, OPERATION.PLUS)
        self.hunger = self.in_range(SLEEP_HUNGER_POINTS * hours, self.hunger, OPERATION.PLUS)
        self.points += SLEEP_POINTS
        text_msg = f"{self.name} sleep {hours} hours"
        self.end_of_action(text_msg)

    def show_games_menu(self):
        """
        Displays the games menu and allows user to choose a game.

        :param: None
        :return: tuple - Selected game item (name, happiness_points).
        """
        menu_str = ""
        game_num = 1
        for item in constants.GAMES_MENU:
            menu_str += f"{game_num}. {item[0]}: +{item[1]} happines points -{PLAY_ENERGY_POINTS} energy points\n "
            game_num += 1
        print(menu_str)
        return menu_str

    def choose_game(self):
        valid = False
        while not valid:
            choice = input("What would you like to play? enter the game number: ")
            
            try:
                choice = int(choice)   
            except ValueError:
                print("Please enter a valid number.")
                continue
            
            if choice > 0 and choice <= len(constants.GAMES_MENU):
                valid = True
                return constants.GAMES_MENU[choice -1]
            else:
                print("No such a game. try again...")

    def play(self):
        """
        Plays a selected game with the pet.
        Increases happiness, decreases energy, and adds points.

        :param: None
        :return: None
        """
        self.show_games_menu()
        game = self.choose_game()
        self.happiness = self.in_range(game[1], self.happiness, OPERATION.PLUS)
        self.energy = self.in_range(PLAY_ENERGY_POINTS, self.energy, OPERATION.MINUS)
        self.points += PLAY_POINTS
        text_msg = f"{self.name} is playing {game[0]}"
        self.end_of_action(text_msg)

    def free_points(self):
        """
        A guessing game where the user can try
        to guess a random number of points.
        Affects happiness, energy and total points.

        :param: None
        :return: None
        """
        self.rand_num = random.randint(FREE_POINTS_MIN, FREE_POINTS_MAX) 
        print("If you will guess the random amount of points, you will receive them!!!")
        guess_points = 0

        valid = False
        while not valid:
            guess_points = input(f"guess num:")

            try:
                guess_points = int(guess_points) 
                valid = True  
            except ValueError:
                print("Please enter a valid number.")
                valid = False
                continue
            
        if guess_points == self.rand_num:
            print("Good job!!!")
            self.points += self.rand_num
        
        else:
            print(f"Not the correct answer :( the number was {self.rand_num}")
        
        self.energy = self.in_range(PLAY_ENERGY_POINTS, self.energy, OPERATION.MINUS)
        text_msg = f"{self.name} play the free points game"
        self.end_of_action(text_msg)
