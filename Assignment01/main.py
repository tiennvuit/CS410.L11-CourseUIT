import os
import numpy as np 
from sGA_onemax import genetic_algorithm
from config import DISTRIB
from utils import initialize_population


def find_MRPS(problem_size):
	"""
	- Description: Find the upper bound of the Minimally Required population size - MRPS
	- Arguments:
		+ problem_size (int): the length of problem
	- Return values:
		+ The population size (int) graranteed find the optimal solution with problem_size parameter.
	"""

	# Stage 1: Find the upper bound of the population size
	population_size = 4

	# Run the the first times
	intital_population = initialize_population(N=population_size, l=problem_size, distribution=DISTRIB) 	
	success, converge_configuration, number_of_evaluations = genetic_algorithm(initialized_population=intital_population, 
														optimized_function='1MAX', tournament_size=4)
	
	while not success:
		print("[INFO] The size of population is {}".format(population_size))
		population_size *= 2

		successes = []

		# Run 10 times
		for i in range(10):
			intital_population = initialize_population(N=population_size, l=problem_size, distribution=DISTRIB) 	
			success, converge_configuration, number_of_evaluations = genetic_algorithm(initialized_population=intital_population, 
															optimized_function='1MAX', tournament_size=4)

			successes.append(success)

		if all(successes):
			return population_size

	return None



def bisection(problem_size):
	pass


def run(problem_sizesm, times=10):
	pass


if __name__ == '__main__':
	
	# problem_sizes = [10, 20, 40, 80, 160]
	# for problem_size in problem_sizes:
	# 	run(problem_size, times=10)

	problem_size = 10
	upperbound_popsize = find_MRPS(10)
	print(upperbound_popsize)