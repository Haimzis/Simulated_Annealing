from simulated_annealing import alpha_scheduler, beta_scheduler

# Hyper Params #
max_steps = 6000000
initial_temperature = 1e6
min_temp = 1e-8
alpha = 0.999992  # T0 * (a** step)
beta = 0.2  # T0 / (1 + beta * step)
temp_epsilon = 1e-6
scheduler = alpha_scheduler
smart_hash = False
# init cooling rate
cooling_rate = 0
scheduler_str = ''
if scheduler == alpha_scheduler:
    scheduler_str = 'alpha'
    max_steps = 6000000
    initial_temperature = 1e6
    min_temp = 1e-8
    cooling_rate = alpha

else:
    scheduler_str = 'beta'
    max_steps = 10000000
    initial_temperature = 1e6
    min_temp = 1e-6
    cooling_rate = beta

# Files #
check_problem_data_path = './tsp_problems/tsp3_xy.txt'
small_problem_data_path = './tsp_problems/tsp15_xy.txt'
medium_problem_data_path = './tsp_problems/tsp48_xy.txt'
hard_problem_data_path = './tsp_problems/tsp131_xy.txt'
output_file_path = './final_result/results.txt'

# Analyzing #
show_distances = False
show_coords = False
