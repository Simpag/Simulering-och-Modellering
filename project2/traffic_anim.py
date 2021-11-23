# Example for simple animation of cars on a circular road

import math
import matplotlib.pyplot as plt
from matplotlib import animation

import matplotlib

roadLength    = 50
numCars       = 10
numFrames     = 200

positions     = []
theta         = []
r             = []
color         = []

for i in range(numCars):
    positions.append(i * 2)
    theta.append(0)
    r.append(1)
    color.append(i)

fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
ax.axis('off')

def animate(frameNr):
    for i in range(numCars):
        positions[i] += 1
        # Convert to radians for plotting  only (do not use radians for the simulation!)
        theta[i] = positions[i] * 2 * math.pi / roadLength
    
    return ax.scatter(theta, r, c=color),

# Call the animator, blit=True means only re-draw parts that have changed
anim = animation.FuncAnimation(fig, animate,
                               frames=numFrames, interval=50, blit=True, repeat=False)

plt.show()
