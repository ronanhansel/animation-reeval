from manim import *

class Scene1(Scene):
    def construct(self):
        title_1pl = Title("1-PL Model")
        title_2pl = Title("2-PL Model")
        title_3pl = Title("3-PL Model")

        self.play(Write(title_1pl))
        self.wait(1)

        pl_1_formula = MathTex(
            r"P_{ij}\left(\theta_j,b_i\right)=\frac{\exp(\theta_j-b_i)}{1+\exp(\theta_j-b_i)}"
        )
        pl_2_formula= MathTex(
            r"P_{ij}\left(\theta_j,b_i,a_i\right)=\frac{\exp\left[a_i(\theta_j-b_i)\right]}{1+\exp\left[a_i(\theta_j-b_i)\right]}"
        )
        pl_3_formula= MathTex(
            r"P(\theta_j,a_i,b_i,c_i)=c_i+(1-c_i)\frac{\exp\left[a_i(\theta_j-b_i)\right]}{1+\exp\left[a_i(\theta_j-b_i)\right]}"
        )
        self.add(pl_1_formula)
        self.play(Write(pl_1_formula))

        self.wait(1.5)

        self.play(ReplacementTransform(title_1pl, title_2pl),
                  ReplacementTransform(pl_1_formula, pl_2_formula), run_time=0.5)

        self.wait(1.5)

        self.play(ReplacementTransform(title_2pl, title_3pl),
                  ReplacementTransform(pl_2_formula, pl_3_formula), run_time=0.5)


        self.wait(1)