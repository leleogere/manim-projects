from manim import *

class Test(Scene):
    def construct(self):
        sq = Square()
        sq.add_updater(lambda s, dt: s.rotate(rush_from(dt)))
        self.add(sq)
        self.wait(2)
        sq.suspend_updating()
        self.wait()
        sq.resume_updating()
        self.wait(2)


class SampleTextTransform(Scene):
    def construct(self):
        T1 = Text("Hello World", font="Buffalo", color=WHITE).shift(3*UP + 4*DOWN)
        ... #some other code
        T1.scale(3)
        self.play(FadeIn(T1))
        self.play(Transform(T1,Text("Goodbye now!", font="Buffalo", color=WHITE).move_to(T1.get_center()).match_width(T1)))
        self.wait()

class SampleTextTransform2(Scene):
    def construct(self):
        T1 = Text("Hello World", font="Buffalo", color=WHITE).shift(3*UP + 4*DOWN)
        ... #some other code
        T1.set(myscale=2).scale(T1.myscale)
        T1.set(myrotation=PI/6).rotate(T1.myrotation)
        self.play(FadeIn(T1))
        self.play(Transform(T1,Text("Goodbye now!", font="Buffalo", color=WHITE).move_to(T1.get_center()).scale(T1.myscale).rotate(T1.myrotation)))
        self.wait()
