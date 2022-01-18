from manim import *
from scipy.integrate import odeint
import random as rd



sigma, beta, rho = 10, 8/3, 28
t_max = 1000
t = np.linspace(0, t_max+1, 10**5)

class AttracteurDeLorenz(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES + 15.5*0.05)
        self.begin_ambient_camera_rotation(rate=0.075)
        axes = ThreeDAxes(x_range=[-8, 8], y_range=[-8, 8], z_range=[-6, 6], color=GREY)

        X_0 = np.array([0.1, 0.1, 0.1])

        X = self.solve_diff_sys(X_0)
        x, y, z = X[:, 0], X[:, 1], X[:, 2]
        lorenz_attractor = axes.get_line_graph(x, y, z, line_color=YELLOW, add_vertex_dots=False, stroke_width=0.1).move_to(ORIGIN).scale(0.25)
        
        #self.add(lorenz_attractor)
        self.wait(0.5)
        self.play(Create(lorenz_attractor), run_time=10)
        self.wait(30)


    def solve_diff_sys(self, init_condition):
        def diff_sys(X, t):
            x, y, z = X
            return np.array([sigma*(y-x), rho*x - y - x*z, x*y - beta*z])

        X = odeint(diff_sys, init_condition, t)
        return X
