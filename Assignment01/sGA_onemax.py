
# Imported Pakages
from utils import *#(initialize_population, fitness, evaluation, crossover, pop_pool, tournament_selection, check_convergence)
from config import DISTRIB


def genetic_algorithm(initialized_population: np.ndarray, optimized_function, tournament_size=4, limit_steps=1e6):
    """
    - Description: Cài đặt giải thuật di truyền để giải bài toán tối ưu hàm OneMax

    - Arguments:
        - initialized_population (np.ndarray): quần thể khởi tạo

    - Return values:
        - converge_configuration (np.ndarray): cấu hình của quần thể khi hội tụ.

        - number_of_evaluations (int): số lượng gọi hàm evaluation - số thế hệ để quần thể ban đầu hội tụ về cấu hình tốt nhất.
    """
    population = initialized_population.copy()
    number_evals, average_eval = average_evaluation(population=population, optimized_function=optimized_function)
    
    # Initialize the number of calling evaluation function times
    number_of_evaluations = number_evals

    # Loop until the population is converge
    steps = 0
    while not check_convergence(population) and steps < limit_steps:

        # Variation step
        offspring = crossover(population=population)

        # Evaluate the offstring
        number_evals, average_eval = average_evaluation(population=offspring, optimized_function=optimized_function)

        # P+O Pool step
        combination_population = pop_pool(population=population, offspring=offspring)

        # Tournament selection
        selected_individuals = tournament_selection(population=combination_population, tournament_size=tournament_size, optimized_function=optimized_function)

        number_of_evaluations += number_evals

        # Update the population
        population = selected_individuals.copy()
        print("Quần thể tại thế hệ thứ {} có độ thích nghi: {}  \n{}".format(number_of_evaluations, average_eval, population))

        steps += 1

    if evaluation(population[0]) == len(population[0]):
            return (True, population[0], number_of_evaluations)

    return (False, population[0], number_of_evaluations)    



def main(args):

    # Print input infomation 
    print("- Population size is {}".format(args['population_size']))
    print("- Problem size is {}".format(args['problem_size']))
    print("- Tournament selection size is {}".format(args['tournament_size']))
    print("- The function need solve is {}".format(args['function']))

    # Get the initial population
    initial_population = initialize_population(N=args['population_size'], l=args['problem_size'], distribution=DISTRIB)
    print("[INFO] The initalized population is \n{}".format(initial_population))

    # Run the genetic algorithm to solve OneMax problem
    print("\n[INFO] Starting algorithm ...")
    succes, converge_configutation, number_of_evalutations = genetic_algorithm(
                                                    initialized_population=initial_population,
                                                    optimized_function='1Max',
                                                    tournament_size=args['tournament_size'])

    if succes:
        print("[INFO] The genetic algorithm find the optimal solution configuration !")
    else:
        print("[INFO] The genetic algorithm DONT'T find the optimal solution configuration !!")


# Run file
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Evaluation Algorithm solve OneMax Problem.')
    parser.add_argument('--population_size', '-pop_size', type=int, required=True, help='The population size.')
    parser.add_argument('--function', '-f', choices=['1MAX', 'TRAP5'], default='1MAX', help='The function needed optimize.')
    parser.add_argument('--problem_size', '-pro_size', type=int, required=True, help='The problem size.')
    parser.add_argument('--tournament_size', '-tour_size', type=int, required=True, help='The tournament size')
    parser.add_argument('--threshold', '-th', type=int, required=False, help='The threshould for random value.')
    args = vars(parser.parse_args())

    main(args)