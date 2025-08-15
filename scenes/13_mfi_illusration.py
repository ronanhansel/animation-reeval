from manim import *
import numpy as np
import random

class AdaptiveTestingVisualization(Scene):
    def construct(self):
        # Configuration
        self.item_bank_size = 50  # Number of items in the bank
        self.num_iterations = 7   # Total number of test items to administer
        self.ability_range = [-2, 2]
        
        # Initialize components
        self.setup_visual_elements()
        
        # Execute the animation storyboard
        self.scene_1_setup()
        self.scene_2_first_response()
        self.scene_3_second_item()
        self.scene_4_iterative_process()
        self.scene_5_conclusion()
    
    def setup_visual_elements(self):
        """Initialize all visual components"""
        
        # Ability Scale (NumberLine)
        self.ability_scale = NumberLine(
            x_range=self.ability_range + [1],
            length=8,
            include_numbers=True,
            numbers_to_include=[-2, -1, 0, 1, 2],
            font_size=24
        ).shift(DOWN * 2)
        
        # Ability Scale Label
        self.ability_label = Text("Ability Estimate", font_size=24).next_to(
            self.ability_scale, DOWN
        )
        
        # Ability Indicator (Triangle)
        self.ability_indicator = Triangle(
            fill_opacity=1, 
            fill_color=BLUE,
            color=BLUE
        ).scale(0.15).next_to(self.ability_scale.n2p(0), UP, buff=0.1)
        
        # Item Bank (Grid of grey dots)
        self.item_positions = []
        self.item_dots = VGroup()
        
        # Create a grid-like arrangement with some randomness
        rows, cols = 5, 5
        for i in range(self.item_bank_size):
            if i < rows * cols:
                row = i // cols
                col = i % cols
                # Add some randomness to make it look more natural
                x = (col - cols//2) * 0.8 + random.uniform(-0.15, 0.15)
                y = (row - rows//2) * 0.6 + random.uniform(-0.1, 0.1) + 1.5
                pos = np.array([x, y, 0])
            else:
                # Random positions for extra dots
                pos = np.array([
                    random.uniform(-3, 3),
                    random.uniform(0.5, 2.5),
                    0
                ])
            
            self.item_positions.append(pos)
            dot = Dot(point=pos, radius=0.08, color=GREY, fill_opacity=0.7)
            self.item_dots.add(dot)
        
        # Initialize tracking variables
        self.current_item_index = 0
        self.selected_items = []
        self.ability_estimate = 0.0
        self.selection_path = VGroup()
        
        # Create tracer path (initially empty)
        self.tracer_points = []
        self.tracer_path = None
    
    def scene_1_setup(self):
        """Scene 1: The Setup - Animate initial components"""
        
        # 1. Animate NumberLine fading in
        self.play(
            FadeIn(self.ability_scale),
            FadeIn(self.ability_label),
            run_time=1.5
        )
        
        # 2. Animate ability indicator appearing at 0
        self.play(
            FadeIn(self.ability_indicator),
            run_time=1
        )
        
        # 3. Animate item bank appearing
        self.play(
            LaggedStart(
                *[FadeIn(dot) for dot in self.item_dots],
                lag_ratio=0.05,
                run_time=2
            )
        )
        
        # 4. Transform first item to glowing yellow
        self.current_item_index = random.randint(0, len(self.item_dots) - 1)
        first_item = self.item_dots[self.current_item_index]
        self.selected_items.append(self.current_item_index)
        
        # Create glowing effect
        glow_circle = Circle(
            radius=0.15,
            color=YELLOW,
            fill_opacity=0.3,
            stroke_width=3
        ).move_to(first_item.get_center())
        
        self.play(
            first_item.animate.set_color(YELLOW).set_fill(YELLOW, opacity=1),
            FadeIn(glow_circle),
            run_time=1
        )
        
        self.current_glow = glow_circle
        self.tracer_points.append(first_item.get_center())
        
        self.wait(0.5)
    
    def scene_2_first_response(self):
        """Scene 2: First Response and Update"""
        
        current_item = self.item_dots[self.current_item_index]
        
        # 1. Item pulses
        self.play(
            current_item.animate.scale(1.3),
            self.current_glow.animate.scale(1.3),
            rate_func=rate_functions.there_and_back,
            run_time=0.8
        )
        
        # 2. Flash green (correct answer)
        green_flash = Circle(
            radius=0.25,
            color=GREEN,
            fill_opacity=0.8,
            stroke_width=0
        ).move_to(current_item.get_center())
        
        self.play(
            FadeIn(green_flash),
            run_time=0.3
        )
        self.play(
            FadeOut(green_flash),
            run_time=0.3
        )
        
        # 3. Update ability estimate to the right
        new_ability = 0.5
        self.ability_estimate = new_ability
        new_position = self.ability_scale.n2p(new_ability)
        
        self.play(
            self.ability_indicator.animate.next_to(new_position, UP, buff=0.1),
            run_time=1.2
        )
        
        # 4. Create initial tracer point
        tracer_dot = Dot(
            point=current_item.get_center(),
            radius=0.04,
            color=YELLOW,
            fill_opacity=1
        )
        self.selection_path.add(tracer_dot)
        
        self.play(FadeIn(tracer_dot), run_time=0.5)
        
        self.wait(0.5)
    
    def scene_3_second_item(self):
        """Scene 3: The Second Item"""
        
        # 1. Transfer glow to new item
        old_item = self.item_dots[self.current_item_index]
        
        # Select adjacent item (or random if no clear adjacent)
        available_indices = [i for i in range(len(self.item_dots)) if i not in self.selected_items]
        self.current_item_index = random.choice(available_indices)
        new_item = self.item_dots[self.current_item_index]
        self.selected_items.append(self.current_item_index)
        
        # Create new glow circle
        new_glow = Circle(
            radius=0.15,
            color=YELLOW,
            fill_opacity=0.3,
            stroke_width=3
        ).move_to(new_item.get_center())
        
        self.play(
            # Old item returns to grey
            old_item.animate.set_color(GREY).set_fill(GREY, opacity=0.7),
            FadeOut(self.current_glow),
            # New item becomes yellow and glowing
            new_item.animate.set_color(YELLOW).set_fill(YELLOW, opacity=1),
            FadeIn(new_glow),
            run_time=1
        )
        
        self.current_glow = new_glow
        
        # Draw tracer line
        if len(self.tracer_points) > 0:
            line = Line(
                self.tracer_points[-1],
                new_item.get_center(),
                color=YELLOW,
                stroke_width=3,
                stroke_opacity=0.8
            )
            self.selection_path.add(line)
            self.play(Create(line), run_time=0.8)
        
        self.tracer_points.append(new_item.get_center())
        
        # Add tracer dot
        tracer_dot = Dot(
            point=new_item.get_center(),
            radius=0.04,
            color=YELLOW,
            fill_opacity=1
        )
        self.selection_path.add(tracer_dot)
        self.play(FadeIn(tracer_dot), run_time=0.3)
        
        # 2. Item pulses
        self.play(
            new_item.animate.scale(1.3),
            new_glow.animate.scale(1.3),
            rate_func=rate_functions.there_and_back,
            run_time=0.8
        )
        
        # 3. Flash red (incorrect answer)
        red_flash = Circle(
            radius=0.25,
            color=RED,
            fill_opacity=0.8,
            stroke_width=0
        ).move_to(new_item.get_center())
        
        self.play(FadeIn(red_flash), run_time=0.3)
        self.play(FadeOut(red_flash), run_time=0.3)
        
        # 4. Update ability estimate to the left
        new_ability = 0.2
        self.ability_estimate = new_ability
        new_position = self.ability_scale.n2p(new_ability)
        
        self.play(
            self.ability_indicator.animate.next_to(new_position, UP, buff=0.1),
            run_time=1.2
        )
        
        self.wait(0.5)
    
    def scene_4_iterative_process(self):
        """Scene 4: The Iterative Process"""
        
        # Define ability updates for remaining iterations (showing convergence)
        ability_updates = [0.4, 0.3, 0.35, 0.33, 0.34]  # Converging around 0.34
        responses = [True, False, True, True, False]  # Mix of correct/incorrect
        
        for i, (response, target_ability) in enumerate(zip(responses, ability_updates)):
            # Speed up later iterations
            speed_multiplier = 1 + (i * 0.3)  # Progressively faster
            base_time = max(0.5, 1.0 / speed_multiplier)
            
            # Transfer to new item
            old_item = self.item_dots[self.current_item_index]
            available_indices = [j for j in range(len(self.item_dots)) if j not in self.selected_items]
            
            if not available_indices:  # If we run out, reuse some items
                available_indices = list(range(len(self.item_dots)))
            
            self.current_item_index = random.choice(available_indices)
            new_item = self.item_dots[self.current_item_index]
            self.selected_items.append(self.current_item_index)
            
            # Create new glow
            new_glow = Circle(
                radius=0.15,
                color=YELLOW,
                fill_opacity=0.3,
                stroke_width=3
            ).move_to(new_item.get_center())
            
            # Transfer glow and create path
            self.play(
                old_item.animate.set_color(GREY).set_fill(GREY, opacity=0.7),
                FadeOut(self.current_glow),
                new_item.animate.set_color(YELLOW).set_fill(YELLOW, opacity=1),
                FadeIn(new_glow),
                run_time=base_time
            )
            
            self.current_glow = new_glow
            
            # Draw tracer line
            line = Line(
                self.tracer_points[-1],
                new_item.get_center(),
                color=YELLOW,
                stroke_width=3,
                stroke_opacity=0.8
            )
            self.selection_path.add(line)
            self.play(Create(line), run_time=base_time * 0.8)
            
            self.tracer_points.append(new_item.get_center())
            
            # Add tracer dot
            tracer_dot = Dot(
                point=new_item.get_center(),
                radius=0.04,
                color=YELLOW,
                fill_opacity=1
            )
            self.selection_path.add(tracer_dot)
            self.play(FadeIn(tracer_dot), run_time=base_time * 0.5)
            
            # Quick pulse (faster for later iterations)
            self.play(
                new_item.animate.scale(1.2),
                new_glow.animate.scale(1.2),
                rate_func=rate_functions.there_and_back,
                run_time=base_time * 0.6
            )
            
            # Flash color based on response
            flash_color = GREEN if response else RED
            flash = Circle(
                radius=0.25,
                color=flash_color,
                fill_opacity=0.8,
                stroke_width=0
            ).move_to(new_item.get_center())
            
            self.play(FadeIn(flash), run_time=base_time * 0.3)
            self.play(FadeOut(flash), run_time=base_time * 0.3)
            
            # Update ability (smaller movements showing convergence)
            self.ability_estimate = target_ability
            new_position = self.ability_scale.n2p(target_ability)
            
            self.play(
                self.ability_indicator.animate.next_to(new_position, UP, buff=0.1),
                run_time=base_time * 0.8
            )
            
            # Shorter wait for later iterations
            self.wait(base_time * 0.3)
    
    def scene_5_conclusion(self):
        """Scene 5: Conclusion"""
        
        # 1. Pause and highlight final position
        self.wait(1)
        
        # Highlight final ability position
        final_highlight = Circle(
            radius=0.2,
            color=BLUE,
            stroke_width=4,
            fill_opacity=0.2
        ).next_to(self.ability_scale.n2p(self.ability_estimate), UP, buff=0.1)
        
        self.play(
            FadeIn(final_highlight),
            self.ability_indicator.animate.set_color(BLUE_C).scale(1.3),
            run_time=1
        )
        
        # 2. Emphasize the complete selection path
        self.play(
            self.selection_path.animate.set_color(YELLOW_C).set_stroke_width(4),
            run_time=1
        )
        
        # 3. Hold for a moment
        self.wait(2)
        
        # 4. Fade to black
        all_objects = VGroup(
            self.ability_scale,
            self.ability_label,
            self.ability_indicator,
            self.item_dots,
            self.current_glow,
            self.selection_path,
            final_highlight
        )
        
        self.play(
            FadeOut(all_objects),
            run_time=2
        )
        
        self.wait(1)

# Alternative scene for faster preview/testing
class AdaptiveTestingPreview(Scene):
    def construct(self):
        # A shorter version for quick testing
        title = Text("Adaptive Testing Visualization", font_size=36)
        subtitle = Text("Item Selection & Ability Estimation", font_size=24).next_to(title, DOWN)
        
        self.play(Write(title), run_time=1)
        self.play(Write(subtitle), run_time=1)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Quick demo with fewer items
        demo = AdaptiveTestingVisualization()
        demo.item_bank_size = 12
        demo.num_iterations = 4
        demo.construct()
