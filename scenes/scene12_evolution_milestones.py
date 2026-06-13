
from manimlib import *
from scenes.utils import *

class Scene12_EvolutionMilestones(Scene):
    def construct(self):
        self.camera.background_color = '#111111'

        # Create a timeline
        timeline = Line(LEFT * 5, RIGHT * 5, stroke_color=WHITE, stroke_width=1)
        self.add(timeline)

        # Define milestones
        milestones = [
            {'name': 'FaceNet', 'year': 2015, 'x': -4},
            {'name': 'SphereFace', 'year': 2017, 'x': -2},
            {'name': 'CosFace', 'year': 2018, 'x': 0},
            {'name': 'ArcFace', 'year': 2018, 'x': 2},
        ]

        # Create milestone markers
        for milestone in milestones:
            marker = Circle(radius=0.1, stroke_color=CYAN, fill_color=CYAN, fill_opacity=1)
            marker.move_to(milestone['x'] * RIGHT)
            self.add(marker)

            # Add milestone name
            name = Tex(milestone['name'], font_size=24)
            name.next_to(marker, UP, buff=0.2)
            self.add(name)

            # Add milestone year
            year = Tex(str(milestone['year']), font_size=20)
            year.next_to(marker, DOWN, buff=0.2)
            self.add(year)

        # Animate camera movement
        self.camera.frame.move_to(milestones[0]['x'] * RIGHT)
        self.play(self.camera.frame.animate.move_to(milestones[-1]['x'] * RIGHT), rate_func=smooth, run_time=10)

        # Zoom out to show entire timeline
        self.play(self.camera.frame.animate.scale(2), rate_func=smooth, run_time=2)
        self.wait(2)
  