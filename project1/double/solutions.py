from doublependulum_template import *
from alive_progress import alive_bar # pip3 install alive_progress

def assignment5_a():
    EList = [1, 5, 10, 15, 40]

    for i in range(len(EList)):
        oscillator = Oscillator(
            m=1, L=1, t0=0, E=EList[i], init_cond=[1, 1, 0, -1])
        simulation = Simulation(oscillator)
        simulation.run(integrator=EulerRichardsonIntegrator(
            dt=0.001), show_plot=False)

        plt.subplot(2, 2, 1)
        plt.title("q1 - time")
        plt.xlabel('time')
        plt.ylabel('q1')
        plt.plot(simulation.obs.time, simulation.obs.q1list,
                 label=f'E={EList[i]}')
        plt.legend()
        plt.tight_layout()

        plt.subplot(2, 2, 2)
        plt.title("q2 - time")
        plt.xlabel('time')
        plt.ylabel('q2')
        plt.plot(simulation.obs.time, simulation.obs.q2list,
                 label=f'E={EList[i]}')
        plt.legend()
        plt.tight_layout()

        plt.subplot(2, 2, 3)
        plt.title("p1 - time")
        plt.xlabel('time')
        plt.ylabel('p1')
        plt.plot(simulation.obs.time, simulation.obs.p1list,
                 label=f'E={EList[i]}')
        plt.legend()
        plt.tight_layout()

        plt.subplot(2, 2, 4)
        plt.title("p2 - time")
        plt.xlabel('time')
        plt.ylabel('p2')
        plt.plot(simulation.obs.time, simulation.obs.p2list,
                 label=f'E={EList[i]}')
        plt.legend()
        plt.tight_layout()

    plt.show()


def assignment5_b():
    EList = [1, 5, 10, 15, 40]

    for E in EList:
        oscillator = Oscillator(
            m=1, L=1, t0=0, E=E, init_cond=[1, 1, 0, -1])
        simulation = Simulation(oscillator)
        simulation.run(integrator=EulerRichardsonIntegrator(
            dt=0.001), show_plot=False, plot_title=f"E={E}")

        plt.subplot(2, 1, 1)
        plt.title("Phase Space Map 1")
        plt.xlabel('q1')
        plt.ylabel('p1')
        plt.plot(simulation.obs.q1list, simulation.obs.p1list,
                 label=f'E={E}')
        plt.legend()
        plt.tight_layout()
        
        plt.subplot(2, 1, 2)
        plt.title("Phase Space Map 2")
        plt.xlabel('q2')
        plt.ylabel('p2')
        plt.plot(simulation.obs.q2list, simulation.obs.p2list,
                 label=f'E={E}')
        plt.legend()
        plt.tight_layout()

    plt.show()


def assignment5_c():
    EList = [1, 5, 10, 15, 25, 40]
    #EList = [40,]
    numInitialConditions = 20

    with alive_bar(len(EList) * numInitialConditions, title="Processing Poincare map") as bar:
        for i in range(len(EList)):
            for j in range(numInitialConditions):
                oscillator = Oscillator(m=1, L=1, t0=0, E=EList[i], init_cond=[1, 1, 0, -1], print_init=False) # Initial conditions are randomized
                simulation = Simulation(oscillator)
                simulation.run(integrator=EulerRichardsonIntegrator(
                    dt=0.001), show_plot=False, tmax=100)
                
                plt.subplot(3, 2, i+1)
                plt.title(f"Poincare Plot - E = {EList[i]}")
                plt.xlabel('q1')
                plt.ylabel('p1')
                plt.plot(simulation.obs.poincare_q1, simulation.obs.poincare_p1, 'o')
                plt.tight_layout()  # adapt the plot area tot the text with larger fonts

                bar()
    plt.show()


def main():
    assignment5_c()
    #oscillator = Oscillator(m=1, L=1, t0=0, E=40, init_cond=[1, 1, 0, -1], print_init=False) # Initial conditions are randomized
    #simulation = Simulation(oscillator)
    #simulation.run_animate(integrator=EulerRichardsonIntegrator(
    #    dt=0.001), tmax=100)
    

# Calling 'main()' if the script is executed.
# If the script is instead just imported, main is not called (this can be useful if you want to
# write another script importing and utilizing the functions and classes defined in this one)
if __name__ == "__main__":
    main()
