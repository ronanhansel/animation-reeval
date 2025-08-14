from manim import *
import random
import numpy as np


MathTex.set_default(font_size=34)
DecimalNumber.set_default(num_decimal_places=0, font_size=34)

class TriangleStackGravityScene(MovingCameraScene):
    """Build a triangular stack of circles, pause, then drop them with gravity and bounces."""

    def construct(self):
        random.seed(7)

        base_count = 12
        circle_radius = 0.18
        gap = 0.06

        diameter = 2 * circle_radius
        horizontal_step = diameter + gap
        vertical_step = (np.sqrt(3) / 2.0) * diameter

        base_y = -1.2

        rows = []
        all_circles = []
        for row_index in range(base_count):
            count_in_row = base_count - row_index
            y = base_y + row_index * vertical_step
            x_offset = -0.5 * (count_in_row - 1) * horizontal_step
            row_circles = VGroup()
            for j in range(count_in_row):
                x = x_offset + j * horizontal_step
                c = Circle(radius=circle_radius, stroke_color=GRAY_B, stroke_width=3, fill_color=GRAY_E, fill_opacity=0.9)
                c.move_to([x, y, 0])
                row_circles.add(c)
                all_circles.append(c)
            rows.append(row_circles)

        pyramid_group = VGroup(*all_circles)
        top_circle = rows[-1][0] if len(rows) > 0 and len(rows[-1]) > 0 else None

        appear_anims = []
        for row in rows:
            for c in row:
                appear_anims.append(FadeIn(c, scale=0.2))

        self.play(
            self.camera.frame.animate.scale(1/2).move_to(pyramid_group.get_top()),
            run_time=0.8,
        )

        self.play(LaggedStart(*appear_anims, lag_ratio=0.06), run_time=2.2)

        self.wait(1)

        self.play(
            self.camera.frame.animate.scale(2).move_to(pyramid_group.get_top()),
            run_time=0.5,
        )

        frame_h = config.frame_height
        frame_w = config.frame_width
        floor_y = -frame_h / 2 + 0.1
        left_x = -frame_w / 2 + 0.1
        right_x = frame_w / 2 - 0.1

        gravity = 5.2

        def apply_physics(mobj: Mobject, dt: float) -> None:
            v = getattr(mobj, "velocity", np.array([0.0, 0.0, 0.0], dtype=float))
            restitution = getattr(mobj, "restitution", 0.65)

            v[1] -= gravity * dt
            mobj.shift(v * dt)

            if mobj.get_bottom()[1] <= floor_y:
                c = mobj.get_center()
                c[1] = floor_y + circle_radius
                mobj.move_to(c)
                if v[1] < 0:
                    v[1] = -v[1] * restitution
                    v[0] += random.uniform(-0.5, 0.5)
                v[0] *= 0.985

            if mobj.get_left()[0] <= left_x:
                c = mobj.get_center()
                c[0] = left_x + circle_radius
                mobj.move_to(c)
                if v[0] < 0:
                    v[0] = -v[0] * restitution

            if mobj.get_right()[0] >= right_x:
                c = mobj.get_center()
                c[0] = right_x - circle_radius
                mobj.move_to(c)
                if v[0] > 0:
                    v[0] = -v[0] * restitution

            if abs(v[1]) < 0.02 and abs(mobj.get_bottom()[1] - floor_y) < 1e-3:
                v[1] = 0.0
            mobj.velocity = v

        falling_circles = [c for c in all_circles if c is not top_circle]
        for c in falling_circles:
            c.velocity = np.array([random.uniform(-0.25, 0.25), 0.0, 0.0], dtype=float)
            c.restitution = random.uniform(0.58, 0.75)
            c.add_updater(apply_physics)

        if top_circle is not None:
            self.play(top_circle.animate.move_to(pyramid_group.get_top()), run_time=1.0)

            theta_text = MathTex(r"\theta =")
            theta_number = DecimalNumber(0, num_decimal_places=0)
            theta_group = VGroup(theta_text, theta_number).arrange(RIGHT, buff=0.15)
            theta_group.next_to(top_circle, DOWN, buff=0.6)
            self.play(FadeIn(theta_group, shift=0.2 * UP), run_time=0.4)
            self.play(ChangeDecimalToValue(theta_number, 2), run_time=1.2, rate_func=linear)

        self.wait(3.8)

        for c in falling_circles:
            c.remove_updater(apply_physics)

        self.wait(0.5)

