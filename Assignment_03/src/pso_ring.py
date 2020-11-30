import os
import argparse
import shutil
import numpy as np

from particle import Particle
from config import w, c1, c2
from problem_config import PROBLEM_CONFIG


class PSO_Ring():


    def __init__(self, n_particles, n_gen, name_func:str, seed=18521489):

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

        # Start Ring topology
        self.mini_swarms = []
        for x in zip(np.arange(n_particles-2), np.arange(n_particles-2) + 1, np.arange(n_particles-2)+2):
            self.mini_swarms.append(x)
        self.mini_swarms.append((n_particles - 2, n_particles - 1, 0))
        self.mini_swarms.append((n_particles - 1, 0, 1))
        self.mini_scores = [float('inf')] * len(self.mini_swarms)
        self.mini_pos = [None] * len(self.mini_swarms)
        # End Ring topology

        self.gen_best_pos = None
        self.gen_best_val = float('inf')
        self.w = w
        self.c1 = c1
        self.c2 = c2


    def update_best_of_swarm(self):

        # Loop through each mini_swarm to UPDATE two info of each mini_swarm:
        #   1. Mini_scores
        #   2. Mini pos
        for i in range(len(self.mini_swarms)):
            # Loop through each group in mini_swarm
            for px in [self.particles[x] for x in self.mini_swarms[i]]:
                if px.score < self.mini_scores[i]:
                    self.mini_scores[i] = px.score
                    self.mini_pos[i] = px.position.copy()

        # Loop through each particle in swarm to UPDATE two info of each partcile
        #   1. Best_of_particle_score
        #   2. Best_of_partcile_pos

        for pid, particle in enumerate(self.particles):
            for sid, trio in enumerate(self.mini_swarms):
                if pid in trio:  # If the particle is in the mini_swarm
                    if self.best_of_particles_score[pid] > self.mini_scores[sid]:
                        self.best_of_particles_score[pid] = self.mini_scores[sid]
                        self.best_of_particles_pos[pid] = self.mini_pos[sid].copy()


    def solve(self, limit_evals, track=False, verbose=True, seed=18521489):

        np.random.seed(seed=seed)

        base_dir = os.path.join('result', 'ring')
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        saving_folder = os.path.join(
            'result', 'ring', "{}_{}_{}_{}".format(self.func, str(self.n_particles), str(self.n_gen), str(seed)))
        if os.path.exists(saving_folder):
            shutil.rmtree(saving_folder)
        os.mkdir(saving_folder)
        
        if verbose:
            print("-"*33 + "RUNING PSO ALGORITHM with RING TOPOLOGY" + "-"*33)
            print("|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|".format(
                    'n_gen', 'evals', 'best_val', 'mean_bscore', 'std_bscore', 'true_optimal_diff'))

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
                    self.gen_best_pos = particle.position
                n_evaluations += 1
                if n_evaluations > limit_evals:
                    return result, self.gen_best_val, self.gen_best_pos

            self.update_best_of_swarm()

            for pid, particle in enumerate(self.particles):
                new_velocity = (self.w*particle.vel) \
                               + (self.c1*np.random.random()) * (particle.best_pos-particle.position) \
                               + (np.random.random()*self.c2) * (self.best_of_particles_pos[pid]-particle.position)
                particle.vel = new_velocity
                particle.move()
            
            if verbose:
                print("|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|".format(
                    i, n_evaluations, 
                    np.round(self.gen_best_val, 5), 
                    np.round(np.array(self.best_of_particles_score).mean(), 5),
                    np.round(np.array(self.best_of_particles_score).std(), 5),
                    np.round(np.abs(self.gen_best_val-PROBLEM_CONFIG[self.func]['true_optimal_minimum']))))

                
            if track:
                np.savetxt(os.path.join(saving_folder, "gen{}".format(str(i).zfill(5))), result)

            if np.array(self.best_of_particles_score).std() < 0.001:
                return result, self.gen_best_val, self.gen_best_pos

        print("-"*127)
            #self.print_particle()
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

    np.random.seed(18251489)

    obj_pso = PSO_Ring(n_particles=args['n_particles'], 
                       n_gen=args['n_gen'], 
                       name_func=args['func'])

    obj_pso.solve(limit_evals=args['evaluations'], verbose=True, track=True)
    