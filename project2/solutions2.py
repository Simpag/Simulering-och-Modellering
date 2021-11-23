from car import Car
import random as rn
import math
import matplotlib.pyplot as plt
from matplotlib import animation
from alive_progress import alive_bar # pip3 install alive_progress

class sim:
    def __init__(self, nCars, roadLength, vmax, p, steps):
        # randomize the starting pos
        startingPos = sorted([int(rn.random() * roadLength) for i in range(nCars)])
        self.cars = [Car(startPos = startingPos[i]) for i in range(nCars)]

        self.roadLength = roadLength
        self.vmax = vmax
        self.p = p
        self.steps = steps

    def loop(self):
        cnt = self.steps
        while cnt > 0:
            cnt -= 1
            for i in range(len(self.cars)):
                if self.cars[i].getVelocity() < self.vmax:
                    self.cars[i].setVelocity(self.cars[i].getVelocity() + 1)

                nextCar = (i + 1) % len(self.cars)  # Periodic boundary condition
                d = self.cars[nextCar].getPosition() - self.cars[i].getPosition()
                if d < 0:
                    d = 100 + d

                if self.cars[i].getVelocity() > d: # Prevent crashes
                    self.cars[i].setVelocity(d - 1)

                if rn.random() < self.p:
                    self.cars[i].setVelocity(self.cars[i].getVelocity() - 1)

                # Update position
                self.cars[i].step(self.roadLength)

    def getFlowRate(self):
        carv = 0
        for car in self.cars:
            carv += car.getVelocity()

        return carv / self.roadLength

def plot1(s: sim):
    carY = []
    carX = []
    indicies = list(range(0,s.steps, 10))

    for t in indicies:
        for car in s.cars:
            carX.append(car._positions[t])
            carY.append(t)


    plt.title("Phase space potrait")
    plt.plot(carX, carY, 'o')
    plt.xlabel(r'$\theta$')
    plt.ylabel(r'$\dot \theta$')
    plt.grid()
    plt.show()

def caranim(s: sim):
    positions     = [0, ] * len(s.cars)
    theta         = [0, ] * len(s.cars)
    r             = [0, ] * len(s.cars)
    color         = [0, ] * len(s.cars)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    ax.axis('off')

    def animate(frameNr):
        for i in range(len(s.cars)):
            positions[i] = s.cars[i]._positions[frameNr]
            # Convert to radians for plotting  only (do not use radians for the simulation!)
            theta[i] = positions[i] * 2 * math.pi / s.roadLength
        
        return ax.scatter(theta, r, c=color),

    # Call the animator, blit=True means only re-draw parts that have changed
    anim = animation.FuncAnimation(fig, animate,
                                frames=s.steps, interval=50, blit=True, repeat=False)

    plt.show()

def flowratePlot():
    ncars = list(range(0,800, 10))
    iterations = 25
    roadLength=1000

    flowRates = []
    densities = []
    with alive_bar(len(ncars), title="Processing fundamental diagram") as bar:
        for n in ncars:
            _flowRates = [0, ] * iterations
            for i in range(iterations):
                s = sim(nCars=n, roadLength=roadLength, vmax=2, p=0.5, steps=1000)
                s.loop()
                _flowRates[i] = s.getFlowRate()

            flowRates.append(sum(_flowRates) / iterations)
            densities.append(n/roadLength)
            bar()

    plt.title("Fundamental Diagram")
    plt.plot(densities, flowRates)
    plt.xlabel(r'Density')
    plt.ylabel(r'Flow rate')
    plt.grid()
    plt.show()


def main():
    s = sim(nCars=10, roadLength=100, vmax=2, p=0.5, steps=1000)

    s.loop()
    caranim(s)

if __name__ == '__main__':
    flowratePlot()