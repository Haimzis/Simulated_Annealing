from matplotlib import pyplot as plt
import numpy as np
import tsp_problem
import params
from IPython.display import clear_output


def get_normalized_cities_identification(state):
    state_after_addition = [x+1 for x in state]
    state_after_addition.append(state_after_addition[0])
    state_as_np_array = np.array(state_after_addition)
    min_val = min(state_after_addition)
    while state_as_np_array[0] != min_val:
        state_as_np_array = np.roll(state_as_np_array, -1)
    return list(state_as_np_array)


class CitiesMap:
    def __init__(self, all_cities):
        self.edges = []
        self.all_cities = all_cities
        coords = all_cities.values()
        x_coords = [x[0] for x in coords]
        y_coords = [x[1] for x in coords]
        self.x_coords = np.array(x_coords)
        self.y_coords = np.array(y_coords)
        self.fig = plt.figure()
        self.graph = self.fig.add_subplot()

    def show_map(self, state):
        plt.close(self.fig)
        self.fig = plt.figure()
        self.graph = self.fig.add_subplot()
        self.graph.scatter(self.x_coords, self.y_coords)
        self.show_cities_id()
        if state is not None:
            self.update_edges(state=state)
            self.fig.canvas.draw()
        self.fig.show()

    def update_edges(self, state):
        circle = state.copy()
        circle.append(circle[0])
        x_circle_coords = [self.x_coords[city] for city in circle]
        y_circle_coords = [self.y_coords[city] for city in circle]
        if params.show_distances:
            self.show_distances(x_circle_coords, y_circle_coords)
        ordered_x_coords = np.array(x_circle_coords)
        ordered_y_coords = np.array(y_circle_coords)
        self.graph.plot(ordered_x_coords, ordered_y_coords, 'r')

    def show_distances(self, x_circle_coords, y_circle_coords):
        circle_len = len(x_circle_coords)
        if params.show_distances:
            for ind in range(0, circle_len+1):
                p1 = (x_circle_coords[ind % circle_len], y_circle_coords[ind % circle_len])
                p2 = (x_circle_coords[(ind + 1) % circle_len], y_circle_coords[(ind + 1) % circle_len])
                self.graph.annotate(tsp_problem.distance(p1, p2), ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2))

    def show_cities_id(self):
        for city_id, (x, y) in self.all_cities.items():
            if params.show_coords:
                self.graph.annotate(s=str(city_id + 1) + " " + str((x, y)), xy=(x - 0.5, y + 1))
            else:
                self.graph.annotate(s=city_id + 1, xy=(x - 0.5, y + 1))

    def save_plot(self):
        self.fig.savefig('./final_result/final_state.png')


if __name__ == '__main__':
    import utils, tsp_problem
    all_cities = utils.generate_cities_dict('big')
    tsp = tsp_problem.TravelingSalesmanProblem(all_cities)
    citiesMap = CitiesMap(all_cities)
    final_state = [1, 6, 12, 5, 13, 18, 25, 17, 16, 15, 14, 19, 26, 27, 28, 29, 30, 20, 31,
                   32, 33, 21, 34, 50, 49, 48, 47, 55, 54, 46, 45, 53, 74, 64, 68, 75, 77,
                   78, 81, 82, 87, 88, 92, 94, 99, 93, 89, 98, 112, 123, 130, 121, 118, 114,
                   105, 100, 101, 102, 106, 107, 108, 113, 124, 125, 126, 131, 127, 128, 129,
                   122, 117, 120, 116, 115, 119, 109, 110, 111, 103, 104, 97, 96, 95, 91, 90,
                   86, 85, 84, 83, 79, 80, 72, 73, 61, 60, 59, 58, 63, 67, 71, 76, 70, 66, 69,
                   65, 62, 56, 57, 51, 52, 35, 36, 22, 37, 38, 39, 23, 40, 41, 42, 43, 43, 44,
                   24, 11, 4, 10, 9, 3, 2, 8, 7]
    for id, city in enumerate(final_state):
        final_state[id] -= 1
    print(get_normalized_cities_identification(final_state))
    citiesMap.show_map(final_state)
    print((-1)*tsp.energy(final_state))
