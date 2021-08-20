from manim import *
from fourier_mobject_epicycles import FourierEpicyclesMobject


########################################################################################################################


class Introduction(Scene):

    def formula_animation(self, formula):
        self.play(Write(formula))
        self.wait(3)
        self.play(Indicate(formula[-1]))
        self.wait(3)
        exp = formula[-1].copy()
        self.play(exp.animate.shift(DOWN+.5*RIGHT).set_color(RED))
        circle_axes = Axes([-1.5, 1.5, .5], [-1.5, 1.5, .5], 5, 5).scale(.4).next_to(formula, RIGHT)
        self.play(Create(circle_axes))
        vect = Line(circle_axes.c2p(0, 0), circle_axes.c2p(1, 0))
        dot = Dot()
        circle = Circle.from_three_points(circle_axes.c2p(0, 1), circle_axes.c2p(1, 0), circle_axes.c2p(-1, 0))
        f_always(dot.move_to, vect.get_end)
        self.play(Create(vect), Write(dot))
        self.play(Rotate(vect, angle=2 * TAU + 0.001, about_point=circle_axes.c2p(0, 0)),
                  FadeIn(circle), run_time=10)
        self.wait()
        self.play(FadeOut(circle, dot, vect, circle_axes, exp))

    def construct(self):
        title = Tex(r"Wavelet transform\\and drawings").scale(2)
        title_up = Title("Wavelet transform and drawings")
        self.play(AnimationGroup(Write(title), Circumscribe(title), lag_ratio=.8))
        self.wait()
        self.play(AnimationGroup(ReplacementTransform(title, title_up[:-1]),
                                 Create(title_up[-1].set_color(YELLOW)),
                                 lag_ratio=.4))

        fourier_shift = 4*LEFT
        fourier_text = Text("Fourier transform").shift(UP + fourier_shift).save_state()
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
        ec = FourierEpicyclesMobject(complex_points, num_coefs=120, speed_factor=0,
                                     color=YELLOW, vectors_width=2, bg_shape_opacity=0,
                                     circles_width=1.5, circles_opacity=1).shift(3*RIGHT+DOWN)
        self.play(Write(ec, rate_func=double_smooth), run_time=5)
        ec.add_updater(lambda e, dt: e.set(speed_factor=np.clip(e.speed_factor+dt, 0, 8)))
        self.wait(20)
        self.play(fourier_text.animate.shift(UP))
        formula = MathTex(r"f(x) = ", "\sum_{n \in \mathbb{Z}} c_n(f)", "e^{inx}").scale(.8).next_to(fourier_text, DOWN)
        self.formula_animation(formula)
        self.wait()
        self.play(Circumscribe(formula[1:], run_time=3),
                  Circumscribe(ec, run_time=3))
        self.wait()
        self.play(FadeOut(formula), fourier_text.animate.restore())
        self.wait(5)
        shape = ec.get_bg().copy().set_stroke(color=YELLOW, opacity=.2, width=2)

        wavelet_text = Text("Wavelet transform").shift(UP + fourier_shift)
        axes_wavelet = Axes(x_range=[-.5, 1.5, .2], x_length=5,
                            y_range=[-1.5, 1.5, .2], y_length=3).shift(2 * DOWN + fourier_shift)
        sq2 = np.sqrt(2)
        scale = axes_wavelet.get_line_graph([-.5, 0, 0, 1, 1, 1.5], [0, 0, sq2, sq2, 0, 0], line_color=RED, add_vertex_dots=False)
        wavelet = DashedVMobject(
            axes_wavelet.get_line_graph([-.5, 0, 0, .5, .5, 1, 1, 1.5],
                                        [0, 0, sq2, sq2, -sq2, -sq2, 0, 0],
                                        line_color=BLUE,
                                        add_vertex_dots=False)["line_graph"],
            num_dashes=60
        ).set_z_index(scale.z_index+1)
        self.play(Transform(fourier_text, wavelet_text))
        self.play(Transform(axes_fourier, axes_wavelet),
                  Transform(sin, scale),
                  Create(wavelet),
                  FadeOut(ec),
                  FadeIn(shape),
                  run_time=3)
        self.wait(2)
        question_mark = Tex("?").scale(7).move_to(ec.get_center())
        self.play(Write(question_mark))
        self.play(Indicate(question_mark))
        self.wait()
        question = Tex(r"How can we\\draw in a similar\\way using the\\wavelet transform?").move_to(question_mark)
        question.add(SurroundingRectangle(question))
        self.play(LaggedStart(question_mark.animate.set_opacity(.1),
                              Write(question, run_time=4), lag_ratio=0.4))
        self.wait()
