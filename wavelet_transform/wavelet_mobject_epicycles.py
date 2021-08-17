from manim import *
from wavelet_helpers import *


class WaveletEpicyclesMobject(VMobject):

    def __init__(
            self,
            mobject: "Mobject",
            hn,
            N,
            K=None,
            L=None,
            speed_factor=.1,
            show_build=False,
            cycles_colors=[RED, BLUE, PINK, GREEN],
            cycles_config={"stroke_width": 2, "stroke_opacity": 1},
            vectors_config={"stroke_width": 4, "stroke_opacity": 1},
            background_config={"color": GRAY_C, "stroke_width": 1, "stroke_opacity": 1},
            trail_config={"stroke_color": YELLOW, "stroke_width": 4, "stroke_opacity": 1},
            **kwargs):
        super().__init__(**kwargs)
        self.mobject = mobject.copy()
        self.hn = hn
        self.N = int(2 ** np.round(np.log(N) / np.log(2)))
        self.complex_points = [R3_to_complex(self.mobject.point_from_proportion(alpha)) for alpha in np.arange(0, 1, 1/self.N)]
        self.K = K if K is not None else self.N
        self.L = pywt.dwt_max_level(self.N, len(self.hn)) if L is None else min(L, pywt.dwt_max_level(self.N, len(self.hn)))
        self.show_build = show_build
        self.speed_factor = speed_factor
        self.cycles = VGroup()
        self.vectors = VGroup()
        self._init_background(background_config)
        self._init_epicycles(cycles_colors, cycles_config, vectors_config)
        self._init_trail(trail_config)

    def _init_background(self, background_config):
        self.background = VMobject(**background_config).set_points_as_corners(self.mobject.get_all_points())
        self.add(self.background)

    def _init_epicycles(self, cycles_colors, cycles_config, vectors_config):
        # compute the wavelet transform
        WT = wvt(self.complex_points, self.hn, self.L)
        self.cycle_points = []
        self.colors = []
        for l in range(0, min(self.K, self.L + 1)):
            print("L =", l)
            func = scale_function_complex if l == 0 else wavelet_function_complex  # scaling function in the first loop, wavelet function after
            self.cycle_points += [   # interpolate complex points to minimize the number of computations (one per frame)
                np.interp(
                    np.arange(0, 1, self.speed_factor / config.frame_rate),
                    np.linspace(0, 1, self.N, endpoint=False),
                    WT[l][i] * np.conj(func(self.hn, self.N, self.L - max(l, 1) + 1, k)),
                ) for i, k in enumerate(np.arange(0, 1, 1 / len(WT[l])))
            ]
            self.colors += [cycles_colors[l % len(cycles_colors)]] * len(WT[l])

        # function making invisible path of functions too close to zero (to declutter the scene)
        def opacity_function(x, xmax, opacity_max=1.):
            return (np.sqrt(1 - np.power(x / xmax - 1, 4)) if x < xmax else 1) * opacity_max

        # convert a complex point to R3 (setting it to zero if too small)
        def to_point(z, tol=1e-5):
            a = 0 if np.isclose(z, 0, atol=tol) else z
            return complex_to_R3(a)

        # update a cycle according to the previous cycle and to the points saved earlier
        def update_cycle(c):
            c.current = (c.current + 1) % len(c.function)
            new_f = c.function[c.current]
            start_vect = c.previous_cycle()
            end_vect = start_vect + to_point(new_f, tol=1e-3)
            c["vect"].become(Line(start_vect, end_vect).match_style(c["vect"]))
            if self.show_build:
                c["curve"].move_to(c.center_offset + c.previous_cycle())
                c["curve"].set_stroke(opacity=opacity_function(abs(new_f), 1, .6))
            return c

        # create all epicycles
        temp = VDict([("vect", Dot(radius=0))])
        self.epicycles = VGroup(temp)
        for i, function in enumerate(self.cycle_points):
            current_cycle = VDict()
            current_cycle["vect"] = Line(color=WHITE if self.show_build else self.colors[i], **vectors_config)
            self.vectors.add(current_cycle["vect"])
            if self.show_build:
                current_cycle["curve"] = VMobject(color=self.colors[i], **cycles_config).set_points_as_corners([complex_to_R3(x) for x in function])
                current_cycle.set(center_offset=current_cycle["curve"].get_center())
                self.cycles.add(current_cycle["curve"])
            current_cycle.set(previous_cycle=self.epicycles[i]["vect"].get_end,
                              function=function,
                              current=0)
            current_cycle.add_updater(lambda c, dt: update_cycle(c))
            self.epicycles.add(current_cycle)
        self.add(self.epicycles)

    def _init_trail(self, trail_config):
        self.trace = TracedPath(self.epicycles[-1]["vect"].get_end, min_distance_to_new_point=.01,
                                **trail_config)
        self.add(self.trace)

    def get_epicycles(self):
        return self.epicycles

    def get_cycles(self):
        return self.cycles

    def get_vectors(self):
        return self.vectors

    def get_trace(self):
        return self.trace

    def get_bg(self):
        return self.path


class TestWavelet(Scene):
    def construct(self):

        # get an array of complex points
        N = 50
        # tex = "$\Sigma$"
        tex = "§"
        def get_shape(tex):
            path = VMobject()
            shape = Tex(tex)
            for sp in shape.family_members_with_points():
                path.append_points(sp.get_points())
            return path
        path = get_shape(tex).scale(12)

        # create my epicycles
        hn = np.zeros(6, dtype=complex)
        hn[0] = hn[-1] = -(3 + np.sqrt(15) * 1j) / 64 * np.sqrt(2)
        hn[1] = hn[-2] = (5 - np.sqrt(15) * 1j) / 64 * np.sqrt(2)
        hn[2] = hn[-3] = (15 + np.sqrt(15) * 1j) / 32 * np.sqrt(2)
        ec = WaveletEpicyclesMobject(path, hn, N=1000, K=None, L=None, speed_factor=.05,
                                     show_build=True)
        # self.play(Write(ec))
        # self.add(path)
        self.add(ec)
        self.wait(10)
        # speed = .8
        # ec.add_updater(lambda e, dt: e.set(speed_factor=np.clip(e.speed_factor+speed*dt, 0, 2)))
        # self.wait(3*TAU)
        # speed = -.2
        # self.wait(2*TAU)


class TestWaveletZoomed(ZoomedScene):
    def __init__(self, **kwargs):
        super().__init__(
            zoom_factor=.3,
            zoomed_display_height=1,
            zoomed_display_width=6,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
                },
            **kwargs
        )

    def construct(self):
        tex = "§"

        def get_shape(tex):
            path = VMobject()
            shape = Tex(tex)
            for sp in shape.family_members_with_points():
                path.append_points(sp.get_points())
            return path

        path = get_shape(tex).scale(12)

        # create my epicycles
        hn = np.zeros(6, dtype=complex)
        hn[0] = hn[-1] = -(3 + np.sqrt(15) * 1j) / 64 * np.sqrt(2)
        hn[1] = hn[-2] = (5 - np.sqrt(15) * 1j) / 64 * np.sqrt(2)
        hn[2] = hn[-3] = (15 + np.sqrt(15) * 1j) / 32 * np.sqrt(2)
        ec = WaveletEpicyclesMobject(path, hn, N=1000, K=2, L=None, speed_factor=.05,
                                     show_build=True)
        self.add(ec)
        self.wait(2)

        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame
        frame.move_to(ec.get_vectors()[-1]).add_updater(lambda f, dt: f.move_to(ec.get_vectors()[-1]))
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)
        self.play(Create(frame))
        self.activate_zooming()

        self.wait(2)
