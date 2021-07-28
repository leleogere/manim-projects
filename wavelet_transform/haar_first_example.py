from manim import *


def animation_speed(i, n, maxim=2, minim=.1, speed=1):
    """Compute the speed of an animation in
    a loop going faster
    n: number of loops
    maxim: duration when i=0
    minim: minimum duration of an animation"""
    return max(minim, maxim - speed * i / n)


class HaarIntroduction(Scene):
    N = 16
    seed = 2
    offset = -2

    def setup_points(self):
        y = [10]
        np.random.seed(self.seed)
        for i in range(self.N - 1):
            y.append(y[-1] + np.random.randint(-2, 3))
        points = np.array([[i + 1, yi + self.offset, 0] for i, yi in enumerate(y)])
        mean_points = np.array([(points[i] + points[i + 1]) / 2 for i in range(0, self.N, 2)])
        diff_points = np.array([(points[i] - points[i + 1]) / 2 for i in range(0, self.N, 2)])
        approx_points = np.array([[i + 1, mean_points[i][1], 0] for i in range(int(self.N / 2))])
        detail_points = np.array([[i + 1, diff_points[i][1], 0] for i in range(int(self.N / 2))])
        self.points = points
        self.mean_points = mean_points
        self.diff_points = diff_points
        self.approx_points = approx_points
        self.detail_points = detail_points

    def setup_axes(self):
        self.axes = Axes(x_range=[0, self.N + 1, 1], y_range=[0, max(self.points[:, 1]) + 1, 1],
                         x_length=config.frame_width / 2.4,
                         axis_config={"number_scale_value": .5})
        self.axes.add_coordinates()
        self.axes.to_edge(LEFT, buff=MED_SMALL_BUFF)
        self.approx_axes = Axes(x_range=[0, self.N / 2 + 1, 1], y_range=[0, max(self.points[:, 1]) + 1, 1],
                                x_length=config.frame_width / 2.4, y_length=config.frame_height / 2.5,
                                axis_config={"number_scale_value": .5})
        self.approx_axes.add_coordinates()
        self.detail_axes = Axes(x_range=[0, self.N / 2 + 1, 1],
                                y_range=[min(self.detail_points[:, 1]) - .5, max(self.detail_points[:, 1]) + .5, .5],
                                x_length=config.frame_width / 2.4, y_length=config.frame_height / 2.5,
                                axis_config={"number_scale_value": .5})
        self.detail_axes.add_coordinates()
        VGroup(self.approx_axes, self.detail_axes).arrange(DOWN, buff=MED_LARGE_BUFF).to_edge(RIGHT,
                                                                                              buff=MED_SMALL_BUFF)
        self.vline = Line(5 * UP, 5 * DOWN)
        self.hline = Line(.1 * DOWN, 8 * RIGHT + .1 * DOWN)

    def setup_dots(self):
        self.dots = VMobject()
        self.dots_left = VMobject()
        for p in self.points:
            self.dots.add(Dot(self.axes.c2p(*p)))
            self.dots_left.add(Dot(self.approx_axes.c2p(*p), fill_opacity=.3))
        self.mean_dots = VMobject()
        self.approx_dots = VMobject()
        self.detail_dots = VMobject()
        for m, a, d in zip(self.mean_points, self.approx_points, self.detail_points):
            self.mean_dots.add(Dot(self.axes.c2p(*m), color=RED))
            self.approx_dots.add(Dot(self.approx_axes.c2p(*a), color=RED))
            self.detail_dots.add(Dot(self.detail_axes.c2p(*d), color=GREEN))

    def setup(self):
        self.setup_points()
        self.setup_axes()
        self.setup_dots()

    def create_main_plot(self):
        self.play(Create(self.axes))
        self.wait()
        self.play(ShowIncreasingSubsets(self.dots))
        self.wait(2)

    def create_approx_space(self):
        current_dots = self.dots[0:2].copy().set_color(RED)
        self.play(FadeIn(current_dots), run_time=2)
        self.dots[0:2].set_opacity(.3)
        self.play(ReplacementTransform(current_dots, self.mean_dots[0]), run_time=2)
        connector_main = DashedLine(self.axes.c2p(0, self.mean_points[0][1]), self.mean_dots[0].get_center(), color=RED)
        self.play(Create(connector_main))
        self.wait()
        self.play(Create(self.vline), Create(self.approx_axes))
        self.wait()
        connector_approx = DashedLine(self.approx_axes.c2p(0, self.mean_points[0][1]), self.approx_dots[0].get_center(),
                                      color=RED)
        self.play(Create(connector_approx))
        self.play(FadeIn(self.approx_dots[0]))
        self.wait()
        self.play(FadeOut(connector_main, connector_approx, self.mean_dots[0]))

        for i in range(1, int(self.N / 2)):
            anim_speed = 2 * (1 - i / (self.N - 1))
            current_dots = self.dots[2 * i:2 * i + 2].copy().set_color(RED)
            self.play(FadeIn(current_dots), run_time=anim_speed / 2)
            self.dots[2 * i:2 * i + 2].set_opacity(.3)
            self.wait(anim_speed / 3)
            self.play(ReplacementTransform(current_dots, self.mean_dots[i]), run_time=anim_speed / 1.5)
            self.wait(anim_speed / 3)
            connector_main = DashedLine(self.axes.c2p(0, self.mean_points[i][1]), self.mean_dots[i].get_center(),
                                        color=RED)
            self.play(Create(connector_main))
            connector_approx = DashedLine(self.approx_axes.c2p(0, self.mean_points[i][1]),
                                          self.approx_dots[i].get_center(), color=RED)
            self.play(Create(connector_approx), run_time=anim_speed)
            self.play(FadeIn(self.approx_dots[i]), run_time=anim_speed / 2)
            self.wait(anim_speed / 3)
            self.play(FadeOut(connector_main, connector_approx, self.mean_dots[i]), run_time=anim_speed)
            self.wait(anim_speed / 3)
        self.play(self.dots.animate.set_opacity(1))

    def inverse_transform_text(self):
        text = Text("Inverse transform impossible:\nInformation has been lost in the process", )
        text.scale(.5).to_edge(UP).shift(3 * LEFT)
        self.play(Write(text))
        self.wait()
        self.play(FadeOut(text))

    def create_detail_space(self):
        def show_distances(dleft, dmiddle, dright, end_line_offset=.5, arrow_offset=.1):
            start_l, start_m, start_r = list(map(lambda d: d.get_center(), [dleft, dmiddle, dright]))
            end_x = start_r[0] + end_line_offset
            line_l = DashedVMobject(Line(start_l, [end_x, *start_l[1:]], stroke_width=2, color=dleft.get_color(),
                                         stroke_opacity=dleft.get_fill_opacity()), num_dashes=15)
            line_m = DashedVMobject(Line(start_m, [end_x, *start_m[1:]], stroke_width=2, color=dmiddle.get_color(),
                                         stroke_opacity=dmiddle.get_fill_opacity()), num_dashes=10)
            line_r = DashedVMobject(Line(start_r, [end_x, *start_r[1:]], stroke_width=2, color=dright.get_color(),
                                         stroke_opacity=dright.get_fill_opacity()), num_dashes=5)
            arrow = DoubleArrow([end_x - arrow_offset, *start_l[1:]], [end_x - arrow_offset, *start_m[1:]], buff=0,
                                color=GREEN)
            return line_l, line_m, line_r, arrow

        self.approx_dots[0].save_state()
        self.play(self.approx_dots[0].animate.scale(2).set_stroke(width=5, color=WHITE))
        self.play(FadeIn(self.mean_dots[0]))
        line_l, line_m, line_r, arrow = show_distances(self.dots[0], self.mean_dots[0], self.dots[1])
        self.play(Create(line_l), Create(line_m), Create(line_r))
        self.play(Write(arrow))
        self.wait()
        self.play(arrow.animate.shift(arrow.get_length() * DOWN))
        self.wait()
        self.play(arrow.animate.shift(arrow.get_length() * UP))
        self.wait()
        self.play(Create(self.hline), Create(self.detail_axes))
        connector_detail = DashedLine(self.detail_axes.c2p(0, self.detail_points[0][1]),
                                      self.detail_dots[0].get_center(), color=GREEN)
        self.play(Create(connector_detail))
        self.play(FadeIn(self.detail_dots[0]))
        self.wait()
        self.play(self.approx_dots[0].animate.become(self.approx_dots[0].saved_state),
                  FadeOut(connector_detail, line_l, line_m, line_r, arrow, self.mean_dots[0]))
        for i in range(1, int(self.N / 2)):
            anim_speed = 2 * (1 - i / (self.N - 1))
            self.approx_dots[i].save_state()
            self.play(self.approx_dots[i].animate.scale(2).set_stroke(width=5, color=WHITE))
            self.play(FadeIn(self.mean_dots[i]))
            line_l, line_m, line_r, arrow = show_distances(self.dots[2 * i], self.mean_dots[i], self.dots[2 * i + 1])
            self.play(Create(line_l), Create(line_m), Create(line_r), Write(arrow))
            self.wait()
            connector_detail = DashedLine(self.detail_axes.c2p(0, self.detail_points[i][1]),
                                          self.detail_dots[i].get_center(), color=GREEN)
            self.play(Create(connector_detail), run_time=anim_speed / 4)
            self.play(FadeIn(self.detail_dots[i]), run_time=anim_speed / 2)
            self.wait()
            self.play(self.approx_dots[i].animate.become(self.approx_dots[i].saved_state),
                      FadeOut(connector_detail, line_l, line_m, line_r, arrow, self.mean_dots[i]),
                      run_time=anim_speed / 2)

    def transform_finished(self):
        self.play(FadeOut(self.dots))
        approx_text = Text(f"Approximation space ({int(self.N / 2)} points)", color=RED).scale(.5).to_corner(UR,
                                                                                                             buff=.2)
        detail_text = Text(f"Detail space ({int(self.N / 2)} points)", color=GREEN).scale(.5).to_corner(DR, buff=.2)
        self.play(Write(approx_text), Write(detail_text))

    def inverse_transform(self):
        text = Text("Inverse transform").scale(.5).to_edge(UP, buff=.2).shift(config.frame_width / 4 * LEFT)
        self.play(Write(text))
        self.wait()
        middle_dot = self.approx_dots[0].copy()
        self.play(middle_dot.animate.scale(2).set_stroke(width=5, color=WHITE))
        self.wait()
        self.play(middle_dot.animate.become(self.mean_dots[0]))
        self.wait()
        detail_dot = self.detail_dots[0].copy()
        self.play(detail_dot.animate.scale(2).set_stroke(width=5, color=WHITE))
        self.wait()
        line = DashedLine([self.dots[0].get_center()[0] - .1, middle_dot[0].get_center()[1], 0],
                          [self.dots[1].get_center()[0] + .1, middle_dot[0].get_center()[1], 0], color=RED)
        arrow_l = DoubleArrow(self.dots[0].get_center(),
                              [self.dots[0].get_center()[0], self.mean_dots[0].get_center()[1], 0],
                              buff=0, color=GREEN)
        arrow_r = DoubleArrow([self.dots[1].get_center()[0], self.mean_dots[0].get_center()[1], 0],
                              self.dots[1].get_center(),
                              buff=0, color=GREEN)
        self.play(ReplacementTransform(detail_dot, arrow_l), Create(line))
        self.play(FadeIn(self.dots[0]))
        self.wait()
        self.play(Transform(arrow_l, arrow_r))
        self.play(FadeIn(self.dots[1]))
        self.wait()
        self.play(FadeOut(arrow_l, middle_dot, line))
        self.wait()
        for i in range(1, int(self.N / 2)):
            anim_speed = animation_speed(i, self.N / 2, maxim=2, minim=.1, speed=2)
            middle_dot = self.approx_dots[i].copy()
            self.play(middle_dot.animate.scale(2).set_stroke(width=5, color=WHITE), run_time=anim_speed)
            self.wait(anim_speed / 2)
            self.play(middle_dot.animate.become(self.mean_dots[i]), run_time=anim_speed)
            self.wait(anim_speed / 2)
            detail_dot = self.detail_dots[i].copy()
            self.play(detail_dot.animate.scale(2).set_stroke(width=5, color=WHITE), run_time=anim_speed)
            self.wait(anim_speed / 2)
            line = DashedLine([self.dots[2 * i].get_center()[0] - .1, middle_dot.get_center()[1], 0],
                              [self.dots[2 * i + 1].get_center()[0] + .1, middle_dot.get_center()[1], 0], color=RED)
            arrow_l = DoubleArrow(self.dots[2 * i].get_center(),
                                  [self.dots[2 * i].get_center()[0], middle_dot.get_center()[1], 0],
                                  buff=0, color=GREEN)
            arrow_r = DoubleArrow([self.dots[2 * i + 1].get_center()[0], middle_dot.get_center()[1], 0],
                                  self.dots[2 * i + 1].get_center(),
                                  buff=0, color=GREEN)
            self.play(ReplacementTransform(detail_dot, arrow_l), Create(line), run_time=anim_speed)
            self.play(FadeIn(self.dots[2 * i]), run_time=anim_speed)
            self.wait(anim_speed / 2)
            self.play(Transform(arrow_l, arrow_r), run_time=anim_speed)
            self.play(FadeIn(self.dots[2 * i + 1]), run_time=anim_speed)
            self.wait(anim_speed / 2)
            self.play(FadeOut(arrow_l, middle_dot, line), run_time=anim_speed)
            self.wait(anim_speed / 2)
        self.wait(2)
        text2 = Text("Orignal signal as it was before").scale(.5).next_to(text, DOWN, buff=SMALL_BUFF)
        text3 = Text("No information lost: change of POV").scale(.5).next_to(text2, DOWN, buff=SMALL_BUFF)
        self.play(Write(text2))
        self.play(Write(text3))

    def construct(self):
        self.create_main_plot()
        self.create_approx_space()
        self.inverse_transform_text()
        self.create_detail_space()
        self.transform_finished()
        self.inverse_transform()


class MultipleTransforms(Scene):
    def transform_rectangles(self, signal, L=1, show_braces=True, buff=SMALL_BUFF):
        def recursive(signal, L, Lmax, complement, show_braces, buff):
            if L != 0:
                approx = VGroup(
                    shape := Rectangle(height=1, width=signal.width / 2 - buff),
                    MathTex("A_" + str(L-1)).move_to(shape.get_center())
                ).align_to(signal, LEFT).set_color(RED)
                detail = VGroup(
                    shape := Rectangle(height=1, width=signal.width / 2 - buff),
                    MathTex("D_" + str(L-1)).move_to(shape.get_center())
                ).align_to(signal, RIGHT).set_color(GREEN)
                if complement is not None:
                    new_complement = VGroup(detail, complement.copy().next_to(detail, RIGHT))
                    result = VGroup(approx, new_complement).next_to(VGroup(signal, complement), DOWN)
                else:
                    new_complement = detail
                    result = VGroup(approx, new_complement).next_to(signal, DOWN)
                self.play(Write(result))
                if show_braces:
                    brace_approx = Brace(approx, DOWN, color=RED)
                    brace_detail = Brace(detail, DOWN, color=GREEN)
                    length_approx = MathTex("N/" + str(2**(Lmax-L+1)), color=RED)
                    length_detail = MathTex("N/" + str(2**(Lmax-L+1)), color=GREEN)
                    if length_approx.get_right()[0] - length_approx.get_left()[0] > approx.width:
                        length_approx.match_width(approx)
                        length_detail.match_width(detail)
                    braces = VGroup(brace_approx, length_approx.next_to(brace_approx, DOWN),
                                    brace_detail, length_detail.next_to(brace_detail, DOWN))
                    self.play(Write(braces))
                    self.wait()
                    self.play(FadeOut(braces))
                self.wait()
                recursive(approx, L - 1, Lmax, VGroup(detail, new_complement), show_braces, buff)
        recursive(signal, L, L, None, show_braces, buff)


class MultipleTransforms1(MultipleTransforms):
    def construct(self):
        signal = VGroup(
            signal_shape := Rectangle(WHITE, height=1, width=14),
            Text("Signal").move_to(signal_shape.get_center())
        ).shift(UP)
        brace = Brace(signal, DOWN)
        length = Tex("$N$ values").next_to(brace, DOWN)
        self.play(Write(signal))
        self.wait()
        self.play(Write(brace), Write(length))
        self.wait()
        self.play(FadeOut(brace, length))
        self.transform_rectangles(signal, L=1)
        self.wait()


class MultipleTransforms2(MultipleTransforms):
    def construct(self):
        signal = VGroup(
            signal_shape := Rectangle(WHITE, height=1, width=14),
            Text("Signal").move_to(signal_shape.get_center())
        ).shift(2*UP)
        brace = Brace(signal, DOWN)
        length = Tex("$N$ values").next_to(brace, DOWN)
        self.play(Write(signal))
        self.wait()
        self.play(Write(brace), Write(length))
        self.wait()
        self.play(FadeOut(brace, length))
        self.transform_rectangles(signal, L=2)
        self.wait()


class MultipleTransforms4(MultipleTransforms):
    def construct(self):
        signal = VGroup(
            signal_shape := Rectangle(WHITE, height=1, width=14),
            Text("Signal").move_to(signal_shape.get_center())
        ).shift(3*UP)
        brace = Brace(signal, DOWN)
        length = Tex("$N$ values").next_to(brace, DOWN)
        self.play(Write(signal))
        self.wait()
        self.play(Write(brace), Write(length))
        self.wait()
        self.play(FadeOut(brace, length))
        self.transform_rectangles(signal, L=4)
        self.wait()


class HaarIntroductionOld(Scene):
    def construct(self):
        N = 16
        seed = 2
        offset = -2

        y = [10]
        np.random.seed(seed)
        for i in range(N - 1):
            y.append(y[-1] + np.random.randint(-2, 3))
        points = np.array([[i + 1, yi + offset] for i, yi in enumerate(y)])
        mean_points = np.array([(points[i] + points[i + 1]) / 2 for i in range(0, N, 2)])
        diff_points = np.array([points[i] - mean_points[int(i / 2)] for i in range(0, N, 2)])
        diff_points[:, 0] = mean_points[:, 0]
        # print(points)
        # print(mean_points)
        # print(diff_points)

        axes = Axes(x_range=[0, N + 1, 1], y_range=[0, max(y), 1],
                    axis_config={"number_scale_value": .5})
        axes.add_coordinates()
        left_axes = Axes(x_range=[0, N + 1, 1], y_range=[0, max(y), 1],
                         x_length=config.frame_width / 2.3,
                         axis_config={"number_scale_value": .5})
        left_axes.add_coordinates()
        right_axes = Axes(x_range=[0, N + 1, 1], y_range=[min(diff_points[:, 1]), max(diff_points[:, 1]) + .5, .5],
                          x_length=config.frame_width / 2.3,
                          axis_config={"number_scale_value": .5})
        right_axes.add_coordinates()

        dots = VMobject()
        dots_left = VMobject()
        for p in points:
            dots.add(Dot(axes.c2p(*p)))
            dots_left.add(Dot(left_axes.c2p(*p), fill_opacity=.3))
        mean_dots = VMobject()
        mean_dots_left = VMobject()
        diff_dots_right = VMobject()
        for m, d in zip(mean_points, diff_points):
            mean_dots.add(Dot(axes.c2p(*m), color=RED))
            mean_dots_left.add(Dot(left_axes.c2p(*m), color=RED))
            diff_dots_right.add(Dot(right_axes.c2p(*d), color=GREEN))

        graph = VGroup(axes, dots, mean_dots)
        left_graph = VGroup(left_axes, dots_left, mean_dots_left).to_edge(LEFT, buff=MED_SMALL_BUFF)
        second_graph = VGroup(right_axes, diff_dots_right).to_edge(RIGHT, buff=MED_SMALL_BUFF)

        brace1 = BraceBetweenPoints(dots_left[0], mean_dots_left[0], direction=RIGHT, color=GREEN)
        brace2 = BraceBetweenPoints(dots_left[1], mean_dots_left[0], direction=RIGHT, color=GREEN)

        self.play(Create(axes))
        self.wait()
        self.play(ShowIncreasingSubsets(dots))
        self.wait(2)
        for i in range(0, int(N / 2)):
            current_dots = dots[2 * i:2 * i + 2].copy().set_color(RED)
            self.play(FadeIn(current_dots), run_time=1 - 2 * i / (N + 1))
            dots[2 * i:2 * i + 2].set_opacity(.3)
            self.play(ReplacementTransform(current_dots, mean_dots[i]), run_time=1 - 2 * i / (N + 1))

        self.play(FadeOut(dots))
        self.wait(2)
        self.play(FadeIn(dots))

        self.play(ReplacementTransform(graph, left_graph))
        self.play(FadeIn(right_axes))

        def show_distances(dleft, dmiddle, dright, end_line_offset=.5, arrow_offset=.1):
            start_l, start_m, start_r = list(map(lambda d: d.get_center(), [dleft, dmiddle, dright]))
            end_x = start_r[0] + end_line_offset
            line_l = DashedVMobject(Line(start_l, [end_x, *start_l[1:]], stroke_width=2, color=dleft.get_color(),
                                         stroke_opacity=dleft.get_fill_opacity()), num_dashes=15)
            line_m = DashedVMobject(Line(start_m, [end_x, *start_m[1:]], stroke_width=2, color=dmiddle.get_color(),
                                         stroke_opacity=dmiddle.get_fill_opacity()), num_dashes=10)
            line_r = DashedVMobject(Line(start_r, [end_x, *start_r[1:]], stroke_width=2, color=dright.get_color(),
                                         stroke_opacity=dright.get_fill_opacity()), num_dashes=5)
            arrow_up = DoubleArrow([end_x - arrow_offset, *start_l[1:]], [end_x - arrow_offset, *start_m[1:]], buff=0)
            arrow_down = DoubleArrow([end_x - arrow_offset, *start_r[1:]], [end_x - arrow_offset, *start_m[1:]], buff=0)
            return line_l, line_m, line_r, arrow_up, arrow_down

        line_l, line_m, line_r, arrow_up, arrow_down = show_distances(dots_left[0], mean_dots_left[0], dots_left[1])
        self.play(FadeIn(line_l, line_m))
        self.play(FadeIn(arrow_up))
        self.play(FadeIn(line_r))
        self.play(ReplacementTransform(arrow_up, arrow_down))
        self.wait()
        self.play(Transform(arrow_up, diff_dots_right[0]), run_time=2)

        # brace1 = BraceBetweenPoints(dots_left[0], mean_dots_left[0], direction=RIGHT, color=GREEN)
        # brace2 = BraceBetweenPoints(dots_left[1], mean_dots_left[0], direction=RIGHT).match_style(brace1)
        # self.play(FadeIn(brace1))
        # self.wait()
        # self.play(FadeIn(brace2))
        # self.play(brace1.animate.align_to(brace2, RIGHT))
        # self.play(ReplacementTransform(VGroup(brace1, brace2).copy(), diff_dots_right[0]), run_time=1)
        # for i in range(1, int(N/2)):
        #     brace2.target = BraceBetweenPoints(dots_left[2*i+1], mean_dots_left[i], direction=RIGHT).match_style(brace1)
        #     brace1.target = BraceBetweenPoints(dots_left[2*i], mean_dots_left[i], direction=RIGHT).align_to(brace2.target, RIGHT).match_style(brace1)
        #     self.play(AnimationGroup(MoveToTarget(brace1), MoveToTarget(brace2), lag_ratio=.2, rate_func=smooth), run_time=1-2*i/(N+1))
        #     self.play(ReplacementTransform(VGroup(brace1, brace2).copy(), diff_dots_right[i]), run_time=1-2*i/(N+1))

        # self.play(FadeIn(diff_dots_right[1:]))

        self.wait(5)
