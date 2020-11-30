import os
import sys
import argparse
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt

from pso_ring import PSO_Ring
from pso_star import PSO_Star
from problem_config import PROBLEM_CONFIG
from constants import a, b, c


topo_dir = sys.argv[2]
func_dir = sys.argv[4]
print(topo_dir)
print(func_dir)


def init():
    ax.set_xlim(-func['search_domain'], func['search_domain'])
    ax.set_ylim(-func['search_domain'], func['search_domain'])
    return ln,


def update(frame):
    
    res = []
    open_file = os.path.join('log_files', topo_dir, func_dir, '{}'.format(str(frame).zfill(5)))
    with open(open_file, 'r') as fi:
        for line in fi:
            li = np.array([0,0], dtype='float64')
            li[0], li[1] = map(float, line.split())
            res.append(li)
        res = np.array(res)
    xdata = res[:,0]
    ydata = res[:,1]
    ax.set_title(f'GEN {frame + 1}')
    ln.set_data(xdata, ydata)
    return ln,


def main(args):

    name_func = os.path.split(args['log_file'])[1].split("_")[0] + "_" + os.path.split(args['log_file'])[1].split("_")[1]
    func = PROBLEM_CONFIG[name_func]
    xlist = np.linspace(-func['search_domain'], func['search_domain'], 100)
    ylist = np.linspace(-func['search_domain'], func['search_domain'], 100)


    X, Y = np.meshgrid(xlist, ylist)
    if name_func == 'Rastrigin_2D':
        Z = (X**2 - 10 * np.cos(2 * 3.14 * X)) + (Y**2 - 10 * np.cos(2 * 3.14 * Y)) + 20
    elif name_func == 'Rosenbrock_2D':
        Z = (1.-X)**2 + 100.*(Y-X*X)**2
    elif name_func == 'Ackley_2D':
        Z = a + np.exp(1) + -a * np.exp(-b*np.sqrt(X*X + Y*Y) / 2) + -np.exp((np.cos(c*X) + np.cos(c*Y)) / 2)
    elif name_func == 'Eggholder_2D':
        Z = -(Y + 47) * np.sin(np.sqrt(np.abs(X/2 + (Y + 47)))) -X * np.sin(np.sqrt(np.abs(X - (Y + 47))))

    fig, ax = plt.subplots(1,1)
    cp = ax.contourf(X, Y, Z)
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'ro')
    plt.show()
    # ani = FuncAnimation(fig, update, frames=np.arange(50, step=4),
    #                     init_func=init, blit=True, interval=500)

    # saving_path = os.path.join("plot", args['topo'], name_func + ".gif")
    # print(saving_path)
    # ani.save(saving_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Swarm with some function.')
    parser.add_argument('--topo', default='star', choices=['star', 'ring'], required=True,
                        help='The topology when running algorithm.')
    parser.add_argument('--log_file', default='log_file/star/Rastrigin_2D_32_50_18521489', required=True,
                        help='The function need optimized.')
    args = vars(parser.parse_args())

    main(args)


