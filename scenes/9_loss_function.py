from manim import *

class BuildLossFunctionBestPractice(Scene):
    def construct(self):
        # 1. Define the three stages using the {{...}} syntax.
        # This makes the matching process more explicit and reliable.
        stage1 = MathTex(r"{{ \log P(Y_{i,j}|p_i) }}")
        
        stage2 = MathTex(
            r"{{ \frac{1}{N}\sum_{i=1}^{N} }} {{ \log P(Y_{i,j}|p_i) }}"
        )
        
        stage3 = MathTex(
            r"{{ - }}",
            r"{{ \frac{1}{N}\sum_{i=1}^{N} }} {{ \log P(Y_{i,j}|p_i) }}"
        )

        stage4 = MathTex(
            r"{{ \mathcal{L} }} {{ = }}",
            r"{{ - }}",
            r"{{ \frac{1}{N}\sum_{i=1}^{N} }} {{ \log P(Y_{i,j}|p_i) }}"
        )

        # --- Animation Sequence ---
        # The animation logic is identical, but now it's more robust.

        # Step 1: Start with the log-probability term
        self.play(Write(stage1))
        self.wait(1.5)

        # Step 2: Add the sum and average
        # Manim clearly matches the 'log P' part from stage1 to stage2.
        self.play(TransformMatchingTex(stage1, stage2))
        self.wait(1.5)

        # Step 3: Complete the loss function
        # Manim now matches the 'sum' and 'log P' parts from stage2 to stage3.
        self.play(TransformMatchingTex(stage2, stage3))
        self.wait(1.5)

        # Step 4: Add the loss function
        self.play(TransformMatchingTex(stage3, stage4))
        self.wait(1.5)