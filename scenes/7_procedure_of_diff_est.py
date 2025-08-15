from __future__ import annotations

import math
import numpy as np
from manim import *

# ====== Layout constants (tweak here to adjust quickly) ======
TEST_TAKER_X = LEFT * 4
TEST_TAKER_Y_OFFSET = DOWN * 0.0  # align horizontally with paper and b (y=0)
TEST_TAKER_POS = TEST_TAKER_X + TEST_TAKER_Y_OFFSET
TAKER_RADIUS = 0.2
PAPER_POS = ORIGIN
DIFFICULTY_POS = RIGHT * 4

THETA_LABEL_OFFSET = UP * 1.6
QUESTION_SCALE = 1.0

AXES_X_RANGE = [-4, 4, 1]
AXES_Y_RANGE = [0, 0.5, 0.1]
AXES_SCALE = 0.25  # smaller distribution to sit on top of the circle
AXES_OFFSET_FROM_THETA = UP * 0.0  # will place relative to the test-taker top

NUM_RANDOM_SAMPLES = 300
DOT_RADIUS = 0.04
DOT_Y_ABOVE_AXIS = 0.02


def create_test_taker_icon() -> VGroup:
    """Plain student circle per request."""
    circle = Circle(
        radius=TAKER_RADIUS,
        stroke_color=GRAY_B,
        stroke_width=3,
        fill_color=GRAY_E,
        fill_opacity=0.9,
    )
    return VGroup(circle)


def create_test_paper() -> VGroup:
    """Create the test paper exactly like in `IntroScene` (no animations)."""
    paper_width = 0.5
    paper_height = 0.8
    return RoundedRectangle(
        corner_radius=0.08,
        width=paper_width,
        height=paper_height,
        stroke_color=GRAY_B,
        stroke_width=3,
        fill_color=BLACK,
        fill_opacity=1,
    )

# def create_test_paper() -> VGroup:
#     """Create the test paper exactly like in `IntroScene` (no animations)."""
#     # Same paper geometry and styling as IntroScene
#     paper_width = 2.4
#     paper_height = 3.8
#     paper = RoundedRectangle(
#         corner_radius=0.08,
#         width=paper_width,
#         height=paper_height,
#         stroke_color=GRAY_B,
#         stroke_width=3,
#         fill_color=BLACK,
#         fill_opacity=0.2,
#     )

#     # Reproduce `_generate_test_rows_inside` from IntroScene
#     num_rows_total = 10
#     num_options = 3

#     rows = VGroup()
#     left = paper.get_left()[0] + 0.25
#     right = paper.get_right()[0] - 0.25
#     bottom = paper.get_bottom()[1] + 0.25
#     top = paper.get_top()[1] - 0.25

#     ys_dense = np.linspace(top - 0.25, bottom + 0.25, num_rows_total)
#     line_len = max(0.6, (right - left) * 0.45)
#     option_gap = 0.18
#     option_radius = 0.06

#     for y in ys_dense:
#         x0 = left
#         stem = Line(
#             start=[x0, y, 0],
#             end=[x0 + line_len, y, 0],
#             stroke_color=BLUE_E,
#             stroke_width=2.5,
#         )
#         opts = VGroup()
#         base_x = x0 + line_len + 0.22
#         for i in range(num_options):
#             cx = base_x + i * (2 * option_radius + option_gap)
#             cy = y
#             c = Circle(radius=option_radius, stroke_color=YELLOW_E, stroke_width=2.2, fill_opacity=0)
#             c.move_to([cx, cy, 0])
#             opts.add(c)
#         row = VGroup(stem, opts)
#         rows.add(row)

#     # Reproduce the reduced and evenly-spaced layout (keep first 6)
#     keep_count = 6
#     keep_rows = VGroup(*[rows[i] for i in range(min(keep_count, len(rows)))])

#     top_y = paper.get_top()[1] - 0.45
#     bottom_y = paper.get_bottom()[1] + 0.45
#     ys_even = np.linspace(top_y, bottom_y, len(keep_rows))
#     for row, y_target in zip(keep_rows, ys_even):
#         x_center = row.get_center()[0]
#         row.move_to([x_center, y_target, 0])

#     return VGroup(paper, keep_rows).scale(0.25)


class UnknownAbilityToDistribution(Scene):
    """Visual explanation: unknown ability -> known distribution -> random samples.

    Stages
    - Stage 1: Show goal using arrows from θ (ability) -> test -> b (difficulty)
    - Stage 2: Transform θ into a question mark (unknown ability)
    - Stage 3: Transform question mark into N(0,1) distribution and draw random samples
    """

    def construct(self) -> None:
        # --- Stage 1: Establish the goal ---
        test_taker_icon = create_test_taker_icon().move_to(TEST_TAKER_POS)
        test_papers = VGroup()
        for i in range(3):
            paper = create_test_paper()
            # Stagger the papers slightly
            offset_x = i * 0.15
            offset_y = i * 0.1
            paper.move_to(PAPER_POS + np.array([offset_x, offset_y, 0]))
            test_papers.add(paper)
        test_paper = test_papers  # Keep the same variable name for compatibility

        theta_label = MathTex(r"\theta")
        theta_label.next_to(test_taker_icon, UP, buff=0.4)

        difficulty_label = MathTex(r"b")
        difficulty_label.move_to(DIFFICULTY_POS)

        # Use a single horizontal baseline aligned with b (and paper center)
        baseline_y = difficulty_label.get_center()[1]

        # Arrow from the student circle to the test paper (horizontal on baseline)
        start_tp = np.array([test_taker_icon.get_right()[0], baseline_y, 0.0])
        end_tp = np.array([test_paper.get_left()[0], baseline_y, 0.0])
        arrow_taker_to_paper = Arrow(start_tp, end_tp, buff=0.2)

        # Arrow from the paper to difficulty label (horizontal on same baseline)
        start_pb = np.array([test_paper.get_right()[0], baseline_y, 0.0])
        end_pb = np.array([difficulty_label.get_left()[0], baseline_y, 0.0])
        arrow_paper_to_b = Arrow(start_pb, end_pb, buff=0.2)

        # Sequential reveal: circle -> arrow -> test -> b (with brief delays)
        self.play(FadeIn(test_taker_icon, shift=UP), run_time=0.6)
        self.wait(1)
        self.play(Create(arrow_taker_to_paper),
                  FadeIn(test_paper, shift=UP), run_time=0.6)
        self.wait(1)
        self.play(FadeIn(difficulty_label, shift=UP), Create(arrow_paper_to_b), run_time=0.6)
        self.wait(1)
        # Add theta label after the ordered sequence (used for the next transformation)
        self.play(Create(theta_label), run_time=0.5)
        self.wait(1)

        # --- Stage 2: The "Unknown" problem ---
        question_mark = MathTex("?").scale(QUESTION_SCALE)
        # Place question mark directly above the circle, not affecting baseline alignment
        question_mark.next_to(test_taker_icon, UP, buff=0.2)
        self.play(ReplacementTransform(theta_label, question_mark), run_time=1)
        self.wait(2)

        # --- Stage 3: Known distribution solution ---
        axes = Axes(x_range=AXES_X_RANGE, y_range=AXES_Y_RANGE, tips=False)
        # Prefer numbers only on x-axis to emphasize θ
        axes.x_axis.add_numbers(x_values=np.arange(-4, 5, 2))
        # y-axis kept clean

        x_axis_label = MathTex(r"\theta").scale(0.8)
        x_axis_label.next_to(axes.x_axis, DOWN, buff=0.25)

        def standard_normal_pdf(x: float) -> float:
            return (1.0 / np.sqrt(2 * np.pi)) * np.exp(-(x**2) / 2.0)

        graph = axes.plot(standard_normal_pdf, color="#2a9d8f")

        distribution_group = VGroup(axes, graph, x_axis_label)
        distribution_group.scale(AXES_SCALE)
        # Keep distribution above the circle (offset from circle, not baseline)
        distribution_group.next_to(test_taker_icon, UP, buff=0.1)

        self.play(ReplacementTransform(question_mark, distribution_group), run_time=1.0)
        self.wait(0.3)

        # Random samples proportional to N(0,1) for tails vs center
        def normal_cdf(x: float) -> float:
            return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

        tail_threshold = 2.0
        p_tail_one_side = 1.0 - normal_cdf(tail_threshold)

        total_n = NUM_RANDOM_SAMPLES
        left_n = int(round(total_n * p_tail_one_side))
        right_n = int(round(total_n * p_tail_one_side))
        center_n = max(0, total_n - left_n - right_n)

        def sample_until(count: int, predicate) -> np.ndarray:
            if count <= 0:
                return np.array([], dtype=float)
            samples: list[float] = []
            batch = max(16, count * 4)
            while len(samples) < count:
                cand = np.random.normal(loc=0.0, scale=1.0, size=batch)
                for val in cand:
                    if predicate(float(val)):
                        samples.append(float(val))
                        if len(samples) >= count:
                            break
            return np.array(samples[:count], dtype=float)

        left_samples = sample_until(left_n, lambda v: v <= -tail_threshold)
        right_samples = sample_until(right_n, lambda v: v >= tail_threshold)
        center_samples = sample_until(center_n, lambda v: (-tail_threshold < v < tail_threshold))

        all_x = np.concatenate([center_samples, left_samples, right_samples])

        dots = VGroup()
        left_tail_dots = VGroup()
        right_tail_dots = VGroup()

        for x_value in all_x:
            x_float = float(x_value)
            dot_point = axes.c2p(x_float, DOT_Y_ABOVE_AXIS)
            dot = Dot(point=dot_point, radius=DOT_RADIUS, color=BLUE)
            dots.add(dot)
            if x_float <= -tail_threshold:
                left_tail_dots.add(dot)
            elif x_float >= tail_threshold:
                right_tail_dots.add(dot)

        self.play(LaggedStart(*[FadeIn(d, scale=0.8) for d in dots], lag_ratio=0.08), run_time=2.0)
        # Highlight both tails at once (skip gracefully if a tail is empty)
        self.wait(2)
        highlight_anims = []
        if len(left_tail_dots) > 0:
            highlight_anims.append(Indicate(left_tail_dots, color=YELLOW, scale_factor=1.4))
        if len(right_tail_dots) > 0:
            highlight_anims.append(Indicate(right_tail_dots, color=YELLOW, scale_factor=1.4))
        if highlight_anims:
            self.play(*highlight_anims, run_time=1.2)
        self.wait(0.8)
