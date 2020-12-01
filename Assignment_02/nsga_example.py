from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

problem = get_problem("zdt5")

algorithm = NSGA2(pop_size=200)

res = minimize(problem, algorithm, 
                ('n_gen', 200),
                seed=1,
                verbose=True)
            
plot = Scatter()
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, color='red')
plot.show()
plot.save('./figures/demo_nsga_zdt5.png')