from manim import *


def animation_speed(i, n, maxim=2, minim=.1, speed=1):
    """Compute the speed of an animation in
    a loop going faster and faster.
    i: indice of the loop
    n: number of loops
    maxim: duration when i=0
    minim: minimum duration of an animation"""
    return max(minim, maxim - speed * i / n)


class MyIndicate(Indicate):
    def create_target(self) -> "Mobject":
        target = self.mobject.copy()
        target.scale_in_place(self.scale_factor)
        target.set_color(self.color)
        target.set_stroke(width=3 * self.scale_factor * self.mobject.get_style()["stroke_width"])
        return target


class HaarScene(Scene):
    # VARIABLES
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

    approx2 = [7, 1]
    detail2 = [-1, 2]
    approx2_x = [-1, 0, 0, 4, 4, 8, 8, 9]
    approx2_y = [0, 0, *[a for a in approx2 for _ in range(2)], 0, 0]

    approx1 = [4]
    detail1 = [3]
    approx1_x = [-1, 0, 0, 8, 8, 9]
    approx1_y = [0, 0, *[a for a in approx1 for _ in range(2)], 0, 0]

    colors = [BLUE_D, BLUE_C, BLUE_B]

    # SETUP
    def setup_axes(self):
        self.axes = Axes(x_range=[self.points_x[0] - .7, self.points_x[-1] + .7, 1],
                         y_range=[min(self.points_y) - 1, max(self.points_y) + 1, 1],
                         x_length=config.frame_width / 2,
                         axis_config={"number_scale_value": .5}).to_edge(LEFT)
        self.axes.add_coordinates()

    def setup_signal(self):
        line = self.axes.get_line_graph(self.points_x, self.points_y, line_color=WHITE)
        self.dots = line["vertex_dots"][2:-2:2]
        self.signal = line["line_graph"]
        self.approx3_graph = \
            self.axes.get_line_graph(self.approx3_x, self.approx3_y, add_vertex_dots=False, line_color=RED)[
                "line_graph"].set_z_index(self.signal.z_index + 1)
        self.approx2_graph = \
            self.axes.get_line_graph(self.approx2_x, self.approx2_y, add_vertex_dots=False, line_color=RED)[
                "line_graph"].set_z_index(self.approx3_graph.z_index + 1)
        self.approx1_graph = \
            self.axes.get_line_graph(self.approx1_x, self.approx1_y, add_vertex_dots=False, line_color=RED)[
                "line_graph"].set_z_index(self.approx2_graph.z_index + 1)

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
        self.tab2 = VGroup(self.tab_approx2, self.tab_detail2, self.tab_detail3.copy()).arrange(RIGHT, buff=.1).next_to(
            self.text2, DOWN)

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
        self.tab1 = VGroup(self.tab_approx1, self.tab_detail1, self.tab_detail2.copy(),
                           self.tab_detail3.copy()).arrange(RIGHT, buff=.1).next_to(self.text1, DOWN)

    def setup(self):
        self.setup_axes()
        self.setup_signal()
        self.setup_text_and_tables()


class HaarDecomposition(HaarScene):
    # HELPERS
    def focus_on_approx_coeffs(self, curve, table):
        corners = curve.get_anchors()[4::2]
        for i in range(int(len(corners) / 2)):
            line = Line(corners[2 * i], corners[2 * i + 1], z_index=curve.z_index + 1).match_style(curve)
            self.add(line)
            self.play(Indicate(table.get_entries((1, i + 1))),
                      MyIndicate(line),
                      run_time=2)
            self.remove(line)

    def focus_on_detail_coeffs(self, curve, prev_curve, table: Table):
        corners = curve.get_anchors()[4::2]
        prev_corners = prev_curve.get_anchors()[4::2]
        for i in range(len(table.get_entries())):
            line = Line(corners[2 * i], corners[2 * i + 1])
            prev_line = Line(prev_corners[4 * i], prev_corners[4 * i + 1])
            arrow = Arrow(line.point_from_proportion(.25), prev_line.get_center(),
                          buff=0, max_stroke_width_to_length_ratio=20, max_tip_length_to_length_ratio=.35,
                          stroke_width=4, color=GREEN, z_index=curve.z_index + 1)
            dot = Dot(line.point_from_proportion(.25), radius=0.05, color=GREEN, z_index=curve.z_index + 1)
            self.play(Indicate(table.get_entries((1, i + 1))),
                      FadeIn(VGroup(dot, arrow), rate_func=there_and_back_with_pause),
                      run_time=2)
            self.remove(dot, arrow)

    # ANIMATIONS
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
        # focus on each coefficient in the approximation space
        self.focus_on_approx_coeffs(self.signal, self.tab_signal)

    def transforms(self):
        # first transform
        self.play(Write(self.text3), Write(self.tab_approx3), run_time=1.5)
        self.play(Create(self.approx3_graph), run_time=4)
        self.wait()
        self.focus_on_approx_coeffs(self.approx3_graph, self.tab_approx3)
        self.wait()
        self.play(Write(self.tab_detail3))
        self.wait()
        self.focus_on_detail_coeffs(self.approx3_graph, self.signal, self.tab_detail3)
        self.wait()
        self.play(self.signal.animate.set_stroke(opacity=.4),
                  self.approx3_graph.animate.set_stroke(color=WHITE))
        self.wait()
        # second transform
        self.play(Write(self.text2), Write(self.tab2), run_time=1.5)
        self.play(Create(self.approx2_graph), run_time=4)
        self.wait()
        self.focus_on_approx_coeffs(self.approx2_graph, self.tab_approx2)
        self.wait()
        self.focus_on_detail_coeffs(self.approx2_graph, self.approx3_graph, self.tab_detail2)
        self.wait()
        self.play(self.signal.animate.set_stroke(opacity=.2),
                  self.approx3_graph.animate.set_stroke(opacity=.4),
                  self.approx2_graph.animate.set_stroke(color=WHITE))
        self.wait()
        # third transform
        self.play(Write(self.text1), Write(self.tab1), run_time=1.5)
        self.play(Create(self.approx1_graph), run_time=4)
        self.wait()
        self.focus_on_approx_coeffs(self.approx1_graph, self.tab_approx1)
        self.wait()
        self.focus_on_detail_coeffs(self.approx1_graph, self.approx2_graph, self.tab_detail1)
        self.wait()
        self.play(self.signal.animate.set_stroke(opacity=.1),
                  self.approx3_graph.animate.set_stroke(opacity=.2),
                  self.approx2_graph.animate.set_stroke(opacity=.4),
                  self.approx1_graph.animate.set_stroke(color=WHITE))

    def construct(self):
        self.create_axis_signal()
        self.wait()
        self.transforms()
        self.wait(10)


class HaarRecomposition(HaarDecomposition):

    def setup_secondary_axes(self):
        self.scale_axes = Axes(x_range=[-1, self.N+3, 1], x_length=3.2,
                               y_range=[-1.2, 1.6, .2], y_length=2.5).to_corner(DL, buff=MED_SMALL_BUFF)
        self.wavelet_axes = self.scale_axes.copy().next_to(self.scale_axes, RIGHT, buff=MED_LARGE_BUFF)
        self.scale_func_x = [-1, 0, 0, self.N, self.N, self.N+1]
        self.scale_func_y = [0, 0, 1, 1, 0, 0]
        self.scale_function = self.scale_axes.get_line_graph(self.scale_func_x, self.scale_func_y, add_vertex_dots=False, line_color=RED)["line_graph"].set_z_index(self.scale_axes.z_index + 1)
        self.wavelet_func_x = [-1, 0, 0, self.N/2, self.N/2, self.N, self.N, self.N + 1]
        self.wavelet_func_y = [0, 0, 1, 1, -1, -1, 0, 0]
        self.wavelet_function = self.wavelet_axes.get_line_graph(self.wavelet_func_x, self.wavelet_func_y, add_vertex_dots=False, line_color=GREEN)["line_graph"].set_z_index(self.wavelet_axes.z_index + 1)
        self.scale_legend = Text("Scaling function", color=RED).scale(.5).next_to(self.scale_axes, UP)
        self.wavelet_legend = Text("Wavelet function", color=GREEN).scale(.5).next_to(self.wavelet_axes, UP)

    def setup(self):
        super().setup()
        self.setup_secondary_axes()

    def prepare_scene(self):
        self.add(self.axes,
                 self.text_signal, self.tab_signal,
                 self.text3, self.tab3,
                 self.text2, self.tab2,
                 self.text1, self.tab1)
        self.play(self.axes.animate.become(
            Axes(x_range=[self.points_x[0], self.points_x[-1], 1],
                 y_range=[min(self.points_y) - 1, max(self.points_y) + 1, 1],
                 x_length=config.frame_width / 2,
                 y_length=config.frame_height / 2,
                 axis_config={"number_scale_value": .5}).to_corner(UL, buff=MED_SMALL_BUFF).add_coordinates()
        ))
        self.play(Create(self.scale_axes), Create(self.wavelet_axes))
        self.wait()
        self.play(Create(self.scale_function), Write(self.scale_legend), run_time=2)
        self.wait()
        self.play(Create(self.wavelet_function), Write(self.wavelet_legend), run_time=2)
        self.wait()
        self.play(VGroup(self.text_signal, self.tab_signal, self.text3, self.tab3, self.text2, self.tab2).animate.set_opacity(.1))

    def reconstruction(self):
        focus = SurroundingRectangle(self.tab1[0].get_entries([1, 1]))
        self.play(Create(focus))
        self.wait()
        y = self.axes.get_y_axis().get_unit_size()

        # def make_a_step(original_curve, entry)

        curr_func = self.scale_function.copy()
        curr_func.target = self.axes.get_line_graph(self.scale_func_x, self.scale_func_y, add_vertex_dots=False, line_color=RED)["line_graph"]
        self.play(MoveToTarget(curr_func))
        curr_num = self.tab1[0].get_entries([1, 1]).copy()
        curr_num.target = MathTex(curr_num.lines_text.text + r"\times", color=RED).next_to(curr_func, UP)
        self.play(MoveToTarget(curr_num))
        self.wait()
        self.play(curr_func.animate.stretch_to_fit_height(self.approx3[0]*y, about_point=curr_func.get_start()))
        self.wait()
        reconstitution = curr_func.copy().set_color(WHITE)
        self.play(FadeOut(curr_num),
                  FadeOut(curr_func),
                  FadeIn(reconstitution))
        self.wait()


        curr_func = self.wavelet_function.copy()
        print(self.axes.x_range)
        curr_func.target = (
            self.axes
                .get_line_graph(self.wavelet_func_x, self.wavelet_func_y, add_vertex_dots=False, line_color=GREEN)["line_graph"]
                # .stretch(.5, 0, about_point=curr_func.get_start())
                .shift((self.axes.c2p(0, self.approx1[0])[1] - self.axes.c2p(0, 0)[1])*UP)
        )
        self.play(MoveToTarget(curr_func))
        # curr_num = self.tab1[0].get_entries([1, 1]).copy()
        # curr_num.target = MathTex(curr_num.lines_text.text + r"\times", color=RED).next_to(curr_func, UP)
        # self.play(MoveToTarget(curr_num))
        # self.wait()
        # self.play(curr_func.animate.stretch(self.approx3[0], 1, about_point=self.axes.c2p(0, 0)))
        # self.wait()

    def construct(self):
        self.prepare_scene()
        self.wait()
        self.reconstruction()
        self.wait(5)
