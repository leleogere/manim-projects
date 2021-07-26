from manim import *

from mob_epicycles import FourierEpicyclesMObject


class Introduction(Scene):
    def construct(self):
        TITLE = "Wavelet transform and drawings"
        title = Tex(r"Wavelet transform\\and drawings").scale(2)
        title_up = Title(TITLE)
        self.play(AnimationGroup(Write(title), Circumscribe(title), lag_ratio=.8))
        self.wait()
        self.play(AnimationGroup(ReplacementTransform(title, title_up[:-1]),
                                 Create(title_up[-1].set_color(YELLOW)),
                                 lag_ratio=.4))

        fourier_shift = 4*LEFT
        fourier_text = Text("Fourier transform").shift(UP + fourier_shift)
        axes_fourier = Axes(x_range=[-TAU, TAU, PI], x_length=5,
                            y_range=[-1.5, 1.5, .5], y_length=3).shift(2*DOWN + fourier_shift)
        sin = axes_fourier.get_graph(lambda x: np.sin(x), color=RED)
        self.play(Write(fourier_text))
        self.wait()
        self.play(Create(axes_fourier))
        self.wait()
        self.play(Create(sin))
        self.wait(2)

        def get_shape(tex):
            path = VMobject()
            shape = Tex(tex)
            for sp in shape.family_members_with_points():
                path.append_points(sp.get_points())
            return path
        path = get_shape("$\Sigma$")
        complex_points = np.array([complex(*path.point_from_proportion(alpha)[:2]) for alpha in np.arange(0, 1, 1 / 150)])
        complex_points = (complex_points - np.mean(complex_points)) / np.max(abs(complex_points)) * 3
        ec = FourierEpicyclesMObject(complex_points, num_coefs=50, speed_factor=0,
                                     color=YELLOW, vectors_width=2, bg_shape_opacity=0,
                                     circles_width=1.5, circles_opacity=1).shift(3*RIGHT+DOWN)
        self.play(Write(ec, rate_func=double_smooth), run_time=5)
        speed = 1
        ec.add_updater(lambda e, dt: e.set(speed_factor=np.clip(e.speed_factor+speed*dt, 0, 9)))
        self.wait(20)

        wavelet_text = Text("Wavelet transform").shift(UP + fourier_shift)
        axes_wavelet = Axes(x_range=[-.5, 1.5, .2], x_length=5,
                            y_range=[-0.1, 1.5, .2], y_length=3).shift(2 * DOWN + fourier_shift)
        scale = axes_wavelet.get_graph(lambda x: np.sqrt(2)*(0 <= x < 1), discontinuities=[0, 1], color=RED)
        wavelet = axes_wavelet.get_graph(lambda x: np.sqrt(2)*(0 <= x < .5) - np.sqrt(2)*(.5 <= x < 1), discontinuities=[0, .5, 1], color=BLUE)
        speed = -2
        self.play(Transform(fourier_text, wavelet_text))
        self.play(Transform(axes_fourier, axes_wavelet),
                  Transform(sin, scale),
                  Create(wavelet))
        while ec.speed_factor > 0:
            self.wait()
        shape = ec.get_bg().copy().set_stroke(color=YELLOW, opacity=.5, width=2)
        self.play(FadeOut(ec),
                  FadeIn(shape))
        question_mark = Tex("?").scale(7).move_to(ec.get_center())
        self.play(Write(question_mark))
        self.play(Indicate(question_mark))
        self.wait(3)
