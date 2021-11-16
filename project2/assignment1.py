#!/bin/python3
import random as rnd
from matplotlib import animation
from pylab import *
import point_class as pnt
from bad_random import *

def walk(N, random_func):
    points = pnt.Points()   # Store the points

    for i in range(N):
        R = int(rnd.random() * 4)  # Random number between 0 and 1

        if R < 2:   # Move on the x axis
            if R == 0:
                R = 1
            else:
                R = -1
            points.step(x_step=R)
        else:       # Move on the y axis
            if R == 2:
                R = 1
            else:
                R = -1
            points.step(y_step=R)

    return points

def a():
    points = pnt.Points()   # Store the points
    N = 1000            # Number of steps

    for i in range(N):
        R = int(rnd.random() * 4)  # Random number between 0 and 1

        if R < 2:   # Move on the x axis
            if R == 0:
                R = 1
            else:
                R = -1
            points.step(x_step=R)
        else:       # Move on the y axis
            if R == 2:
                R = 1
            else:
                R = -1
            points.step(y_step=R)


    x, y = points.get_as_lists()
    plt.plot(x, y)
    plt.show()

def b():
    r0 = 1
    a = 3
    c = 4
    m = 128
    br = BadRandom(a, c, m, r0)
    
    points = pnt.Points()   # Store the points
    N = 10                  # Number of steps

    for i in range(N):
        R = br.random()  # Random number between 0 and 1

        if R < 2:   # Move on the x axis
            if R == 0:
                R = 1
            else:
                R = -1
            points.step(x_step=R)
        else:       # Move on the y axis
            if R == 2:
                R = 1
            else:
                R = -1
            points.step(y_step=R)


    x, y = points.get_as_lists()
    plt.plot(x, y)
    plt.show()


def c():

    

if __name__ == "__main__":
    b()
