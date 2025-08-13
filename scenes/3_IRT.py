from manim import *
import numpy as np

Text.set_default(font_size=34)
MathTex.set_default(font_size=34)
def icc_function(theta, a=2.5, b=0, c=0):
    """
    Calculates the probability of a correct response using the 3-Parameter Logistic (3PL) IRT model.

    Args:
        theta (float or np.array): The ability level(s).
        a (float): The discrimination parameter.
        b (float): The difficulty parameter.
        c (float): The guessing parameter (lower asymptote).
    """
    # The original 2PL probability calculation
    prob_from_ability = 1 / (1 + np.exp(-a * (theta - b)))

    # Scale the probability by the (1-c) range and add the 'c' floor
    return c + (1 - c) * prob_from_ability

class Scene1(Scene):
    """Scene 1: The Basic Item Characteristic Curve (ICC)"""
    
    def construct(self):
        # Create the coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1, 0.2],
            x_length=10,
            y_length=6,
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
            },
            tips=False
        )
        
        # Add axis labels
        y_label = axes.get_y_axis_label(r"P(\theta)", edge=UP, direction=LEFT, buff=0.3)
        x_label = axes.get_x_axis_label(r"\theta", edge=DOWN, direction=DOWN, buff=0.3)
        y_label_text = axes.get_y_axis_label(Text("Probability of correct"), edge=UP, direction=LEFT, buff=0.3)
        x_label_text = axes.get_x_axis_label(Text("Ability"), edge=DOWN, direction=DOWN, buff=0.3)

        # Create the basic ICC curve with more curvature
        icc_curve = axes.plot(
            lambda theta: icc_function(theta, a=2.5, b=0),
            color=BLUE,
            stroke_width=4,
            x_range=[-4, 4]
        )

        initial_y_label = y_label.copy()
        initial_x_label = x_label.copy()
        
        # Animate the creation of axes
        self.play(Create(axes), Write(initial_y_label), Write(initial_x_label))

        self.wait(1)

        self.play(ReplacementTransform(initial_y_label, y_label_text))

        self.wait(1)

        self.play(ReplacementTransform(initial_x_label, x_label_text))
        
        self.wait(1)

        self.play(ReplacementTransform(y_label_text, y_label.copy()),
                  ReplacementTransform(x_label_text, x_label.copy()))
        
        # Animate the drawing of the sigmoid curve
        self.play(Create(icc_curve), run_time=2)
        
        # Hold the final state
        self.wait(2)


class Scene2(Scene):
    """Scene 2: Visualizing the 'Difficulty' Parameter (b)"""
    
    def construct(self):
        # Create the same coordinate system as Scene 1
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1, 0.2],
            x_length=10,
            y_length=6,
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
            },
            tips=False
        )
        

        # Create animated counter for b parameter
        b_tracker = ValueTracker(0)
        
        # Create dynamic label that updates with b_tracker
        dynamic_y_label = always_redraw(lambda: axes.get_y_axis_label(
            rf"P(\theta, b={b_tracker.get_value():.1f})", 
            edge=UP, 
            direction=LEFT, 
            buff=0.3
        ))
        x_label = axes.get_x_axis_label(r"\theta", edge=DOWN, direction=DOWN, buff=0.3)
        
        # Create the basic ICC curve with more curvature
        original_curve = always_redraw(lambda: axes.plot(
            lambda theta: icc_function(theta, a=2.5, b=b_tracker.get_value()),
            color=BLUE,
            stroke_width=4,
            x_range=[-4, 4]
        ))

        # Start with the basic setup
        self.add(axes, dynamic_y_label, x_label, original_curve)

        self.wait(1)
        
        # Perform the transformation to difficult curve (b=2) with animated counter
        self.play(
            b_tracker.animate.set_value(2),
            run_time=2
        )

        self.wait(1)

        # Transform to easy curve (b=-2) with animated counter
        self.play(
            b_tracker.animate.set_value(-2),
            run_time=2
        )

        self.wait(1)

        # Transform back to original curve (b=0) with animated counter
        self.play(
            b_tracker.animate.set_value(0),
            run_time=2
        )
        
        # Hold the final state
        self.wait(3)


class Scene3(Scene):
    """Scene 3: Visualizing the 'Discrimination' Parameter (a)"""
    
    def construct(self):
        # Create the same coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1, 0.2],
            x_length=10,
            y_length=6,
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
            },
            tips=False
        )
        
        # Create animated counter for a parameter
        a_tracker = ValueTracker(2.5)

        # Create dynamic label that updates with a_tracker
        dynamic_y_label = always_redraw(lambda: axes.get_y_axis_label(
            rf"P(\theta, b, a={a_tracker.get_value():.1f})",
            edge=UP, 
            direction=LEFT, 
            buff=0.3
        ))
        x_label = axes.get_x_axis_label(r"\theta", edge=DOWN, direction=DOWN, buff=0.3)
        
        # Sigmoid function
        def sigmoid(x, a=1, b=0):
            return 1 / (1 + np.exp(-a * (x - b)))
        
        original_curve = always_redraw(lambda: axes.plot(
            lambda x: sigmoid(x, a=a_tracker.get_value(), b=0),
            x_range=[-4, 4],
            color=BLUE,
            stroke_width=4
        ))

        # Start with the basic setup
        self.add(axes, dynamic_y_label, x_label, original_curve)
        
        self.wait(1)

        # First show the high discrimination curve transformation
        self.play(
            a_tracker.animate.set_value(1),
            run_time=2.5
        )
        self.wait(1)
        self.play(
            a_tracker.animate.set_value(6),
            run_time=2.5
        )
        # Hold the final state
        self.wait(4)

class Scene4(Scene):
    """Scene 4: Visualizing the 'Guessing' Parameter (c)"""
    
    def construct(self):
        # Create the same coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1, 0.2],
            x_length=10,
            y_length=6,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=False
        )
        x_label = axes.get_x_axis_label(r"\theta", edge=DOWN, direction=DOWN, buff=0.3)

        # Create animated counter for the c parameter
        c_tracker = ValueTracker(0)

        # Create a dynamic label that updates with c_tracker
        dynamic_y_label = always_redraw(lambda: axes.get_y_axis_label(
            rf"P(\theta, b, a, c={c_tracker.get_value():.2f})",
            edge=UP, 
            direction=LEFT, 
            buff=0.3
        ))

        # Create the initial ICC curve with a low guessing parameter
        # We use always_redraw so the curve morphs as the tracker changes
        icc_curve = always_redraw(lambda: axes.plot(
            lambda theta: icc_function(theta, a=1.5, b=0, c=c_tracker.get_value()),
            color=BLUE,
            stroke_width=4,
            x_range=[-4, 4]
        ))

        # Dashed line to show the "floor" set by the c-parameter
        c_line = always_redraw(lambda: DashedLine(
            start=axes.c2p(-4, c_tracker.get_value()),
            end=axes.c2p(4, c_tracker.get_value()),
            color=YELLOW,
            stroke_width=3,
        ))
        
        c_line_label = always_redraw(lambda: MathTex("c", color=YELLOW).next_to(c_line, LEFT, buff=0.2))

        # Add initial objects to the scene
        self.add(axes, x_label, dynamic_y_label, icc_curve)
        self.wait(1)
        self.play(Create(c_line), Write(c_line_label))

        # Animate the c-parameter increasing to 0.25 (e.g., a 4-option MC question)
        self.play(
            c_tracker.animate.set_value(0.25),
            run_time=3
        )
        self.wait(1)

        # Animate the c-parameter decreasing back to almost zero
        self.play(
            c_tracker.animate.set_value(0.05),
            run_time=3
        )
        
        # Hold the final state
        self.wait(2)