import argparse
import numpy as np

from problem_config import Rastrigin_2D, Rastrigin_10D, \
                           Rosenbrock_2D, Rosenbrock_10D, \
                           Ackley_2D, Eggholder_2D
from problem_config import PROBLEM_CONFIG

class Particle():


    def __init__(self, optimizing_func):
        self.func = optimizing_func
        self.position = []
        self.dim = optimizing_func['dimension']
        
        for _ in range(self.dim):
            #self.position.append((-1) ** (bool(random.getrandbits(1))) * random.random()*optimizing_func['search_domain'])
            # CHANGE latter with np.random
            self.position.append((-1) ** (bool(np.random.randint(low=0, high=2, size=1))) * np.random.random()*self.func['search_domain'])

        self.position = np.array(self.position)
        self.score = float('inf')
        self.best_pos = self.position.copy()
        self.best_val = float('inf')
        self.vel = np.zeros(self.position.shape)


    def move(self):
        self.position = self.position + self.vel
        for i in range(len(self.position)):
            if self.position[i] > self.func['search_domain']:
                self.position[i] = self.func['search_domain']
            elif self.position[i] < -self.func['search_domain']:
                self.position[i] = -self.func['search_domain']
        

    def fitness(self):
        self.score = self.func['score'](self.position)
        if self.score < self.best_val:
            self.best_val = self.score
            self.best_pos = self.position


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Particle with some function.')
    parser.add_argument('--func', default='Rastrigin_2D', required=True,
                        help='The function need optimized.')

    args = vars(parser.parse_args())


    np.random.seed(18251489)

    optimizing_func = PROBLEM_CONFIG[args['func']]

    obj_particle = Particle(optimizing_func=optimizing_func)
    attrs = vars(obj_particle)    
    print('\n '.join("%s: %s" % item for item in attrs.items()))

    obj_particle.move()
    obj_particle.fitness()
    attrs = vars(obj_particle)    
    print('\n '.join("%s: %s" % item for item in attrs.items()))

