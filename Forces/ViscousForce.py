from Forces.SingleForce import SingleForce
from Objects.Circle import Circle


class ViscousForce(SingleForce):
    def __init__(self, particle_list, cd=100):
        super().__init__(particle_list)
        self.cd = cd

    def force(self, o: Circle):
        return -self.cd * o.radius * o.vel
