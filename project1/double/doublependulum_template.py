#!/bin/python3

# Python simulation of a double pendulum with real time animation.
# BH, MP, AJ 2020-10-27, latest version 2021-11-02.

from matplotlib import animation
from pylab import *

"""
    This script simulates and animates a double pendulum.
    Classes are similar to the ones of pendolum_template.py. The main differences are:
    - coordinates are obtained from the total energy value E (look at what functions
        Oscillator.p2squaredFromH and Oscillator.__init__ do)
    - you are asked to implement the expression for the derivatives of the Hamiltonian 
        w.r.t. coordinates p1 and p2
    - you are asked to check when the conditions to produce the Poincare' map are
        satisfied and append the coordinates' values to some container to then plot
"""

# Global constants
G = 9.8  # gravitational acceleration

# Kinetic energy


def Ekin(osc):
    return 1 / (2.0 * osc.m * osc.L * osc.L) * (
        osc.p1 * osc.p1 + 2.0 * osc.p2 * osc.p2 - 2.0 * osc.p1 * osc.p2 * np.cos(osc.q1 - osc.q2)) / (
        1 + (np.sin(osc.q1 - osc.q2)) ** 2)

# Potential energy


def Epot(osc):
    return osc.m * G * osc.L * (3 - 2 * math.cos(osc.q1) - math.cos(osc.q2))


# Class that holds the parameter and state of a double pendulum
class Oscillator:

    def p2squaredFromH(self):
        return (self.E - Epot(self)) * (1 + (np.sin(self.q1 - self.q2)) ** 2) * self.m * self.L * self.L

    # Initial condition is [q1, q2, p1, p2]; p2 is however re-obtained based on the value of E
    # therefore you can use any value for init_cond[3]
    def __init__(self, m=1, L=1, t0=0, E=15, init_cond=[0.0, 0.0, 0.0, -1.0], print_init = True):
        self.m = m      # mass of the pendulum bob
        self.L = L      # arm length
        self.t = t0     # the initial time
        self.E = E      # total conserved energy
        self.q1 = init_cond[0]
        self.q2 = init_cond[1]
        self.p1 = init_cond[2]
        self.p2 = -1.0
        while (self.p2 < 0):
            # Comment the two following lines in case you want to exactly prescribe values to q1 and q2
            # However, be sure that there exists a value of p2 compatible with the imposed total energy E!
            self.q1 = math.pi * (2 * np.random.random() - 1)
            self.q2 = math.pi * (2 * np.random.random() - 1)
            p2squared = self.p2squaredFromH()
            if (p2squared >= 0):
                self.p2 = math.sqrt(p2squared)
        self.q2_prev = self.q2
        if print_init:
            print("Initialization:")
            print("E  = "+str(self.E))
            print("q1 = "+str(self.q1))
            print("q2 = "+str(self.q2))
            print("p1 = "+str(self.p1))
            print("p2 = "+str(self.p2))


# Class for storing observables for an oscillator
class Observables:

    def __init__(self):
        self.time = []          # list to store time
        self.q1list = []        # list to store q1
        self.q2list = []        # list to store q2
        self.p1list = []        # list to store p1
        self.p2list = []        # list to store p2
        self.epot = []          # list to store potential energy
        self.ekin = []          # list to store kinetic energy
        self.etot = []          # list to store total energy
        self.poincare_q1 = []   # list to store q1 for Poincare plot
        self.poincare_p1 = []   # list to store p1 for Poincare plot


# Derivate of H with respect to p1
def dHdp1(q1, q2, p1, p2, m, L):
    # TODO: Write and return the formula for the derivative of H with respect to p1 here
    return (p1-p2*np.cos(q1-q2)) / (L**2 * m * (np.sin(q1-q2)**2 + 1))


# Derivate of H with respect to p2
def dHdp2(q1, q2, p1, p2, m, L):
    # TODO: Write and return the formula for the derivative of H with respect to p2 here
    return (2*p2 - p1*np.cos(q1-q2)) / (L**2 * m * (np.sin(q1-q2)**2 + 1))


# Derivate of H with respect to q1
def dHdq1(q1, q2, p1, p2, m, L):
    return 1 / (2.0 * m * L * L) * (
        -2 * (p1 * p1 + 2 * p2 * p2) * np.cos(q1 - q2) + p1 * p2 * (4 + 2 * (np.cos(q1 - q2)) ** 2)) * np.sin(
            q1 - q2) / (1 + (np.sin(q1 - q2)) ** 2) ** 2 + m * G * L * 2.0 * np.sin(q1)


# Derivate of H with respect to q2
def dHdq2(q1, q2, p1, p2, m, L):
    return 1 / (2.0 * m * L * L) * (
        2 * (p1 * p1 + 2 * p2 * p2) * np.cos(q1 - q2) - p1 * p2 * (4 + 2 * (np.cos(q1 - q2)) ** 2)) * np.sin(q1 - q2) / (
            1 + (np.sin(q1 - q2)) ** 2) ** 2 + m * G * L * np.sin(q2)


class BaseIntegrator:

    def __init__(self, dt=0.01):
        self.dt = dt    # time step

    def integrate(self,
                  osc,
                  obs,
                  ):
        """ Perform a single integration step """
        self.timestep(osc, obs)

        """ Append observables to their lists """
        obs.time.append(osc.t)
        obs.q1list.append(osc.q1)
        obs.q2list.append(osc.q2)
        obs.p1list.append(osc.p1)
        obs.p2list.append(osc.p2)
        obs.epot.append(Epot(osc))
        obs.ekin.append(Ekin(osc))
        obs.etot.append(Epot(osc) + Ekin(osc))
        # TODO: Append values for the Poincare map

        if abs(osc.q2) < 0.005 and osc.p2 > 0:
            obs.poincare_q1.append(osc.q1)
            obs.poincare_p1.append(osc.p1)

    def timestep(self, osc, obs):
        """ Virtual function: implemented by the child classes """
        pass


# Euler-Richardson integrator
class EulerRichardsonIntegrator(BaseIntegrator):
    def timestep(self, osc, obs):
        dt = self.dt
        osc.t += dt
        # TODO: Add integration here
        # see page 46 for algorithm details
        # eq. 6.37 and 6.52

        p1mid = osc.p1 - dHdq1(osc.q1, osc.q2, osc.p1,
                               osc.p2, osc.m, osc.L) * dt/2
        p2mid = osc.p2 - dHdq2(osc.q1, osc.q2, osc.p1,
                               osc.p2, osc.m, osc.L) * dt/2
        q1mid = osc.q1 + dHdp1(osc.q1, osc.q2, osc.p1,
                               osc.p2, osc.m, osc.L) * dt/2
        q2mid = osc.q2 + dHdp2(osc.q1, osc.q2, osc.p1,
                               osc.p2, osc.m, osc.L) * dt/2

        osc.p1 = osc.p1 - dHdq1(q1mid, q2mid, p1mid, p2mid, osc.m, osc.L) * dt
        osc.p2 = osc.p2 - dHdq2(q1mid, q2mid, p1mid, p2mid, osc.m, osc.L) * dt
        osc.q1 = osc.q1 + dHdp1(q1mid, q2mid, p1mid, p2mid, osc.m, osc.L) * dt
        osc.q2 = osc.q2 + dHdp2(q1mid, q2mid, p1mid, p2mid, osc.m, osc.L) * dt


# Runge-Kutta 4 integrator
class RK4Integrator(BaseIntegrator):
    def timestep(self, osc, obs):
        dt = self.dt
        osc.t += dt
        # TODO: Add integration here


# Animation function which integrates a few steps and return a line for the pendulum
def animate(framenr, osc, obs, integrator, pendulum_lines, stepsperframe):
    for it in range(stepsperframe):
        integrator.integrate(osc, obs)

    x1 = math.sin(osc.q1)
    y1 = -math.cos(osc.q1)
    x2 = x1 + math.sin(osc.q2)
    y2 = y1 - math.cos(osc.q2)
    pendulum_lines.set_data([0, x1, x2], [0, y1, y2])
    return pendulum_lines,


class Simulation:

    def reset(self, osc=Oscillator(print_init = False)):
        self.oscillator = osc
        self.obs = Observables()

    def __init__(self, osc=Oscillator(print_init = False)):
        self.reset(osc)

    def plot_observables(self, plot_title=""):

        plt.figure()
        plt.title(plot_title)
        plt.xlabel('q1')
        plt.ylabel('p1')
        plt.plot(self.obs.q1list, self.obs.p1list)
        plt.tight_layout()  # adapt the plot area tot the text with larger fonts

        plt.figure()
        plt.title(plot_title)
        plt.xlabel('q2')
        plt.ylabel('p2')
        plt.plot(self.obs.q2list, self.obs.p2list)
        plt.tight_layout()  # adapt the plot area tot the text with larger fonts

        plt.figure()
        plt.title("Poincare Plot - " + plot_title)
        plt.xlabel('q1')
        plt.ylabel('p1')
        plt.plot(self.obs.poincare_q1, self.obs.poincare_p1, 'ro')
        plt.tight_layout()  # adapt the plot area tot the text with larger fonts

        plt.figure()
        plt.title(plot_title)
        plt.xlabel('time')
        plt.ylabel('energy')
        plt.plot(self.obs.time, self.obs.epot, self.obs.time,
                 self.obs.ekin, self.obs.time, self.obs.etot)
        plt.legend(('Epot', 'Ekin', 'Etot'))
        plt.tight_layout()  # adapt the plot area tot the text with larger fonts
        plt.show()

    def run(self,
            integrator,
            tmax=30.,   # final time
            outfile='energy1.pdf',
            show_plot=True, 
            plot_title=""
            ):

        n = int(tmax / integrator.dt)

        for it in range(n):
            integrator.integrate(self.oscillator, self.obs)

        # If you experience problems visualizing the animation and/or
        # the following figures comment out the next line
        # plt.waitforbuttonpress(30)

        if show_plot:
            self.plot_observables(plot_title)

    def run_animate(self,
                    integrator,
                    tmax=30.,           # final time
                    stepsperframe=5,    # how many integration steps between visualising frames
                    outfile='energy1.pdf'
                    ):

        numframes = int(tmax / (stepsperframe * integrator.dt))

        # plt.clf()
        fig = plt.figure()
        ax = plt.subplot(xlim=(-2.2, 2.2), ylim=(-2.2, 2.2))
        plt.axhline(y=0)  # draw a default hline at y=1 that spans the xrange
        plt.axvline(x=0)  # draw a default vline at x=1 that spans the yrange
        pendulum_lines, = ax.plot([], [], lw=5)

        # Call the animator, blit=True means only re-draw parts that have changed
        anim = animation.FuncAnimation(fig, animate,  # init_func=init,
                                       fargs=[
                                           self.oscillator, self.obs, integrator, pendulum_lines, stepsperframe],
                                       frames=numframes, interval=25, blit=True, repeat=False)
        plt.show()

        # If you experience problems visualizing the animation and/or
        # the following figures comment out the next line
        plt.waitforbuttonpress(30)

        self.plot_observables()

# It's good practice to encapsulate the script execution in
# a main() function (e.g. for profiling reasons)


def main():
    # Be sure you are passing the correct initial conditions!, init_cond = [q1, q2, p1, p2] (p2 is not used)
    oscillator = Oscillator(m=1, L=1, t0=0, E=15, init_cond=[1, 1, 0, -1])

    # Create the simulation object for your oscillator instance:
    simulation = Simulation(oscillator)

    # Run the simulation using the various integration schemes (that you are asked to implement):
    #simulation.run(integrator=EulerRichardsonIntegrator(),  tmax=100.)
    simulation.run(integrator=EulerRichardsonIntegrator(dt=0.001))


# Calling 'main()' if the script is executed.
# If the script is instead just imported, main is not called (this can be useful if you want to
# write another script importing and utilizing the functions and classes defined in this one)
if __name__ == "__main__":
    main()
    
