from manim import *

class IRT(Scene):
    def construct(self):
        self.play(Write(Title("Item Response Theory")))
        self.wait(1)

        irt_formula = MathTex(
            r"P_{i,j}",  # 0
            r"(",        # 1
            r"\theta_j", # 2
            r",",        # 3
            r"b_i",      # 3
            r",",        # 5
            r"a_i",      # 6
            r",",        # 7
            r"c_i",      # 8
            r")",        # 9
        )

        self.add(irt_formula)
        self.play(Write(irt_formula))
        self.wait(1)

        # Labels (mirroring style from 2_ctt.py)
        corr_label = (
            Tex("Correct probability")
                .scale(0.55)
                .set_color(GREEN)
                .next_to(irt_formula[0], UP, buff=0.35)
        )
        ability_label = (
            Tex("Ability")
                .scale(0.55)
                .set_color(BLUE)
                .next_to(irt_formula[2], DOWN, buff=0.35)
        )
        traits_group = VGroup(irt_formula[4], irt_formula[6], irt_formula[8])
        traits_label = (
            Tex("Traits")
                .scale(0.55)
                .set_color(RED)
                .next_to(traits_group, UP, buff=0.35)
        )

        # Highlight theta
        self.play(
            irt_formula[2].animate.set_color(BLUE),  # \theta_j
            FadeIn(ability_label, shift=UP*0.1),
            run_time=0.8,
        )
        self.wait(1.5)

        # Highlight b_i, a_i, c_i
        self.play(
            irt_formula[4].animate.set_color(RED),   # b_i
            irt_formula[6].animate.set_color(RED),   # a_i
            irt_formula[8].animate.set_color(RED),  # c_i
            FadeIn(traits_label, shift=UP*0.1),
            run_time=0.8,
        )
        self.wait(1.5)

        # Highlight P_{i,j} and brackets
        self.play(
            FadeIn(corr_label, shift=UP*0.1),
            irt_formula[0].animate.set_color(GREEN),  # P_{i,j} (left side)
            irt_formula[1].animate.set_color(GREEN),  # (
            irt_formula[9].animate.set_color(GREEN), # )
            run_time=0.8,
        )
        self.wait(1.5)

        # Remove labels and colours
        self.play(irt_formula.animate.set_color(WHITE),
                FadeOut(VGroup(corr_label, ability_label, traits_label)), run_time=0.6)

        self.wait(1)