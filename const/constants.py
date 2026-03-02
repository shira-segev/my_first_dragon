import os

AVAILABLE_ACTIONS = ["eat", "sleep", "play", "getpoints"]

# guess points constans
FREE_POINTS_MAX = 10
FREE_POINTS_MIN = 1


VEGAN_HUNGER_POINTS = 10
PASTRY_HUNGER_POINTS = 20
PROTEIN_HUNGER_POINTS = 30
# Food menu: (food_name, points_value, category)
FOOD_MENU = [("Banana", VEGAN_HUNGER_POINTS, "vegan"), ("Apple", VEGAN_HUNGER_POINTS, "vegan"), ("Carrot", VEGAN_HUNGER_POINTS, "vegan"), ("Watermelon", VEGAN_HUNGER_POINTS, "vegan"),
                ("Bread", PASTRY_HUNGER_POINTS, "pastry"), ("Croissant", PASTRY_HUNGER_POINTS, "pastry"), ("Cookie", PASTRY_HUNGER_POINTS, "pastry"), ("Cake", PASTRY_HUNGER_POINTS, "pastry"),
                ("Cheese", PROTEIN_HUNGER_POINTS, "protein"),("Omelet", PROTEIN_HUNGER_POINTS, "protein"),("Chicken", PROTEIN_HUNGER_POINTS, "protein"), ("Meat", PROTEIN_HUNGER_POINTS, "protein"),]

# Games menu: (game_name, happiness_points)
GAMES_MENU = [("Jumping Rope", 25), ("Football", 40), ("Tennis", 40), ("Trampoline", 25)]

# explanation to the sleep action
SLEEP_EXPLANATION = """For every hour of sleep you will receive 10 energy points and 5 \nhunger points will increase.\n
Your maximum energy is 100, no matter how many hours you sleep."""

TEMPLATES_FOR_ACTION = {"eat": "eat.html", "sleep": "sleep.html", "play": "play.html", "getpoints": "getpoints.html"}

FORM_KEY_FOR_ACTION = {"eat": "food", "sleep": "hours", "play": "game", "getpoints": "guess"}

MESSAGE_FOR_ACTION = {"eat": "{name} ate the {value}!", "sleep": "{name} slept {value} hours!", "play": "{name} played {value}!", "getpoints": "well done {value} was the correct number!"}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))