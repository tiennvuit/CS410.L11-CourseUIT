import os
import argparse

import numpy as np
from scipy import stats


from pso_ring import PSO_Ring
from pso_star import PSO_Star
from problem_config import PROBLEM_CONFIG

PSO = {
    'star': PSO_Star,
    'ring': PSO_Ring,
}


def print_info(args):

    print("-"*24 + "INPUT ARGUMENTS" + "-"*24)
    print("|{:<30}|{:<30}|".format("Topology", args['topo']))
    print("|{:<30}|{:<30}|".format("Optimizing Function", args['func']))
    print("|{:<30}|{:<30}|".format("Number of particles", args['n_particles']))
    print("|{:<30}|{:<30}|".format("Number of generation", args['n_gen']))
    print("|{:<30}|{:<30}|".format("Limit evaluations", args['evaluations']))
    print("-"*63)

def main(args):
    

    if args['func']=='Rastrigin_10D' or args['func']=='Rosenbrock_10D':    
        
        n_PARTICLES = [128, 256, 512, 1024, 2048]

        # print("-"*19 + "STATISTIC TABLE FOR {} TOPOLOPY WITH DIFFERENT NUMBER OF PARTICLES".format(
        #                         args['topo'].upper())+ "-"*19)
        # print("|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|".format(
        #       'n_particles', 'mean_value', 'std_value', 'mean_pos', 'std_pos', 'true_optimal_diff'))
        print("-"*106)
        for n_particles in n_PARTICLES:
            
            SEED = 18521489

            star_values = []
            ring_values = []

            # Run 10 times
            for i in range(10):
                np.random.seed(SEED)
                # solver = PSO[args['topo']](n_particles=n_particles, 
                #                 n_gen=int(1e12), 
                #                 name_func=args['func'], seed=SEED)
                # res, value, pos = solver.solve(limit_evals=1e6, verbose=False, track=True, seed=SEED)
                # values.append(value)
                # positions.append(pos)

                solver = PSO['star'](n_particles=n_particles, 
                                n_gen=int(1e12), 
                                name_func=args['func'], seed=SEED)
                res, value, pos = solver.solve(limit_evals=1e6, verbose=False, track=True, seed=SEED)
                star_values.append(value)

                solver = PSO['ring'](n_particles=n_particles, 
                                n_gen=int(1e12), 
                                name_func=args['func'], seed=SEED)
                res, value, pos = solver.solve(limit_evals=1e6, verbose=False, track=True, seed=SEED)
                ring_values.append(value)
                SEED += 1

            star_values = np.array(star_values)
            ring_values = np.array(ring_values)

            t_test_res = stats.ttest_ind(star_values, ring_values)
            print("|{:^20}|{:^20}|{:^20}|".format(n_particles, np.round(t_test_res[0], 5), np.round(t_test_res[1]),5))


            # print("|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|".format(
            #     n_particles, np.round(values.mean(), 5), np.round(values.std(), 5), 
            #     np.round(positions.mean(), 5), np.round(positions.std(), 5),
            #     np.round(np.abs(values.mean()-PROBLEM_CONFIG[args['func']]['true_optimal_minimum']), 5)))
        print("-"*106)

    else:
        SEED = 18521489

        solver = PSO[args['topo']](n_particles=args['n_particles'], 
                            n_gen=args['n_gen'], 
                            name_func=args['func'], seed=SEED)
        res, gbest, bpos = solver.solve(limit_evals=args['evaluations'], verbose=True, track=True, seed=SEED)
        print("--> gen_best_val is {}".format(np.round(gbest, 4)))
        print("--> gen_best_pos is {}".format(np.round(bpos, 4)))
        print("--> true_objective_diff is {}".format(np.round(np.abs(gbest-PROBLEM_CONFIG[args['func']]['true_optimal_minimum']), 4)))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Swarm with some function.')
    parser.add_argument('--topo', default='star', choices=['star', 'ring'], required=True,
                        help='The topology when running algorithm.')
    parser.add_argument('--func', default='Rastrigin_2D', required=True,
                        choices=['Rastrigin_2D', 'Rastrigin_10D', 'Rosenbrock_2D', 
                                'Rosenbrock_10D', 'Ackley_2D', 'Eggholder_2D'],
                        help='The function need optimized.')
    parser.add_argument('--n_particles', default=32, type=int,
                        help='The number of particles in the swarm.')
    parser.add_argument('--n_gen', default=50, type=int,
                        help='The number of generations.')
    parser.add_argument('--evaluations', default=1e6, type=int,
                        help='The limit number of evaluations when running algorithm.')
    args = vars(parser.parse_args())

    print_info(args)

    main(args)