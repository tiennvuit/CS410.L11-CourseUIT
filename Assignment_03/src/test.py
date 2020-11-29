import numpy as np
from functions import Rastrigin, Rosenbrock, Eggholder, Ackley


if __name__ == '__main__':
    
    np.random.seed(18521489)

    x = np.random.rand(2)
    res = Ackley(x)
    print("x: ", x)
    print("Ackley(x): ", res)