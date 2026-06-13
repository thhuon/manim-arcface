from manimlib import *
from scenes.utils import *

class Scene04_ChallengesWhyAccuracyMatters(Scene):
    def construct(self):
        # 1. Background setup
        self.camera.background_color = DARK
        
        # 2. Main Title
        title = Tex(r"\textbf{Why Accuracy Matters}", font_size=40)
        title.set_color(WHITE)
        title.to_edge(UP, buff=0.8)
        
        subtitle = Tex(r"\text{When face recognition is widely deployed, errors have real consequences.}", font_size=20)
        subtitle.set_color(MUTED)
        subtitle.next_to(title, DOWN, buff=0.2)
        
        self.play(
            Write(title),
            Write(subtitle),
            run_time=1.5
        )
        self.wait(1.0)
        
        # 3. Create three columns/use cases
        
        # Column 1: Smartphone (User Experience / Convenience)
        phone_body = RoundedRectangle(width=1.0, height=1.8, corner_radius=0.15, stroke_color=WHITE, stroke_width=2)
        phone_screen = RoundedRectangle(width=0.9, height=1.7, corner_radius=0.10, stroke_color=MUTED, stroke_width=1)
        phone_screen.move_to(phone_body)
        phone_notch = Rectangle(width=0.4, height=0.1, stroke_width=0, fill_color=WHITE, fill_opacity=1)
        phone_notch.move_to(phone_body.get_top() + 0.08 * DOWN)
        
        # Lock SVG on screen
        lock_icon = SVGMobject(asset_path("lock.svg"))
        lock_icon.set_height(0.5)
        lock_icon.set_color(CYAN)
        lock_icon.move_to(phone_body.get_center())
        
        smartphone_group = VGroup(phone_body, phone_screen, phone_notch, lock_icon)
        
        smartphone_label = Tex(r"\textbf{User Experience}", font_size=22)
        smartphone_label.set_color(WHITE)
        smartphone_desc = Tex(
            r"\begin{array}{c}"
            r"\text{Daily convenience}\\"
            r"\text{e.g., unlocking phone}"
            r"\end{array}",
            font_size=18,
            color=MUTED
        )
        smartphone_col = VGroup(smartphone_group, smartphone_label, smartphone_desc)
        smartphone_col.arrange(DOWN, buff=0.3)
        
        # Column 2: Security (Surveillance / Security)
        sec_camera = make_camera_icon()
        sec_camera.scale(1.2)
        
        # Add a scanning cone or detection box under it to look advanced
        cone = Polygon(
            sec_camera.get_center(),
            sec_camera.get_center() + DOWN * 1.5 + LEFT * 0.8,
            sec_camera.get_center() + DOWN * 1.5 + RIGHT * 0.8,
            stroke_width=0,
            fill_color=CYAN,
            fill_opacity=0.15
        )
        sec_camera_group = VGroup(cone, sec_camera)
        
        security_label = Tex(r"\textbf{Security Systems}", font_size=22)
        security_label.set_color(WHITE)
        security_desc = Tex(
            r"\begin{array}{c}"
            r"\text{Intrusion prevention}\\"
            r"\text{e.g., suspect tracking}"
            r"\end{array}",
            font_size=18,
            color=MUTED
        )
        security_col = VGroup(sec_camera_group, security_label, security_desc)
        security_col.arrange(DOWN, buff=0.3)
        
        # Column 3: eKYC / Banking (Financial Security)
        ekyc_shield = Circle(radius=0.75, stroke_color=GREEN, stroke_width=2, fill_opacity=0)
        lock_icon_bank = SVGMobject(asset_path("lock.svg"))
        lock_icon_bank.set_height(0.6)
        lock_icon_bank.set_color(GREEN)
        lock_icon_bank.move_to(ekyc_shield)
        ekyc_group = VGroup(ekyc_shield, lock_icon_bank)
        
        ekyc_label = Tex(r"\textbf{eKYC \& Banking}", font_size=22)
        ekyc_label.set_color(WHITE)
        ekyc_desc = Tex(
            r"\begin{array}{c}"
            r"\text{Financial safety}\\"
            r"\text{e.g., card verification}"
            r"\end{array}",
            font_size=18,
            color=MUTED
        )
        ekyc_col = VGroup(ekyc_group, ekyc_label, ekyc_desc)
        ekyc_col.arrange(DOWN, buff=0.3)
        
        # Arrange all three columns
        columns = Group(smartphone_col, security_col, ekyc_col)
        columns.arrange(RIGHT, buff=1.2)
        columns.move_to(DOWN * 0.5)
        
        # Show columns
        self.play(
            FadeIn(smartphone_col, shift=UP),
            FadeIn(security_col, shift=UP),
            FadeIn(ekyc_col, shift=UP),
            run_time=1.8
        )
        self.wait(1.0)
        
        # 4. Scenario animations (interactive beat)
        
        # Scenario 1: Phone fails to unlock
        self.play(
            smartphone_col.animate.scale(1.2),
            security_col.animate.set_opacity(0.3),
            ekyc_col.animate.set_opacity(0.3),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Show lock blinking red to show failure
        red_cross = Tex(r"\times", font_size=60, color=RED)
        red_cross.move_to(lock_icon.get_center())
        
        self.play(
            lock_icon.animate.set_color(RED),
            FadeIn(red_cross, scale=0.5),
            run_time=0.5
        )
        self.wait(1.5)
        self.play(
            FadeOut(red_cross),
            lock_icon.animate.set_color(CYAN),
            smartphone_col.animate.scale(1.0/1.2),
            run_time=0.8
        )
        
        # Scenario 2: Security Camera misidentifying
        self.play(
            smartphone_col.animate.set_opacity(0.3),
            security_col.animate.set_opacity(1.0).scale(1.2),
            ekyc_col.animate.set_opacity(0.3),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Cone flashes red / warning
        warning_mark = Tex(r"!", font_size=48, color=RED)
        warning_mark.next_to(sec_camera, UP, buff=0.2)
        
        self.play(
            cone.animate.set_color(RED).set_opacity(0.25),
            sec_camera.animate.set_color(RED),
            FadeIn(warning_mark, scale=0.5),
            run_time=0.6
        )
        self.wait(1.5)
        self.play(
            FadeOut(warning_mark),
            cone.animate.set_color(CYAN).set_opacity(0.15),
            sec_camera.animate.set_color(CYAN),
            security_col.animate.scale(1.0/1.2),
            run_time=0.8
        )
        
        # Scenario 3: eKYC / Banking failure (Serious risks)
        self.play(
            smartphone_col.animate.set_opacity(0.3),
            security_col.animate.set_opacity(0.3),
            ekyc_col.animate.set_opacity(1.0).scale(1.2),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Bank account access alarm / lock breaks or error message
        dollar_sign = Tex(r"\$ \rightarrow \text{Blocked}", font_size=20, color=RED)
        dollar_sign.next_to(ekyc_group, UP, buff=0.2)
        
        self.play(
            ekyc_shield.animate.set_color(RED),
            lock_icon_bank.animate.set_color(RED),
            Write(dollar_sign),
            run_time=0.6
        )
        self.wait(1.8)
        self.play(
            FadeOut(dollar_sign),
            ekyc_shield.animate.set_color(GREEN),
            lock_icon_bank.animate.set_color(GREEN),
            ekyc_col.animate.scale(1.0/1.2),
            run_time=0.8
        )
        
        # Restore all to normal
        self.play(
            smartphone_col.animate.set_opacity(1.0),
            security_col.animate.set_opacity(1.0),
            ekyc_col.animate.set_opacity(1.0),
            run_time=1.0
        )
        
        # Summary text
        summary = Tex(r"\text{Real-world variations require high-stability representation.}", font_size=24)
        summary.set_color(CYAN)
        summary.move_to(DOWN * 3.4)
        
        self.play(
            Write(summary),
            run_time=1.2
        )
        self.wait(2.0)
        
        # Fade out everything
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(columns),
            FadeOut(summary),
            run_time=1.2
        )
        self.wait(0.5)
