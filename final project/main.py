import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

plt.rcParams.update({'font.size': 22})

from object_classes import Rocket, Earth

"""
Gravity
Drag

Thrust

Momentum

https://www.narom.no/undervisningsressurser/sarepta/rocket-theory/rocket-dynamics-2/4-1aerodynamics-and-forces-acting-on-the-rocket/

https://spaceflight101.com/ariane-5-va226/ariane-5-va226-launch-profile/

alpha = 0 (angle of attack)
delta = 0 (angle of thrust)
gamma = down (angle of gravitational pull)


Equations?

Crude
M dv/dt = T - Mg0 r0/r - D

dR/dt = V
dV/dt = 1/M (Tv - Mg0 r0/r k - Dv) # v = unit velocity vector, k = unit vector from earth to rocket
a = D V / D t # D = delta
D = q cD A #  A is the frontal area of the rocket, q is the dynamic pressure and cD is the drag coefficient

V0 = [0,0]
R0 = [0,0]
"""

timestep = 0.1
duration = 1500
steps = duration/timestep

rocket = Rocket()
earth = Earth()

for i in range(steps):
    # D = q*cd*rocket.area
    accel = 1/rocket.getTotalMass() * (rocket.thrustStage1-rocket.getTotalMass()*earth.g0*(earth.radius/(rocket.positions[-1]+earth.radius))**2)
    rocket.usefuel(timestep)
    rocket.accelerations.append(accel)
    rocket.velocities.append(rocket.velocities[-1] + accel*timestep)
    rocket.positions.append(rocket.positions[-1] + rocket.velocities*timestep)

plt.figure()
plt.suptitle("Position")
plt.xlabel("Time")
plt.ylabel("Position from the earth")
plt.grid()
plt.plot(range(steps), rocket.positions)
