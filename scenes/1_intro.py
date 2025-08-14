from manim import *
import random


class IntroScene(Scene):
    def construct(self):
        random.seed(7)

        # 1) Create the test paper (always portrait)
        paper_width = 2.4
        paper_height = 3.8
        paper = RoundedRectangle(
            corner_radius=0.08,
            width=paper_width,
            height=paper_height,
            stroke_color=GRAY_B,
            stroke_width=3,
            fill_color=BLACK,
            fill_opacity=0.2,
        )

        self.play(Create(paper))

        self.wait(1)

        # Create ordered rows: each row has a short line (question stem) and option circles
        rows = self._generate_test_rows_inside(paper, num_rows=10, num_options=3)
        self.play(
            LaggedStart(*[FadeIn(r, scale=0.9) for r in rows], lag_ratio=0.03),
            run_time=1.5,
        )
        self.wait(1)

        # Ease out / reduce number of rows to illustrate a balanced test
        keep_count = 6
        keep_rows = VGroup(*[rows[i] for i in range(min(keep_count, len(rows)))])
        remove_rows = VGroup(*[rows[i] for i in range(keep_count, len(rows))])

        # Target positions: spread remaining rows evenly from top to bottom
        targets = self._even_layout_rows_inside(paper, len(keep_rows))
        move_anims = []
        for r, y in zip(keep_rows, targets):
            x = r.get_center()[0]
            move_anims.append(r.animate.move_to([x, y, 0]))

        # Move removed shapes slightly outward and fade (no there-and-back to avoid flicker)
        def out_dir():
            ang = random.uniform(0, TAU)
            return 0.6 * np.array([np.cos(ang), np.sin(ang), 0])

        remove_anims = [FadeOut(r, shift=out_dir()) for r in remove_rows]

        self.play(
            AnimationGroup(*move_anims, lag_ratio=0.05, rate_func=smooth, run_time=1.0),
            LaggedStart(*remove_anims, lag_ratio=0.03, run_time=0.8),
        )
        self.remove(*remove_rows)
        balanced_rows = keep_rows
        paper_group = VGroup(paper, balanced_rows)
        self.wait(0.4)

        # 2) Introduce the test-taker: scale so its height equals twice the circle's height
        taker_radius = 0.16
        target_height = 4 * taker_radius
        scale_factor = target_height / paper_group.height
        paper_target_pos = ORIGIN
        self.play(paper_group.animate.scale(scale_factor).move_to(paper_target_pos), run_time=0.8)

        taker = Circle(radius=taker_radius, stroke_color=GRAY_B, stroke_width=3, fill_color=GRAY_E, fill_opacity=0.9)
        taker.next_to(paper_group, RIGHT, buff=0.2)
        self.play(GrowFromCenter(taker))
        self.wait(0.3)

        # 3) Show the population: replicate into a grid
        base_pair = VGroup(paper_group, taker)
        grid_rows = 4
        grid_cols = 8

        # Compute positions for a uniform grid across the screen
        grid_positions = self._grid_positions(rows=grid_rows, cols=grid_cols, x_min=-6.2, x_max=6.2, y_min=-3.3, y_max=3.3)

        # Move the base pair to the first grid cell, then clone for the rest
        pairs = VGroup()
        if len(grid_positions) > 0:
            first_pos = grid_positions[0]
            self.play(base_pair.animate.move_to([first_pos[0], first_pos[1], 0]), run_time=0.5)
            pairs.add(base_pair)
        for (gx, gy) in grid_positions[1:]:
            clone = base_pair.copy()
            clone.move_to([gx, gy, 0])
            pairs.add(clone)

        # Animate the replication (others fade in)
        fresh_pairs = [p for p in pairs if p is not base_pair]
        self.play(LaggedStart(*[FadeIn(p, scale=0.95) for p in fresh_pairs], lag_ratio=0.02), run_time=1.3)
        self.wait(0.2)

        # 4) Visualize evaluation: randomly color taker circles (green/red)
        all_circles = []
        for p in pairs:
            # circle is second mobject in the pair
            all_circles.append(p[1])

        # Randomly assign outcomes
        for c in all_circles:
            roll = random.random()
            if roll < 0.35:
                target_color = GREEN
            elif roll < 0.55:
                target_color = RED
            else:
                target_color = GRAY_E
            c.set_fill(opacity=0.9)
            self.play(c.animate.set_fill(target_color), run_time=0.08)

        self.wait(1.0)

    # --- helpers ---
    def _generate_test_rows_inside(self, paper: Mobject, num_rows: int = 8, num_options: int = 3) -> VGroup:
        rows = VGroup()
        left = paper.get_left()[0] + 0.25
        right = paper.get_right()[0] - 0.25
        bottom = paper.get_bottom()[1] + 0.25
        top = paper.get_top()[1] - 0.25

        # Start densely packed from top to bottom
        ys = np.linspace(top - 0.25, bottom + 0.25, num_rows)
        line_len = max(0.6, (right - left) * 0.45)
        option_gap = 0.18
        option_radius = 0.06

        for y in ys:
            x0 = left
            stem = Line(
                start=[x0, y, 0],
                end=[x0 + line_len, y, 0],
                stroke_color=BLUE_E,
                stroke_width=2.5,
            )
            opts = VGroup()
            base_x = x0 + line_len + 0.22
            for i in range(num_options):
                cx = base_x + i * (2 * option_radius + option_gap)
                cy = y
                c = Circle(radius=option_radius, stroke_color=YELLOW_E, stroke_width=2.2, fill_opacity=0)
                c.move_to([cx, cy, 0])
                opts.add(c)
            row = VGroup(stem, opts)
            rows.add(row)
        return rows

    def _even_layout_rows_inside(self, paper: Mobject, count: int) -> list:
        top = paper.get_top()[1] - 0.45
        bottom = paper.get_bottom()[1] + 0.45
        ys = np.linspace(top, bottom, count)
        return list(ys)

    def _grid_positions(self, rows: int, cols: int, x_min: float, x_max: float, y_min: float, y_max: float) -> list:
        xs = np.linspace(x_min, x_max, cols)
        ys = np.linspace(y_min, y_max, rows)
        # Return positions row-major from top to bottom to fill the screen uniformly
        positions = []
        for y in ys[::-1]:
            for x in xs:
                positions.append((x, y))
        return positions


