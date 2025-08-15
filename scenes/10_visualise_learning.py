import json
import numpy as np
from manim import *

Text.set_default(font_size=24)

class VisualizeLearningScene(Scene):
    def construct(self):
        # Load data
        z_data, theta_data = self.load_data()

        # We'll create different axes for each phase
        # Start with Z axes (will be replaced later)
        # The excess tick at 0.5 on the y-axis is due to y_range and numbers_to_include not matching.
        # To avoid an extra tick at 0.5, set y_range to [0, 0.4, 0.1] and numbers_to_include to np.arange(0, 0.5, 0.1)
        z_axes = Axes(
            x_range=[-4, 4, 0.5],
            y_range=[0, 0.4, 0.1],
            x_length=10,
            y_length=5,
            axis_config={"color": BLUE, "include_tip": False},
            x_axis_config={"numbers_to_include": np.arange(-4, 5, 1)},
            y_axis_config={"numbers_to_include": np.arange(0, 0.5, 0.1)},  # Only up to 0.4
        )

        # Create theta axes (different y-range)
        theta_axes = Axes(
            x_range=[-4, 4, 0.5],
            y_range=[0, 1, 0.2],
            x_length=10,
            y_length=5,
            axis_config={"color": BLUE, "include_tip": False},
            x_axis_config={"numbers_to_include": np.arange(-4, 5, 1)},
            y_axis_config={"numbers_to_include": np.arange(0, 1.1, 0.2)},
        )
        
        # Start with Z axes
        self.add(z_axes)
        current_axes = z_axes
        
        # Legend (will be added later during theta phase)
        
        # Phase 1: Show Z distributions (iterations 0-3)
        z_iterations = len(z_data)  # Should be 4
        theta_iterations = len(theta_data)  # Should be 14
        
        # Phase 1: Z Distribution Animation
        current_hist = None
        
        for iteration in range(z_iterations):
            z_values = z_data[iteration]
            z_hist = self.create_histogram(z_values, current_axes, RED, 0.7)
            
            
            if iteration == 0:
                # First iteration: create histogram
                self.play(
                    Create(z_hist),
                    run_time=1.5
                )
                current_hist = z_hist
            else:
                self.play(ReplacementTransform(current_hist, z_hist), run_time=1.0)
                current_hist = z_hist
            
            self.wait(0.1)
        
        # Keep the final Z histogram and switch to theta axes
        # First, rescale the Z histogram for the new theta axes range
        final_z_values = z_data[-1]  # Get the last Z iteration
        final_z_hist_rescaled = self.create_histogram(final_z_values, theta_axes, RED, 0.4)  # Lower opacity
        
        self.play(
            ReplacementTransform(current_hist, final_z_hist_rescaled),  # Rescale Z histogram
            ReplacementTransform(current_axes, theta_axes),
            run_time=1.5
        )
        
        # Update current axes references
        current_axes = theta_axes
        final_z_histogram = final_z_hist_rescaled  # Keep reference to the Z histogram
        
        # Phase 2: Theta Distribution Animation
        current_theta_hist = None
        
        for iteration in range(theta_iterations):
            theta_values = theta_data[iteration]
            theta_hist = self.create_histogram(theta_values, current_axes, BLUE, 0.6)  # Semi-transparent
            
            if iteration == 0:
                # First theta iteration: create histogram (Z histogram stays in background)
                self.play(
                    Create(theta_hist),
                    run_time=1.5
                )
                current_theta_hist = theta_hist
            else:
                # Smoothly transform theta histogram bars (Z histogram remains unchanged)
                self.play(ReplacementTransform(current_theta_hist, theta_hist), run_time=1.0)
                current_theta_hist = theta_hist
            
            self.wait(0.1)
        
        self.wait(2)
    
    def load_data(self):
        """Load theta and z batch data"""
        # Load theta data
        theta_data = []
        with open('/Users/ronan/Library/CloudStorage/OneDrive-LECOLECO.,LTD/Media - Personal/REEVAL/animation/data/rasch_global_theta.jsonl', 'r') as f:
            for line in f:
                entry = json.loads(line.strip())
                theta_data.append(entry['parameters']['theta'])
        
        # Load z batch data (combine both batches)
        z_data = []
        
        # Load first batch
        with open('/Users/ronan/Library/CloudStorage/OneDrive-LECOLECO.,LTD/Media - Personal/REEVAL/animation/data/rasch_global_z_batch_0_50000.jsonl', 'r') as f:
            z_batch_1 = []
            for line in f:
                entry = json.loads(line.strip())
                z_batch_1.append(entry['parameters']['z'])
        
        # Load second batch
        with open('/Users/ronan/Library/CloudStorage/OneDrive-LECOLECO.,LTD/Media - Personal/REEVAL/animation/data/rasch_global_z_batch_50000_78712.jsonl', 'r') as f:
            z_batch_2 = []
            for line in f:
                entry = json.loads(line.strip())
                z_batch_2.append(entry['parameters']['z'])
        
        # Combine z batches for each iteration
        max_iterations = min(len(z_batch_1), len(z_batch_2))
        for i in range(max_iterations):
            combined_z = z_batch_1[i] + z_batch_2[i]  # Concatenate the two batches
            z_data.append(combined_z)
        
        return z_data, theta_data
    
    def create_histogram(self, data, axes, color, opacity):
        """Create a normalized histogram (density) from data values"""
        # Create bins
        bins = np.arange(-4, 4.2, 0.2)
        density, _ = np.histogram(data, bins=bins, density=True)
        
        # Scale density to fit within axes range
        max_density = np.max(density)
        axes_max_y = axes.y_range[1]  # Get the maximum y value from axes
        
        if max_density > axes_max_y:
            # Scale down all density values to fit within axes range
            scale_factor = (axes_max_y * 0.9) / max_density  # Use 90% of max to leave some headroom
            density = density * scale_factor
        
        # Create rectangles for histogram - ALWAYS create all bars for consistent structure
        rectangles = VGroup()
        bin_width = 0.2
        
        for i, dens in enumerate(density):
            bin_left = bins[i]
            bin_center = bin_left + bin_width / 2
            
            # Create rectangle even if density is 0 (for smooth transformations)
            if dens > 0:
                rect_height = axes.c2p(0, dens)[1] - axes.c2p(0, 0)[1]
            else:
                rect_height = 0.01  # Minimum height for zero bars
            
            rect_width = axes.c2p(bin_width, 0)[0] - axes.c2p(0, 0)[0]
            
            rect = Rectangle(
                height=max(rect_height, 0.01),
                width=rect_width,
                fill_color=color,
                fill_opacity=opacity if dens > 0 else 0.1,  # Lower opacity for zero bars
                stroke_width=1 if dens > 0 else 0,
                stroke_color=color if dens > 0 else GRAY
            )
            
            # Position rectangle properly
            if dens > 0:
                rect.move_to(axes.c2p(bin_center, dens/2))
            else:
                rect.move_to(axes.c2p(bin_center, 0.005))  # Position zero bars at bottom
                
            rectangles.add(rect)
        
        return rectangles


class HistogramSplitMergeScene(Scene):
    def construct(self):
        # Load data to get final distributions
        z_data, theta_data = self.load_data()
        final_z_values = z_data[-1]  # Last Z iteration
        final_theta_values = theta_data[-1]  # Last Theta iteration

        # Create dummy axes for histogram creation (won't be displayed)
        dummy_axes = Axes(
            x_range=[-4, 4, 0.5],
            y_range=[0, 1, 0.2],
            x_length=10,
            y_length=5,
            axis_config={"color": BLUE, "include_tip": False},
            x_axis_config={"numbers_to_include": np.arange(-4, 5, 1)},
            y_axis_config={"numbers_to_include": np.arange(0, 1.1, 0.2)},
        )
        
        # Create the overlapping histograms (final state)
        z_hist = self.create_histogram(final_z_values, dummy_axes, RED, 0.4)
        theta_hist = self.create_histogram(final_theta_values, dummy_axes, BLUE, 0.6)
        
        # Initial setup - show overlapping histograms
        self.play(
            Create(z_hist),
            Create(theta_hist),
            run_time=2.0
        )
        self.wait(1)
        
        # Zoom out to make space for splitting
        camera_group = VGroup(z_hist, theta_hist)
        self.play(
            camera_group.animate.scale(0.7),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Split animation
        self.play(
            # Split the histograms
            z_hist.animate.shift(LEFT * 4),
            theta_hist.animate.shift(RIGHT * 4),
            run_time=1
        )
        self.wait(2)
        
        # Merge back animation
        self.play(
            # Move histograms back to center
            z_hist.animate.shift(RIGHT * 4),  # Move Z back from left to center
            theta_hist.animate.shift(LEFT * 4),  # Move Theta back from right to center
            run_time=1
        )
        self.wait(1)
        
        # Zoom back in
        final_group = VGroup(z_hist, theta_hist)
        self.play(
            final_group.animate.scale(1/0.7),  # Reverse the initial scaling
            run_time=1
        )
        
        self.wait(3)
    
    def load_data(self):
        """Load theta and z batch data (same as original scene)"""
        # Load theta data
        theta_data = []
        with open('/Users/ronan/Library/CloudStorage/OneDrive-LECOLECO.,LTD/Media - Personal/REEVAL/animation/data/rasch_global_theta.jsonl', 'r') as f:
            for line in f:
                entry = json.loads(line.strip())
                theta_data.append(entry['parameters']['theta'])
        
        # Load z batch data (combine both batches)
        z_data = []
        
        # Load first batch
        with open('/Users/ronan/Library/CloudStorage/OneDrive-LECOLECO.,LTD/Media - Personal/REEVAL/animation/data/rasch_global_z_batch_0_50000.jsonl', 'r') as f:
            z_batch_1 = []
            for line in f:
                entry = json.loads(line.strip())
                z_batch_1.append(entry['parameters']['z'])
        
        # Load second batch
        with open('/Users/ronan/Library/CloudStorage/OneDrive-LECOLECO.,LTD/Media - Personal/REEVAL/animation/data/rasch_global_z_batch_50000_78712.jsonl', 'r') as f:
            z_batch_2 = []
            for line in f:
                entry = json.loads(line.strip())
                z_batch_2.append(entry['parameters']['z'])
        
        # Combine z batches for each iteration
        max_iterations = min(len(z_batch_1), len(z_batch_2))
        for i in range(max_iterations):
            combined_z = z_batch_1[i] + z_batch_2[i]  # Concatenate the two batches
            z_data.append(combined_z)
        
        return z_data, theta_data
    
    def create_histogram(self, data, axes, color, opacity):
        """Create a normalized histogram (density) from data values (same as original scene)"""
        # Create bins
        bins = np.arange(-4, 4.2, 0.2)
        density, _ = np.histogram(data, bins=bins, density=True)
        
        # Scale density to fit within axes range
        max_density = np.max(density)
        axes_max_y = axes.y_range[1]  # Get the maximum y value from axes
        
        if max_density > axes_max_y:
            # Scale down all density values to fit within axes range
            scale_factor = (axes_max_y * 0.9) / max_density  # Use 90% of max to leave some headroom
            density = density * scale_factor
        
        # Create rectangles for histogram - ALWAYS create all bars for consistent structure
        rectangles = VGroup()
        bin_width = 0.2
        
        for i, dens in enumerate(density):
            bin_left = bins[i]
            bin_center = bin_left + bin_width / 2
            
            # Create rectangle even if density is 0 (for smooth transformations)
            if dens > 0:
                rect_height = axes.c2p(0, dens)[1] - axes.c2p(0, 0)[1]
            else:
                rect_height = 0.01  # Minimum height for zero bars
            
            rect_width = axes.c2p(bin_width, 0)[0] - axes.c2p(0, 0)[0]
            
            rect = Rectangle(
                height=max(rect_height, 0.01),
                width=rect_width,
                fill_color=color,
                fill_opacity=opacity if dens > 0 else 0.1,  # Lower opacity for zero bars
                stroke_width=1 if dens > 0 else 0,
                stroke_color=color if dens > 0 else GRAY
            )
            
            # Position rectangle properly
            if dens > 0:
                rect.move_to(axes.c2p(bin_center, dens/2))
            else:
                rect.move_to(axes.c2p(bin_center, 0.005))  # Position zero bars at bottom
                
            rectangles.add(rect)
        
        return rectangles
