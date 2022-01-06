from manim import *


class Test(Scene):
    def construct(self):
            N = 50
            axes = PolarPlane(radius_max=1, size=5)
            disc = Circle(2.5)
            self.add(axes, disc)
            
     
            r = np.linspace(0, 1, N)
            t = np.linspace(0, 2*np.pi, 3*N)

            polygons = VGroup()

            for i in range(len(r) - 1):
                for j in range(len(t) - 1):
                    r1, r2 = r[i: i + 2]
                    t1, t2 = t[j: j + 2]
                    c = [RED,BLUE,GREEN,WHITE][np.random.randint(4)]
                    polygon = Polygon(
                        axes.polar_to_point(r1, t1),
                        axes.polar_to_point(r2, t1),
                        axes.polar_to_point(r2, t2),
                        axes.polar_to_point(r1, t2),
                        fill_color=c,
                        stroke_color=c,
                        fill_opacity=1,
                        stroke_opacity=1
                    )
                    polygons.add(polygon)

            self.add(polygons)

            def f(r, t):
                return np.sin(r*10)*np.cos(2*t)

            f_values = np.array([f(*axes.point_to_polar(p.get_center())[:2]) for p in polygons])
            f_normalised = (f_values - f_values.min()) / (f_values.max() - f_values.min())
            for p, alpha in zip(polygons, f_normalised):
                p.set_color(interpolate_color(RED, BLUE, alpha))
