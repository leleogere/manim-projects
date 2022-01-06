from typing import Callable, Sequence, Union, Iterable

from colour import Color

from manim import *

from manim.mobject.opengl_compatibility import ConvertToOpenGL
from manim.utils.deprecation import deprecated_params





R = np.linspace(0, 1, 50)
T = np.linspace(0, 2*np.pi, 50)
rr, tt = np.meshgrid(R, T)


def f(r, t):
    return np.cos(t)

def f2(x, y):
    return f(np.sqrt(x**2 + y**2), np.arctan(np.divide(y,x)))


class Surface2(VGroup, metaclass=ConvertToOpenGL):
    @deprecated_params(
        params="u_min,u_max,v_min,v_max",
        since="v0.9.0",
        until="v0.10.0",
        message="Use u_range and v_range instead.",
    )
    def __init__(
        self,
        func: Callable[[float, float], np.ndarray] = None,
        u_range: Sequence[float] = [0, 1],
        v_range: Sequence[float] = [0, 1],
        resolution: Sequence[int] = 32,
        surface_piece_config: dict = {},
        fill_color: "Color" = BLUE_D,
        fill_opacity: float = 1.0,
        checkerboard_colors: Sequence["Color"] = [BLUE_D, BLUE_E],
        stroke_color: "Color" = LIGHT_GREY,
        stroke_width: float = 0.5,
        should_make_jagged: bool = False,
        pre_function_handle_to_anchor_scale_factor: float = 0.00001,
        **kwargs
    ) -> None:
        self.u_min = kwargs.pop("u_min", None) or u_range[0]
        self.u_max = kwargs.pop("u_max", None) or u_range[1]
        self.v_min = kwargs.pop("v_min", None) or v_range[0]
        self.v_max = kwargs.pop("v_max", None) or v_range[1]
        super().__init__(**kwargs)
        self.resolution = resolution
        self.surface_piece_config = surface_piece_config
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.checkerboard_colors = checkerboard_colors
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.should_make_jagged = should_make_jagged
        self.pre_function_handle_to_anchor_scale_factor = (
            pre_function_handle_to_anchor_scale_factor
        )
        self.func = func
        self.setup_in_uv_space()
        #self.apply_function(lambda p: func(p[0], p[1]))
        #if self.should_make_jagged:
        #    self.make_jagged()

    def setup_in_uv_space(self):
        r_values, t_values = R, T
        faces = VGroup()
        for i in range(len(r_values) - 1):
            for j in range(len(t_values) - 1):
                r1, r2 = r_values[i: i + 2]
                t1, t2 = t_values[j: j + 2]
                u1, u2 = r1*np.cos(t1), r2*np.cos(t2)
                v1, v2 = r1*np.sin(t1), r2*np.sin(t2)
                face = ThreeDVMobject()
                face.set_points_as_corners(
                    [
                        [u1, v1, f(r1, t1)],
                        [u2, v1, f(r2, t1)],
                        [u2, v2, f(r2, t2)],
                        [u1, v2, f(r1, t2)],
                        [u1, v1, f(r1, t1)],
                    ]
                )
                faces.add(face)
                face.u_index = i
                face.v_index = j
                face.u1 = u1
                face.u2 = u2
                face.v1 = v1
                face.v2 = v2
        faces.set_fill(color=self.fill_color, opacity=self.fill_opacity)
        faces.set_stroke(
            color=self.stroke_color,
            width=self.stroke_width,
            opacity=self.stroke_opacity,
        )
        self.add(*faces)
        if self.checkerboard_colors:
            self.set_fill_by_checkerboard(*self.checkerboard_colors)

    def set_fill_by_checkerboard(self, *colors, opacity=None):
        n_colors = len(colors)
        for face in self:
            c_index = (face.u_index + face.v_index) % n_colors
            face.set_fill(colors[c_index], opacity=opacity)
        return self



class SurfaceFromMesh(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        s = Surface2()
        self.set_camera_orientation(phi = 75 * DEGREES, theta = 45 * DEGREES)
        self.add(axes, s)
        self.interactive_embed()
