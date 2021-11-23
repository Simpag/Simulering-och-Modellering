class Car:
    def __init__(self, startPos = 0, startVel = 0) -> None:
        self._positions = [startPos, ]
        self._velocities = [startVel, ]

    def step(self, roadLength):
        newPos = (self.getPosition() + self.getVelocity()) % roadLength
        self._positions.append(newPos)

    def setVelocity(self, vel):
        if vel < 0: # Only allow positive velocitites
            vel = 0

        self._velocities.append(vel)

    def getVelocity(self):
        return self._velocities[-1]

    def getPosition(self):
        return self._positions[-1]