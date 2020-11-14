# Usage

"""
     python main.py --algorithm NSGA2 --problem dascmop4 --difficulity 4 --pop_size 500 --n_gen 500
"""


from pymoo.algorithms.moead import MOEAD
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_problem, get_sampling, get_crossover, get_mutation, get_visualization, get_reference_directions
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.util.plotting import plot
from pymoo.factory import get_performance_indicator


import argparse
import time
import numpy as np

from utils import print_information


MSSV = 18521489

def main(args, experiment=True, verbose=False):

    # Print information
    print_information(info=args)
    # if input("\nAre you sure with input ? (Enter 'N' to try again)").upper() == "N":
    #     exit(0)

    # Get problem
    if 'zdt' in args['problem']:
        problem = get_problem(args['problem'])
        print("Fuck")
    else:
        problem = get_problem(args['problem'], args['difficulity'])
        print("Tien")

    # Get the algorithm
    if args['algorithm'] == 'MOEA/D':
        algorithm = MOEAD(get_reference_directions("das-dennis", 3, n_partitions=12),
                            n_neighbors=15, decomposition="pbi",
                            prob_neighbor_mating=0.7, seed=MSSV)
    else:
        algorithm = NSGA2(pop_size=args['pop_size'], sampling=get_sampling("bin_random"),
                  crossover=get_crossover("bin_two_point"),
                  mutation=get_mutation("bin_bitflip"),
                  eliminate_duplicates=True)

    # Run the algorithm to solve the problem
    res = minimize(problem, algorithm, 
                    ('n_gen', args['n_gen']),
                    seed=MSSV,
                    verbose=verbose)
    # print(res.F)
    # print(type(res.F))
    # input()
    # Plot the result
    if not experiment: 
        plot = Scatter()
        plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
        plot.add(res.F, color="red")
        plot.show()

    # Return the solution set and distance IGD+ measure.
    pf = problem.pareto_front()
    print(pf)
    input()
    igd_plus = get_performance_indicator("igd+", pf)
    IGD = igd_plus.calc(res.F)

    return (res, IGD)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Experimental on MOEA/D and NSGA algorithms.')
    parser.add_argument('--algorithm', type=str, 
                        default='NSGA2', choices=['MOEA/D', 'NSGA2'],
                        help='The evalutary algorithm using')
    parser.add_argument('--problem', type=str, default='zdt1', 
                        choices=['zdt1', 'zdt2', 'zdt3', 'zdt4', 'zdt6',
                                'dascmop1', 'dascmop2', 'dascmop3', 'dascmop4', 'dascmop5', 'dascmop6'],
                        help='The problem solving.')
    parser.add_argument('--difficulity', type=int, default=1, choices=[1, 2, 3, 4, 5, 6],
                        help='The difficulty of problem.')
    parser.add_argument('--pop_size', type=int, default=100,
                        choices=[100, 200, 300, 400, 500],
                        help='The population in genetic algorithm.')
    parser.add_argument('--n_gen', type=int, default=100,
                        choices=[100, 200, 300, 400, 500],
                        help='The maximum generations of EA.')
    args = vars(parser.parse_args())

    # Run the block main execution
    main(args, experiment=False)

    print("Thank you !")