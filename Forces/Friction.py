from Forces.SingleForce import SingleForce


class Friction(SingleForce):
    def __init__(self, particle_list, d=1):
        super().__init__(particle_list)
        self.d = d

    def force(self, o):
        return -self.d * o.vel
