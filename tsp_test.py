import math
import params
import utils
import tsp_problem
import numpy as np
from cities_visualization import CitiesMap
import simulated_annealing
from analyze_visualization import Analyzer
from matplotlib.animation import FuncAnimation


def run_tsp(chosen_scheduler=params.scheduler,
            cooling_rate=params.cooling_rate,
            initial_temperature=params.initial_temperature,
            max_steps=params.max_steps,
            min_temp=params.min_temp, test_number=None):
    tsp = tsp_problem.TravelingSalesmanProblem(all_cities,
                                               chosen_scheduler,
                                               cooling_rate,
                                               initial_temperature,
                                               max_steps,
                                               min_temp)
    cities_map = CitiesMap(all_cities)
    cities_map.show_map(state=None)
    last_acceptance_prob = 0.0

    for step in range(tsp.max_steps):
        tsp.schedule(step)
        next_state = tsp.next_successor()

        #if (step + 1) % (tsp.max_steps//4) == 0:
        #    cities_map.show_map(tsp.state)
        if tsp.done():
            # is metal got cold
            break
        if tsp.is_suggested(next_state):
            # dont repeat on unworthy suggestions
            print('step: ' + str(step) + ' ### already suggested state ###')
            continue
        else:
            # remember suggestion
            if last_acceptance_prob < 1e-10:
                tsp.remember_suggestion(next_state)

        loss = tsp.eval_loss(new_state=next_state)
        if loss > 0:
            # improving state
            tsp.move(next_state)
            utils.print_algorithm_state_after_improvement(tsp, step, loss, test_number)
        else:
            random_sample = np.random.random_sample()
            last_acceptance_prob = tsp.acceptance_prob(loss=loss)
            if random_sample <= last_acceptance_prob:
                # bad move acceptance
                tsp.move(next_state)
            utils.print_algorithm_state_after_acceptance(tsp, step, loss, random_sample, last_acceptance_prob, test_number)

    print(tsp.state)
    print((-1)*tsp.energy(tsp.state))
    cities_map.show_map(tsp.state)
    return tsp, cities_map


if __name__ == '__main__':
    all_cities = utils.generate_cities_dict('medium')
    best_res = float('Inf')
    max_tries = 2
    try_num = 1

    ### Hyper Parameters ###
    addition2steps = 10000
    addition2temperature = 1000
    initial_temp = 500000
    scheduler_str = 'beta'
    ### alpha ###
    alpha = 0.9
    alpha_max_steps = 10000
    alpha_min_temp = 1e-8
    ### beta ###
    beta = 5
    beta_min_temp = 1e-6
    beta_max_steps = 25
    analyzer_diagram = Analyzer({}, 'medium', '<function beta_scheduler>', str(alpha_max_steps))
    for i in range(0, 600):
        if try_num == max_tries:
            break
        if scheduler_str == 'alpha':
            tsp, cities_map = run_tsp(simulated_annealing.alpha_scheduler, alpha, initial_temp, alpha_max_steps, alpha_min_temp,i)
        else:
            tsp, cities_map = run_tsp(simulated_annealing.beta_scheduler, beta, initial_temp, beta_max_steps, beta_min_temp,i)
        tsp_result = (-1)*tsp.energy(tsp.state)
        analyzer_diagram.add_sample((beta, tsp_result))
        if tsp_result < best_res:
            best_res = tsp_result
            tsp.save_results()
            cities_map.save_plot()
            try_num = 1
        else:
            try_num += 1
            if scheduler_str == 'alpha':
                alpha = alpha - 0.00005
                #alpha_max_steps += addition2steps
                initial_temp += addition2temperature

            else:
                beta = beta + 0.03
                #beta_max_steps -= addition2steps
                #initial_temp -= addition2temperature
        #if i % 35 == 0:
        #    if scheduler_str == 'beta':
        #        scheduler_str = 'alpha'
        #    else:
        #        scheduler_str = 'beta'

        print("test number: " + str(i))

    analyzer_diagram.show_diagram()
    analyzer_diagram.save_plot()
