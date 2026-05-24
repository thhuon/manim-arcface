from manimlib import *
import numpy as np


class Scene00Introduction(ThreeDScene):
    """
    Scene 0: Introduction
    - Black screen then reveal vector diagram of laptop and locked phone
    - Face bounding box around simplified vector face
    - 3D: Face transforms into rotating wireframe mesh, vertices glow as vector points
    - Vector points disperse into pixel/matrix streams converging to single math point
    - Title: "Understanding ArcFace: The Geometry Behind Modern Face Recognition"
    """

    def construct(self):
        # Start with black screen
        self.wait(0.5)

        # === Part 1: Phone and Laptop with Face Detection ===
        self.camera.background_color = BLACK
        phone = RoundedRectangle(
            width=1.2,
            height=2.4,
            corner_radius=0.15,
            stroke_color="#4fc3f7",
            stroke_width=3,
            fill_opacity=0
        )

        lock_icon = VGroup(
            Square(0.4, stroke_color="#ff6b9d", stroke_width=2),
            Arc(
                start_angle=PI * 0.2,
                angle=-PI * 0.4,
                radius=0.15,
                stroke_color="#ff6b9d",
                stroke_width=2
            ),
        ).scale(0.6).move_to(phone.get_center() + UP * 0.2)

        phone.add(lock_icon)

        laptop_screen = RoundedRectangle(
            width=3,
            height=2,
            corner_radius=0.1,
            stroke_color="#4fc3f7",
            stroke_width=3,
            fill_opacity=0
        )
        laptop_base = Rectangle(
            width=3.5,
            height=0.15,
            stroke_color="#4fc3f7",
            stroke_width=2,
            fill_opacity=0
        ).move_to(laptop_screen.get_bottom() + DOWN * 0.15)

        laptop = VGroup(laptop_screen, laptop_base)

        phone.move_to(LEFT * 3)
        laptop.move_to(RIGHT * 2.5)

        face_box = SurroundingRectangle(
            Rectangle(width=1.5, height=2),
            stroke_color="#ffe66d",
            stroke_width=2,
            buff=0.1
        )

        simple_face = VGroup(
            Circle(
                radius=0.5,
                stroke_color="#4ecdc4",
                stroke_width=2,
                fill_opacity=0
            ),
            Line(LEFT * 0.15, RIGHT * 0.15, stroke_color="#4ecdc4", stroke_width=2),
            Arc(
                start_angle=PI * 0.2,
                angle=-PI * 0.4,
                radius=0.15,
                stroke_color="#4ecdc4",
                stroke_width=2
            ),
        ).move_to(laptop_screen.get_center())

        devices_group = VGroup(phone, laptop).arrange(RIGHT, buff=2)

        self.play(FadeIn(devices_group, run_time=1.5))
        self.wait(0.5)

        face_box.move_to(laptop_screen.get_center())
        self.play(ShowCreation(face_box, run_time=0.8))
        self.wait(0.3)

        self.play(FadeIn(simple_face, run_time=0.5))
        self.wait(0.5)

        # === Part 2: Transform to 3D Wireframe ===
        self.play(FadeOut(VGroup(devices_group, face_box, simple_face)))

        # Create wireframe sphere
        sphere = Sphere(radius=1.5, resolution=(12, 24))
        sphere_mesh = SurfaceMesh(sphere, stroke_color="#4fc3f7", stroke_opacity=0.6)
        sphere_mesh.set_stroke(width=1)

        # Create glowing dots on sphere
        np.random.seed(42)
        n_points = 30
        points_on_sphere = []

        for _ in range(n_points):
            theta = np.random.uniform(0, 2 * PI)
            phi = np.random.uniform(0, PI)
            x = 1.5 * np.sin(phi) * np.cos(theta)
            y = 1.5 * np.cos(phi)
            z = 1.5 * np.sin(phi) * np.sin(theta)
            points_on_sphere.append([x, y, z])

        # Create GlowDots with all points
        point_cloud = GlowDots(
            points=np.array(points_on_sphere),
            radius=0.08,
            glow_factor=2.0,
            color="#4fc3f7"
        )

        # Set up camera for 3D
        self.frame.reorient(phi_degrees=70, theta_degrees=-45)

        self.play(FadeIn(sphere_mesh, run_time=1.5))
        self.play(FadeIn(point_cloud, run_time=1))
        self.wait(0.5)

        # Rotate the sphere
        self.play(Rotate(sphere_mesh, PI / 6, run_time=3))
        self.play(Rotate(point_cloud, PI / 6, run_time=3))
        self.wait(0.5)

        # === Part 3: Vector Points Converging to Embedding Point ===
        # Create embedding point as a simple glowing dot
        embedding_dot = GlowDot(center=[5, 0, 0], radius=0.15, color=WHITE)

        # Create stream points - subset of point_cloud
        stream_points = np.array(points_on_sphere[:15])
        stream_cloud = GlowDots(
            points=stream_points,
            radius=0.06,
            glow_factor=2.0,
            color="#4ecdc4"
        )

        # Move camera to see the convergence
        self.play(self.frame.animate.reorient(phi_degrees=0, theta_degrees=0), run_time=1.5)
        self.wait(0.3)

        self.add(embedding_dot)
        self.play(FadeIn(embedding_dot, run_time=0.8))
        self.wait(0.3)

        # Animate points converging
        self.play(
            stream_cloud.animate.move_to([5, 0, 0]),
            run_time=2,
            rate_func=smooth
        )

        self.play(
            point_cloud.animate.move_to([5, 0, 0]),
            run_time=2,
            rate_func=smooth
        )

        # Final effect on embedding point
        self.play(embedding_dot.animate.scale(1.5), run_time=0.3)
        self.play(embedding_dot.animate.scale(1 / 1.5), run_time=0.3)
        self.wait(0.5)

        # Fade out 3D elements
        self.remove(stream_cloud, point_cloud, embedding_dot, sphere_mesh)
        self.wait(0.3)

        # === Part 4: Title - 3B1B Style ===
        # Set pure black background for 3B1B aesthetic
        self.camera.background_color = BLACK
        self.play(self.frame.animate.reorient(phi_degrees=0, theta_degrees=0), run_time=1)

        # Load SVG accent decoration
        accent_path = "scenes/decorations/3b1b_accent.svg"
        accent = SVGMobject(accent_path)
        accent.set_fill(WHITE, 1)
        accent.scale(0.5)
        accent.to_edge(UP, buff=2.5)

        # Main title - white, large, using LaTeX (3B1B style)
        title = Tex(
            r"\text{Understanding ArcFace}",
            font_size=72,
            color=WHITE
        )
        # No backstroke - pure white text like 3B1B

        # Subtitle - smaller, slightly dimmed
        subtitle = Tex(
            r"\text{The Geometry Behind Modern Face Recognition}",
            font_size=32,
            color="#cccccc"
        )

        # Add accent decoration above title
        self.play(FadeIn(accent, run_time=0.8))
        self.wait(0.2)

        # Fade in title and subtitle
        self.play(FadeIn(title, run_time=1.2, rate_func=smooth))
        self.wait(0.3)
        self.play(FadeIn(subtitle, run_time=1, rate_func=smooth))
        self.wait(2)

        self.play(FadeOut(VGroup(title, subtitle, accent)), run_time=1)
        self.wait(0.5)
