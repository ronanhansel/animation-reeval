from manim import *
from manim.opengl import *
import numpy as np
import random

config.background_color = WHITE
num_students = 12

# Predetermined random choices for NaN replacement (for reproducibility across scenes)
# This is a 12x8 matrix of 0s and 1s to replace NaN values
nan_replacements = [
    [1, 0, 1, 0, 1, 1, 0, 1],  # Student 0
    [0, 1, 0, 1, 0, 1, 1, 0],  # Student 1
    [1, 1, 0, 0, 1, 0, 1, 1],  # Student 2
    [0, 0, 1, 1, 0, 1, 0, 0],  # Student 3
    [1, 0, 0, 1, 1, 0, 1, 1],  # Student 4
    [0, 1, 1, 0, 0, 1, 0, 1],  # Student 5
    [1, 1, 1, 0, 1, 1, 1, 0],  # Student 6
    [0, 0, 0, 1, 0, 0, 1, 1],  # Student 7
    [1, 0, 1, 1, 1, 0, 0, 1],  # Student 8
    [0, 1, 0, 0, 0, 1, 1, 0],  # Student 9
    [1, 1, 0, 1, 1, 1, 0, 1],  # Student 10
    [0, 0, 1, 0, 0, 0, 1, 0],  # Student 11
]

class Scene1(Scene):
    def construct(self):
        # Load response matrix data
        response_matrix_data = np.load("../data/resmat_trunc.npy")
        # Use a smaller subset for visualization (first 12 students, first 8 questions)
        matrix_subset = response_matrix_data[:12, :8]
        
        # Create a cleaner matrix by replacing NaN with predetermined values for visualization
        for i in range(matrix_subset.shape[0]):
            for j in range(matrix_subset.shape[1]):
                if np.isnan(matrix_subset[i, j]):
                    matrix_subset[i, j] = nan_replacements[i][j]  # Use predetermined values
        
        
        # === Initial State: Blank Scene ===
        self.camera.background_color = "#141414"
        
        # === Introduce Test-Takers ===
        # Create circles for test-takers on the left side
        test_taker_circles = VGroup()
        
        # Arrange circles in a cluster formation (3x4 grid with some offset)
        rows, cols = 3, 4
        # Generate random offsets for each student for a more scattered look
        offsets_x = [-0.125, 0.218, -0.268, -0.014, 0.152, 0.207, 0.191, 0.297, 0.178, -0.288, -0.128, 0.066]
        offsets_y = [0.197, -0.049, 0.038, -0.236, 0.146, -0.131, -0.298, 0.276, 0.199, 0.113, -0.209, -0.117]

        for i in range(num_students):
            row = i // cols
            col = i % cols

            # Use precomputed offsets for reproducibility
            offset_x = offsets_x[i]
            offset_y = offsets_y[i]
            circle = Circle(
                radius=0.2,
                color=GREY,
                fill_opacity=0.8,
                stroke_color=DARK_GREY,
                stroke_width=2
            )
            circle.move_to([-5.5 + col * 0.8 + offset_x, 1.5 - row * 0.8 + offset_y, 0])
            test_taker_circles.add(circle)

        # Animate test-takers appearing
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(circle) for circle in test_taker_circles],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.wait(1)
        
        # Add dimmer background population (fades in behind selected test-takers)
        background_population_circles = VGroup()
        np.random.seed(7)
        num_background = 60
        for _ in range(num_background):
            x = np.random.uniform(-6.2, -2.6)
            y = np.random.uniform(-1.0, 2.4)
            bg_circle = Circle(
                radius=0.16,
                color=GREY,
                fill_opacity=0.15,
                stroke_color=DARK_GREY,
                stroke_width=1,
            )
            bg_circle.set_opacity(0)
            bg_circle.set_z_index(-1)
            bg_circle.move_to([x, y, 0])
            background_population_circles.add(bg_circle)
        self.add(background_population_circles)
        self.play(
            LaggedStart(
                *[c.animate.set_opacity(0.15) for c in background_population_circles],
                lag_ratio=0.02
            ),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(background_population_circles))
        self.wait(2)
        
        # === Fade Out for Simulation ===
        self.play(
            *[circle.animate.set_opacity(0.1) for circle in test_taker_circles],
            run_time=1.5
        )
        self.wait(0.5)
        
        # === Introduce Questions & Data ===
        
        # Create empty difficulty boxes on the right side
        num_questions = 8
        difficulty_boxes = VGroup()
        box_labels = VGroup()
        
        for i in range(num_questions):
            # Empty rectangular container
            box = Rectangle(
                width=0.4,
                height=2.0,
                color=DARK_GRAY,
                fill_opacity=0,
                stroke_width=2
            )
            box.move_to([4.5 + (i % 4) * 0.6, 1 - (i // 4) * 2.5, 0])
            
            # Question label
            label = Text(f"Q{i+1}", color=WHITE, font_size=16)
            label.next_to(box, DOWN, buff=0.1)
            
            difficulty_boxes.add(box)
            box_labels.add(label)
        # Create response matrix in the center
        matrix_entries = []
        for i in range(matrix_subset.shape[0]):
            row = []
            for j in range(matrix_subset.shape[1]):
                if matrix_subset[i, j] == 1:
                    cell = Rectangle(width=0.3, height=0.3, fill_color=GREEN, fill_opacity=0.8, stroke_color=WHITE, stroke_width=1)
                else:
                    cell = Rectangle(width=0.3, height=0.3, fill_color=RED, fill_opacity=0.8, stroke_color=WHITE, stroke_width=1)
                row.append(cell)
            matrix_entries.append(row)
        
        # Create matrix group
        matrix_group = VGroup()
        for i, row in enumerate(matrix_entries):
            for j, cell in enumerate(row):
                cell.move_to([j * 0.35 - 1.2, 1.5 - i * 0.35, 0])
                matrix_group.add(cell)
        
        # Matrix label
        matrix_label = Text(
            "Response Matrix",
            color=WHITE,
            font_size=24
        ).next_to(matrix_group, DOWN, buff=0.5)
        
        # Animate questions and matrix appearing
        self.play(
            LaggedStart(
                *[Create(box) for box in difficulty_boxes],
                lag_ratio=0.1
            ),
            Write(box_labels),
            run_time=2
        )
        
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(cell) for cell in matrix_group],
                lag_ratio=0.02
            ),
            Write(matrix_label),
            run_time=3
        )
        self.wait(1)
        
        # === Animate guiding lines ===
        # Lines from test-takers to matrix
        left_lines = VGroup()
        for i, circle in enumerate(test_taker_circles):  # Only some for clarity
            line = DashedLine(
                circle.get_right(),
                matrix_group[i * 8].get_left(),
                color=BLUE,
                stroke_width=1,
                stroke_opacity=0.5
            )
            left_lines.add(line)
        
        # Lines from matrix to difficulty boxes
        right_lines = VGroup()
        for j in range(num_questions):
            matrix_col_center = [j * 0.35 - 1.2, 0.5, 0]
            line = DashedLine(
                matrix_col_center,
                difficulty_boxes[j].get_left(),
                color=PURPLE,
                stroke_width=1,
                stroke_opacity=0.5
            )
            right_lines.add(line)
        
        self.play(
            Create(left_lines),
            Create(right_lines),
            run_time=2
        )
        self.wait(2)

        # Fade dashed lines
        self.play(
            FadeOut(left_lines),
            FadeOut(right_lines),
            run_time=2
        )
        
        self.wait(2)


class Scene2(Scene):
    def construct(self):
        # Load response matrix data (same as Scene 1)
        response_matrix_data = np.load("../data/resmat_trunc.npy")
        matrix_subset = response_matrix_data[:12, :8]
        
        # Create a cleaner matrix by replacing NaN with predetermined values for visualization
        for i in range(matrix_subset.shape[0]):
            for j in range(matrix_subset.shape[1]):
                if np.isnan(matrix_subset[i, j]):
                    matrix_subset[i, j] = nan_replacements[i][j]  # Use predetermined values
        
        # === Recreate Scene 1 final state ===
        self.camera.background_color = "#141414"
        
        # Test-takers (faded)
        test_taker_circles = VGroup()
        rows, cols = 3, 4
        offsets_x = [-0.125, 0.218, -0.268, -0.014, 0.152, 0.207, 0.191, 0.297, 0.178, -0.288, -0.128, 0.066]
        offsets_y = [0.197, -0.049, 0.038, -0.236, 0.146, -0.131, -0.298, 0.276, 0.199, 0.113, -0.209, -0.117]

        for i in range(num_students):
            row = i // cols
            col = i % cols

            # Use precomputed offsets for reproducibility
            offset_x = offsets_x[i]
            offset_y = offsets_y[i]
            circle = Circle(
                radius=0.2,
                color=GREY,
                fill_opacity=0.1,
                stroke_color=DARK_GREY,
                stroke_width=2,
                stroke_opacity=0.1
            )
            circle.move_to([-5.5 + col * 0.8 + offset_x, 1.5 - row * 0.8 + offset_y, 0])
            test_taker_circles.add(circle)
        # Difficulty boxes (empty)
        difficulty_boxes = VGroup()
        box_labels = VGroup()
        
        for i in range(8):
            box = Rectangle(
                width=0.4,
                height=2.0,
                color=DARK_GRAY,
                fill_opacity=0,
                stroke_width=2
            )
            box.move_to([4.5 + (i % 4) * 0.6, 1 - (i // 4) * 2.5, 0])
            
            label = Text(f"Q{i+1}", color=WHITE, font_size=16)
            label.next_to(box, DOWN, buff=0.1)
            
            difficulty_boxes.add(box)
            box_labels.add(label)
        # Response matrix
        matrix_group = VGroup()
        matrix_entries = []
        for i in range(matrix_subset.shape[0]):
            row = []
            for j in range(matrix_subset.shape[1]):
                if matrix_subset[i, j] == 1:
                    cell = Rectangle(width=0.3, height=0.3, fill_color=GREEN, fill_opacity=0.8, stroke_color=WHITE, stroke_width=1)
                else:
                    cell = Rectangle(width=0.3, height=0.3, fill_color=RED, fill_opacity=0.8, stroke_color=WHITE, stroke_width=1)
                cell.move_to([j * 0.35 - 1.2, 1.5 - i * 0.35, 0])
                matrix_group.add(cell)
                row.append(cell)
            matrix_entries.append(row)
        
        matrix_label = Text(
            "Response Matrix",
            color=WHITE,
            font_size=24
        ).next_to(matrix_group, DOWN, buff=0.5)
        
        # Add everything to scene
        self.add(
            test_taker_circles,
            difficulty_boxes, box_labels,
            matrix_group, matrix_label
        )
        
        # === PART A: Estimating Question Difficulty ===
        
        # Analyze first column in detail - Create manual rectangle for OpenGL compatibility
        col_mobjects = [matrix_group[i * 8] for i in range(12)]
        if col_mobjects:  # Check if we have mobjects
            # Get bounding box of the column
            min_x = min([mob.get_left()[0] for mob in col_mobjects])
            max_x = max([mob.get_right()[0] for mob in col_mobjects]) 
            min_y = min([mob.get_bottom()[1] for mob in col_mobjects])
            max_y = max([mob.get_top()[1] for mob in col_mobjects])
            
            # Create rectangle manually
            width = max_x - min_x + 0.1  # Add some padding
            height = max_y - min_y + 0.1
            center_x = (min_x + max_x) / 2
            center_y = (min_y + max_y) / 2
            
            first_col_highlight = Rectangle(
                width=width,
                height=height,
                color=YELLOW,
                stroke_width=3,
                fill_opacity=0
            ).move_to([center_x, center_y, 0])
        
        self.play(Create(first_col_highlight), run_time=1)
        self.wait(0.5)
        
        # Calculate difficulty for first question (proportion of incorrect answers)
        first_col_data = matrix_subset[:, 0]
        difficulty_prop = 1 - np.mean(first_col_data)  # Higher when more students got it wrong
        
        # Fill the first difficulty box
        fill_height = difficulty_prop * 1.8  # Scale to box height
        first_fill = Rectangle(
            width=0.4,
            height=fill_height,
            fill_color=RED,
            fill_opacity=0.7,
            stroke_width=0
        )
        first_fill.align_to(difficulty_boxes[0], DOWN)
        first_fill.align_to(difficulty_boxes[0], LEFT)
        
        self.play(
            DrawBorderThenFill(first_fill),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Move highlight to second column and demonstrate
        col2_mobjects = [matrix_group[i * 8 + 1] for i in range(12)]
        if col2_mobjects:  # Check if we have mobjects
            # Get bounding box of the second column
            min_x = min([mob.get_left()[0] for mob in col2_mobjects])
            max_x = max([mob.get_right()[0] for mob in col2_mobjects]) 
            min_y = min([mob.get_bottom()[1] for mob in col2_mobjects])
            max_y = max([mob.get_top()[1] for mob in col2_mobjects])
            
            # Create rectangle manually
            width = max_x - min_x + 0.1  # Add some padding
            height = max_y - min_y + 0.1
            center_x = (min_x + max_x) / 2
            center_y = (min_y + max_y) / 2
            
            second_col_highlight = Rectangle(
                width=width,
                height=height,
                color=YELLOW,
                stroke_width=3,
                fill_opacity=0
            ).move_to([center_x, center_y, 0])
        
        self.play(Transform(first_col_highlight, second_col_highlight), run_time=1)
        
        # Fill second box
        second_col_data = matrix_subset[:, 1]
        difficulty_prop_2 = 1 - np.mean(second_col_data)
        fill_height_2 = difficulty_prop_2 * 1.8
        
        second_fill = Rectangle(
            width=0.4,
            height=fill_height_2,
            fill_color=RED,
            fill_opacity=0.7,
            stroke_width=0
        )
        second_fill.align_to(difficulty_boxes[1], DOWN)
        second_fill.align_to(difficulty_boxes[1], LEFT)
        
        self.play(DrawBorderThenFill(second_fill), run_time=1.5)
        self.wait(0.5)
        
        # Remove highlight
        self.play(FadeOut(first_col_highlight), run_time=0.5)
        
        # Fill remaining boxes rapidly with LaggedStart
        remaining_fills = VGroup()
        for j in range(2, 8):
            col_data = matrix_subset[:, j]
            difficulty_prop = 1 - np.mean(col_data)
            fill_height = difficulty_prop * 1.8
            
            fill = Rectangle(
                width=0.4,
                height=fill_height,
                fill_color=RED,
                fill_opacity=0.7,
                stroke_width=0
            )
            fill.align_to(difficulty_boxes[j], DOWN)
            fill.align_to(difficulty_boxes[j], LEFT)
            remaining_fills.add(fill)
        
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(fill) for fill in remaining_fills],
                lag_ratio=0.2
            ),
            run_time=2
        )

        self.wait(2)
        
        # === PART B: Estimating Student Ability ===
        
        # Re-engage students
        self.play(
            *[circle.animate.set_opacity(1.0) for circle in test_taker_circles],
            run_time=1
        )
        
        # Move circles to form a vertical line
        target_positions = []
        for i in range(12):
            target_pos = [-5.5, 2.5 - i * 0.5, 0]
            target_positions.append(target_pos)
        
        self.play(
            *[circle.animate.move_to(pos) for circle, pos in zip(test_taker_circles, target_positions)],
            run_time=2
        )

        # Demonstrate ability estimation for first student
        first_row_highlight = SurroundingRectangle(
            VGroup(*[matrix_group[j] for j in range(8)]),
            color=YELLOW,
            stroke_width=3,
            buff=0.05
        )
        
        self.play(Create(first_row_highlight), run_time=1)
        # Make all filled boxes glow briefly
        all_fills = VGroup(first_fill, second_fill, *remaining_fills)
        glow_effect = all_fills.copy().set_stroke(YELLOW, width=4, opacity=1)
        
        self.play(
            Create(glow_effect),
            run_time=0.5
        )
        self.play(
            FadeOut(glow_effect),
            run_time=0.5
        )
        
        # Calculate and apply opacity for first student
        first_student_data = matrix_subset[0, :]
        ability_score = np.mean(first_student_data)
        opacity = 0.3 + 0.7 * ability_score  # Higher ability = more opaque
        
        # Create theta label for first student
        first_theta_label = MathTex(f"\\theta = {ability_score:.2f}", color=WHITE, font_size=24)
        first_theta_label.next_to(test_taker_circles[0], RIGHT, buff=0.3)
        
        self.play(
            test_taker_circles[0].animate.set_fill(BLUE).set_stroke(DARK_BLUE).set_opacity(opacity),
            Write(first_theta_label),
            run_time=1
        )
        self.wait(0.5)
        
        # Demonstrate for a second student
        second_row_highlight = SurroundingRectangle(
            VGroup(*[matrix_group[8 + j] for j in range(8)]),  # Second row
            color=YELLOW,
            stroke_width=3,
            buff=0.05
        )
        
        self.play(Transform(first_row_highlight, second_row_highlight), run_time=1)
        
        self.play(
            Create(glow_effect),
            run_time=0.5
        )
        self.play(
            FadeOut(glow_effect),
            run_time=0.5
        )
        
        # Calculate and apply opacity for second student
        second_student_data = matrix_subset[1, :]
        second_ability_score = np.mean(second_student_data)
        second_opacity = 0.3 + 0.7 * second_ability_score
        
        # Create theta label for second student
        second_theta_label = MathTex(f"\\theta = {second_ability_score:.2f}", color=WHITE, font_size=24)
        second_theta_label.next_to(test_taker_circles[1], RIGHT, buff=0.3)
        
        self.play(
            test_taker_circles[1].animate.set_fill(BLUE).set_stroke(DARK_BLUE).set_opacity(second_opacity),
            Write(second_theta_label),
            run_time=1
        )
        self.wait(0.5)
        
        # Remove highlight
        self.play(FadeOut(first_row_highlight), run_time=0.5)

        # Apply opacity changes to all remaining students quickly
        remaining_opacity_animations = []
        remaining_theta_labels = []
        for i in range(2, 12):
            student_data = matrix_subset[i, :]
            ability_score = np.mean(student_data)
            opacity = 0.3 + 0.7 * ability_score
            
            # Create theta label for this student
            theta_label = MathTex(f"\\theta = {ability_score:.2f}", color=WHITE, font_size=24)
            theta_label.next_to(test_taker_circles[i], RIGHT, buff=0.3)
            remaining_theta_labels.append(theta_label)
            
            remaining_opacity_animations.append(test_taker_circles[i].animate.set_fill(BLUE).set_stroke(DARK_BLUE).set_opacity(opacity))

        self.play(
            LaggedStart(*remaining_opacity_animations, lag_ratio=0.1),
            LaggedStart(*[Write(label) for label in remaining_theta_labels], lag_ratio=0.1),
            run_time=2
        )
        self.wait(1)
        
        # Now sort students by ability (keep them in vertical line, just reorder top to bottom)
        # Calculate ability scores and create sorted list
        student_abilities = []
        all_theta_labels = [first_theta_label, second_theta_label] + remaining_theta_labels
        
        for i in range(12):
            student_data = matrix_subset[i, :]
            ability_score = np.mean(student_data)
            student_abilities.append((ability_score, i, test_taker_circles[i], all_theta_labels[i]))
        
        # Sort by ability (highest first)
        student_abilities.sort(key=lambda x: x[0], reverse=True)
        
        # Animate sorting - move circles and labels to vertical positions based on ability ranking
        sorting_animations = []
        for rank, (ability, original_idx, circle, label) in enumerate(student_abilities):
            new_y_pos = 2.5 - rank * 0.5
            new_circle_pos = [-5.5, new_y_pos, 0]
            new_label_pos = [-5.5 + 0.68 + 0.3, new_y_pos, 0]  # radius (0.2) + buff (0.3)
            
            sorting_animations.append(circle.animate.move_to(new_circle_pos))
            sorting_animations.append(label.animate.move_to(new_label_pos))
        
        self.play(
            *sorting_animations,
            run_time=2.5
        )
        self.wait(2)
