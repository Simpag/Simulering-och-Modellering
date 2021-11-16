class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)


class Points:
    def __init__(self, point=Point(0, 0)):
        self.pointList = [point, ]

    def add(self, point: Point):
        self.pointList.append(point)

    def step(self, x_step=0, y_step=0):
        p = self.pointList[-1].copy()   # Copy the last point
        p.x += x_step                   # Take a step
        p.y += y_step
        self.add(p)                     # Save the step

    def get_as_lists(self):
        x, y = [], []
        for p in self.pointList:
            x.append(p.x)
            y.append(p.y)

        return x, y

    def __getitem__(self, key):
        return self.pointList[key]