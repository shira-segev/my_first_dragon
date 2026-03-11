import models.pet as pet
from enum import Enum

# List of allowed pet types
PET_TYPES =  Enum('PetTypes', [('DOG', "dog"), ('DRAGON', "dragon"), ('CAT', "cat")])
PET_TYPES_LIST = [pet.value for pet in PET_TYPES]

# list of created pets
pets = []

def make_pet():
    """
    Creates a new pet by asking the user for type and name.
    Validates that the chosen type exists in PET_TYPES.

    :param: None
    :return: Pet.Pet - A new Pet object created with user input.
    """
    print("lets create your pet!!!")
    pet_type = input(f"Which type of pet would you like to create? Options: {', '.join(PET_TYPES_LIST)} ")
    while pet_type not in PET_TYPES_LIST:
        print(f"{pet_type} is not a valid pet type. Try again...")
        pet_type = input(f"Choose a valid type: {', '.join(PET_TYPES_LIST)} ")
    name = input("Choose a name to your pet: ")
    return pet.Pet(name, pet_type)


def game_menu():
    """
    Displays the list of available actions to the user.

    :param: None
    :return: None
    """
    print("List of available actions:\n"
        "1. Sleep\n"
        "2. Play\n"
        "3. Eat\n"
        "4. Get Points\n"
        "5. Exit\n")


def start_game():
    """
    Starts the main game loop.
    Creates a pet and repeatedly asks the user to choose actions.

    :param: None
    :return: None
    """
    # Create the pet
    pet = make_pet()
    pets.append(pet)

    actions = {1: pet.sleep, 2: pet.play, 3: pet.eat, 4: pet.free_points}

    # Main game loop 
    while True:
        game_menu()
        choice = input("Enter which action do you want to do (the number of the action): ")

        # convert to int
        try:
            choice = int(choice)
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if choice == 5:
            break

        action = actions.get(choice)

        # Perform action based on choice
        if action:
            action() 
        else:
            print("Not a valid option. Try again...")

def main():
    """
    Entry point of the program.

    :param: None
    :return: None
    """
    start_game()


if __name__ == "__main__":
    main()