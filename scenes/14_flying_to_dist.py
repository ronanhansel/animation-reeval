from manim import *
import random
import numpy as np

class RacingCircles(Scene):
    def construct(self):
        # Set random seed for reproducible results (optional)
        random.seed(42)
        np.random.seed(42)
        
        # 1. Create the main circle in the center
        main_circle = Circle(radius=0.5, color=GRAY, fill_opacity=1.0)
        main_circle.move_to(ORIGIN)
        
        # Animate the appearance of the main circle
        self.play(FadeIn(main_circle, scale=0.5))
        self.wait(0.5)
        
        # 2. Generate the racer circles (positioned off-screen to the left)
        num_racers = 50
        racer_circles = []
        
        for i in range(num_racers):
            # Vary circle sizes slightly
            radius = random.uniform(0.35, 0.4)
            
            # Create grey circle with lower opacity
            circle = Circle(radius=radius, color=GRAY, fill_opacity=0.15)
            
            # Position circles off-screen to the left
            x_offset = random.uniform(-14, -12)  # Start from far left (off-screen)
            y_offset = random.uniform(-4, 4)    # Spread vertically across screen
            
            circle.move_to([x_offset, y_offset, 0])
            racer_circles.append(circle)
        
        # Add all racer circles to the scene (they're off-screen so not visible yet)
        self.add(*racer_circles)
        
        # 3. The Race Animation - circles racing in from the left
        race_animations = []
        
        # List of different rate functions for varied acceleration
        rate_functions_list = [
            # rate_functions.ease_in_sine,
            # rate_functions.ease_in_quad,
            # rate_functions.ease_in_cubic,
            # rate_functions.ease_in_quart,
            rate_functions.ease_in_expo,
            # rate_functions.ease_out_sine,
            # rate_functions.ease_out_quad,
            # rate_functions.ease_in_out_sine,
            # rate_functions.ease_in_out_quad,
            # rate_functions.linear,
            # rate_functions.smooth,
        ]
        
        # Create custom rate functions for more variety
        def custom_acceleration_1(t):
            return t ** 2

        # Add custom functions to the list
        rate_functions_list.extend([custom_acceleration_1])
        
        for i, circle in enumerate(racer_circles):
            # Random destination (off-screen to the right)
            end_x = random.uniform(10, 14)
            end_y = circle.get_y() + random.uniform(-0.5, 0.5)  # Slight y variation
            end_position = [end_x, end_y, 0]
            
            # Random run time (speed variation)
            run_time = random.uniform(2, 4)
            
            # Random rate function (acceleration pattern)
            rate_func = random.choice(rate_functions_list)
            
            # Create the movement animation
            move_animation = circle.animate(
                run_time=run_time,
                rate_func=rate_func
            ).move_to(end_position)
            
            race_animations.append(move_animation)
        
        # Execute all race animations simultaneously
        self.play(*race_animations)
        
        self.wait(2)

class NormalDistributionFormation(Scene):
    def construct(self):
        # Set random seed for reproducible results
        random.seed(42)
        np.random.seed(42)
        
        # Parameters for the bell curve outline
        num_circles = 200
        
        # Create circles that will form the bell curve outline
        circles = []
        animations = []
        
        # Define the bell curve function
        def bell_curve(x, mu=0, sigma=1.2):
            return 2.5 * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        
        # Generate points along the bell curve outline
        x_range = np.linspace(-4, 4, num_circles // 2)  # Half the circles for one side
        
        # Create circles for both sides of the bell curve
        for i, x in enumerate(x_range):
            y = bell_curve(x)
            
            # Create two circles - one for each side of the curve
            for side in [-1, 1]:  # Left and right side
                if i < len(x_range):  # Make sure we don't exceed our circle count
                    # Create small grey circles
                    radius = random.uniform(0.04, 0.05)
                    circle = Circle(radius=radius, color=GRAY, fill_opacity=0.5)
                    
                    # Start position: off-screen to the left
                    start_x = random.uniform(-10, -8)
                    start_y = random.uniform(-3, 3)
                    circle.move_to([start_x, start_y, 0])
                    
                    # Target position: on the bell curve outline
                    target_x = x * side  # Mirror for both sides
                    target_y = y - 1.25  # Center the curve vertically
                    
                    # Add slight randomness for natural look
                    target_x += random.uniform(-0.05, 0.05)
                    target_y += random.uniform(-0.05, 0.05)
                    
                    target_position = [target_x, target_y, 0]
                    
                    # Varied timing and acceleration
                    run_time = random.uniform(2.0, 4.5)
                    
                    # Rate functions for varied movement
                    rate_functions_list = [
                        rate_functions.ease_in_out_sine
                    ]
                    
                    rate_func = random.choice(rate_functions_list)
                    
                    # Create movement animation
                    move_animation = circle.animate(
                        run_time=run_time,
                        rate_func=rate_func
                    ).move_to(target_position)
                    
                    circles.append(circle)
                    animations.append(move_animation)
        

        
        # Add all circles to scene (off-screen initially)
        self.add(*circles)
        
        # Execute all animations simultaneously to form the bell curve outline
        self.play(*animations)
        
        # Hold the final formation
        self.wait(3)