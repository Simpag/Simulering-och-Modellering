from pendulum_template import *

def assignment1():
    # Be sure you are passing the correct initial conditions!
    initTheta = [0.1, 0.3, 0.5]
    oscillators = []
    simulations = []

    for theta in initTheta:
        oscillators.append(Oscillator(m=1, c=9, theta0=theta*np.pi, dtheta0=0))

        # Create the simulation object for your oscillator instance:
        simulations.append(Simulation(oscillators[-1]))

        # Harmonic
        simulations[-1].run(simsystem=Harmonic(), integrator=EulerCromerIntegrator(), title=f'Harmonic-Euler-Cromer, Theta:{theta}', tmax=70)
        simulations[-1].run(simsystem=Harmonic(), integrator=VerletIntegrator(), title=f'Harmonic-Verlet, Theta:{theta}', tmax=70)
        simulations[-1].run(simsystem=Harmonic(), integrator=RK4Integrator(), title=f'Harmonic-RK, Theta:{theta}', tmax=70)

        # Pendulum
        simulations[-1].run(simsystem=Pendulum(), integrator=EulerCromerIntegrator(), title=f'Pendulum-Euler-Cromer, Theta:{theta}', tmax=70)
        simulations[-1].run(simsystem=Pendulum(), integrator=VerletIntegrator(), title=f'Pendulum-Verlet, Theta:{theta}', tmax=70)
        simulations[-1].run(simsystem=Pendulum(), integrator=RK4Integrator(), title=f'Pendulum-RK, Theta:{theta}', tmax=70)

def assignment2():
    # Determine the period
    T_Harmonic = []
    T_Pendulum = []
    T_True = []
    theta0 = []
    dTheta = 0.1

    for _theta0 in np.arange(0.000001,np.pi,dTheta):
        if _theta0 % 0.1 == 0:
            print(_theta0)
        theta0.append(_theta0)
        oscillator = Oscillator(m=1, c=9, theta0=_theta0, dtheta0=0)
        simulation = Simulation(oscillator)
        T_Harmonic.append(simulation.get_period(simsystem=Harmonic(), integrator=RK4Integrator(), tmax=80))
        oscillator = Oscillator(m=1, c=9, theta0=_theta0, dtheta0=0) # This fixes some bug, cant be bothered
        simulation = Simulation(oscillator)
        T_Pendulum.append(simulation.get_period(simsystem=Pendulum(), integrator=RK4Integrator(), tmax=80))
        T_True.append(2*np.pi/np.sqrt(oscillator.c)*(1 + _theta0**2 / 16 + _theta0**4 *11/3072 + 173/737280 * _theta0**6))

    # Plot the period time as a function of theta0
    plt.clf()
    plt.title("Period time")
    plt.plot(theta0, T_Harmonic, label="Harmonic")
    plt.plot(theta0, T_Pendulum, label="Pendulum")
    plt.plot(theta0, T_True, label="True")
    plt.xlabel(r'$\theta$')
    plt.ylabel('Period Time (s)')
    plt.legend()
    #plt.savefig("plots" + "period" + ".png")
    plt.show()

def assignment3():
    oscillator = Oscillator(m=1, c=9, theta0=1, dtheta0=0, gamma=5.908207397460938)
    simulation = Simulation(oscillator)
    simulation.run_animate(simsystem=DampenedHarmonic(), integrator=EulerCromerIntegrator(), tmax=100, title="HarmonicDampening")

def assignment3_1():
    gammas = [0.5, 1, 2, 3]

    for gamma in gammas:
        oscillator = Oscillator(m=1, c=9, theta0=1, dtheta0=0, gamma=gamma)
        simulation = Simulation(oscillator)
        simulation.run(simsystem=DampenedHarmonic(), integrator=EulerCromerIntegrator(), tmax=100, title=f"HarmonicDampening-RK4, gamma: {gamma}")

def assignment3_2():
    # find the smallest gamma such that the pendulum doesnot pass x = 0
    tolerance = 0.001
    left = 0 # min gamma
    right = 30 # max gamma
    middle = 0

    while left <= right:
        middle = (left + right) / 2

        oscillator = Oscillator(m=1, c=9, theta0=1, dtheta0=0, gamma=middle)
        simulation = Simulation(oscillator)
        simulation.run(simsystem=DampenedHarmonic(), integrator=EulerCromerIntegrator(), tmax=50, show_plot=False)
        x = simulation.obs.pos

        if np.sum(n < 0 for n in x) > 0:
            left = middle + tolerance
        elif np.sum(n < 0 for n in x) == 0:
            right = middle - tolerance
        
        if (right - left) <= tolerance:
            print(f'Smallest gamma is {middle}')
            return

    print("Could not find critical damping")

def assignment4():
    # Plot the phase space portait
    oscillator = Oscillator(m=1, c=9, theta0=np.pi*0.5, dtheta0=0, gamma=1)
    simulation = Simulation(oscillator)
    simulation.run(simsystem=DampenedPendulum(), integrator=EulerCromerIntegrator(), tmax=100, show_plot=False)

    plt.clf()
    plt.title("Phase space potrait")
    plt.plot(simulation.obs.pos, simulation.obs.vel)
    plt.xlabel(r'$\theta$')
    plt.ylabel(r'$\dot \theta$')
    plt.show()

def main():
    # Select assignment 
    assignment4()

if __name__ == '__main__':
    main()
    #oscillator = Oscillator(m=1, c=9, theta0=np.pi, dtheta0=0)
    #simulation = Simulation(oscillator)
    #simulation.run_animate(simsystem=Pendulum(), integrator=EulerCromerIntegrator(), tmax=100)
