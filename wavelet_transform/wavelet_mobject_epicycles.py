from manim import *
from wavelet_helpers import *


########################################################################################################################


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
            show_background=True,
            cycles_colors=[RED, BLUE, PINK, GREEN],
            cycles_config={"stroke_width": 2, "stroke_opacity": .8},
            vectors_config={"stroke_width": 4, "stroke_opacity": 1},
            background_config={"stroke_color": GRAY_C, "stroke_width": 1, "stroke_opacity": 1, "fill_opacity": 0},
            trail_config={"stroke_color": YELLOW, "stroke_width": 4, "stroke_opacity": 1},
            **kwargs):
        super().__init__(**kwargs)
        self.mobject = mobject.copy()
        self.hn = hn
        self.N = int(2 ** np.round(np.log(N) / np.log(2)))
        self.complex_points = [R3_to_complex(self.mobject.point_from_proportion(alpha)) for alpha in
                               np.arange(0, 1, 1 / self.N)]
        self.K = K if K is not None else self.N
        self.L = pywt.dwt_max_level(self.N, len(self.hn)) if L is None else min(L, pywt.dwt_max_level(self.N,
                                                                                                      len(self.hn)))
        self.show_build = show_build
        self.speed_factor = .1 * speed_factor
        self.cycles = VGroup()
        self.vectors = VGroup()
        if show_background:
            self._init_background(background_config)
        self._init_epicycles(cycles_colors, cycles_config, vectors_config)
        self._init_trail(trail_config)

    def _init_background(self, background_config):
        self.background = self.mobject.copy().set_style(**background_config)
        self.add(self.background)

    def _init_epicycles(self, cycles_colors, cycles_config, vectors_config):
        # compute the wavelet transform
        WT = wvt(self.complex_points, self.hn, self.L)
        self.cycle_points = []
        self.colors = []
        for l in range(0, min(self.K, self.L + 1)):
            print("L =", l)
            func = scale_function_complex if l == 0 else wavelet_function_complex  # scaling function in the first loop, wavelet function after
            self.cycle_points += [  # interpolate complex points to minimize the number of computations (one per frame)
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
                c["curve"].set_stroke(opacity=opacity_function(abs(new_f), 1, cycles_config["stroke_opacity"]))
            return c

        # create all epicycles
        temp = VDict([("vect", Dot(radius=0))])
        self.epicycles = VGroup(temp)
        for i, function in enumerate(self.cycle_points):
            current_cycle = VDict()
            current_cycle["vect"] = Line(color=WHITE if self.show_build else self.colors[i], **vectors_config)
            self.vectors.add(current_cycle["vect"])
            if self.show_build:
                current_cycle["curve"] = VMobject(color=self.colors[i], **cycles_config).set_points_as_corners(
                    [complex_to_R3(x) for x in function] + [complex_to_R3(function[0])])
                current_cycle.set(center_offset=current_cycle["curve"].get_center())
                self.cycles.add(current_cycle["curve"])
            current_cycle.set(previous_cycle=self.epicycles[i]["vect"].get_end,
                              function=function,
                              current=0)
            current_cycle.add_updater(lambda c, dt: update_cycle(c))
            self.epicycles.add(current_cycle)
        self.epicycles.update(.00001)  # first update to move all to the right place
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
