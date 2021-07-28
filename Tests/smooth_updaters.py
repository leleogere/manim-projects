from manim import *

class MyVMoject(Square):
    mine = True

    updating_variation = 1
    updating_speed = 1

    def update(self, dt: float = 0, recursive: bool = True) -> "Mobject":
        print(config.frame_rate, self.updating_variation, self.updating_speed, smooth(self.updating_speed))
        if self.updating_speed == 0:
            return self
        for updater in self.updaters:
            parameters = get_parameters(updater)
            if "dt" in parameters:
                updater(self, self.updating_speed * dt)
                if 0 < self.updating_speed < 1:
                    self.updating_speed = np.clip(self.updating_speed + self.updating_variation, 0, 1)
            else:
                updater(self)
        if recursive:
            for submob in self.submobjects:
                submob.update(dt, recursive)
        return self

    def suspend_updating(self, recursive: bool = True) -> "Mobject":
        self.updating_speed = 0
        if recursive:
            for submob in self.submobjects:
                submob.suspend_updating(recursive)
        return self

    def resume_updating(self, recursive: bool = True) -> "Mobject":
        self.updating_speed = 1
        if recursive:
            for submob in self.submobjects:
                submob.resume_updating(recursive)
            self.update(dt=0, recursive=recursive)
        return self

    def resume_updating_smoothly(self, run_time: float = 1, recursive: bool = True) -> "Mobject":
        self.updating_variation = 1 / (config.frame_rate * run_time)
        self.updating_speed += self.updating_variation
        if recursive:
            for submob in self.submobjects:
                submob.resume_updating_smoothly(run_time, recursive)
            self.update(dt=0, recursive=recursive)
        return self

    def suspend_updating_smoothly(self, run_time: float = 1, recursive: bool = True) -> "Mobject":
        self.updating_variation = -1 / (config.frame_rate * run_time)
        self.updating_speed += self.updating_variation
        if recursive:
            for submob in self.submobjects:
                submob.suspend_updating_smoothly(run_time, recursive)
            self.update(dt=0, recursive=recursive)
        return self



class Smooth(Scene):
    def construct(self):
        s = MyVMoject()
        # s.add_updater(lambda s, dt: s.shift(dt*RIGHT))
        s.add_updater(lambda s, dt: s.rotate(dt))
        # d = DecimalNumber(num_decimal_places=2).add_updater(lambda d, dt: d.set_value(d.get_value() + dt))
        self.add(s)
        self.wait()
        s.suspend_updating()
        self.wait()
        s.resume_updating_smoothly(3)
        self.wait(6)
        s.suspend_updating_smoothly(3)
        self.wait(5)

class Test(Scene):
    def construct(self):
        times = [1, 3, 5]
        texts = ["Suspend/resume instantaneously (already existing)\nsquare1.suspend_updating()",  *[f"Suspend/resume in {t} second\nsquare{i+2}.suspend_updating_smoothly(run_time={t})" for i, t in enumerate(times)]]
        colors = [RED, BLUE, YELLOW, GREEN]
        s = MyVMoject(color=colors[0]).scale(.6).add_updater(lambda s, dt: s.shift(dt*RIGHT).rotate(dt))
        group = VGroup(s)
        for i in range(3):
            group.add(s.copy().set_color(colors[i+1]))
        group.arrange(DOWN, buff=.5).to_edge(LEFT)
        for i, g in enumerate(group):
            self.add(Text(texts[i], color=colors[i]).scale(.4).next_to(g, RIGHT).to_edge(RIGHT))
        self.add(group)
        self.wait(2)
        group[0].suspend_updating()
        group[1].suspend_updating_smoothly(run_time=1)
        group[2].suspend_updating_smoothly(run_time=3)
        group[3].suspend_updating_smoothly(run_time=5)
        self.wait(6)
        group[0].resume_updating()
        group[1].resume_updating_smoothly(run_time=1)
        group[2].resume_updating_smoothly(run_time=3)
        group[3].resume_updating_smoothly(run_time=5)
        self.wait(10)
