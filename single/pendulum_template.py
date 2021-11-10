#!/bin/python3

# Python simulation of a simple planar pendulum with real time animation
# BH, OF, MP, AJ 2020-10-20, latest version 2021-11-02.

from matplotlib import animation
from pylab import *

"""
    This script defines all the classes needed to simulate (and animate) a single pendolum.
    Hierarchy (somehow in order of encapsulation):
    - Oscillator: a struct that stores the parameters of an oscillator (harmonic or pendolum)
    - Observable: a struct that stores the oscillator's coordinates and energy values over time
    - BaseSystem: harmonic oscillators and pendolums are distinguished only by the expression of
                    the return force. This base class defines a virtual force method, which is
                    specified by its child classes
                    -> Harmonic: specifies the return force as -k*t (i.e. spring)
                    -> Pendulum: specifies the return force as -k*sin(t)
    - BaseIntegrator: parent class for all time-marching schemes; function integrate performs
                    a numerical integration steps and updates the quantity of the system provided
                    as input; function timestep wraps the numerical scheme itself and it's not
                    directly implemented by BaseIntegrator, you need to implement it in his child
                    classes (names are self-explanatory)
                    -> EulerIntegrator: ...
                    -> EulerCromerIntegrator: ...
                    -> VerletIntegrator: ...
                    -> RK4Integrator: ...
    - Simulation: this last class encapsulates the whole simulation procedure; functions are 
                    self-explanatory; you can decide whether to just run the simulation or to
                    run while also producing an animation: the latter option is slower
"""

# Global constants
G = 9.8  # gravitational acceleration


class Oscillator:

    """ Class for a general, simple oscillator """

    def __init__(self, m=1, c=9, t0=0, theta0=0, dtheta0=0, gamma=0.5):
        self.m = m              # mass of the pendulum bob
        self.c = c              # c = g/L
        self.L = G / c          # string length
        self.t = t0             # the time
        self.theta = theta0     # the position/angle
        self.dtheta = dtheta0   # the velocity
        self.gamma = gamma


class Observables:

    """ Class for storing observables for an oscillator """

    def __init__(self):
        self.time = []          # list to store time
        self.pos = []           # list to store positions
        self.vel = []           # list to store velocities
        self.energy = []        # list to store energy


class BaseSystem:

    def force(self, osc):
        """ Virtual method: implemented by the childc lasses  """

        pass


class Harmonic(BaseSystem):
    def force(self, osc):
        return -osc.m*osc.c * osc.theta


class Pendulum(BaseSystem):
    def force(self, osc):
        return -osc.m*osc.c * np.sin(osc.theta)

class DampenedHarmonic(BaseSystem):
    def force(self, osc):
        return osc.m * (-osc.c*osc.theta - osc.gamma*osc.dtheta)

class DampenedPendulum(BaseSystem):
    def force(self, osc):
        return -osc.m*osc.c * np.sin(osc.theta) - osc.m*osc.gamma*osc.dtheta


class BaseIntegrator:

    def __init__(self, _dt=0.01):
        self.dt = _dt   # time step

    def integrate(self, simsystem, osc, obs):
        """ Perform a single integration step """

        self.timestep(simsystem, osc, obs)

        # Append observables to their lists
        obs.time.append(osc.t)
        obs.pos.append(osc.theta)
        obs.vel.append(osc.dtheta)
        # Function 'isinstance' is used to check if the instance of the system object is 'Harmonic' or 'Pendolum'
        if isinstance(simsystem, Harmonic):
            # Harmonic oscillator energy
            obs.energy.append(0.5 * osc.m * osc.L ** 2 * osc.dtheta **
                              2 + 0.5 * osc.m * G * osc.L * osc.theta ** 2)
        else:
            # Pendolum energy
            # TODO: Append the total energy for the pendolum (use the correct formula!)
            obs.energy.append(0.5*osc.m*osc.L**2*osc.dtheta **
                              2 + osc.m*G*osc.L*(1-np.cos(osc.theta)))

    def timestep(self, simsystem, osc, obs):
        """ Virtual method: implemented by the child classes """

        pass


# HERE YOU ARE ASKED TO IMPLEMENT THE NUMERICAL TIME-MARCHING SCHEMES:

class EulerIntegrator(BaseIntegrator):
    def timestep(self, simsystem, osc, obs):
        accel = simsystem.force(osc) / osc.m
        # TODO: Implement the integration here, updating osc.theta and osc.dtheta
        # [your implementation goes here ...]
        osc.theta = osc.theta + osc.dtheta*self.dt
        osc.dtheta = osc.dtheta + accel * self.dt

        osc.t += self.dt


class EulerCromerIntegrator(BaseIntegrator):
    def timestep(self, simsystem, osc, obs):
        accel = simsystem.force(osc) / osc.m
        # TODO: Implement the integration here, updating osc.theta and osc.dtheta
        # [your implementation goes here ...]
        osc.dtheta = osc.dtheta + accel * self.dt
        osc.theta = osc.theta + osc.dtheta * self.dt

        osc.t += self.dt


class VerletIntegrator(BaseIntegrator):
    def timestep(self, simsystem, osc, obs):
        accel = simsystem.force(osc) / osc.m
        # TODO: Implement the integration here, updating osc.theta and osc.dtheta
        # [your implementation goes here ...]
        osc.theta = osc.theta + osc.dtheta * self.dt + 0.5 * accel * self.dt**2
        nextAccel = simsystem.force(osc) / osc.m
        osc.dtheta = osc.dtheta + 0.5*(nextAccel + accel) * self.dt

        osc.t += self.dt


class RK4Integrator(BaseIntegrator):
    def timestep(self, simsystem, osc, obs):
        accel = simsystem.force(osc) / osc.m
        # TODO: Implement the integration here, updating osc.theta and osc.dtheta
        # [your implementation goes here ...]
        theta = osc.theta  # Need a copy of both parameters
        dtheta = osc.dtheta

        # Runge-Kutta vars
        a1 = accel * self.dt
        b1 = dtheta * self.dt

        # Due to system.force() we need to update the system to execute the half timesteps
        osc.theta = theta + b1/2
        osc.dtheta = osc.dtheta + a1/2
        a2 = simsystem.force(osc) / osc.m * self.dt
        b2 = osc.dtheta * self.dt

        osc.theta = theta + b2/2
        osc.dtheta = dtheta + a2/2
        a3 = simsystem.force(osc) / osc.m * self.dt
        b3 = osc.dtheta * self.dt

        osc.theta = theta + b3
        osc.dtheta = dtheta + a3
        a4 = simsystem.force(osc) / osc.m * self.dt
        b4 = osc.dtheta * self.dt

        osc.dtheta = dtheta + 1/6*(a1 + 2*a2 + 2*a3 + a4)
        osc.theta = theta + 1/6*(b1 + 2*b2 + 2*b3 + b4)

        osc.t += self.dt


# Animation function which integrates a few steps and return a line for the pendulum
def animate(framenr, simsystem, oscillator, obs, integrator, pendulum_line, stepsperframe):

    for it in range(stepsperframe):
        integrator.integrate(simsystem, oscillator, obs)

    x = np.array([0, np.sin(oscillator.theta)])
    y = np.array([0, -np.cos(oscillator.theta)])
    pendulum_line.set_data(x, y)
    return pendulum_line,


class Simulation:

    def reset(self, osc=Oscillator()):
        self.oscillator = osc
        self.obs = Observables()

    def __init__(self, osc=Oscillator()):
        self.reset(osc)

    def plot_observables(self, title="simulation"):
        folder = "single/plots/"
        plt.clf()
        plt.title(title)
        plt.plot(self.obs.time, self.obs.pos, label="Position")
        plt.plot(self.obs.time, self.obs.vel, label="Velocity")
        plt.plot(self.obs.time, self.obs.energy, label="Energy")
        plt.xlabel('time')
        plt.ylabel('observables')
        plt.legend()
        plt.savefig(folder + title + ".png")
        plt.show()

    def get_period(self,
                   simsystem,
                   integrator,
                   tmax=30.,               # final time
                   ):
        self.run(simsystem, integrator, tmax, show_plot=False)

        t1, t2 = None, None
        for i in range(len(self.obs.vel)-1):
            if self.obs.vel[i] * self.obs.vel[i+1] <= 0: # If its leq 0 then the velocity changed sign 
                if t1 is None:
                    t1 = self.obs.time[i+1]
                else:
                    t2 = self.obs.time[i+1]
                    break
        
        # reset the system
        self.reset(self.oscillator)
        return (t2-t1)*2


    # Run without displaying any animation (fast)
    def run(self,
            simsystem,
            integrator,
            tmax=30.,               # final time
            title="simulation",     # Name of output file and title shown at the top
            show_plot=True,
            ):

        n = int(tmax / integrator.dt)

        for it in range(n):
            integrator.integrate(simsystem, self.oscillator, self.obs)

        if show_plot:
            self.plot_observables(title)

    # Run while displaying the animation of a pendolum swinging back and forth (slow-ish)
    def run_animate(self,
                    simsystem,
                    integrator,
                    tmax=30.,               # final time
                    stepsperframe=5,        # how many integration steps between visualising frames
                    title="simulation",     # Name of output file and title shown at the top
                    ):

        numframes = int(tmax / (stepsperframe * integrator.dt))

        plt.clf()
        # fig = plt.figure()
        ax = plt.subplot(xlim=(-1.2, 1.2), ylim=(-1.2, 1.2))
        plt.axhline(y=0)  # draw a default hline at y=1 that spans the xrange
        plt.axvline(x=0)  # draw a default vline at x=1 that spans the yrange
        pendulum_line, = ax.plot([], [], lw=5)
        plt.title(title)
        # Call the animator, blit=True means only re-draw parts that have changed
        anim = animation.FuncAnimation(plt.gcf(), animate,  # init_func=init,
                                       fargs=[simsystem, self.oscillator, self.obs,
                                              integrator, pendulum_line, stepsperframe],
                                       frames=numframes, interval=25, blit=True, repeat=False)
        plt.show()

        # If you experience problems visualizing the animation and/or
        # the following figures comment out the next line
        plt.waitforbuttonpress(30)

        self.plot_observables(title)

# It's good practice to encapsulate the script execution in
# a main() function (e.g. for profiling reasons)


def main():

    # Here you can define one or more instances of oscillators, with possibly different parameters,
    # and pass them to the simulator

    # Be sure you are passing the correct initial conditions!
    oscillator = Oscillator(m=1, c=9, theta0=np.pi/2, dtheta0=0)

    # Create the simulation object for your oscillator instance:
    simulation = Simulation(oscillator)

    # Examples of calls to 'simulation.run'
    simulation.run(simsystem=Harmonic(),
                   integrator=EulerIntegrator(), title="Harmonic-Euler")
    #simulation.run_animate(simsystem=Harmonic(), integrator=EulerCromerIntegrator(), title="Harmonic-EulerCromer")
    # simulation.run(simsystem=Harmonic(), integrator=VerletIntegrator(), title="Harmonic-Verlet")
    # simulation.run(simsystem=Pendulum(), integrator=VerletIntegrator(), title="Pendulum-Verlet")
    # simulation.run(simsystem=Pendulum(), integrator=RK4Integrator(), title="Harmonic-RK4")


# Calling 'main()' if the script is executed.
# If the script is instead just imported, main is not called (this can be useful if you want to
# write another script importing and utilizing the functions and classes defined in this one)
if __name__ == "__main__":
    main()
