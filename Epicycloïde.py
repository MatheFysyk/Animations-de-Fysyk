from manim import *
from scipy.fft import fft


class Cycle(VMobject):
    def __init__(
            self,
            radius,
            angle=0,
            **kwargs
        ):
        VMobject.__init__(self, **kwargs)
        circle = Circle(radius=radius, color=YELLOW, **kwargs)
        arrow = Arrow(ORIGIN, radius * RIGHT, buff=0, color=WHITE, **kwargs)
        self.add(circle, arrow)
        self.rotate(angle)
        self.circle = circle
        self.arrow = arrow
        
        
        
class EpicycloidSVG(Scene):
    def construct(self):
        svg = SVGMobject('chemin_de_votre_fichier_svg').set_color(WHITE)
        path = self.get_path(svg)

        amplitudes, velocities, phases = self.get_Fourier_coef(path=path, num_points=750)
        origin_object = Cycle(radius=0, stroke_opacity=0.4).move_to(ORIGIN)
        epicycles = VGroup(origin_object)

        for (i, (r, a, s)) in enumerate(zip(amplitudes, phases, velocities)):
            cycle = Cycle(r, a, stroke_opacity=0.4)
            cycle.add_updater(lambda mob, dt, i=i, s=s: mob.rotate(s * dt).move_to(epicycles[i].arrow.get_end()))
            epicycles.add(cycle)

        traced_path = TracedPath(epicycles[-1].arrow.get_end, stroke_width=1.5, dissipating_time=None)
        self.add(epicycles, traced_path)
        self.wait(18)


    def get_Fourier_coef(self, path: list, num_points: int=50, speed_factor: float=0.5) -> tuple[np.ndarray]:
        """Computes the Fourier coefficients of the `path` to draw the circles and arrows."""
        alpha_list = np.linspace(0, 1, num_points)
        points = np.array([R3_to_complex(p) for p in [path.point_from_proportion(alpha) for alpha in alpha_list]])
        fft_array = fft(points)/num_points

        velocities_bis = np.array([(-1)**i * int(i/2) for i in range(1, num_points + 1)])
        amplitudes = np.abs(fft_array)[velocities_bis]
        phases = np.angle(fft_array)[velocities_bis]
        velocities = np.array([speed_factor * (-1)**i * int(i/2) for i in range(1, num_points + 1)])

        return amplitudes, velocities, phases


    def get_path(self, mobject: VMobject) -> list:
        """Returns the list of points forming the `VMobject`."""
        return mobject.family_members_with_points()[0]
