# Usage
"""
	python main.py -pro_size 10 -func 1MAX -crossover 1X
"""

import os
import math
import argparse
import random


import numpy as np 
from sGA_onemax import genetic_algorithm
from config import DISTRIB, RANDOM_SEED_VALUES
from utils import initialize_population



def bisection(problem_size, optimized_function, crossover_way):
	"""
	- Description: Find the upper bound of the Minimally Required population size - MRPS
	- Arguments:
		+ problem_size (int): the length of problem
	- Return values:
		+ The population size (int) graranteed find the optimal solution with problem_size parameter.
	"""

	# Stage 1: Find the upper bound of the population size
	population_size = 4

	# # Run the the first times
	# intital_population = initialize_population(N=population_size, l=problem_size, distribution=DISTRIB) 	
	# success, converge_configuration, number_of_evaluations = genetic_algorithm(initialized_population=intital_population, 
	# 													optimized_function='1MAX', tournament_size=4)

	# Stage 1: Find the upper bound of MRPS
	print("|\t ---> Stage 1: Find upper bound of MRPS ...")
	while True:

		#print("|\t ---> [INFO] The size of population is {}".format(population_size))
		
		flag = True
		# Run 10 times
		for i in range(10):

			random.seed(RANDOM_SEED_VALUES[i])

			intitial_population = initialize_population(N=population_size, l=problem_size, distribution=DISTRIB)
			success, converge_configuration, number_of_evaluations = genetic_algorithm(initialized_population=intitial_population, 
																		optimized_function=optimized_function, crossover_way=crossover_way, tournament_size=4)
			if not success:
				flag = False
				break
		if flag:
			break

		population_size *= 2


	print("|\t\t ---> The upper bound of MRPS is {}".format(population_size))

	# Stage 2: Find MRPS
	print("|\t ---> Stage 2: Find MRPS")
	upper_N = population_size
	lower_N = upper_N // 2
	number_of_evaluations_ = number_of_evaluations
	update = False

	while (upper_N - lower_N) / upper_N > 0.1:
		
		N = math.ceil((upper_N + lower_N) / 2)

		flag = True

		if not update:
			number_of_evaluations_ = 0

		# Run 10 times
		for i in range(10):

			random.seed(RANDOM_SEED_VALUES[i])

			intitial_population = initialize_population(N=N, l=problem_size, distribution=DISTRIB) 	
			success, converge_configuration, number_of_evaluations = genetic_algorithm(initialized_population=intitial_population, 
															optimized_function=optimized_function, crossover_way=crossover_way, tournament_size=4)
			if not success:
				flag = False
				break

			number_of_evaluations_ += number_of_evaluations
		
			# print("The popszie {}, {}th sGA".format(N, i), number_of_evaluations_)
			# input()

		if flag:
			upper_N = N
			update = True
		else:
			lower_N = N

		# print("Lower bound: {}".format(lower_N))
		# print("Upper bound: {}".format(upper_N))

		if upper_N - lower_N <= 2:
			break

	print("|\t\t ---> [INFO] The found MRPS is {}".format(population_size))
	print("|\t\t ---> [INFO] The number of average evaluations is {}".format(number_of_evaluations_/10))

	return (upper_N, number_of_evaluations_/10)


def main(args):

	# Create directory to optimized function
	function_directory = os.path.join('../hypothesis', args['function'])
	if not os.path.exists(function_directory):
		os.mkdir(function_directory)

	# Create directory for crossover
	crossover_directory = os.path.join(function_directory, args['crossover_way'])
	if not os.path.exists(crossover_directory):
		os.mkdir(crossover_directory)


	saving_path = os.path.join(crossover_directory, str(args['problem_size']).zfill(3) + '.npy')

	# print Information before run
	print("\n\n", "-"*10, "THE INPUT INFORMATION RUNNING EXPERIMENT", "-"*10)
	print('-'*62)
	print("|- {:25} | {:<30}|".format("The optimized function ", args['function']))
	print('-'*62)
	print("|- {:25} | {:<30}|".format("The crossover way", args['crossover_way']))
	print('-'*62)
	print("|- {:25} | {:<30}|".format("The problem size", args['problem_size']))
	print('-'*62)
	print("|- {:25} | {:<30}|".format("The output path", saving_path))
	print('-'*62)
	# print(" - The output path: ", saving_path)


	# Run 10 times bisection
	storage_result = []

	for i in range(10):
		print("| ---> Running {}th bisection ...".format(i+1))
		np.random.seed(RANDOM_SEED_VALUES[i])
		upperbound_popsize, average_evaluations = bisection(problem_size=args['problem_size'], 
							optimized_function=args['function'], crossover_way=args['crossover_way'])

		storage_result.append(np.array([upperbound_popsize, average_evaluations])) 
	
	with open(saving_path, 'wb+') as f:
		np.save(f, np.array(storage_result))

	print("DONE ! Check the {} directory to see the hypothesis output".format(saving_path))


if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='Solve 1MAX and Trap5 problem using sGA.')
	parser.add_argument('--problem_size', '-pro_size', type=int 
						,required=True, choices=[4, 10, 20, 40, 80, 160] 
	                    , help='The problem size.')
	parser.add_argument('--function', '-func', choices=['1MAX', 'TRAP5'], required=True
						,help='The function need to be optimized')
	parser.add_argument('--crossover_way', '-crossover', choices=['1X', 'UX'], required=True
						,help='The way we make the crossover in each generation.')
	args = vars(parser.parse_args())
	
	main(args)
	