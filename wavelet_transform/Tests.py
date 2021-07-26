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
