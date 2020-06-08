import math
import numpy as np
import params
from abc import abstractmethod


def alpha_scheduler(sa_instance, step):
    return sa_instance.initial_temperature * (sa_instance.cooling_rate ** step)


def beta_scheduler(sa_instance, step):
    return sa_instance.initial_temperature / (1 + sa_instance.cooling_rate * step)


class SimulatedAnnealing:
    def __init__(self, chosen_scheduler,
                 cooling_rate=0.5,
                 initial_temperature=1e6,
                 max_steps=1,
                 min_temp=1e-6):

        self.state = []
        self.max_steps = max_steps
        self.curr_temperature = self.initial_temperature = initial_temperature
        self.min_temp = min_temp
        self.cooling_rate = cooling_rate
        self.scheduler = chosen_scheduler
        self.smart_hash = params.smart_hash
        self.hash_table = {}

    def get_state_hash(self, state):
        if self.smart_hash:
            copy_state = state.copy()
            min_val = min(copy_state)
            copy_state = np.array(copy_state)
            while copy_state[0] != min_val:
                copy_state = np.roll(copy_state, -1)
            return hash(str(list(copy_state)))
        else:
            return hash(str(state))

    def is_suggested(self, state):
        return self.get_state_hash(state) in self.hash_table.keys()

    def schedule(self, step):
        self.curr_temperature = self.scheduler(self, step)

    def acceptance_prob(self, loss):
        try:
            if self.curr_temperature < params.temp_epsilon:
                return 0.0
            else:
                return math.exp(loss / self.curr_temperature)
        except OverflowError:
            print("loss: " + str(loss) + " temp: " + str(self.curr_temperature))
            return 0

    def done(self):
        return self.curr_temperature < self.min_temp

    def get_randomly_couple(self):
        random_indexes = np.random.randint(0, len(self.state), 2)
        while random_indexes[0] == random_indexes[1]:
            random_indexes = np.random.randint(0, len(self.state), 2)
        return random_indexes

    def eval_loss(self, new_state):
        return self.energy(new_state) - self.energy(self.state)


    def move(self, next_state):
        self.state = next_state
        self.reset_hash_table()

    def reset_hash_table(self):
        self.hash_table = {}

    def remember_suggestion(self, suggested_state):
        self.hash_table[self.get_state_hash(suggested_state)] = suggested_state

    @abstractmethod
    def energy(self, state):
        pass

    @abstractmethod
    def init_state(self, data):
        pass

    @abstractmethod
    def next_successor(self):
        pass

    @abstractmethod
    def save_results(self):
        pass

