import numpy as np
from manim import *




class HeatEq(Scene):
    def construct(self):
        N = 100
        alpha = 5
        valeur_derivee_au_bord = 0

        def T_init(x):
            if x <= 0.5:
                return 1
            else:
                return -1

        axes = Axes(x_range=[0, 1, 0.25], y_range=[-1, 1, 0.5], x_length=5, y_length=5).scale(0.9).shift(2.5 * RIGHT)
        labels = VGroup(MathTex("x").next_to(axes[0].get_end(), DOWN), MathTex("T").next_to(axes[1].get_end(), LEFT))

        t = ValueTracker(0)

        x_values = np.linspace(0, 1, N + 1)

        curve_init = axes.get_graph(T_init, x_range=[0, 1], discontinuities=[0.5], color=YELLOW)

        title = Tex('\\underline{Equation de la chaleur en 1 dimension}').to_edge(UP)
        heat_eq = MathTex('\\frac{\\partial T}{\\partial t} - \\alpha \\frac{\partial^2 T}{\\partial x^2} = 0').to_edge(LEFT, buff=1.5).shift(0.3 * DOWN)
        box_heat_eq = SurroundingRectangle(heat_eq, buff=0.15)

        rod_1, rod_2 = Rectangle(color=PURE_RED, width=0.9 * 2.5, height=0.4, fill_opacity=1, stroke_opacity=0), Rectangle(color=PURE_BLUE, width=0.9 * 2.5, height=0.4, fill_opacity=1, stroke_opacity=0)
        rod_1.next_to(axes.c2p(0.2, 0), DOWN).shift(2.25 * DOWN)
        rod_2.next_to(axes.c2p(0.8, 0), DOWN).shift(2.25 * DOWN)

        self.add(title, axes, labels)
        self.wait(0.5)
        self.play(Write(heat_eq), run_time=2)
        self.play(Create(box_heat_eq))
        self.wait(0.25)
        self.play(Create(VGroup(rod_1, rod_2)), run_time=1.5)
        self.play(Create(curve_init))
        self.wait(0.5)

        curve = always_redraw(lambda: axes.get_line_graph(x_values, self.get_temp_list(N, alpha, T_init, t.get_value(), valeur_derivee_au_bord),
                                        line_color=YELLOW, add_vertex_dots=False)
        )

        rod = Rectangle(color=WHITE, width=5 * 0.9, height=0.4, fill_opacity=1, stroke_opacity=0, sheen_direction=RIGHT).next_to(axes.c2p(0.5, 0), DOWN).shift(2.25 * DOWN)
        rod.set(tmin=None, tmax=None)   # AJOUT

        def update_rod(mob):
            temp_list_bis = self.get_temp_list(N, alpha, T_init, t.get_value(), valeur_derivee_au_bord)
            if mob.tmin is None:  # AJOUT : necessaire pour pas recalculer le tmin/max a chaque fois pour avoir une couleur qui varie
                mob.tmin = temp_list_bis.min()
                mob.tmax = temp_list_bis.max()
            temp_list_normalized = (temp_list_bis - mob.tmin) / (mob.tmax - mob.tmin)
            colors = [interpolate_color(PURE_BLUE, PURE_RED, np.clip(alpha, 0, 1)) for alpha in temp_list_normalized]  # AJOUT : clip au cas ou on depasse 1
            mob.set_color(colors)

        rod.add_updater(update_rod)

        self.play(
            rod_1.animate.next_to(axes.c2p(0.25, 0), DOWN).shift(2.25 * DOWN),
            rod_2.animate.next_to(axes.c2p(0.75, 0), DOWN).shift(2.25 * DOWN),
            run_time=1.5
        )

        self.add(rod)
        self.remove(rod_1, rod_2)
        self.add(curve)
        self.remove(curve_init)

        self.play(t.animate.set_value(6), run_time=12, rate_func=linear)
        self.wait(0.5)



    def get_temp_list(self, N, alpha, T_init, n, valeur_derivee_au_bord):
        x = np.linspace(0, 1, N + 1)
        t = np.linspace(0, 1, N + 1)

        dx = x[1] - x[0]
        dt = t[1] - t[0]

        l = alpha * dt / dx ** 2

        T_0 = np.array([T_init(x) for x in x])

        A = (1 + 2 * l) * np.eye(N + 1)

        A[0, :2] = [1, valeur_derivee_au_bord]  # AJOUT : on impose une derivee aux bords
        A[N, N-1:] = [1, valeur_derivee_au_bord]

        for i in range(N - 1):
            A[i + 1, i] = -l
            A[i + 1, i + 2] = -l

        P = np.linalg.eig(A)[1]
        D = np.diag(np.linalg.eig(A)[0])

        def A_power_n(m):
            if m == 0:
                return np.eye(N + 1)
            elif m > 0:
                return np.dot(P, np.dot(D ** (m), np.linalg.inv(P)))
            elif m < 0:
                return np.dot(P, np.dot(np.linalg.inv(D) ** (-m), np.linalg.inv(P)))

        return np.dot(A_power_n(-n), T_0)
