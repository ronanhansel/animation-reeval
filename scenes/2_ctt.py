from manim import *

class CTTAlgo(Scene):
    def construct(self):
        self.play(Write(Title("Classical Test Theory")))
        self.wait(1)


        ctt_formula = MathTex(
            r"X = T + e",
        )

        self.add(ctt_formula)
        self.play(Write(ctt_formula))
        self.wait(1)
        
        # Add labels for each component (tuned spacing)
        obs_label = (
            Tex("Observed score")
                .scale(0.55)
                .next_to(ctt_formula[0][0], DOWN, buff=0.35)
        )
        true_label = (
            Tex("True score")
                .scale(0.55)
                .set_color(BLUE)
                .next_to(ctt_formula[0][2], UP, buff=0.35)
        )
        error_label = (
            Tex("Random error")
                .scale(0.55)
                .set_color(RED)
                .next_to(ctt_formula[0][4], DOWN, buff=0.35)
        )

        # Show X label first
        self.play(FadeIn(obs_label, shift=UP*0.1))
        self.wait(0.6)
        
        # Highlight the Error component
        self.play(
            ctt_formula[0][4].animate.set_color(RED),
            FadeIn(error_label, shift=UP*0.1),
            run_time=0.8,
        )
        self.wait(1.5)

        # Highlight the True Score component
        self.play(
            ctt_formula[0][2].animate.set_color(BLUE),
            FadeIn(true_label, shift=UP*0.1),
            run_time=0.8,
        )
        self.wait(1.5)

        # Reset all colors to white
        self.play(ctt_formula.animate.set_color(WHITE), run_time=0.6)
        # Remove labels
        self.play(FadeOut(VGroup(obs_label, true_label, error_label)), run_time=0.6)
        # Box the formula
        box = SurroundingRectangle(ctt_formula, color=WHITE, buff=0.3)
        self.play(Create(box), run_time=0.6)
        self.wait(1)