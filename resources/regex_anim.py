from manim import *

class RegexMatch(Scene):
    def setup(self):
        self.camera.frame_width = 20.0
        self.camera.frame_height = 20.0 * (9/16)
    def construct(self):
        # 1. Setup the Scene Data
        regex_str = r"(abc|def)+_..._x*y?"
        target_str = "abcdefabc_xyz_xx"
        
        # VGroups for characters
        regex_mobs = VGroup(*[Text(c, font="Monospace") for c in regex_str]).arrange(RIGHT, buff=0.4)
        target_mobs = VGroup(*[Text(c, font="Monospace") for c in target_str]).arrange(RIGHT, buff=0.4)
        
        # Create a margin so it's not touching the screen edges
        screen_margin = config.frame_width - 1.5 

        # Scale Regex if too wide
        if regex_mobs.width > screen_margin:
            regex_mobs.scale(screen_margin / regex_mobs.width)

        # Scale Target String if too wide
        if target_mobs.width > screen_margin:
            target_mobs.scale(screen_margin / target_mobs.width)

        # Re-center them horizontally after scaling
        regex_mobs.move_to(UP * 1.5)
        target_mobs.move_to(DOWN * 0.5)
        
        regex_label = Text("Regex:", font_size=30, color=YELLOW).next_to(regex_mobs, LEFT, buff=1)
        target_label = Text("String:", font_size=30, color=BLUE).next_to(target_mobs, LEFT, buff=1)
        
        self.play(Write(regex_label), Write(regex_mobs))
        self.play(Write(target_label), Write(target_mobs))
        
        # 2. Setup the Pointers (Arrows)
        # Starting slightly off-screen to the left of the first char
        r_ptr = Arrow(start=UP, end=ORIGIN, color=YELLOW, buff=0.1).scale(0.5)
        t_ptr = Arrow(start=DOWN, end=ORIGIN, color=BLUE, buff=0.1).scale(0.5)
        
        r_ptr.next_to(regex_mobs[0], UP)
        t_ptr.next_to(target_mobs[0], DOWN)
        
        self.play(FadeIn(r_ptr), FadeIn(t_ptr))
        
        # 3. Define the Animation Step Helper
        def animate_step(r_idx, t_idx, action="eval"):
            anims = []
            
            # Move Regex Pointer safely
            if 0 <= r_idx < len(regex_mobs):
                anims.append(r_ptr.animate.next_to(regex_mobs[r_idx], UP))
            else: # Point past the end
                anims.append(r_ptr.animate.next_to(regex_mobs[-1], UP).shift(RIGHT * 0.8))
            
            # Move Target String Pointer safely
            if 0 <= t_idx < len(target_mobs):
                anims.append(t_ptr.animate.next_to(target_mobs[t_idx], DOWN))
            else: # Point past the end
                anims.append(t_ptr.animate.next_to(target_mobs[-1], DOWN).shift(RIGHT * 0.8))
                
            if anims:
                self.play(*anims, run_time=0.4)
                
            if action == "match":
                match_anims = []
                if 0 <= r_idx < len(regex_mobs):
                    match_anims.append(regex_mobs[r_idx].animate.set_color(GREEN))
                if 0 <= t_idx < len(target_mobs):
                    match_anims.append(target_mobs[t_idx].animate.set_color(GREEN))
                if match_anims:
                    self.play(*match_anims, run_time=0.2)
                    
            elif action == "fail":
                # Get position for the cross
                cross_pos = target_mobs[t_idx] if 0 <= t_idx < len(target_mobs) else t_ptr
                cross = Cross(cross_pos, stroke_width=6).scale(0.5)
                self.play(Create(cross), run_time=0.2)
                self.play(FadeOut(cross), run_time=0.1)
                
            elif action == "backtrack":
                if 0 <= t_idx < len(target_mobs):
                    self.play(
                        target_mobs[t_idx].animate.set_color(WHITE),
                        Wiggle(t_ptr),
                        run_time=0.4
                    )

        # 4. The Execution Trace (Corrected for a*b vs aab)
        # Format: (regex_index, target_index, action)
        trace = [(4, 0, 'eval'), (1, 0, 'eval'), (1, 0, 'match'), (2, 1, 'eval'), (2, 1, 'match'), (3, 2, 'eval'), (3, 2, 'match'), (4, 3, 'eval'), (1, 3, 'eval'), (1, 3, 'fail'), (4, 3, 'backtrack'), (5, 3, 'eval'), (5, 3, 'match'), (6, 4, 'eval'), (6, 4, 'match'), (7, 5, 'eval'), (7, 5, 'match'), (4, 6, 'eval'), (1, 6, 'eval'), (1, 6, 'match'), (2, 7, 'eval'), (2, 7, 'match'), (3, 8, 'eval'), (3, 8, 'match'), (4, 9, 'eval'), (1, 9, 'eval'), (1, 9, 'fail'), (4, 9, 'backtrack'), (5, 9, 'eval'), (5, 9, 'fail'), (9, 9, 'eval'), (10, 9, 'eval'), (10, 9, 'match'), (11, 10, 'eval'), (11, 10, 'match'), (12, 11, 'eval'), (12, 11, 'match'), (13, 12, 'eval'), (13, 12, 'match'), (14, 13, 'eval'), (14, 13, 'match'), (15, 14, 'eval'), (15, 14, 'match'), (15, 15, 'eval'), (15, 15, 'match'), (15, 16, 'eval'), (15, 16, 'fail'), (16, 16, 'eval'), (17, 16, 'eval'), (17, 16, 'fail'), (18, 16, 'eval')]
        for r_i, t_i, action in trace:
            animate_step(r_i, t_i, action)
            
        # 5. Success State
        success_text = Text("Full Match Found!", color=GREEN).scale(0.8).shift(DOWN * 2.5)
        self.play(Write(success_text))
        self.play(Circumscribe(target_mobs, color=GREEN))
        self.wait(2)