from manim import *

class MFIAlgorithmFlow(Scene):
    def construct(self):
        # Create the three formulae
        formula1 = MathTex(
            r"I(\theta^t_{\text{new}}, \hat{z}_j) = p_j(1-p_j)",
            font_size=36
        )
        
        formula2 = MathTex(
            r"\hat{b}_j^{*t}, q_j^{*t} = \arg\max_{b_j, q_j \in Q^t} I(\theta^t_{\text{new}}, \hat{z}_j), \quad Q^{t+1} = Q^t \setminus \{q_j^{*t}\}",
            font_size=30
        )
        
        formula3 = MathTex(
            r"\theta^{t+1}_{\text{new}} = \arg\max_\theta \sum_{j=1}^t \log p(Y_{\text{new},j} | \theta, \hat{b}_j)",
            font_size=32
        )
        
        # Position formulae vertically with spacing
        formula1.move_to(UP * 2.5)
        formula2.move_to(ORIGIN)
        formula3.move_to(DOWN * 2.5)

        # Show all formulae first
        self.play(
            Write(formula1),
            run_time=2
        )
        self.wait(1)
        
        self.play(
            Write(formula2),
            run_time=2
        )
        self.wait(1)
        
        self.play(
            Write(formula3),
            run_time=2
        )
        self.wait(1)
        
        # Create arrows
        # Arrow 1 -> 2
        arrow1_2 = Arrow(
            start=formula1.get_bottom() + DOWN * 0.2,
            end=formula2.get_top() + UP * 0.2,
            color=WHITE,
            buff=0.1,
            stroke_width=4
        )
        
        # Arrow 2 -> 3  
        arrow2_3 = Arrow(
            start=formula2.get_bottom() + DOWN * 0.2,
            end=formula3.get_top() + UP * 0.2,
            color=WHITE,
            buff=0.1,
            stroke_width=4
        )
        
        # Curved arrow 3 -> 1
        # Create a curved path from formula3 to formula1
        start_point = formula3.get_left() + LEFT * 0.5
        end_point = formula1.get_left() + LEFT * 0.5
        
        # Create control points for the curved arrow
        control1 = start_point + LEFT * 2 + UP * 1
        control2 = end_point + LEFT * 2 + DOWN * 1
        
        curved_arrow = CurvedArrow(
            start_point=start_point,
            end_point=end_point,
            color=WHITE,
            stroke_width=4,
            angle=-TAU/4  # Makes it curve to the left
        )
        
        # Animate arrows in sequence
        self.play(
            Create(arrow1_2),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Highlight the flow with brief color changes
        self.play(
            formula2.animate.set_color(YELLOW),
            run_time=0.5
        )
        self.play(
            formula2.animate.set_color(WHITE),
            run_time=0.5
        )
        
        self.play(
            Create(arrow2_3),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Highlight formula 3
        self.play(
            formula3.animate.set_color(YELLOW),
            run_time=0.5
        )
        self.play(
            formula3.animate.set_color(WHITE),
            run_time=0.5
        )
        
        self.play(
            Create(curved_arrow),
            run_time=2
        )

        self.wait(2)
