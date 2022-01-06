from manim import *


class Cycle(VMobject):
    def __init__(self, radius, angle=0, **kwargs):
        VMobject.__init__(self, **kwargs)
        circle = Circle(radius=radius, stroke_width=.8)
        arrow = Arrow(ORIGIN, radius * RIGHT, buff=0)
        self.add(circle, arrow)
        self.rotate(angle)
        self.circle = circle
        self.arrow = arrow


class Epicycles(Scene):
    radiuses = np.array([0.3, 0.5, 1.2, 0.3])
    angles = np.array([0, PI / 3, 3 * PI / 4, PI / 2])
    speeds = 6 * np.array([1.52, -.5, 0.1, -.6])
    origin = np.array([0, 0, 0])

    def construct(self):
        origin_object = Cycle(radius=0).move_to(self.origin)
        epicycles = VGroup(origin_object)
        for (i, (r, a, s)) in enumerate(zip(self.radiuses, self.angles, self.speeds)):
            cycle = Cycle(r, a)
            cycle.add_updater(lambda c, dt, i=i, s=s: c.rotate(s * dt).move_to(epicycles[i].arrow.get_end()))
            epicycles.add(cycle)
        path = TracedPath(epicycles[-1].arrow.get_end)
        self.add(epicycles, path)
        self.wait(15)


object = Star().scale(3).shift(UL)
N = 51
points = np.array([R3_to_complex(p) for p in [object.point_from_proportion(i / N) for i in range(N + 1)]])
fft = np.fft.fft(points)/N
speed_factor = 0.2

class FourierSquare(Scene):
    speeds = np.array([(-1)**i * int(i/2) for i in range(1, N + 1)])
    radiuses = np.abs(fft)[speeds]
    angles = np.angle(fft)[speeds]
    origin = np.array([0, 0, 0])

    def construct(self):
        origin_object = Cycle(radius=0).move_to(self.origin)
        epicycles = VGroup(origin_object)
        for (i, (r, a, s)) in enumerate(zip(self.radiuses, self.angles, self.speeds)):
            cycle = Cycle(r, a)
            cycle.add_updater(lambda c, dt, i=i, s=s: c.rotate(speed_factor * s * dt).move_to(epicycles[i].arrow.get_end()))
            epicycles.add(cycle)
        path = TracedPath(epicycles[-1].arrow.get_end)
        self.add(object.set_opacity(.2))
        # self.add(*[Dot(complex_to_R3(p), color=RED) for p in points])
        self.add(epicycles, path)
        self.wait(30)