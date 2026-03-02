from services import exporter
from models import pet

def calc_actions_counters_monitoring(my_pet: pet.Pet):
    pet_samples = exporter.load_metrics_data(my_pet.samples_file)

    action_counters = [["eat", 0], ["sleep", 0], ["play", 0], ["getpoints", 0]]
    sum = 0

    for action in action_counters:
        action_name = action[0]
        action[1] = len(pet_samples[action_name])
        sum += len(pet_samples[action_name])
    
    action_counters.append(("all", sum))

    return action_counters

