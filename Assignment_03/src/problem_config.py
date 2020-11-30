from functions import Rastrigin, RosenBrock, Eggholder, Ackley


Rastrigin_2D = {
    'search_domain': 5.12,
    'score': Rastrigin,
    'dimension': 2,
    'true_optimal_minimum': 0,
    'name': "Rastrigin 2 Dimension"
}

Rastrigin_10D = {
    'search_domain': 5.12,
    'score': Rastrigin,
    'dimension': 10,
    'true_optimal_minimum': 0,
    'name': "Rastrigin 10 Dimension"
}

Rosenbrock_2D = {
    'search_domain': 100.0,
    'score': RosenBrock,
    'dimension': 2,
    'true_optimal_minimum': 0,
    'name': "RosenBrock 2 Dimension"
}

Rosenbrock_10D = {
    'search_domain': 100.0,
    'score': RosenBrock,
    'dimension': 10,
    'true_optimal_minimum': 0,
    'name': "RosenBrock 10 Dimension"
}

Ackley_2D = {
    'search_domain': 5,
    'score': Ackley,
    'dimension': 2,
    'true_optimal_minimum': 0,
    'name': "Ackley"    
}

Eggholder_2D = {
    'search_domain': 512,
    'score': Eggholder,
    'dimension': 2,
    'true_optimal_minimum': -959.6407,
    'name': "Eggholder"    
}


PROBLEM_CONFIG = {
    'Rastrigin_2D': Rastrigin_2D,
    'Rastrigin_10D': Rastrigin_10D,
    'Rosenbrock_2D': Rosenbrock_2D, 
    'Rosenbrock_10D': Rosenbrock_10D,
    'Ackley_2D': Ackley_2D,
    'Eggholder_2D': Eggholder_2D,
}