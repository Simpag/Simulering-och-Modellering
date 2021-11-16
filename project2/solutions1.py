#!/bin/python3
import random as rnd
from matplotlib import animation
from pylab import *
import point_class as pnt
from bad_random import *
from alive_progress import alive_bar  # pip3 install alive_progress


def walk(N, random_func):
    points = pnt.Points()   # Store the points

    for i in range(N):
        R = random_func()   # Random number between 0 and 1

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
    N = 100
    points = walk(N, lambda: int(rnd.random() * 4))

    x, y = points.get_as_lists()
    plt.plot(x, y)
    plt.show()


def b():
    r0 = 1
    a = 3
    c = 4
    m = 128
    br = BadRandom(a, c, m, r0)

    N = 100                  # Number of steps
    points = walk(N, br.random)

    x, y = points.get_as_lists()
    plt.plot(x, y)
    plt.show()


def c():
    def random_func(): return int(rnd.random() * 4)

    def RMSD(N, iterations):
        """Root-mean-squared end-to-end distance"""
        dist_squared = []
        for i in range(iterations):
            points = walk(N, random_func)
            dist_squared.append(walk_length_squared(points))

        return np.sqrt(np.average(dist_squared))

    def RMSF(N, iterations):
        """ Root-mean-sqare fluctuation"""
        dist_squared, dist = [], []
        for i in range(iterations):
            points = walk(N, random_func)
            dist.append(np.sqrt(walk_length_squared(points)))
            dist_squared.append(walk_length_squared(points))

        return np.sqrt((np.average(dist_squared)-np.average(dist)**2) * iterations / (iterations - 1))

    def walk_length_squared(points):
        start = points[0]
        end = points[-1]

        return (end.x - start.x)**2 + (end.y - start.y)**2

    #########################################################################################################
    # Variables
    NList = list(range(0, 10**3, 10))  # A list from 0 to 1000
    avg_iterations = 100

    if False:
        rmsd = []
        with alive_bar(len(NList), title="Processing RMSD") as bar:
            for N in NList:
                rmsd.append(RMSD(N, avg_iterations))
                bar()

        plt.title(f"RMSD for random walk with rnd.random()")
        plt.xlabel('Number of steps')
        plt.ylabel('RMSD')
        plt.plot(NList, rmsd)
        plt.tight_layout()  # adapt the plot area tot the text with larger fonts
        plt.show()

    if True:
        rmsf = []
        with alive_bar(len(NList), title="Processing RMSF") as bar:
            for N in NList:
                rmsf.append(RMSF(N, avg_iterations))
                bar()

        plt.title(f"RMSF for random walk with rnd.random()")
        plt.xlabel('Number of steps')
        plt.ylabel('RMSF')
        plt.plot(NList, rmsf)
        plt.tight_layout()  # adapt the plot area tot the text with larger fonts
        plt.show()

    # What the fuck is standard error estimate

#############################################################################################################


def self_avoiding_walk_1(N):
    """
    Tries to create a self avoiding walk one time,
    loop the function to generate a successful walk

    Returns the points if a walk was successful, else None
    """
    points = pnt.Points()   # Store the points

    for i in range(N):
        R = int(rnd.random() * 4)   # Random number between 0 and 1

        if R < 2:   # Move on the x axis
            if R == 0:
                R = 1
            else:
                R = -1
            if not points.step(x_step=R, self_avoid=True):  # Ran into itself
                return None
        else:       # Move on the y axis
            if R == 2:
                R = 1
            else:
                R = -1
            if not points.step(y_step=R, self_avoid=True):
                return None

    return points


def self_avoiding_walk_2(N):
    """
    Tries to create a self avoiding walk one time,
    loop the function to generate a successful walk

    Returns the points if a walk was successful, else None
    """
    points = pnt.Points()   # Store the points
    prev_R = None

    R = 0
    for i in range(N):
        while True:                     # Dont go in the same direction as you came from
            R = int(rnd.random() * 4)   # Random number between 0 and 1

            if prev_R is None:
                break
            elif prev_R == 0 and R != 1:
                break
            elif prev_R == 1 and R != 0:
                break
            elif prev_R == 2 and R != 3:
                break
            elif prev_R == 3 and R != 2:
                break

        prev_R = R

        if R < 2:   # Move on the x axis
            if R == 0:
                R = 1
            else:
                R = -1
            if not points.step(x_step=R, self_avoid=True):  # Ran into itself
                return None
        else:       # Move on the y axis
            if R == 2:
                R = 1
            else:
                R = -1
            if not points.step(y_step=R, self_avoid=True):
                return None

    return points


def d_1(show_plot=True, NList=list(range(0, 20, 2)), iterations=1000):
    successFraction = [0, ] * len(NList)

    with alive_bar(len(NList), title="Processing success of self avoiding walk 1") as bar:
        for i in range(len(NList)):
            _sf = []  # local success fraction
            for j in range(iterations):
                walks = 0
                failedAttempts = 0
                while True:
                    points = self_avoiding_walk_1(NList[i])
                    walks += 1

                    if points is None:
                        failedAttempts += 1
                    else:
                        break
                _sf.append((walks-failedAttempts) / walks)
                # x,y = points.get_as_lists()
                # plt.plot(x,y)
                # plt.show()

            successFraction[i] = np.average(_sf)
            bar()

    if show_plot:
        plt.plot(NList, successFraction)
        plt.show()

    return successFraction


def d_2(show_plot=True, NList=list(range(0, 50, 2)), iterations=1000):
    successFraction = [0, ] * len(NList)

    with alive_bar(len(NList), title="Processing success of self avoiding walk 2") as bar:
        for i in range(len(NList)):
            _sf = []  # local success fraction
            for j in range(iterations):
                walks = 0
                failedAttempts = 0
                while True:
                    points = self_avoiding_walk_2(NList[i])
                    walks += 1

                    if points is None:
                        failedAttempts += 1
                    else:
                        break
                _sf.append((walks-failedAttempts) / walks)
                # x,y = points.get_as_lists()
                # plt.plot(x,y)
                # plt.show()

            successFraction[i] = np.average(_sf)
            bar()

    if show_plot:
        plt.plot(NList, successFraction)
        plt.show()

    return successFraction


def d_3():
    """Compare sucess rates"""
    NList = list(range(0, 25, 2))
    iterations = 1000
    walk1 = d_1(False, NList, iterations)
    walk2 = d_2(False, NList, iterations)
    improvement = [0,] * len(walk1)

    for i in range(len(walk1)):
        improvement[i] = (walk2[i] - walk1[i]) / walk1[i]
    
    plt.plot(NList, improvement)
    plt.show()


def e():
    def RMSD(N, iterations):
        """Root-mean-squared end-to-end distance"""
        dist_squared = []
        for i in range(iterations):
            points = None
            while points is None:
                points = self_avoiding_walk_2(N)

            dist_squared.append(walk_length_squared(points))

        return np.sqrt(np.average(dist_squared))

    def walk_length_squared(points):
        start = points[0]
        end = points[-1]

        return (end.x - start.x)**2 + (end.y - start.y)**2

    #########################################################################################################
    # Variables
    NList = list(range(0, 70))
    avg_iterations = 100

    rmsd = []
    with alive_bar(len(NList), title="Processing RMSD") as bar:
        for N in NList:
            rmsd.append(RMSD(N, avg_iterations))
            bar()

    plt.title(f"RMSD for self avoiding random walk")
    plt.xlabel('Number of steps')
    plt.ylabel('RMSD')
    plt.plot(NList, rmsd)
    plt.tight_layout()  # adapt the plot area tot the text with larger fonts
    plt.show()

if __name__ == "__main__":
    e()
