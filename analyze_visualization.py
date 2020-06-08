from matplotlib import pyplot as plt
import numpy as np
import tsp_problem
import params
from IPython.display import clear_output


class Analyzer:
    def __init__(self, samples, problem_difficulty, scheduler, max_steps):
        self.scheduler = scheduler
        self.max_steps = max_steps
        self.problem_difficulty = problem_difficulty
        samples_x = [x for x, y in samples.items()]
        samples_y = [y for x, y in samples.items()]
        self.x_coords = np.array(samples_x)
        self.y_coords = np.array(samples_y)
        self.fig = plt.figure()
        self.graph = self.fig.add_subplot()

    def show_diagram(self):
        plt.close(self.fig)
        self.fig = plt.figure()
        self.graph = self.fig.add_subplot()
        self.graph.scatter(self.x_coords, self.y_coords)
        plt.title(self.scheduler + ' | ' + self.problem_difficulty + ' | ' + self.max_steps)
        self.graph.plot(self.x_coords, self.y_coords, 'r')
        self.fig.show()

    def save_plot(self):
        self.fig.savefig('./final_result/analyzer_diagram.png')

    def add_sample(self, sample):
        self.x_coords = np.append(self.x_coords, sample[0])
        self.y_coords = np.append(self.y_coords, (-1)*sample[1])
