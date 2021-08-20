from manim import *
from wavelet_mobject_epicycles import WaveletEpicyclesMobject


########################################################################################################################


class WaveletScene(Scene):
    def set_params(self, tex=r"$\Sigma$", N=512, K=6, L=None, speed_factor=1., show_build=True, show_background=False, duration=20):
        def get_shape(tex):
            path = VMobject()
            shape = Tex(tex)
            for sp in shape.family_members_with_points():
                path.append_points(sp.get_points())
            return path

        path = get_shape(tex).scale(15)
        hn = np.zeros(6, dtype=complex)
        hn[0] = hn[-1] = -(3 + np.sqrt(15) * 1j) / 64 * np.sqrt(2)
        hn[1] = hn[-2] = (5 - np.sqrt(15) * 1j) / 64 * np.sqrt(2)
        hn[2] = hn[-3] = (15 + np.sqrt(15) * 1j) / 32 * np.sqrt(2)
        self.wait_duration = duration
        self.ec_config = {"mobject": path,
                          "hn": hn,
                          "N": N,
                          "K": K,
                          "L": L,
                          "speed_factor": speed_factor,
                          "show_build": show_build,
                          "show_background": show_background}

    def construct(self):
        ec = WaveletEpicyclesMobject(**self.ec_config)
        self.add(ec)
        self.wait(self.wait_duration)


class WaveletSceneSlowFull(WaveletScene):
    def construct(self):
        self.set_params(speed_factor=.05, duration=20)
        super().construct()


class WaveletSceneSlowVectors(WaveletScene):
    def construct(self):
        self.set_params(speed_factor=.05, show_build=False, duration=40)
        super().construct()


class WaveletSceneMediumVectors(WaveletScene):
    def construct(self):
        self.set_params(speed_factor=.1, show_build=False, duration=40)
        super().construct()


class WaveletSceneNormalVectors(WaveletScene):
    def construct(self):
        self.set_params(speed_factor=.5, show_build=False, duration=40)
        super().construct()


class WaveletSceneCreation(WaveletScene):
    def construct(self):
        self.set_params()
        ec = WaveletEpicyclesMobject(**self.ec_config).suspend_updating()
        self.play(Write(ec), run_time=20)
