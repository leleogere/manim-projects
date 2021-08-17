from typing import Callable

from manim import *

class MyVMoject(Square):
    mine = True

    updating_variation = 1
    updating_speed = 1

    def suspend_updating(self, recursive: bool = True, run_time: float = 0, rate_func: Callable[[float], float] = linear) -> "Mobject":
        """Disable updating from updaters and animations.


        Parameters
        ----------
        recursive
            Whether to recursively suspend updating on all submobjects.
        run_time
            Duration of the interruption of the animations (instantaneous if 0).
        rate_func
            Function controlling the behavior of the animation's interruption (useless
            if run_time=0).

        Returns
        -------
        :class:`Mobject`
            ``self``

        See also
        --------
        :meth:`resume_updating`
        :meth:`add_updater`

        """
        frame_duration = 1/config.frame_rate
        if run_time < frame_duration:
            self.updating_speed = 0
        else:
            self.updating_variation = - frame_duration / run_time
            self.updating_speed += self.updating_variation
        if recursive:
            for submob in self.submobjects:
                submob.suspend_updating(recursive=recursive, run_time=run_time, rate_func=rate_func)
            self.update(dt=0, recursive=recursive, rate_func=rate_func)
        return self

    def resume_updating(self, recursive: bool = True, run_time: float = 0, rate_func: Callable[[float], float] = linear) -> "Mobject":
        """Enable updating from updaters and animations.

        Parameters
        ----------
        recursive
            Whether to recursively enable updating on all submobjects.
        run_time
            Duration needed to get the animation to its full speed of the animations
            (instantaneous if 0).
        rate_func
            Function controlling the behavior of the animation's start (useless if
            run_time=0).

        Returns
        -------
        :class:`Mobject`
            ``self``

        See also
        --------
        :meth:`suspend_updating`
        :meth:`add_updater`

        """
        frame_duration = 1/config.frame_rate
        if run_time < frame_duration:
            self.updating_speed = 1
        else:
            self.updating_variation = frame_duration / run_time
            self.updating_speed += self.updating_variation
        if recursive:
            for submob in self.submobjects:
                submob.resume_updating(recursive=recursive, run_time=run_time, rate_func=rate_func)
            self.update(dt=0, recursive=recursive, rate_func=rate_func)
        return self

    def update(self, dt: float = 0, recursive: bool = True, rate_func : Callable[[float], float] = linear) -> "Mobject":
        """Apply all updaters.

        Does nothing if updation speed is 0 (updating suspended)

        Parameters
        ----------
        dt
            The parameter ``dt`` to pass to the update functions. Usually this is the time in seconds since the last call of ``update``.
        recursive
            Whether to recursively update all submobjects.
        rate_func
            Function controlling the behavior of the animation when the suspending/resuming is not
            instantaneous.

        Returns
        -------
        :class:`Mobject`
            ``self``

        See Also
        --------
        :meth:`add_updater`
        :meth:`get_updaters`

        """
        if self.updating_speed == 0:
            return self
        for updater in self.updaters:
            parameters = get_parameters(updater)
            if "dt" in parameters:
                updater(self, rate_func(self.updating_speed * dt))
                if 0 < self.updating_speed < 1:
                    self.updating_speed = np.clip(self.updating_speed + self.updating_variation, 0, 1)
            else:
                updater(self)
        if recursive:
            for submob in self.submobjects:
                submob.update(dt, recursive)
        return self

    # def suspend_updating(self, recursive: bool = True) -> "Mobject":
    #     self.updating_speed = 0
    #     if recursive:
    #         for submob in self.submobjects:
    #             submob.suspend_updating(recursive)
    #     return self
    #
    # def resume_updating(self, recursive: bool = True) -> "Mobject":
    #     self.updating_speed = 1
    #     if recursive:
    #         for submob in self.submobjects:
    #             submob.resume_updating(recursive)
    #         self.update(dt=0, recursive=recursive)
    #     return self
    #
    # def resume_updating_smoothly(self, run_time: float = 1, recursive: bool = True) -> "Mobject":
    #     self.updating_variation = 1 / (config.frame_rate * run_time)
    #     self.updating_speed += self.updating_variation
    #     if recursive:
    #         for submob in self.submobjects:
    #             submob.resume_updating_smoothly(run_time, recursive)
    #         self.update(dt=0, recursive=recursive)
    #     return self
    #
    # def suspend_updating_smoothly(self, run_time: float = 1, recursive: bool = True) -> "Mobject":
    #     self.updating_variation = -1 / (config.frame_rate * run_time)
    #     self.updating_speed += self.updating_variation
    #     if recursive:
    #         for submob in self.submobjects:
    #             submob.suspend_updating_smoothly(run_time, recursive)
    #         self.update(dt=0, recursive=recursive)
    #     return self



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

class Test2(Scene):
    def construct(self):
        times = [0, 1, 3, 5]
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
        for g, t in zip(group, times):
            g.suspend_updating(run_time=t)
        self.wait(6)
        for g, t in zip(group, times):
            g.resume_updating(run_time=t)
        self.wait(10)

class Test3(Scene):
    def construct(self):
        times = [0, 1, 3, 5]
        texts = ["Suspend/resume instantaneously (already existing)\nsquare1.suspend_updating()",  *[f"Suspend/resume in {t} second\nsquare{i+2}.suspend_updating_smoothly(run_time={t})" for i, t in enumerate(times[1:])]]
        colors = [RED, BLUE, YELLOW, GREEN]
        s = Square(color=colors[0]).scale(.6).add_updater(lambda s, dt: s.shift(dt*RIGHT).rotate(dt))
        group = VGroup(s)
        for i in range(3):
            group.add(s.copy().set_color(colors[i+1]))
        group.arrange(DOWN, buff=.5).to_edge(LEFT)
        for i, g in enumerate(group):
            self.add(Text(texts[i], color=colors[i]).scale(.4).next_to(g, RIGHT).to_edge(RIGHT))
        self.add(group)
        self.wait(2)
        for g, t in zip(group, times):
            g.suspend_updating(run_time=t)
        self.wait(6)
        for g, t in zip(group, times):
            g.resume_updating(run_time=t)
        self.wait(10)

class SmoothRecursiveTest(Scene):
    def construct(self):
        s = Square(3).add_updater(lambda a, dt: a.rotate(dt))
        print(s.get_vertices())
        sul = Square(1).add_updater(lambda c, dt: c.move_to(s.get_vertices()[0]).rotate(-2*dt))
        sur = Square(1).add_updater(lambda c, dt: c.move_to(s.get_vertices()[1]).rotate(-2*dt))
        sdl = Square(1).add_updater(lambda c, dt: c.move_to(s.get_vertices()[2]).rotate(-2*dt))
        sdr = Square(1).add_updater(lambda c, dt: c.move_to(s.get_vertices()[3]).rotate(-2*dt))
        corners = VGroup(sul, sur, sdl, sdr)
        s.add(corners)
        self.add(s)
        self.wait(3)
        s.suspend_updating(recursive=False)
        self.wait(5)


class RecursiveTest(Scene):
    def construct(self):
        s = Square(3).add_updater(lambda a, dt: a.rotate(dt))
        print(s.get_vertices())
        sul = Square(1).add_updater(lambda c, dt: c.move_to(s.get_vertices()[0]).rotate(-2*dt))
        sur = Square(1).add_updater(lambda c, dt: c.move_to(s.get_vertices()[1]).rotate(-2*dt))
        sdl = Square(1).add_updater(lambda c, dt: c.move_to(s.get_vertices()[2]).rotate(-2*dt))
        sdr = Square(1).add_updater(lambda c, dt: c.move_to(s.get_vertices()[3]).rotate(-2*dt))
        corners = VGroup(sul, sur, sdl, sdr)
        s.add(corners)
        self.add(s)
        self.wait(3)
        s.suspend_updating(recursive=False)
        self.wait(5)
