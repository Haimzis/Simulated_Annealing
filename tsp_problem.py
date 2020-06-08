import math
import random
import params
from simulated_annealing import SimulatedAnnealing
import numpy as np


def distance(coords1, coords2):
    return math.sqrt((coords1[0] - coords2[0])**2 + (coords1[1] - coords2[1])**2)


def init_distance_matrix(cities_dict):
    return {row_ind: {col_ind: distance(row_coords, col_coords) for col_ind, col_coords in cities_dict.items()}
            for row_ind, row_coords in cities_dict.items()}


class TravelingSalesmanProblem(SimulatedAnnealing):
    def __init__(self, all_cities_and_distances,
                 chosen_scheduler=params.beta_scheduler,
                 cooling_rate=params.cooling_rate,
                 initial_temperature=params.initial_temperature,
                 max_steps=params.max_steps,
                 min_temp=params.min_temp):
        SimulatedAnnealing.__init__(self,
                                    chosen_scheduler=chosen_scheduler,
                                    cooling_rate=cooling_rate,
                                    initial_temperature=initial_temperature,
                                    max_steps=max_steps,
                                    min_temp=min_temp)
        self.init_state(all_cities_and_distances)
        self.distances = init_distance_matrix(all_cities_and_distances)

    def next_successor(self):
        cities2swap = self.get_randomly_couple()
        new_state = self.state.copy()
        temp = new_state[cities2swap[0]]
        new_state[cities2swap[0]] = new_state[cities2swap[1]]
        new_state[cities2swap[1]] = temp
        return new_state

    def energy(self, state):
        overall_distance = 0.0
        state_max_ind = len(self.state)
        for ind, city in enumerate(state):
            overall_distance += self.distances[state[ind % state_max_ind]][state[(ind+1) % state_max_ind]]
        return (-1)*overall_distance

    def init_state(self, all_cities_and_distances):
        self.state = list(all_cities_and_distances.keys())
        random.shuffle(self.state)

    def save_results(self):
        output_file = open(params.output_file_path, 'w')
        output_file.write('final_evaluation: ' + str((-1)*self.energy(self.state)) + '\n')
        output_file.write('final_state: ' + str(self.get_normalized_cities_identification()) + '\n')
        output_file.write('### Hyper Parameters ###\n ')
        output_file.write('max_steps: ' + str(self.max_steps) + '\n')
        output_file.write('initial_temperature: ' + str(self.initial_temperature) + '\n')
        output_file.write('min_temp: ' + str(self.min_temp) + '\n')
        output_file.write('cooling_rate: ' + str(self.cooling_rate) + '\n')
        output_file.write('temp_epsilon: ' + str(params.temp_epsilon) + '\n')
        output_file.write('scheduler: ' + str(self.scheduler) + '\n')

    def get_normalized_cities_identification(self):
        copy_state = self.state.copy()
        state_after_addition = [x+1 for x in copy_state]
        state_after_addition.append(state_after_addition[0])
        state_as_np_array = np.array(state_after_addition)
        min_val = min(state_after_addition)
        while state_as_np_array[0] != min_val:
            state_as_np_array = np.roll(state_as_np_array, -1)
        return list(state_as_np_array)
