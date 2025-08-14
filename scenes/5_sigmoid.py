from manim import *
import numpy as np

Text.set_default(font_size=24)

class SigmoidSquash(Scene):
    def construct(self):
        # Axes covering a wide range
        axes = Axes(
            x_range=[-10, 10, 2],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": WHITE, "stroke_width": 2},
            y_axis_config={"include_numbers": True, "font_size": 24},
            tips=False,
        )
        x_label = axes.get_x_axis_label(Tex("x", font_size=24))
        y_label = axes.get_y_axis_label(Tex("y", font_size=24))

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        # Sigmoid function and its graph
        def sigmoid(x: float) -> float:
            return 1.0 / (1.0 + np.exp(-x))

        curve = axes.plot(lambda x: sigmoid(x), x_range=[-10, 10], color=YELLOW, stroke_width=4)

        # Random dots scattered across the entire plot
        num_dots = 240  # at least 200
        x_min, x_max = -10, 10
        y_min, y_max = -2, 2
        xs = np.random.uniform(x_min, x_max, size=num_dots)
        ys = np.random.uniform(y_min, y_max, size=num_dots)

        dots = VGroup(
            *[Dot(point=axes.c2p(x, y), radius=0.03, color=WHITE) for x, y in zip(xs, ys)]
        )

        self.play(FadeIn(dots, lag_ratio=0.04, run_time=1.2))
        self.play(Create(curve), run_time=1.5)

        # Transform each dot to (x, sigmoid(x)) while keeping x fixed
        animations = []
        for i, dot in enumerate(dots):
            x_value = xs[i]
            target_point = axes.c2p(x_value, sigmoid(x_value))
            animations.append(Transform(dot, Dot(point=target_point, radius=0.03, color=WHITE)))

        self.play(*animations, run_time=3, rate_func=smooth)

        # Hold final state
        self.wait(3)


