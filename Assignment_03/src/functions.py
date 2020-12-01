import numpy as np
from constants import a, b, c


def Rastrigin(x: np.array):
    return 10*len(x) + np.sum(x**2 - 10*np.cos(2*np.pi*x))


def RosenBrock(x: np.array):
    return (1-x[0])**2 + 100*(x[1]-x[0]**2)**2


def Eggholder(x: np.array):
    return -(x[1]+47)*np.sin(np.sqrt(np.abs(x[1]+x[0]/2+47))) \
            -x[0]*np.sin(np.sqrt(np.abs(x[0]-(x[1]+47))))


def Ackley(x: np.array):
    return -a*np.e**(-b*np.sqrt(1/len(x)*np.sum(x**2))) \
            -np.e**(1/len(x)*np.sum(np.cos(c*x))) + a + np.e**1


# Test functions
if __name__ == '__main__':
        
    np.random.seed(18521489)

    x = np.random.rand(2)
    res = Ackley(x)
    print("x: ", x)
    print("Ackley(x): ", res)