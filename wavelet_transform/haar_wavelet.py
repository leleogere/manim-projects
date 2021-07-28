from manim import *


def animation_speed(i, n, maxim=2, minim=.1, speed=1):
    """Compute the speed of an animation in
    a loop going faster and faster.
    i: indice of the loop
    n: number of loops
    maxim: duration when i=0
    minim: minimum duration of an animation"""
    return max(minim, maxim - speed * i / n)


class Haar(Scene):
    N = 8
    seed = 2
    offset = -2
    points_x = [-1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9]
    points_y = [0, 0, 5, 5, 7, 7, 8, 8, 8, 8, 4, 4, 2, 2, -.5, -.5, -1.5, -1.5]

    approx3_x = [-1, 0, 0, 2, 2, 4, 4, 6, 6, 8, 8, 9]
    approx3_y = [0, 0, 6, 6, 8, 8, 3, 3, -1, -1, 0, 0]

    approx2_x = [-1, 0, 0, 4, 4, 8, 8, 9]
    approx2_y = [0, 0, 7, 7, 1, 1, 0, 0]

    approx1_x = [-1, 0, 0, 8, 8, 9]
    approx1_y = [0, 0, 4, 4, 0, 0]

    def setup_axes(self):
        self.axes = Axes(x_range=[self.points_x[0], self.points_x[-1], 1], y_range=[min(self.points_y) - 1, max(self.points_y) + 1, 1],
                         x_length=config.frame_width / 2,
                         axis_config={"number_scale_value": .5})
        self.axes.add_coordinates()

    def setup_signal(self):
        self.signal = self.axes.get_line_graph(self.points_x, self.points_y, add_vertex_dots=False, line_color=WHITE)
        self.approx3 = self.axes.get_line_graph(self.approx3_x, self.approx3_y, add_vertex_dots=False, line_color=YELLOW)
        self.approx2 = self.axes.get_line_graph(self.approx2_x, self.approx2_y, add_vertex_dots=False, line_color=GREEN)
        self.approx1 = self.axes.get_line_graph(self.approx1_x, self.approx1_y, add_vertex_dots=False, line_color=RED)

    def setup(self):
        self.setup_axes()
        self.setup_signal()

    def construct(self):
        self.play(Create(self.axes))
        self.wait()
        self.play(Create(self.signal))
        self.wait()
        self.play(Create(self.approx3))
        self.wait()
        self.play(Create(self.approx2))
        self.wait()
        self.play(Create(self.approx1))
        self.wait(10)
