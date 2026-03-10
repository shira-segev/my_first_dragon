from services import exporter
from models import pet
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import os
from const import constants



BELOW_STANDART = 20
ACTION_LST = ["eat", "sleep", "play", "getpoints"]
FEATURE_LST = ["happiness", "hunger", "energy", "general_rate"]
MAX_POINT_TIMES_60_MINUTES = 360000
STATIC_DIR = os.path.join(constants.BASE_DIR, "web", "static")

def calc_actions_today_reps(my_pet: pet.Pet):
    pet_samples = exporter.load_metrics_data(my_pet.samples_file)

    action_counters = [["eat", 0], ["sleep", 0], ["play", 0], ["getpoints", 0]]
    sum = 0
    today_date = datetime.now().date()

    for action in action_counters:
        action_name = action[0]
        today_count = 0

        for timestamp_str in pet_samples[action_name].keys():
            sample_time = datetime.strptime(timestamp_str, "%a %b %d %H:%M:%S %Y")

            if sample_time.date() == today_date:
                today_count += 1
        
        action[1] = today_count
        sum += today_count
    
    action_counters.append(("all", sum))
    action_counters[3][0] = "get points"
    return action_counters

def cacl_first_place_action(my_pet: pet.Pet):
    pet_samples = exporter.load_metrics_data(my_pet.samples_file)
    first_place_action = [("action_name", 0)]

    for action in pet_samples:
        if len(pet_samples[action]) > first_place_action[0][1] and action in ACTION_LST:
            first_place_action = [(action, len(pet_samples[action]))]
        
        elif len(pet_samples[action]) == first_place_action[0][1] and action in ACTION_LST:
            first_place_action.append((action, len(pet_samples[action])))

    return first_place_action

def calc_actions_history(my_pet: pet.Pet):
    pet_samples = exporter.load_metrics_data(my_pet.samples_file)

    action_counters = [["eat", 0], ["sleep", 0], ["play", 0], ["getpoints", 0]]
    sum = 0

    for action in action_counters:
        action_name = action[0]
        action[1] = len(pet_samples[action_name])
        sum += len(pet_samples[action_name])
    
    action_counters.append(("all", sum))
    action_counters[3][0] = "get points"
    return action_counters

def calc_below_standart_features(my_pet: pet.Pet):
    pet_samples = exporter.load_metrics_data(my_pet.samples_file)
    features_counters = [["happiness", 0], ["hunger", 0], ["energy", 0], ["general_rate", 0]]
    sum = 0
    sample_before = 100
    hunger_sample_before = 0

    for feature in features_counters:
        feature_name = feature[0]
        for sample in pet_samples[feature_name]:
            if feature_name != "hunger" and pet_samples[feature_name][sample] <= BELOW_STANDART and sample_before > BELOW_STANDART:
                sum += 1
                sample_before = pet_samples[feature_name][sample]
            
            elif feature_name == "hunger" and pet_samples[feature_name][sample] >= 100 - BELOW_STANDART and hunger_sample_before < 100 - BELOW_STANDART:
                sum += 1
                hunger_sample_before = pet_samples[feature_name][sample]

        feature[1] = sum
        sum = 0
        sample_before = 100
        hunger_sample_before = 0

    features_counters[3][0] = "general rate"
    return features_counters

def calc_features_avg_rate(my_pet: pet.Pet):
    pet_samples = exporter.load_metrics_data(my_pet.samples_file)
    features_avg = [["happiness", 0], ["hunger", 0], ["energy", 0], ["general_rate", 0]]
    
    sample_duration = 0

    this_time = datetime.now()
    one_hour_ago = datetime.now() - timedelta(hours=1)
    last_sample_time = one_hour_ago

    for feature in features_avg:
        feature_name = feature[0]
        last_sample_time = one_hour_ago
        feature_sum = 0
        last_sample_value = -1

        samples = sorted(pet_samples[feature_name].items())

        for sample_timestamp_str, sample_value in samples:
            sample_time = datetime.strptime(sample_timestamp_str,"%a %b %d %H:%M:%S %Y")
            
            # if its a sample before this houre- save the value for the begginig of the hour value
            if sample_time >= one_hour_ago:
                last_sample_value = sample_value

            # if its a samplefrom the current hour- calc the avg 
            else:
                # if no sample was made ill use the first value of the hour
                if last_sample_value == -1:
                    last_sample_value = sample_value
                

                sample_duration = (sample_time - last_sample_time).total_seconds()
                feature_sum += last_sample_value * sample_duration

                # save the current value of sample for the next sample so ill know the duration this value was relevant
                last_sample_value = sample_value
                last_sample_time = sample_time



                sample_value = pet_samples[feature_name][sample_timestamp_str]
                sample_duration = (this_time - last_sample_time).total_seconds()
                feature_sum += sample_value * sample_duration
        
        if last_sample_value != -1:
            sample_duration = (this_time - last_sample_time).total_seconds()
            feature_sum += last_sample_value * sample_duration

        feature[1] = round(feature_sum / MAX_POINT_TIMES_60_MINUTES, 2)

    features_avg[3][0] = "general rate"
    return features_avg

def create_progress_graphes(my_pet: pet.Pet):
    pet_samples = exporter.load_metrics_data(my_pet.samples_file)
    x_value = []
    y_value = []

    for feature_name in FEATURE_LST:
        samples = sorted(pet_samples[feature_name].items())

        for sample_timestamp_str, sample_value in samples:
            sample_time = datetime.strptime(sample_timestamp_str,"%a %b %d %H:%M:%S %Y")
            x_value.append(sample_time)
            y_value.append(sample_value)
        plt.plot(x_value, y_value)
        plt.xlabel("time")
        plt.ylabel("point")
        plt.title(f"{feature_name} progress")

        file_path = os.path.join(STATIC_DIR, f"{feature_name}_progress_graph.png")
        plt.savefig(file_path)
        plt.close()
        x_value = []
        y_value = []
        plt.figure()
    













