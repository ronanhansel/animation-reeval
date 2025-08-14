from manim import *

class EMAlgorithmSteps(Scene):
    def construct(self):
        e_step = MathTex(
            r"\text{E step: }",
            r"p(Y_{i,j} \mid f_{\phi_t}(e_j)) = \mathbb{E}_{\theta_i} p(Y_{i,j} \mid \theta_i, f_{\phi_t}(e_j)) \forall i \in [M]",
            substrings_to_isolate=["\text{E step: }"]
        )
        m_step = MathTex(
            r"\text{M step: }",
            r"\phi_{t+1} = \arg\max_{\phi_t} \sum_{i=1}^M \log p(Y_{i,j} \mid f_{\phi_t} \circ f_\omega(q_j)).",
            substrings_to_isolate=["\text{M step: }"]
        )

        # Left align both equations
        e_step[0].set_color(WHITE)
        m_step[0].set_color(WHITE)
        e_step.align_to(e_step, LEFT)
        m_step.align_to(e_step, LEFT)

        # Group vertically and center the group
        group = VGroup(e_step, m_step).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        group.move_to(ORIGIN)

        # Only show e_step at first
        m_step.set_opacity(0)
        self.add(group)
        self.play(Write(e_step))
        self.wait(2)
        # Make m_step visible and animate its writing
        m_step.set_opacity(1)
        self.play(Write(m_step))
        self.wait(2)

        # Fade out M step
        self.play(FadeOut(m_step))
        self.wait(0.5)