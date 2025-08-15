from manim import *

class RevisiRaschFormulae(Scene):
    def construct(self):
        
        self.wait(1)
        
        # Title
        title = Text("Rasch Model Revision Formulas", font_size=36)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title))
        self.wait(1)
        
        # First formula: p_j = p(Y_{new,j} = 1 | theta_new^t, z_hat_j) = sigma(theta_new^t - b_hat_j)
        # Break it into parts for better animation
        p_j_part = MathTex(r"p_j = ")
        prob_part = MathTex(r"p\left(Y_{\text{new},j} = 1 \mid \theta_{\text{new}}^t, \hat{z}_j\right) = ")
        sigma_part = MathTex(r"\sigma\left(\theta_{\text{new}}^t - \hat{b}_j\right)")
        
        # Group the first formula
        formula1_group = VGroup(p_j_part, prob_part, sigma_part)
        formula1_group.arrange(RIGHT, buff=0.1)
        formula1_group.move_to(ORIGIN + UP * 1.5)
        
        # Animate first formula appearance
        self.play(Write(p_j_part))
        self.wait(0.5)
        self.play(Write(prob_part))
        self.wait(0.5)
        self.play(Write(sigma_part))
        self.wait(2)
        
        # Add a separator line
        separator = Line(LEFT * 4, RIGHT * 4)
        separator.move_to(ORIGIN)
        self.play(Create(separator))
        self.wait(1)
        
        # Second formula: I(theta_new^t; z_hat_j) = p_j(1 - p_j)
        fisher_info_part = MathTex(r"\mathcal{I}\left(\theta_{\text{new}}^t; \hat{z}_j\right) = ")
        variance_part = MathTex(r"p_j(1 - p_j)")
        
        # Group the second formula
        formula2_group = VGroup(fisher_info_part, variance_part)
        formula2_group.arrange(RIGHT, buff=0.1)
        formula2_group.move_to(ORIGIN + DOWN * 1.5)
        
        # Animate second formula appearance
        self.play(Write(fisher_info_part))
        self.wait(0.5)
        self.play(Write(variance_part))
        self.wait(2)
        
        # Highlight the connection between formulas
        # Highlight p_j in both formulas
        p_j_highlight_box1 = SurroundingRectangle(p_j_part, color=YELLOW, buff=0.1)
        p_j_highlight_box2 = SurroundingRectangle(variance_part[0][0:2], color=YELLOW, buff=0.1)  # p_j part in second formula
        
        self.play(Create(p_j_highlight_box1), Create(p_j_highlight_box2))
        self.wait(2)
        self.play(FadeOut(p_j_highlight_box1), FadeOut(p_j_highlight_box2))
        
        self.wait(1)
        
        # Final highlight of both complete formulas
        final_box1 = SurroundingRectangle(formula1_group, color=BLUE, buff=0.2)
        final_box2 = SurroundingRectangle(formula2_group, color=GREEN, buff=0.2)
        
        self.play(Create(final_box1))
        self.wait(0.5)
        self.play(Create(final_box2))
        self.wait(2)
        
        self.play(FadeOut(final_box1), FadeOut(final_box2))
        self.wait(2)
