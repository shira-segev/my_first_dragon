from flask import Flask, request, redirect, url_for, render_template
import models.pet as pet
import services.pet_service as pet_service
import services.json_data as json_data 
import const.constants as constants
import services.monitoring_calculation as monitoring_calculation

APP_HOST = "0.0.0.0"
APP_PORT = 8080
pets = json_data.load_pets()
app = Flask(__name__)

# home page
@app.route("/")
def home_page():
    return render_template('home.html')

# create a new pet page
@app.route("/home/create/", methods=["GET", "POST"])
def create_page():
    # to use the values the user sent in the form
    if request.method == "POST":
        name = request.form.get("name")
        pet_type = request.form.get("type")

        if not name:
            # if no name entered- no pet created + error message
            return render_template("create.html", error=f"your new pet didnt received a name- try again...")

        # check if this name is in use
        if name in pets:
            # error message
            return render_template("create.html", error=f"A pet named '{name}' already exists!")

        # if name is not in use- the pet is created under this name and then the user is moved to his pet's page
        pets[name] = pet.Pet(name, pet_type)
        json_data.save_pets(pets)
        return redirect(url_for("mypet_page", name=name))
    
    # show the html with the form- in this form the user send the information
    return render_template("create.html")

# connect to your pet page
@app.route("/home/connect/", methods=["POST", "GET"])
def connect_page():
    # to use the values the user sent in the form
    if request.method == "POST":
        name = request.form.get("name")

        # if the name of the pet is not in the dict- the pet is not exist
        if name not in pets:
            return render_template("connect.html", error=f"A pet named '{name}' is not exists!")

        # if there is a pet under this name- the user is moved to his pet's page
        return redirect(url_for("mypet_page", name=name))
    
    # show the html with the form- in this form the user send the information
    return render_template("connect.html")
    
# the pet home page
@app.route("/home/<name>/")
def mypet_page(name):
    my_pet = pets.get(name)
    if not my_pet:
        return render_template("error.html")
    return render_template("mypet.html", name=name)

# pet- get status
@app.route("/home/<name>/status/")
def status_page(name):
    my_pet = pets.get(name)
    if not my_pet:
        return render_template("error.html")
    return render_template("status.html", pet=my_pet, name=name)

# the pet BI page
@app.route("/home/<name>/bi/")
def bi_page(name):
    my_pet = pets.get(name)
    if not my_pet:
        return render_template("error.html")
    monitoring_calculation.create_progress_graphes(my_pet)
    return render_template("bi.html", pet=my_pet, name=name, 
                           today_reps=monitoring_calculation.calc_actions_today_reps(my_pet), 
                           reps_history=monitoring_calculation.calc_actions_history(my_pet), 
                           below_standart=monitoring_calculation.calc_below_standart_features(my_pet),
                           feature_avg=monitoring_calculation.calc_features_avg_rate(my_pet),
                           best_action=monitoring_calculation.cacl_first_place_action(my_pet))



# pet- get actions
@app.route("/home/<name>/actions/")
def actions_page(name):
    my_pet = pets.get(name)
    if not my_pet:
        return render_template("error.html")    
    return render_template("actions.html", name=name)


@app.route("/home/<name>/actions/<action>", methods=["GET", "POST"])
def one_action_page(name, action):
    my_pet = pets.get(name)
    message = ""

    # the page is not exist- no such a pet/action
    if not my_pet or action not in constants.TEMPLATES_FOR_ACTION:
        return render_template("error.html")
    
    if request.method == "POST":
        form_value = request.form.get(constants.FORM_KEY_FOR_ACTION[action])

        if not form_value:
            message = "you didnt enter your choise"
            return render_template(constants.TEMPLATES_FOR_ACTION[action], name=name, my_pet=my_pet, message=message, 
        food_menu=constants.FOOD_MENU, games_menu=constants.GAMES_MENU)
        
        if action == "sleep" or action == "getpoints":
            form_value = int(form_value)

        if (action == "getpoints" or action == "play") and my_pet.energy == 0:
            message = f"{name} is to tired to play..."
            return render_template(constants.TEMPLATES_FOR_ACTION[action], name=name, my_pet=my_pet, message=message, 
        food_menu=constants.FOOD_MENU, games_menu=constants.GAMES_MENU)


        elif pet_service.flask_action(my_pet, action, form_value):
            message = constants.MESSAGE_FOR_ACTION[action].format(name=name, value=form_value, my_pet=my_pet)
            json_data.save_pets(pets)

        else:
            message = f"your guess was wrong :( the number was {my_pet.rand_num}"

        return render_template(constants.TEMPLATES_FOR_ACTION[action], name=name, my_pet=my_pet, message=message, 
        food_menu=constants.FOOD_MENU, games_menu=constants.GAMES_MENU)
    
    return render_template(constants.TEMPLATES_FOR_ACTION[action], name=name, my_pet=my_pet, message=message, 
        food_menu=constants.FOOD_MENU, games_menu=constants.GAMES_MENU)


def main():
    app.run(debug=True, port=APP_PORT, host=APP_HOST)

if __name__ == "__main__":
    main()