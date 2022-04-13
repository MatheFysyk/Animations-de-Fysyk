from manim import *


g = 2.5
m = 1
l = 1.5        
init_angle = 5*PI/6



class Pendulum(VMobject):
    def __init__(self,
        angle,
        angular_velocity,
        point: np.ndarray = ORIGIN,
        mass: float = 1,
        length: float = 1, 
        rod_color: str = YELLOW,
        end_mass_color: str = WHITE,
        end_mass_radius: float = DEFAULT_DOT_RADIUS,
        **kwargs
    ):
        super().__init__(self, **kwargs)
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.point = point
        self.mass = mass
        self.length = length
        self.rod = Line(point, point + length*DOWN, color=rod_color, **kwargs).rotate(angle, about_point=point)
        self.end_mass_radius = end_mass_radius
        self.end_mass = Dot(self.rod.get_end(), radius=self.end_mass_radius, color=end_mass_color, **kwargs).move_to(self.rod.get_end())
        self.add(self.rod, self.end_mass)
    
    def enable_angle_label(self, label: str = "\\theta") -> None:
        angle_radius = max(self.rod.get_length()/5, 0.4)
        dashed_line = always_redraw(lambda: DashedLine(self.rod.get_start(), self.rod.get_start() + self.length/2 * DOWN))
        angle_drawn = Angle(dashed_line, self.rod, radius=angle_radius)
        angle_label = MathTex(label)

        def updater_angle(angle):
            if self.angle > 0.01:
                if self.angle <= PI:
                    angle.become(Angle(dashed_line, self.rod, radius=angle.radius))
                else:
                    angle.become(Angle(dashed_line, self.rod, radius=angle.radius, other_angle=False))
            if np.abs(self.angle) <= 0.01:
                angle.become(Angle(dashed_line, self.rod, radius=angle.radius, color=BLACK))
            if self.angle < -0.01:
                if self.angle >= -PI:
                    angle.become(Angle(dashed_line, self.rod, radius=angle.radius, other_angle=True))
                else:
                    angle.become(Angle(dashed_line, self.rod, radius=angle.radius, other_angle=False))
            
        def updater_angle_label(label):
            if self.angle > 0.01:
                if self.angle <= PI:
                    label.move_to(Angle(dashed_line, self.rod, radius=angle_drawn.radius + 0.3).point_from_proportion(0.5))
                else:
                    label.move_to(Angle(dashed_line, self.rod, radius=angle_drawn.radius + 0.3, other_angle=True).point_from_proportion(0.5))
            if np.abs(self.angle) <= 0.01:
                pass
            if self.angle < -0.01:
                if self.angle >= -PI:
                    label.move_to(Angle(dashed_line, self.rod, radius=angle_drawn.radius + 0.3, other_angle=True).point_from_proportion(0.5))
                else:
                    label.move_to(Angle(dashed_line, self.rod, radius=angle_drawn.radius + 0.3).point_from_proportion(0.5))

        
        angle_drawn.add_updater(updater_angle)
        angle_label.add_updater(updater_angle_label)
        self.dashed_line = dashed_line
        self.angle_drawn = angle_drawn
        self.angle_label = angle_label

    def enable_speed_vector(self, vector_color: str = YELLOW) -> None:
        self.speed_vector = always_redraw(
            lambda: Vector(self.angular_velocity/1.5 * (np.cos(self.angle) * RIGHT + np.sin(self.angle) * UP), color=vector_color).shift(self.point + self.rod.get_end() - self.rod.get_start())
        )
        


class SimplePendulum(Scene):
    def construct(self):
        pendulum = Pendulum(init_angle, 0, point=2.5*UP + 5.25*RIGHT, length=l, end_mass_radius=0.1)
        pendulum.set_z_index(10)
        pendulum_box = Rectangle(BLACK, height=4, width=3.65, stroke_color=WHITE, stroke_width=0.5, fill_opacity=0.75).to_corner(UR, buff=0.05).set_z_index(8)
        
        pendulum.enable_angle_label()
        pendulum.enable_speed_vector()
        VGroup(pendulum.angle_drawn, pendulum.angle_label, pendulum.speed_vector).set_z_index(9)

        def Y_derivative(Y):
            theta, dtheta, z = Y
            return np.array([dtheta, -g * np.sin(theta)/l, 0])

        def pendulum_updater(pendulum, dt):
            prev_angular_velocity = pendulum.angular_velocity
            prev_angle = pendulum.angle
            Y = np.array([prev_angle, prev_angular_velocity, 0])

            k_1 = Y_derivative(Y)
            k_2 = Y_derivative(Y + dt/2*k_1)
            k_3 = Y_derivative(Y + dt/2*k_2)
            k_4 = Y_derivative(Y + dt*k_3)
            new_Y = Y + dt/6 * (k_1 + 2*k_2 + 2*k_3 + k_4)

            pendulum.angular_velocity = new_Y[1]
            pendulum.angle = new_Y[0]
            pendulum.rotate(dt*pendulum.angular_velocity, about_point=pendulum.point)

        pendulum.add_updater(pendulum_updater)
        
        plane = NumberPlane().set_opacity(0.4).set_z_index(5)
        phase_space = ArrowVectorField(
            lambda pos: Y_derivative(pos),
            x_range=[np.floor(-config["frame_width"] / 2), np.ceil(config["frame_width"] / 2), 0.75],
            y_range=[np.floor(-config["frame_height"] / 2), np.ceil(config["frame_height"] / 2), 0.75],
        ).set_z_index(6)
        dot = always_redraw(lambda: Dot(np.array([pendulum.angle, pendulum.angular_velocity, 0])).set_z_index(9))
        path = TracedPath(dot.get_center).set_z_index(8)
        
        self.add(pendulum, pendulum.angle_drawn, pendulum.angle_label, pendulum.dashed_line, pendulum.speed_vector, pendulum_box, plane, phase_space, dot, path)

        self.wait(10)

