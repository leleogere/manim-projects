from manim import *
from wavelet_helpers import *


class ScaleWaveletFunctionsDb2(Scene):
    N = 1024
    wavelet = "db2"
    L = 8
    k = .25
    def construct(self):
        scale_func_points = scale_function(self.N, self.wavelet, self.L, self.k)
        wavelet_func_points = wavelet_function(self.N, self.wavelet, self.L, self.k)
        y_min = min([*scale_func_points, *wavelet_func_points])
        self.y_min_real = max([*scale_func_points, *wavelet_func_points])
        axes = Axes(x_range=[0, self.N, 100],
                    y_range=[y_min, self.y_min_real, .02])
        scale_func_graph = axes.get_line_graph(range(self.N), scale_func_points, line_color=RED, add_vertex_dots=False)["line_graph"]
        wavelet_func_graph = axes.get_line_graph(range(self.N), wavelet_func_points, line_color=GREEN, add_vertex_dots=False)["line_graph"]
        title = Paragraph("Characteristic functions of", "Daubechies wavelets 2", alignment="center").scale(.8).to_corner(UR)
        scale_legend = Text("Scaling function", color=RED).move_to(axes.c2p(200, .1)).scale(.7)
        wavelet_legend = Text("Wavelet function", color=GREEN).move_to(axes.c2p(200, -.04)).scale(.7)
        self.play(Create(axes), Write(title), run_time=2)
        self.play(Create(scale_func_graph, run_time=10),
                  Write(scale_legend, run_time=2))
        self.play(Create(wavelet_func_graph, run_time=10),
                  Write(wavelet_legend, run_time=2))

        self.wait(10)


########################################################################################################################


class ScaleWaveletFunctionsCdb(Scene):
    N = 1024
    hn = np.zeros(6, dtype=complex)
    hn[0] = hn[-1] = -(3 + np.sqrt(15) * 1j)/64 * np.sqrt(2)
    hn[1] = hn[-2] =  (5 - np.sqrt(15) * 1j)/64 * np.sqrt(2)
    hn[2] = hn[-3] = (15 + np.sqrt(15) * 1j)/32 * np.sqrt(2)
    L = 8
    k = .2
    scale_func_points = scale_function_complex(hn, N, L, k)
    wavelet_func_points = wavelet_function_complex(hn, N, L, k)

    def setup_real_part(self):
        self.y_min_real = min([*self.scale_func_points.real, *self.wavelet_func_points.real])
        self.y_max_real = max([*self.scale_func_points.real, *self.wavelet_func_points.real])
        self.y_tick_real = .02
        self.window = 1.2
        self.axes_real = Axes(x_range=[0, 1.1*self.N, 100],
                              x_length=config.frame_width / 2.3,
                              y_range=[self.window*self.y_min_real, self.window*self.y_max_real, self.y_tick_real],
                              y_length=config.frame_height-3)
        self.axes_real.add(Text("Real part").scale(.6).move_to(self.axes_real.c2p(900, .8*self.y_max_real)))
        self.axes_real.to_corner(DL)
        self.scale_func_graph_real = self.axes_real.get_line_graph(range(self.N), self.scale_func_points.real, line_color=RED, add_vertex_dots=False)["line_graph"].set(z_index=self.axes_real.z_index+1)
        self.wavelet_func_graph_real = self.axes_real.get_line_graph(range(self.N), self.wavelet_func_points.real, line_color=GREEN, add_vertex_dots=False)["line_graph"].set(z_index=self.axes_real.z_index+1)

    def setup_imag_part(self):
        self.y_min_imag = min([*self.scale_func_points.imag, *self.wavelet_func_points.imag])
        self.y_max_imag = max([*self.scale_func_points.imag, *self.wavelet_func_points.imag])
        self.y_tick_imag = .01
        self.axes_imag = Axes(x_range=[0, 1.1*self.N, 100],
                              x_length=config.frame_width / 2.3,
                              y_range=[self.window*self.y_min_imag, self.window*self.y_max_imag, self.y_tick_imag],
                              y_length=config.frame_height-3).to_corner(DR)
        self.axes_imag.add(Text("Imaginary part").scale(.6).move_to(self.axes_imag.c2p(900, .8*self.y_max_imag)))
        self.scale_func_graph_imag = self.axes_imag.get_line_graph(range(self.N), self.scale_func_points.imag, line_color=RED, add_vertex_dots=False)["line_graph"].set(z_index=self.axes_imag.z_index+1)
        self.wavelet_func_graph_imag = self.axes_imag.get_line_graph(range(self.N), self.wavelet_func_points.imag, line_color=GREEN, add_vertex_dots=False)["line_graph"].set(z_index=self.axes_imag.z_index+1)

    def setup_complex_plane(self):
        self.complex_axes = Axes(x_range=[self.window*self.y_min_real, self.window*self.y_max_real, self.y_tick_real],
                                 x_length=config.frame_width/1.9,
                                 y_range=[self.window*self.y_min_imag, self.window*self.y_max_imag, self.y_tick_imag],
                                 y_length=config.frame_height/1.4)
        self.complex_axes.add(Text("Real axis").scale(.45).move_to(self.complex_axes.get_x_axis().get_end() + .5*UP),
                              Text("Imaginary axis").scale(.45).move_to(self.complex_axes.get_y_axis().get_end() + 1.3*RIGHT + .2*DOWN))
        self.complex_axes.to_corner(DR)
        self.scale_func = self.complex_axes.get_line_graph(self.scale_func_points.real, self.scale_func_points.imag, line_color=RED, add_vertex_dots=False)["line_graph"].set(z_index=self.complex_axes.z_index+1)
        self.wavelet_func = self.complex_axes.get_line_graph(self.wavelet_func_points.real, self.wavelet_func_points.imag, line_color=GREEN, add_vertex_dots=False)["line_graph"].set(z_index=self.complex_axes.z_index+1)

    def setup_titles(self):
        self.title = Text("Characteristic functions of Complex Daubechies Wavelets").scale(.7).to_edge(UP)
        self.scale_legend = Text("Scaling function", color=RED).next_to(self.title, DOWN, buff=.1).scale(.6)
        self.wavelet_legend = Text("Wavelet function", color=GREEN).next_to(self.scale_legend, DOWN, buff=.1).scale(.6)

    def setup(self):
        self.setup_real_part()
        self.setup_imag_part()
        self.setup_complex_plane()
        self.setup_titles()

    def create_with_dot(self, curves, text=None, rate_func=smooth, run_time=20):
        dots = VGroup()
        for i, curve in enumerate(curves):
            dot = Dot(curve.get_start(), color=curve.get_color())
            f_always(dot.move_to, curve.get_end).suspend_updating()
            dots.add(dot)
        if text is not None:
            self.play(FadeIn(*dots), Write(text))
        else:
            self.play(FadeIn(*dots))
        dots.resume_updating()
        self.play(Create(VGroup(*curves), lag_ratio=0), run_time=run_time-2, rate_func=rate_func)
        self.play(FadeOut(*dots))

    def separated_graphs(self):
        self.play(Create(self.axes_real), Create(self.axes_imag), Write(self.title), run_time=2)
        self.create_with_dot([self.scale_func_graph_real, self.scale_func_graph_imag],
                             text=self.scale_legend, run_time=14)
        self.create_with_dot([self.wavelet_func_graph_real, self.wavelet_func_graph_imag],
                             text=self.wavelet_legend, run_time=14)

    def transition(self):
        self.title.target = self.title.copy().scale(.7).to_corner(UR)
        self.play(
            VGroup(self.axes_real, self.scale_func_graph_real, self.wavelet_func_graph_real).animate.scale(.65).to_corner(UL),
            VGroup(self.axes_imag, self.scale_func_graph_imag, self.wavelet_func_graph_imag).animate.scale(.65).to_corner(DL),
            # FadeOut(VGroup(self.scale_legend, self.wavelet_legend)),
            MoveToTarget(self.title),
            VGroup(self.scale_legend, self.wavelet_legend).animate.scale(.8).arrange(RIGHT).next_to(self.title.target, DOWN, buff=.1)
        )
        self.play(VGroup(self.scale_func_graph_real, self.scale_func_graph_imag,
                  self.wavelet_func_graph_real, self.wavelet_func_graph_imag).animate.set_stroke(opacity=.5))

    def combined_graphs(self):
        self.play(Create(self.complex_axes), run_time=2)

        scale_func_real_copy = self.scale_func_graph_real.copy().set_stroke(opacity=1)
        scale_func_imag_copy = self.scale_func_graph_imag.copy().set_stroke(opacity=1)
        self.create_with_dot([scale_func_real_copy, scale_func_imag_copy, self.scale_func],
                             rate_func=linear, run_time=30)
        self.play(FadeOut(scale_func_real_copy, scale_func_imag_copy))

        wavelet_func_real_copy = self.wavelet_func_graph_real.copy().set_stroke(opacity=1)
        wavelet_func_imag_copy = self.wavelet_func_graph_imag.copy().set_stroke(opacity=1)
        self.create_with_dot([wavelet_func_real_copy, wavelet_func_imag_copy, self.wavelet_func],
                             rate_func=linear, run_time=30)
        self.play(FadeOut(wavelet_func_real_copy, wavelet_func_imag_copy),
                  VGroup(self.scale_func_graph_real, self.scale_func_graph_imag,
                         self.wavelet_func_graph_real, self.wavelet_func_graph_imag).animate.set_stroke(opacity=1))

    def construct(self):
        self.separated_graphs()
        self.wait()
        self.transition()
        self.wait()
        self.combined_graphs()
        self.wait(10)
