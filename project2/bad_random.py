class BadRandom:
    def __init__(self, a, c, m, r0=1):
        self.prev_r = r0
        self.a = a
        self.c = c
        self.m = m

    def random(self):
        r = (self.a * self.prev_r + self.c) % self.m
        self.prev_r = r
        return r//((self.m+3)//4)
