from manim import *

class Scene1(Scene):
    def construct(self):

        self.wait(1)

        lhs = MathTex(r"p\left(", r"Y_{i,j}", r"|b_i\right) = ")
        rhs_exp = MathTex(r"\frac{\exp(\theta_j-b_i)}{1+\exp(\theta_j-b_i)}")

        expr_group = VGroup(lhs, rhs_exp)
        expr_group.arrange(RIGHT, buff=0.2)
        original_center = expr_group.get_center()

        self.play(Write(lhs))
        self.play(Write(rhs_exp))
        self.wait(1)

        rhs_sigma = MathTex(r"\sigma(\theta_j-b_i)").move_to(rhs_exp)
        self.play(ReplacementTransform(rhs_exp, rhs_sigma))
        self.play(rhs_sigma.animate.next_to(lhs, RIGHT, buff=0.2))
        self.play(VGroup(lhs, rhs_sigma).animate.move_to(original_center))
        self.wait(1)

        # Color the Y_{i,j} part in the lhs
        self.play(lhs[1].animate.set_color(YELLOW), run_time=0.2)
        self.wait(1)
        self.play(lhs[1].animate.set_color(WHITE), run_time=0.2)
        self.wait(1)