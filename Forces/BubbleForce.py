from Forces.PairForce import PairForce
from Objects.Circle import Circle


class BubbleForce(PairForce):
    def __init__(self, particle_list, s=200):
        super().__init__(particle_list)
        self.s = s

    def force(self, a: Circle, b: Circle):
        e = self.s * a.radius * b.radius
        o = a.radius + b.radius
        r = a.pos - b.pos

        orx = (o / r.mag()) ** 2

        return e * (orx - 1) * orx * r.hat()
