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
    points = [5, 7, 8, 8, 4, 2, -.5, -1.5]
    points_x = [-1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9]
    points_y = [0, 0, *[p for p in points for _ in range(2)], 0, 0]

    approx3 = [6, 8, 3, -1]
    detail3 = [-1, 0, 1, .5]
    approx3_x = [-1, 0, 0, 2, 2, 4, 4, 6, 6, 8, 8, 9]
    approx3_y = [0, 0, *[a for a in approx3 for _ in range(2)], 0, 0]
    print(approx3_y)

    approx2 = [7, 1]
    detail2 = [-1, 2]
    approx2_x = [-1, 0, 0, 4, 4, 8, 8, 9]
    approx2_y = [0, 0, *[a for a in approx2 for _ in range(2)], 0, 0]

    approx1 = [4]
    detail1 = [3]
    approx1_x = [-1, 0, 0, 8, 8, 9]
    approx1_y = [0, 0, *[a for a in approx1 for _ in range(2)], 0, 0]

    colors = [BLUE_D, BLUE_C, BLUE_B]

    def setup_axes(self):
        self.axes = Axes(x_range=[self.points_x[0]-.7, self.points_x[-1]+.7, 1], y_range=[min(self.points_y) - 1, max(self.points_y) + 1, 1],
                         x_length=config.frame_width / 2,
                         axis_config={"number_scale_value": .5}).to_edge(LEFT)
        self.axes.add_coordinates()

    def setup_signal(self):
        line = self.axes.get_line_graph(self.points_x, self.points_y, line_color=WHITE)
        self.dots = line["vertex_dots"][2:-2:2]
        self.signal = line["line_graph"]
        self.approx3_graph = self.axes.get_line_graph(self.approx3_x, self.approx3_y, add_vertex_dots=False, line_color=RED).set_z_index(self.signal.z_index+1)
        self.approx2_graph = self.axes.get_line_graph(self.approx2_x, self.approx2_y, add_vertex_dots=False, line_color=RED).set_z_index(self.approx3_graph.z_index+1)
        self.approx1_graph = self.axes.get_line_graph(self.approx1_x, self.approx1_y, add_vertex_dots=False, line_color=RED).set_z_index(self.approx2_graph.z_index+1)

    def setup_text_and_tables(self):
        tab_args = {"h_buff": .4, "v_buff": .4, "include_outer_lines": True}
        scale = .8
        label_color = BLUE
        buffer = .4
        self.tab_signal = Table([list(map(str, self.points))], **tab_args).scale(scale).to_corner(UR)
        self.text_signal = Text("Signal").move_to(self.tab_signal)
        self.tab_signal.next_to(self.text_signal, DOWN)

        self.tab_approx3 = Table([list(map(str, self.approx3))],
                                 **tab_args,
                                 element_to_mobject_config={"color": label_color},
                                 line_config={"color": RED}
                                 ).scale(scale)
        self.tab_detail3 = Table([list(map(str, self.detail3))], **tab_args,
                                 element_to_mobject_config={"color": label_color},
                                 line_config={"color": GREEN}
                                 ).scale(scale)
        self.text3 = Text("First transform").next_to(self.tab_signal, DOWN, buff=buffer)
        self.tab3 = VGroup(self.tab_approx3, self.tab_detail3).arrange(RIGHT, buff=.1).next_to(self.text3, DOWN)

        self.tab_approx2 = Table([list(map(str, self.approx2))],
                                 **tab_args,
                                 element_to_mobject_config={"color": label_color},
                                 line_config={"color": RED}
                                 ).scale(scale)
        self.tab_detail2 = Table([list(map(str, self.detail2))], **tab_args,
                                 element_to_mobject_config={"color": label_color},
                                 line_config={"color": GREEN}
                                 ).scale(scale)
        self.text2 = Text("Second transform").next_to(self.tab3, DOWN, buff=buffer)
        self.tab2 = VGroup(self.tab_approx2, self.tab_detail2, self.tab_detail3.copy()).arrange(RIGHT, buff=.1).next_to(self.text2, DOWN)

        self.tab_approx1 = Table([list(map(str, self.approx1))],
                                 **tab_args,
                                 element_to_mobject_config={"color": label_color},
                                 line_config={"color": RED}
                                 ).scale(scale)
        self.tab_detail1 = Table([list(map(str, self.detail1))], **tab_args,
                                 element_to_mobject_config={"color": label_color},
                                 line_config={"color": GREEN}
                                 ).scale(scale)
        self.text1 = Text("Third transform").next_to(self.tab2, DOWN, buff=buffer)
        self.tab1 = VGroup(self.tab_approx1, self.tab_detail1, self.tab_detail2.copy(), self.tab_detail3.copy()).arrange(RIGHT, buff=.1).next_to(self.text1, DOWN)

    def setup(self):
        self.setup_axes()
        self.setup_signal()
        self.setup_text_and_tables()

    def create_axis_signal(self):
        self.play(Create(self.axes))
        self.wait()
        self.play(Write(self.text_signal))
        self.play(Create(self.dots), Write(self.tab_signal), run_time=4)
        self.wait()
        self.play(Create(self.signal), run_time=4)
        self.wait()
        self.play(FadeOut(self.dots))
        self.wait()
        corners = self.signal.get_anchors()[4::2]
        print(corners)
        print(len(corners))
        for i in range(int(len(corners)/2-1)):
            self.play(Circumscribe(self.tab_signal.get_entries((1, i+1))),
                      Circumscribe(Line(corners[2*i], corners[2*i+1])))

    def transforms(self):
        # first transform
        self.play(Write(self.text3), Write(self.tab_approx3), run_time=1.5)
        self.play(Create(self.approx3_graph), run_time=4)
        self.wait()
        self.play(Write(self.tab_detail3))
        self.wait()
        self.play(self.signal.animate.set_stroke(opacity=.4),
                  self.approx3_graph.animate.set_stroke(color=WHITE))
        self.wait()
        # second transform
        self.play(Write(self.text2), Write(self.tab2), run_time=1.5)
        self.play(Create(self.approx2_graph), run_time=4)
        self.wait()
        self.play(self.signal.animate.set_stroke(opacity=.2),
                  self.approx3_graph.animate.set_stroke(opacity=.4),
                  self.approx2_graph.animate.set_stroke(color=WHITE))
        self.wait()
        # third transform
        self.play(Write(self.text1), Write(self.tab1), run_time=1.5)
        self.play(Create(self.approx1_graph), run_time=4)
        self.play(self.signal.animate.set_stroke(opacity=.1),
                  self.approx3_graph.animate.set_stroke(opacity=.2),
                  self.approx2_graph.animate.set_stroke(opacity=.4),
                  self.approx1_graph.animate.set_stroke(color=WHITE))


    def construct(self):
        self.create_axis_signal()
        self.wait()
        self.transforms()
        self.wait(10)
