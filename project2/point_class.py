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

    def step(self, x_step=0, y_step=0, self_avoid=False):
        p = self.pointList[-1].copy()   # Copy the last point
        p.x += x_step                   # Take a step
        p.y += y_step

        if self_avoid:
            if p not in self:
                self.add(p)             # Save the step
                return True
            
            return False
        else:
            self.add(p)                 # Save the step
            return True

    def get_as_lists(self):
        x, y = [], []
        for p in self.pointList:
            x.append(p.x)
            y.append(p.y)

        return x, y

    def __getitem__(self, key):
        return self.pointList[key]

    def __contains__(self, key:  Point):
        # This is bad and linear but idc
        for p in self.pointList:
            if key.x == p.x and key.y == p.y:
                return True

        return False

def utest():
    points = Points()
    assert points.step(x_step=1, self_avoid=True) == True
    assert points.step(y_step=1, self_avoid=True) == True
    assert points.step(x_step=-1, self_avoid=True) == True
    assert points.step(y_step=-1, self_avoid=True) == False

    print("Passed")

if __name__ == "__main__":
    utest()