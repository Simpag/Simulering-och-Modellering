import numpy as np


class Rocket:
    # Ariane 5 case study
    # Combine mainstage and boosters
    #
    # Stage 1 = Boosters
    # Stage 2 = Core stage
    # Stage 3 = Second stage
    #
    # Stage 1 thrust = 2 * 7.080 kN
    # Stage 2 thrust = 1.390 kN
    # Stage 3 thrust = 67 kN
    #
    # https://en.wikipedia.org/wiki/Ariane_5#Cryogenic_main_stage
    def __init__(self, centerOfMass = 20, area=22.9, massStage1=33*10**3, massStage2=14.7*10**3, massStage3=4.54*10**3, payload=0.5*10**3,
                 fuelMassStage1=480*10**3, fuelMassStage2=170*10**3, fuelMassStage3=14.9*10**3, burntimeStage1=140,
                 burntimeStage2=540, burntimeStage3=945, thrustStage1=2*7080*10**3, thrustStage2=1390*10**3, thrustStage3=67*10**3) -> None:
        self.area = area
        self.massStage1 = massStage1
        self.massStage2 = massStage2
        self.massStage3 = massStage3
        self.payload = payload
        self.fuelMassStage1 = fuelMassStage1
        self.fuelMassStage2 = fuelMassStage2
        self.fuelMassStage3 = fuelMassStage3
        self.burntimeStage1 = burntimeStage1
        self.burntimeStage2 = burntimeStage2
        self.burntimeStage3 = burntimeStage3
        self.thrustStage1 = thrustStage1
        self.thrustStage2 = thrustStage2
        self.thrustStage3 = thrustStage3

        self.startingFuelMassStage1 = fuelMassStage1
        self.startingFuelMassStage2 = fuelMassStage2
        self.startingFuelMassStage3 = fuelMassStage3
        
        self.positions = [centerOfMass, ]
        self.velocities = [0, ]
        self.accelerations = [0, ]

        self.stage3Cooldown = 4 # 4 seconds before stage 3 initiates after stage 2 finishes

    def getTotalMass(self):
        return self.massStage1 + self.massStage2 + self.massStage3 + self.payload + self.fuelMassStage1 + self.fuelMassStage2 + self.fuelMassStage3

    def getThrust(self):
        if self.fuelMassStage1 > 0:
            print("Stage one")
            return self.thrustStage1 + self.thrustStage2
        elif self.fuelMassStage2 > 0:
            print("Stage 2")
            return self.thrustStage2
        elif self.fuelMassStage3 > 0 and self.stage3Cooldown <= 0:
            print("Stage 3")
            return self.thrustStage3
        else:
            return 0

    def usefuel(self, duration):
        # Assume linear fuel consumption
        if self.fuelMassStage1 > 0:
            self.fuelMassStage1 -= duration/self.burntimeStage1 * self.startingFuelMassStage1
            self.fuelMassStage2 -= duration/self.burntimeStage2 * self.startingFuelMassStage2
        elif self.fuelMassStage2 > 0:
            self.fuelMassStage2 -= duration/self.burntimeStage2 * self.startingFuelMassStage2
            self.massStage1 = 0
        elif self.fuelMassStage3 > 0 and self.stage3Cooldown > 0:
            self.stage3Cooldown -= duration
        elif self.fuelMassStage3 > 0 and self.stage3Cooldown <= 0:
            self.fuelMassStage3 -= duration/self.burntimeStage3 * self.startingFuelMassStage3
            self.massStage2 = 0
        else:
            print("Ran out of fuel!")

    def getPosition(self):
        return self.positions[-1]

    def getVelocity(self):
        return self.velocities[-1]

    def getAcceleration(self):
        return self.accelerations[-1]


class Earth:
    def __init__(self) -> None:
        self.mass = 5.972 * 10**24  # kg
        self.radius = 6371 * 10**3  # m
        self.g0 = 9.82
