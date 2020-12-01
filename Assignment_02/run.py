# Usage
"""
    python run.py --problem zdt1 --pop_size 100 --n_gen 100
"""
import argparse
from main import main as run_one_time
from pymoo.factory import get_problem
from matplotlib import pyplot as plt
import numpy as np
import os


def main(args):

    # Get problem
    if 'zdt' in args['problem']:
        problem = get_problem(args['problem'])
    else:
        problem = get_problem(args['problem'], args['difficulity'])
    pareto_front = problem.pareto_front()

    nsga2 = dict()
    moead = dict()

    # Run the NSGA2 algorithm
    input_args = {
        'algorithm': 'NSGA2',
        'pop_size': args['pop_size'],
        'n_gen': args['n_gen'],            
    }
    nsga2['res'], nsga2['igd'] = run_one_time(args={**args, **input_args}, experiment=False, verbose=False)

    # Run the MOEAD/D algorithm
    input_args = {
        'algorithm': 'MOEAD',
        'pop_size': args['pop_size'],
        'n_gen': args['n_gen']+10,            
    }
    moead['res'], moead['igd'] = run_one_time(args={**args, **input_args}, experiment=False, verbose=False)
    
    
    # Plot two solution of two algorithms
    fig, ax = plt.subplots()
    ax.plot(pareto_front[:, 0], pareto_front[:, 1], color="black", label='Pareto front')
    ax.scatter(moead['res'].F[:, 0], moead['res'].F[:, 1], color="red", label="MOEA/D") 
    ax.scatter(nsga2['res'].F[:, 0], nsga2['res'].F[:, 1], color="blue", label="NSGA2")
    ax.set_xlabel(r'$f_1$', fontsize=12)
    ax.set_ylabel(r'$f_2$', fontsize=12)
    ax.set_title('MOEA/D and NSGA2 on {} problem with {} evalutaions'.format(args['problem'], args['pop_size']*args['n_gen']))
    ax.legend(loc='best')

    print("\n{:^77s}".format("COMPARATION BETWEEN TWO ALGORITHMS"))
    print("| {:50} | {:>20} |".format("The inverted general distance plus of MOEA/D is", moead['igd']))
    print("| {:50} | {:>20} |".format("The inverted general distance plus of NSGA2 is", nsga2['igd']))
    
    plt.show()
    saving_name = os.path.join('figures', '{}_{}_{}.png'.format(args['problem'], args['pop_size'], args['n_gen']))
    fig.savefig(saving_name)
    print("Saved the plot to {}".format(saving_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate two algorithms on specific problem')
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

    main(args)
    print("Thank you !")