
# Imported Pakages
from utils import *#(initialize_population, fitness, evaluation, crossover, pop_pool, tournament_selection, check_convergence)


def genetic_algorithm(initialized_population: np.ndarray, optimized_function, tournament_size=4):
    """
    - Description: Cài đặt giải thuật di truyền để giải bài toán tối ưu hàm OneMax

    - Arguments:
        - initialized_population (np.ndarray): quần thể khởi tạo

    - Return values:
        - converge_configuration (np.ndarray): cấu hình của quần thể khi hội tụ.

        - number_of_evaluations (int): số lượng gọi hàm evaluation - số thế hệ để quần thể ban đầu hội tụ về cấu hình tốt nhất.
    """
    
    population = initialized_population.copy()

    # Initialize the number of calling evaluation function times
    number_of_evaluations = 0

    # Loop until the population is converge
    while not check_convergence(population) :

        # Variation step
        offspring = crossover(population=population)

        # P+O Pool step
        combination_population = pop_pool(population=population, offspring=offspring)

        # Tournament selection
        selected_individuals = tournament_selection(population=combination_population, tournament_size=tournament_size, optimized_function=optimized_function)

        # Evaluate the average fitness of new population
        average_fitness = evaluation(selected_individuals, optimized_function)
        number_of_evaluations += 1

        # Update the population
        population = selected_individuals.copy()
        print("Quần thể tại thế hệ thứ {} có độ thích nghi: {}  \n{}".format(number_of_evaluations, average_fitness, population))

    return (population[0], number_of_evaluations)


def main(args):

    # Print input infomation 
    print("- Population size is {}".format(args['population_size']))
    print("- Problem size is {}".format(args['problem_size']))
    print("- Tournament selection size is {}".format(args['tournament_size']))
	
    # Get the initial population
    

# Run file
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Evaluation Algorithm solve OneMax Problem.')
    parser.add_argument('--population_size', '-pop_size', required=True, help='The population size.')
    parser.add_argument('--problem_size', '-pro_size', required=True, help='The problem size.')
    parser.add_argument('--tournament_size', '-tour_size', required=True, help='The tournament size')
    parser.add_argument('--threshold', '-threshoul', required=False, help='The threshould for random value.')
    args = vars(parser.parse_args())

    main(args)