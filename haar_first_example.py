from manim import *


class HaarIntroduction(Scene):
    def construct(self):
        N = 16
        seed = 2
        offset = -2

        y = [10]
        np.random.seed(seed)
        for i in range(N-1):
            y.append(y[-1] + np.random.randint(-2, 3))
        points = np.array([[i+1, yi + offset] for i, yi in enumerate(y)])
        mean_points = np.array([(points[i]+points[i+1])/2 for i in range(0, N, 2)])
        diff_points = np.array([points[i]-mean_points[int(i/2)] for i in range(0, N, 2)])
        diff_points[:, 0] = mean_points[:, 0]
        # print(points)
        # print(mean_points)
        # print(diff_points)

        axes = Axes(x_range=[0, N+1, 1], y_range=[0, max(y), 1],
                    axis_config={"number_scale_value": .5})
        axes.add_coordinates()
        left_axes = Axes(x_range=[0, N+1, 1], y_range=[0, max(y), 1],
                          x_length=config.frame_width/2.3,
                          axis_config={"number_scale_value": .5})
        left_axes.add_coordinates()
        right_axes = Axes(x_range=[0, N+1, 1], y_range=[min(diff_points[:, 1]), max(diff_points[:, 1])+.5, .5],
                           x_length=config.frame_width/2.3,
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
        for i in range(0, int(N/2)):
            current_dots = dots[2*i:2*i+2].copy().set_color(RED)
            self.play(FadeIn(current_dots), run_time=1-2*i/(N+1))
            dots[2*i:2*i+2].set_opacity(.3)
            self.play(ReplacementTransform(current_dots, mean_dots[i]), run_time=1-2*i/(N+1))

        self.play(FadeOut(dots))
        self.wait(2)
        self.play(FadeIn(dots))

        self.play(ReplacementTransform(graph, left_graph))
        self.play(FadeIn(right_axes))

        def show_distances(dleft, dmiddle, dright, end_line_offset=.5, arrow_offset=.1):
            start_l, start_m, start_r = list(map(lambda d: d.get_center(), [dleft, dmiddle, dright]))
            end_x = start_r[0] + end_line_offset
            line_l = DashedVMobject(Line(start_l, [end_x, *start_l[1:]], stroke_width=2, color=dleft.get_color(), stroke_opacity=dleft.get_fill_opacity()), num_dashes=15)
            line_m = DashedVMobject(Line(start_m, [end_x, *start_m[1:]], stroke_width=2, color=dmiddle.get_color(), stroke_opacity=dmiddle.get_fill_opacity()), num_dashes=10)
            line_r = DashedVMobject(Line(start_r, [end_x, *start_r[1:]], stroke_width=2, color=dright.get_color(), stroke_opacity=dright.get_fill_opacity()), num_dashes=5)
            arrow_up = DoubleArrow([end_x-arrow_offset, *start_l[1:]], [end_x-arrow_offset, *start_m[1:]], buff=0)
            arrow_down = DoubleArrow([end_x-arrow_offset, *start_r[1:]], [end_x-arrow_offset, *start_m[1:]], buff=0)
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
