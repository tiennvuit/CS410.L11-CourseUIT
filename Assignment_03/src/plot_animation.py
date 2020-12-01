import os
import sys
import argparse
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pso_ring import PSO_Ring
from pso_star import PSO_Star
from problem_config import PROBLEM_CONFIG
from constants import a, b, c


def init():
    ax.set_xlim(-func['search_domain']-50, func['search_domain']+50)
    ax.set_ylim(-func['search_domain']-50, func['search_domain']+50)
    return ln,


def update_star(frame):
    res = []
    with open('log_files/star/Eggholder_2D_32_50_18521489/gen{}'.format(str(frame).zfill(5)), 'r') as fi:
        for line in fi.readlines():
            li = np.array([0,0], dtype='float64')
            li[0], li[1] = map(float,line.split())
            res.append(li)
        res = np.array(res)
    xdata = res[:,0]
    ydata = res[:,1]
    ax.set_title(f'Star topology GEN {frame + 1}')
    ln.set_data(xdata, ydata)
    return ln,


def update_ring(frame):
    res = []
    with open('log_files/ring/Eggholder_2D_32_50_18521489/gen{}'.format(str(frame).zfill(5)), 'r') as fi:
        for line in fi.readlines():
            li = np.array([0, 0], dtype='float64')
            li[0], li[1] = map(float,line.split())
            res.append(li)
        res = np.array(res)
    xdata = res[:,0]
    ydata = res[:,1]
    ax.set_title(f'Ring topology - GEN {frame + 1}')
    ln.set_data(xdata, ydata)
    return ln,


function_list = ["Rastrigin_2D", "Rosenbrock_2D", "Ackley_2D", "Eggholder_2D", "Rastrigin_10D"]

name_func = function_list[3]
func = PROBLEM_CONFIG[name_func]

xlist = np.linspace(-func['search_domain']-50, func['search_domain']+50, 1000)
ylist = np.linspace(-func['search_domain']-50, func['search_domain']+50, 1000)

X, Y = np.meshgrid(xlist, ylist)
if name_func == 'Rastrigin_2D':
    Z = (X**2 - 10 * np.cos(2 * 3.14 * X)) + (Y**2 - 10 * np.cos(2 * 3.14 * Y)) + 20
elif name_func == 'Rosenbrock_2D':
    Z = (1.-X)**2 + 100.*(Y-X*X)**2
elif name_func == 'Ackley_2D':
    Z = a + np.exp(1) + -a * np.exp(-b*np.sqrt(X*X + Y*Y) / 2) + -np.exp((np.cos(c*X) + np.cos(c*Y))/2)
elif name_func == 'Eggholder_2D':
    Z = -(Y + 47) * np.sin(np.sqrt(np.abs(X/2 + (Y + 47)))) -X * np.sin(np.sqrt(np.abs(X - (Y + 47))))

# Create animation gif for Star topo
writergif = animation.PillowWriter(fps=1) 

fig, ax = plt.subplots(1,1)
#fig.set_tight_layout(True)
#sns.set_style("white")
cp = ax.contourf(X, Y, Z)
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')
ani = FuncAnimation(fig, update_star, frames=np.arange(50, step=4),
                    init_func=init, blit=True, interval=500)
plt.show()
print("Saving {} animation in to plot/star/{}.gif".format(name_func, name_func))
ani.save("plot/star/{}.gif".format(name_func), writer=writergif)

# Create animation gif for Star topo
fig, ax = plt.subplots(1, 1)
fig.set_tight_layout(True)
cp = ax.contourf(X, Y, Z)
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')
ani = FuncAnimation(fig, update_ring, frames=np.arange(50, step=4),
                    init_func=init, blit=True, interval=500)
plt.show()
print("Saving {} animation in to plot/ring/{}.gif".format(name_func, name_func))
ani.save("plot/ring/{}.gif".format(name_func), writer=writergif)