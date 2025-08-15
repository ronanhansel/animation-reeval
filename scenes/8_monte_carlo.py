from manim import *
import numpy as np
import random


class MonteCarloPi(MovingCameraScene):
    def construct(self):
        # Visual style
        self.camera.background_color = "#141414"

        # --- 1) Initial Scene Setup ---
        side_length = 8.0
        radius = side_length / 2.0

        # First quadrant only: square from (0,0) to (radius, radius)
        square = Rectangle(width=radius, height=radius, color=WHITE, stroke_width=1)
        square.move_to([radius / 2.0, radius / 2.0, 0])
        # Quarter-circle arc centered at origin from (radius,0) to (0,radius)
        quarter_circle = Arc(radius=radius, start_angle=0, angle=PI / 2, color=WHITE, stroke_width=1)

        # Start zoomed so the square + circle fill the frame
        frame = self.camera.frame
        frame.save_state()
        # Start focused tightly on the quadrant
        frame.set_width(radius * 1.5)
        frame.move_to(square.get_corner(UR))

        self.play(
            LaggedStart(Create(square), Create(quarter_circle), lag_ratio=0.2),
            run_time=1.5,
        )

        # --- 3) Approximating Pi (readout below the square) ---
        inside_tracker = ValueTracker(0.0)
        total_tracker = ValueTracker(0.0)

        pi_label = MathTex("\\pi \\approx", color=WHITE)
        pi_number = DecimalNumber(
            0.0,
            num_decimal_places=4,
            color=YELLOW,
            include_sign=False,
        )

        # Update the displayed value smoothly based on trackers
        def update_pi_value(mobj):
            total = max(1.0, total_tracker.get_value())
            inside = inside_tracker.get_value()
            approx = 4.0 * (inside / total)
            mobj.set_value(approx)

        pi_number.add_updater(update_pi_value)
        pi_formula = MathTex(r"\frac{b}{r} \approx \pi \approx", color=WHITE)
        pi_formula[0][0].set_color(BLUE)
        pi_formula[0][2].set_color(RED)
        pi_group = VGroup(pi_formula, pi_number).arrange(RIGHT, buff=0.25)
        pi_group.next_to(square, DOWN, buff=0.5)
        self.play(Write(pi_group))

        # --- 2) The Monte Carlo Simulation ---
        random.seed(7)
        np.random.seed(7)

        dots_group = VGroup()

        # Generate a target number of points but animate in batches for performance
        target_points = 2000
        batch_size = 200
        num_batches = int(np.ceil(target_points / batch_size))

        # Helper to build one batch of dots and final tracker values
        def build_batch(start_index: int, count: int):
            dots = []
            inside_count = 0
            for _ in range(count):
                x = random.uniform(0.0, radius)
                y = random.uniform(0.0, radius)
                is_inside = (x * x + y * y) <= (radius * radius)
                color = BLUE if is_inside else RED
                if is_inside:
                    inside_count += 1
                dot = Dot(point=[x, y, 0], radius=0.015, color=color, fill_opacity=1.0)
                dots.append(dot)
            return dots, inside_count

        current_inside = 0
        current_total = 0

        for b in range(num_batches):
            remaining = target_points - current_total
            this_batch = min(batch_size, remaining)
            batch_dots, batch_inside = build_batch(current_total, this_batch)

            # Prepare animations: dots fade in one-by-one using lag for a dynamic feel
            dots_group.add(*batch_dots)
            dot_anims = [FadeIn(d, scale=0.2) for d in batch_dots]

            # Compute new totals and animate trackers to smoothly update the decimal
            new_total = current_total + this_batch
            new_inside = current_inside + batch_inside

            self.play(
                AnimationGroup(*dot_anims, lag_ratio=0.04),
                inside_tracker.animate.set_value(new_inside),
                total_tracker.animate.set_value(new_total),
                *([] if b != num_batches // 10 else [frame.animate.move_to([square.get_center()]).set_width(side_length * 2)]),
                run_time=2.0,
            )

            current_total = new_total
            current_inside = new_inside

        self.wait(2.5)

class MonteCarloText(Scene):
    def construct(self):
        title = Text("Monte Carlo", color=WHITE)
        title.scale(1.1)
        self.play(Write(title), run_time=1.2)
        self.wait(2.5)
