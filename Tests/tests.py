from manim import *

class transformers(Scene):
    def construct(self):
        values = [1, 2, 3, 4]
        a_num = Text("1")
        b_num = Text("2")
        a_sum = Text("3")
        b_sum = Text("4")
        a_num.add_updater(lambda z: z.become(Text(str(values[0]))).move_to([-2, -1, 0]))
        b_num.add_updater(lambda z: z.become(Text(str(values[1]))).move_to([-1, -1, 0]))
        a_sum.add_updater(lambda z: z.become(Text(str(values[2]))).move_to([0, -1, 0]))
        b_sum.add_updater(lambda z: z.become(Text(str(values[3]))).move_to([1, -1, 0]))
        one = VGroup(a_num, b_num)
        two = VGroup(a_sum, b_sum)
        self.add(one)
        a_num.remove_updater(a_num.get_updaters())
        b_num.remove_updater(b_num.get_updaters())
        self.play(Transform(a_num, b_num))

class CreateMoveAlong(Scene):
    def construct(self):
        dot = Dot()
        square = Square()
        self.play(Create(square), MoveAlongPath(dot, square.copy()), run_time=5)

# class CreateWithDot(Create):
#     def begin(self) -> None:
#         self.dot = Dot()
#
#     def interpolate_submobject(
#         self, submobject: Mobject, starting_submobject: Mobject, alpha: float
#     ) -> None:
#

def CreateWithDot(curves, dot):

    f_always(dot.move_to, curve.get_end)
    return FadeIn(dot), Create(curves), FadeOut(dot)

class CreateDot(Scene):
    def construct(self):
        square = Square()
        self.play(*CreateWithDot(square, Dot()))


class Loading(Scene):
    def construct(self):
        dot = Dot(color=RED)
        circle = Circle(2)
        turn_animation_into_updater(MoveAlongPath(dot, circle, rate_func=linear, run_time=5), cycle=True)
        path = TracedPath(dot.get_center, dissipating_time=4, stroke_width=[0,18], stroke_color=[YELLOW, RED])
        self.add(dot)
        self.add(path)
        self.wait(30)

class ReducingPath(Scene):
    def construct(self):
        dot = Dot()
        path = TracedPath(dot.get_center, dissipating_time=1, stroke_width=[0,1])
        self.add(dot, path)
        self.play(dot.animate.to_corner(DR))
        self.play(dot.animate.to_corner(UR))
        self.wait()

class PathProblems(Scene):
    def construct(self):
        dot1 = Dot().to_corner(UR)
        dot2 = Dot().to_edge(RIGHT)
        dot3 = Dot().to_corner(DR)
        path1 = TracedPath(dot1.get_center, dissipating_time=2, stroke_opacity=[1, 0])
        path2 = TracedPath(dot2.get_center, dissipating_time=2, stroke_width=[1, 0])
        path3 = TracedPath(dot3.get_center, dissipating_time=2, stroke_color=[RED, YELLOW])
        self.add(dot1, dot2, dot3, path1, path2, path3)
        self.play(VGroup(dot1, dot2, dot3).animate(run_time=3).to_edge(LEFT))
        self.wait(3)

class BlueText(Text):
    def __init__(self, text, **kwargs):
        super().__init__(text, color=BLUE, **kwargs)

class TestText(Scene):
    def construct(self):
        text = BlueText("Hello world!")
        self.add(text)
