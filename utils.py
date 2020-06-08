import params


def generate_data_from_file(data_file_path):
    cities_dict = {}
    with open(data_file_path) as data_file:
        content = data_file.readlines()
    for ind, line in enumerate(content):
        x = y = None
        for separated_str in line.split(' '):
            if separated_str is not None and len(separated_str) != 0 and separated_str != '\n':
                if x is None:
                    x = separated_str
                elif y is None:
                    y = separated_str.split('\n')[0]
        if x is not None and y is not None:
            cities_dict[ind] = (float(x), float(y))
        x = y = None
    return cities_dict


def generate_cities_dict(tsp_problem_difficulty):
    problems_dict = {'check': params.check_problem_data_path,
                     'small': params.small_problem_data_path,
                     'medium': params.medium_problem_data_path,
                     'big': params.hard_problem_data_path}

    cities_dict = generate_data_from_file(problems_dict[tsp_problem_difficulty])
    return cities_dict


def print_algorithm_state_after_acceptance(tsp, step, loss, sample_for_acceptance, last_acceptance_prob, test_number):
    print("step: " + str(step) + ', temp: ' + str(tsp.curr_temperature) + ', loss: ' + str(loss)
          + ' swapped: ' + str(sample_for_acceptance <= last_acceptance_prob) + ' prob: ' +
          str(last_acceptance_prob) + ' test_number: ' + str(test_number))


def print_algorithm_state_after_improvement(tsp, step, loss, test_number):
    print("step: " + str(step) + ', temp: ' + str(tsp.curr_temperature) + ', loss: ' + str(loss) +
          ' swapped: yes, improved ' + ' test_number: ' + str(test_number))
