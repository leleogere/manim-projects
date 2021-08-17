from manim import *
from svg.path import parse_path


class WaveletEpicycles(Scene):
    """Scene creating an approximation of a periodic function using the wavelet transform.

    Parameters
    ----------
    N : int
      Number of points to use along the curve to compute the fft
    K : int
      Number of epicycles used to approximate the function (1<=K<=N)
    tex_symbol : str, override svg_path if set
      A tex symbol to approximate (should be surrounded by '$')
    svg_path : str, useless if tex_symbol is set
      A svg path to approximate
    show_shape : bool
      Boolean indicating if the shape to approximate must be drawn behind the epicycles
    duration : int
      Duration of the animation after starting animating the epicycles
    speed_factor : float
      Speed of the animation (higher value will result in epicycles rotating faster)

    Notes
    -----
    Either tex_symbol or svg_path must be set or it will raise an error. If both of them
    are set, tex_symbol will override svg_path.
    """

    def set_params(self, N, K, tex_symbol=None, svg_path=None, show_shape=True, duration=30, speed_factor=.1):
        self.N = N
        self.K = K
        self.tex = tex_symbol
        self.svg_path = svg_path
        self.show_shape = show_shape
        self.anim_duration = duration
        self.speed_factor = speed_factor * N


    def setup(self):
        if self.tex_symbol is not None:
            path = self.get_shape()
            self.complex_points = normalize(
            np.array([complex(*path.point_from_proportion(alpha)[:2]) for alpha in np.arange(0, 1, 1 / N)]))
        elif self.svg_path is not None:
            path = parse_path(self.svg_path)
            self.complex_points = np.array([np.conj(path.point(alpha)) for alpha in np.arange(0, 1, 1 / N)])
        else:
            raise Exception("Not defined symbol")
        self.normalize()
        points = np.array([[p.real, p.imag, 0] for p in self.complex_points])
        self.path = VMobject(stroke_color=GRAY_C, stroke_width=1).set_points_as_corners([points[-1], *points])
        self.fft = np.fft.fft(self.complex_points) / self.N
        self.epicycles = self.create_all_epicycles().suspend_updating()
        self.trace = TracedPath(self.epicycles[-1][-1].get_end, min_distance_to_new_point=.01,
                                stroke_color=YELLOW, stroke_width=4)

    # function to get a path from a tex symbol
    def get_shape(self):
        path = VMobject()
        shape = Tex(self.tex)
        for sp in shape.family_members_with_points():
            path.append_points(sp.get_points())
        return path

    # function to normalize an array of complex numbers
    def normalize(self, factor=4):
        offset = self.complex_points.mean()
        centered = self.complex_points - offset
        normalization = np.max(np.abs(centered))
        self.complex_points = centered / normalization * factor

    # function to create all epicycles
    def create_all_epicycles(self):
        # function to create an epicycle (circle + vector)
        def create_epicycle(radius, angle):
            circle = Circle(radius=radius, stroke_color=RED, stroke_width=1)
            arrow = Vector(circle.get_right())
            epicycle = VGroup(circle, arrow).rotate(angle)
            return epicycle

        temp = Dot(radius=0)
        epicycles = VGroup(temp)
        for i, k in enumerate([int(i / 2) * (-1) ** i for i in range(1, self.K + 1)]):
            epicycle = create_epicycle(radius=abs(self.fft[k]), angle=np.angle(self.fft[k]))
            epicycle.set(previous=epicycles[i][-1])
            epicycle.set(speed=TAU * k / self.N)
            epicycle.move_to(epicycle.previous.get_end())
            epicycle.add_updater(lambda e, dt: e.move_to(e.previous.get_end()).rotate(e.speed * dt * self.speed_factor))
            epicycles.add(epicycle)
        return epicycles

    # play the animation
    def construct(self):
        if self.show_shape:
            self.play(FadeIn(self.path))
            self.wait()
        self.play(FadeIn(self.epicycles))
        self.add(self.trace)
        self.wait(2)
        self.epicycles.resume_updating()
        self.wait(self.anim_duration)


def V_coeffs(signal, hn):
    N = len(hn)
    coeffs = []
    for i in range(0, len(signal), 2):
        c = np.dot(hn, np.roll(signal, -i)[:N])
        coeffs.append(c)
    return np.array(coeffs)


# calcule les coefficients dans l'espace de détail
def W_coeffs(signal, hn):
    N = len(hn)
    gn = [(-1) ** n * np.conj(hn[N - 1 - n]) for n in range(N)]
    return V_coeffs(signal, gn)


# réalise la récomposition en ondelettes de niveau L
# /!\ retourne une liste de listes:
# [np.array(V0...), np.array(W0...), np.array(W1), ...]
def wvt(signal, hn, L=1):
    if L == 0 or len(signal) < len(hn):
        return [signal]
    else:
        Vn = V_coeffs(signal, hn)
        Wn = W_coeffs(signal, hn)
        return wvt(Vn, hn, L - 1) + [Wn]


def coefs_to_array(w):
    return np.array([i for a in w for i in a]), list(map(len, w))


# reforme une liste de coefficients à partir d'une vecteur et de la shape
# (comme pywt.array_to_coeffs)
def array_to_coefs(arr, shapes):
    coefs = []
    start = 0
    for s in shapes:
        coefs.append(np.array(arr[start:start + s]))
        start += s
    return coefs


# réalise la transformée inverse
def iwvt(coefs, hn):
    if len(coefs) > 2:
        Vn = iwvt(coefs[:-1], hn)
    else:
        Vn = coefs[0]
    Wn = coefs[-1]
    N = len(hn)
    M = len(Vn)
    gn = [(-1) ** n * np.conj(hn[N - 1 - n]) for n in range(N)]
    Vn2 = np.zeros(2 * M, dtype=type(hn[0]))
    Wn2 = np.zeros(2 * M, dtype=type(hn[0]))
    for i in range(0, M):
        for j in range(N):
            index_in_rec = 2 * i + j
            Vn2[index_in_rec % (2 * M)] += Vn[i] * hn[j]
            Wn2[index_in_rec % (2 * M)] += Wn[i] * gn[j]
    return Vn2 + Wn2


class WaveletEpicycles(Scene):
    """Scene using complex wavelet to approximate a complex function.

    Parameters
    ----------
    N : int
      Proportional to the number of points to use along the curve to compute the
      decomposition (will be get_coomultiplied by frame_rate for time consistency, and
      rounded to closest power of two for the wavelet transform)
    K : int
      Number of spaces to keep for the representation (K=4 -> V0+W0+W1+W2 if L=Lmax)
    L : int
      Number indicating the depth of the wavelet transform (the maximum if not set)
    tex_symbol : str, override svg_path if set
      A tex symbol to approximate (should be surrounded by '$')
    svg_path : str, useless if tex_symbol is set
      A svg path to approximate
    show_shape : bool
      Boolean indicating if the shape to approximate must be drawn behind the epicycles
    show_build : bool
      Boolean indicating if the build cycles should be drawn (increases significantly
      computation time)
    duration : int
      Duration of the animation after starting animating the epicycles

    Notes
    -----
    Either tex_symbol or svg_path must be set or it will raise an error. If both of them
    are set, tex_symbol will override svg_path.
    """

    def __init__(self, N, K, L=None, tex_symbol=None, svg_path=None, show_shape=True, show_build=False, duration=30,
                 **kwargs):
        # create the complex hn filter
        self.hn = np.zeros(6, dtype=complex)
        self.hn[0] = self.hn[-1] = -(3 + np.sqrt(15) * 1j) / 64 * np.sqrt(2)
        self.hn[1] = self.hn[-2] = (5 - np.sqrt(15) * 1j) / 64 * np.sqrt(2)
        self.hn[2] = self.hn[-3] = (15 + np.sqrt(15) * 1j) / 32 * np.sqrt(2)
        # initialize variables
        self.N = int(2 ** np.round(np.log(N * config.frame_rate) / np.log(2)))  # round to closer power of 2
        self.K = K
        self.L = pywt.dwt_max_level(self.N, len(self.hn)) if L is None else min(L, pywt.dwt_max_level(self.N,
                                                                                                      len(self.hn)))
        self.show_shape = show_shape
        self.show_build = show_build
        self.anim_duration = duration
        # get points from a tex symbol or a svg path
        if tex_symbol is not None:
            self.tex = tex_symbol
            path = self.get_shape()
            self.complex_points = normalize(
                np.array([complex(*path.point_from_proportion(alpha)[:2]) for alpha in np.arange(0, 1, 1 / self.N)]))
        elif svg_path is not None:
            from svg.path import parse_path
            path = parse_path(svg_path)
            self.complex_points = np.array([np.conj(path.point(alpha)) for alpha in np.arange(0, 1, 1 / self.N)])
        else:
            raise Exception("Not defined symbol")
        # normalize points to fit on screen
        self.normalize()
        # create the path of shape
        if show_shape:
            points = np.array([complex_to_R3(p) for p in self.complex_points])
            self.path = VMobject(stroke_color=GRAY_C, stroke_width=1).set_points_as_corners([points[-1], *points])
        # compute the wavelet transform and get points for all subspaces (and associate different colors)
        colors_available = [RED, BLUE, PINK, GREEN]
        WT = wvt(self.complex_points, self.hn, self.L)
        self.cycle_points = [WT[0][i] * np.conj(self.get_phi(self.L, k)) for i, k in
                             enumerate(np.arange(0, 1, 1 / len(WT[0])))]
        self.colors = [colors_available[0]] * len(WT[0])
        for l in range(1, min(K, self.L + 1)):
            print("l =", l)
            self.cycle_points += [WT[l][i] * np.conj(self.get_psi(self.L - l + 1, k)) for i, k in
                                  enumerate(np.arange(0, 1, 1 / len(WT[l])))]
            self.colors += [colors_available[l % len(colors_available)]] * len(WT[l])
        self.construction = self.create_all_epicycles()
        self.trace = TracedPath(self.construction[-1]["vect"].get_end, min_distance_to_new_point=.01,
                                stroke_color=YELLOW, stroke_width=4)
        super().__init__(**kwargs)

    # function to get a path from a tex symbol
    def get_shape(self):
        path = VMobject()
        shape = Tex(self.tex)
        for sp in shape.family_members_with_points():
            path.append_points(sp.get_points())
        return path

    # function to normalize an array of complex numbers to fit on screen
    def normalize(self, factor=4):
        offset = self.complex_points.mean()
        centered = self.complex_points - offset
        normalization = np.max(np.abs(centered))
        self.complex_points = centered / normalization * factor

    # function to get scale function
    def get_phi(self, scale, pos):
        L = min(scale, self.L)
        Ne = int(np.floor(self.N / 2 ** L))
        k = int(np.floor(Ne * pos))
        temp = np.zeros(self.N)
        WT = wvt(temp, self.hn, L)
        arr, coeff_slices = coefs_to_array(WT)
        temp[k] = 1
        coeffs_from_arr = array_to_coefs(temp, coeff_slices)
        phi = iwvt(coeffs_from_arr, self.hn)
        return phi

    # function to get wavelet function
    def get_psi(self, scale, pos):
        L = min(scale, self.L)
        Ne = int(np.floor(self.N / 2 ** L))
        k = int(np.floor(Ne * pos))
        temp = np.zeros(self.N)
        WT = wvt(temp, self.hn, L)
        arr, coeff_slices = coefs_to_array(WT)
        temp[Ne + k] = 1
        coeffs_from_arr = array_to_coefs(temp, coeff_slices)
        psi = iwvt(coeffs_from_arr, self.hn)
        return psi

    # function to create all epicycles
    def create_all_epicycles(self):
        def opacity_function(x, xmax, opacity_max=1.):
            return (np.sqrt(1 - np.power(x / xmax - 1, 4)) if x < xmax else 1) * opacity_max

        def to_point(z, tol=1e-5):
            a = 0 if np.isclose(z, 0, atol=tol) else z
            return complex_to_R3(a)

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

        temp = VDict([("vect", Dot(radius=0))])
        wvtcycles = VGroup(temp)
        for i, f in enumerate(self.cycle_points):
            current_cycle = VDict()
            current_cycle["vect"] = Line(color=WHITE if self.show_build else self.colors[i], stroke_width=2)
            if self.show_build:
                current_cycle["curve"] = VMobject(color=self.colors[i], stroke_width=2).set_points_as_corners([complex_to_R3(x) for x in f])
                current_cycle.set(center_offset=current_cycle["curve"].get_center())
            current_cycle.set(previous_cycle=wvtcycles[i]["vect"].get_end,
                              function=f,
                              current=0)
            current_cycle.add_updater(lambda c, dt: update_cycle(c))
            wvtcycles.add(current_cycle)
        return wvtcycles

    # play the animation
    def construct(self):
        if self.show_shape:
            self.play(FadeIn(self.path))
            self.wait()
        self.add(self.construction, self.trace)
        self.wait(self.anim_duration)
