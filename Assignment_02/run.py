# Usage
"""
    python run.py --problem zdt1 --pop_size 100 --n_gen 100
"""
import argparse
from main import main as run_one_time


def main(args):

    # Run MOEAD algorithm on the given problem.
    pop_sizes = [100, 200, 400, 800]
    n_gens = [100, 200, 400, 800]

    for pop_size in pop_sizes:
        for n_gen in n_gens:
            
            # input_args = {
            #     'algorithm': 'MOEAD/D',
            #     'pop_size': pop_size,
            #     'n_gen': n_gen,            
            # }
            # print({**args, **input_args})
            # input()

            # run_one_time(args={**args, **input_args})

            input_args = {
                'algorithm': 'NSGA2',
                'pop_size': pop_size,
                'n_gen': n_gen,            
            }
            run_one_time(args={**args, **input_args})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate two algorithms on specific problem')
    parser.add_argument('--problem', type=str, default='zdt1', 
                        choices=['zdt1', 'zdt2', 'zdt3', 'zdt4', 'zdt6',
                                'dascmop1', 'dascmop2', 'dascmop3', 'dascmop4', 'dascmop5', 'dascmop6'],
                        help='The problem solving.')
    parser.add_argument('--difficulity', type=int, default=1, choices=[1, 2, 3, 4, 5, 6],
                        help='The difficulty of problem.')
    # parser.add_argument('--pop_size', type=int, default=100,
    #                     choices=[100, 200, 300, 400, 500],
    #                     help='The population in genetic algorithm.')
    # parser.add_argument('--n_gen', type=int, default=100,
    #                     choices=[100, 200, 300, 400, 500],
    #                     help='The maximum generations of EA.')
    args = vars(parser.parse_args())

    main(args)
    print("Thank you !")