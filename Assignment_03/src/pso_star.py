import os
import argparse
import shutil
import numpy as np

from particle import Particle
from config import w, c1, c2
from problem_config import PROBLEM_CONFIG


class PSO_Star():


    def __init__(self, n_particles:int, n_gen:int, name_func:str, seed=18521489):

        np.random.seed(seed=seed)
        self.n_particles = n_particles
        self.n_gen = n_gen
        self.func = name_func
        self.best_of_particles_score = [float('inf')] * n_particles
        self.best_of_particles_pos = [None] * n_particles
        self.particles = []

        optimized_function = PROBLEM_CONFIG[self.func]

        for _ in range(self.n_particles):
            self.particles.append(Particle(optimized_function))

        self.gen_best_pos = None
        self.gen_best_val = float('inf')
        self.w = w
        self.c1 = c1
        self.c2 = c2


    def solve(self, limit_evals, track=False, verbose=True, seed=18521489):

        np.random.seed(seed=seed)

        base_dir = os.path.join('log_files', 'star')
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        saving_folder = os.path.join(
            'log_files', 'star', "{}_{}_{}_{}".format(self.func, str(self.n_particles), str(self.n_gen), str(seed)))
        if os.path.exists(saving_folder):
            shutil.rmtree(saving_folder)
        os.mkdir(saving_folder)
        
        if verbose:
            print("-"*33 + "RUNING PSO ALGORITHM with STAR TOPOLOGY" + "-"*33)
            print("|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|".format(
                    'n_gen', 'evals', 'best_val', 'mean_particle', 'std_particle', 'true_optimal_diff'))
            print("-"*127)
        n_evaluations = 0
    
        for i in range(self.n_gen):
            result = []
            for particle in self.particles:
                result.append(particle.position)
            result = np.array(result)

            for particle in self.particles:

                particle.fitness()
                if particle.score < self.gen_best_val:
                    self.gen_best_val = particle.score
                    self.gen_best_pos = particle.position.copy()

                n_evaluations += 1
                
                if n_evaluations > limit_evals:
                    return result, self.gen_best_val, self.gen_best_pos
            
            for particle in self.particles:
                new_velocity = (self.w*particle.vel)\
                            + (self.c1*np.random.random()) * (particle.best_pos - particle.position) \
                            + (np.random.random()*self.c2) * (self.gen_best_pos - particle.position)
                particle.vel = new_velocity
                particle.move()
            
            if verbose:
                print("|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|".format(
                    i, n_evaluations, np.round(self.gen_best_val, 5), 
                    np.round(np.array([x.score for x in self.particles]).mean(), 5),
                    np.round(np.array([x.score for x in self.particles]).std(), 5),
                    np.round(np.abs(self.gen_best_val-PROBLEM_CONFIG[self.func]['true_optimal_minimum']))))

            if track:
                np.savetxt(os.path.join(saving_folder, "gen{}".format(str(i).zfill(5))), result)

            if np.array([x.score for x in self.particles]).std() < 0.00001:
                return result, self.gen_best_val, self.gen_best_pos
            
        if verbose:
            print("-"*127)
            #self.print_particle()
            #input()
        return result, self.gen_best_val, self.gen_best_pos


    def print_particle(self):
        print('---------------------------')
        for particle in sorted(self.particles, key=lambda x: x.score)[:1]:
            print(f'{particle.score} - {particle.position} : vel {particle.vel}')

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Swarm with some function.')
    parser.add_argument('--func', default='Rastrigin_2D', required=True,
                        help='The function need optimized.')
    parser.add_argument('--n_particles', default=32, type=int,
                        help='The number of particles in the swarm.')
    parser.add_argument('--n_gen', default=50, type=int,
                        help='The number of generations.')
    parser.add_argument('--evaluations', default=1e6, type=int,
                        help='The limit number of evaluations when running algorithm.')
    args = vars(parser.parse_args())
    print(args)
    np.random.seed(18251489)

    obj_pso = PSO_Star(n_particles=args['n_particles'], 
                       n_gen=args['n_gen'], 
                       name_func=args['func'])

    obj_pso.solve(limit_evals=args['evaluations'], verbose=True, track=False)
    