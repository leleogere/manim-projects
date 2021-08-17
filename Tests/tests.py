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
