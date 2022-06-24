from vpython import sphere, vec, cross, sin, color, attach_arrow, scene, rate


class MySphere(sphere):

    def __init__(self, vel: vec = vec(0, 0, 0), pos: vec = vec(0, 0, 0), mass: float = 1, force: vec = vec(0, 0, 0),
                 **kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        self.mass = mass
        self.force = force
        self.vel = vel


# force function
def apply_force(shape: MySphere, t: float) -> vec:
    return sin(t) * cross(shape.vel, vec(3, 1, 5))


def main() -> None:
    # Initial conditions
    shape = MySphere(make_trail=True, mass=1, pos=vec(0, 0, 0), vel=vec(1, 1, 1), force=vec(0, 0, 0), opacity=0.75)

    # Scene Setup
    scene.width = 900
    scene.height = 550
    attach_arrow(shape, "vel", color=color.green, shaftwidth=0.5, scale=.1)
    attach_arrow(shape, "force", color=color.blue, shaftwidth=0.5, scale=.1)
    scene.pause()

    t: float = 0
    dt: float = 0.01

    # Simulation loop goes here
    while True:
        rate(100)
        t += dt
        shape.force = apply_force(shape, t)
        shape.vel += (shape.force / shape.mass) * dt
        shape.pos += shape.vel * dt


if __name__ == "__main__":
    main()
