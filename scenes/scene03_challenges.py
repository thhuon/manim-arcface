from manimlib import *
import os
from scenes.utils import *


# =============================================================================
# SCENE-SPECIFIC HELPERS - For scene03_Challenges
# =============================================================================

ACCENT = "#4A7DFF"

def get_face_image(filename: str, height: float = 1.0):
    """Load face image with consistent styling."""
    path = asset_path(filename)
    if not os.path.exists(path):
        return None
    img = ImageMobject(path)
    img.set_height(height)
    return img


def create_pixel_grid(width=2.0, height=2.0, n=6):
    """Create a grid overlay to represent pixelation concept."""
    grid = VGroup()
    step_x = width / n
    step_y = height / n

    for i in range(n + 1):
        x = -width / 2 + i * step_x
        grid.add(Line(
            [x, -height/2, 0],
            [x, height/2, 0],
            stroke_color=WHITE,
            stroke_width=0.5,
            stroke_opacity=0.3
        ))

    for j in range(n + 1):
        y = -height / 2 + j * step_y
        grid.add(Line(
            [-width/2, y, 0],
            [width/2, y, 0],
            stroke_color=WHITE,
            stroke_width=0.5,
            stroke_opacity=0.3
        ))

    return grid


def create_block_pixels(width=1.6, height=1.6, n=5):
    """Create blocky pixel representation for animation."""
    pixels = VGroup()
    step_x = width / n
    step_y = height / n

    for i in range(n):
        for j in range(n):
            rect = Rectangle(
                width=step_x * 0.88,
                height=step_y * 0.88,
                stroke_color=WHITE,
                stroke_width=0.25,
                stroke_opacity=0.4,
                fill_color=DARK,
                fill_opacity=0.7
            )
            rect.move_to([
                -width/2 + step_x/2 + i * step_x,
                -height/2 + step_y/2 + j * step_y,
                0
            ])
            pixels.add(rect)

    return pixels


# =============================================================================
# MAIN SCENE CLASS - Scene 03: Challenges
# =============================================================================

class Scene03_Challenges(Scene):

    def construct(self):
        self.camera.background_color = DARK

        # =====================================================================
        # BEAT 0: TITLE / HOOK
        # =====================================================================
        # Part 1: Human recognition - face grid appears rapidly
        self.beat_0_part_1_human_recognition()

        # Part 2: Pixel comparison problem
        self.beat_0_part_2_pixel_comparison()

        # Part 3: The central question
        self.beat_0_part_3_central_question()

        # Part 4: Scene title
        self.beat_0_part_4_scene_title()

    # =========================================================================
    # BEAT 0 - PART 1: Human Recognition
    # =========================================================================

    def beat_0_part_1_human_recognition(self):
        """
        Show face grid rapidly: face_1.png to face_12.png
        Then show "They are the same person?" and human ability text.
        """
        self.wait(0.3)

        # Load 48 face images for 8x6 grid
        face_files = [
            "face_1.png", "face_2.png", "face_3.png", "face_4.png",
            "face_5.png", "face_6.png", "face_7.png", "face_8.png",
            "face_9.png", "face_10.png", "face_11.png", "face_12.png",
            "face_13.png", "face_14.png", "face_15.png", "face_16.png",
            "face_17.png", "face_18.png", "face_19.png", "face_20.png",
            "face_21.png", "face_22.png", "face_23.png", "face_24.png",
            "face_25.png", "face_26.png", "face_27.png", "face_28.png",
            "face_29.png", "face_30.png", "face_31.png", "face_32.png",
            "face_33.png", "face_34.png", "face_35.png", "face_36.png",
            "face_37.png", "face_38.png", "face_39.png", "face_40.png",
            "face_41.png", "face_42.png", "face_43.png", "face_44.png",
            "face_45.png", "face_46.png", "face_47.png", "face_48.png"
        ]

        # Fallback if files don't exist
        available_faces = []
        for f in face_files:
            path = asset_path(f)
            if os.path.exists(path):
                available_faces.append(f)

        # Grid layout: 6 rows x 8 columns (48 images)
        # 408x408 pixels each - fit to frame with no gaps
        rows, cols = 6, 8

        # Calculate img size to fill frame (no gaps)
        # FRAME_WIDTH ≈ 14.22, FRAME_HEIGHT ≈ 8.0
        # Height: 8 * img_size ≤ 7.5 (leave room for text at top)
        img_size = 1.5  # each image size in manim units
        spacing = img_size  # no gaps between images

        face_images = []
        for idx in range(min(len(available_faces), rows * cols)):
            row = idx // cols
            col = idx % cols

            img = get_face_image(available_faces[idx], height=img_size)
            if img is None:
                continue

            # Position in grid with no gaps
            x = (col - (cols - 1) / 2) * spacing
            y = ((rows - 1) / 2 - row) * spacing
            img.move_to([x, y, 0])
            face_images.append(img)
            img.move_to([x, y, 0])
            face_images.append(img)

        # Animate: each face appears one by one rapidly
        for img in face_images:
            img.save_state()
            self.add(img)
            self.wait(0.05)

        # Wait for 0.3 seconds after all faces appear
        self.wait(0.3)

        # Store grid for next part
        self.face_grid = Group(*face_images)
        self.face_grid.scale(0.85) 
        self.wait(0.5)
        self.face_grid.move_to(ORIGIN)
        

        # Fade all the faces to low opacity
        other_faces = Group(*[self.face_grid[i] for i in range(0, len(self.face_grid))])
        self.play(other_faces.animate.set_opacity(0.1), run_time=0.3)
        self.wait(0.3)

        # Question text ABOVE grid (grid now fills most of screen) and centered
        question = latex(r"\textbf{They are the same person?}", size=55)
        question.center()
        self.add(question)
        self.play(Write(question), run_time=0.4)

        # Human ability text 
        ability = latex(r"\textbf{Humans are able to recognize this instantly.}", size=26, color=CYAN)
        ability.next_to(question, DOWN, buff=0.4)

        self.add(ability)
        self.play(Write(ability), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(question), FadeOut(ability), run_time=0.3)
        self.wait(0.5)

        # Store references
        self.question_text = question
        self.ability_text = ability

    # =========================================================================
    # BEAT 0 - PART 2: Pixel Comparison Problem
    # =========================================================================

    def beat_0_part_2_pixel_comparison(self):
        # =====================================================================
        # PART 2: RAW PIXELS AND MISLEADING DISTANCE
        # =====================================================================

        # STEP 0: Clear the face grid
        # Fade out the face grid to make room for the new comparison cards
        self.play(FadeOut(self.face_grid), run_time=0.5)
        self.wait(0.3)

        # Part 2 title
        part_2_title = Tex(r"\textbf{A Subtle Problem}", color=CYAN, font_size=30)
        part_2_subtitle = Tex(r"\text{Which faces should be considered close?}", color=WHITE, font_size=40)
        part_2_title.move_to(UP * 3.8)
        part_2_subtitle.next_to(part_2_title, DOWN, buff=0.15)
        self.add(part_2_title, part_2_subtitle)
        self.play(Write(part_2_title), Write(part_2_subtitle), run_time=0.5)
        self.wait(0.5)


        # STEP 1: Create and position face cards A and B (LARGE, CENTER)
        # Get face images A and B - initially at LARGE size (height=2.5)
        face_a = get_face_image("face_A.png", height=2.5)
        face_a.scale(2.0)
        face_b = get_face_image("face_B.png", height=2.5)
        face_b.scale(2.0)

        # Create labels under A and B
        label_a = Tex(r"\text{A: same identity}", font_size=30, color=WHITE)
        label_b = Tex(r"\text{B: same identity, different conditions}", font_size=30, color=WHITE)

        # Create card groups (face + label) to move them together
        card_a = Group(face_a, label_a)
        card_b = Group(face_b, label_b)

        # Position labels below faces
        label_a.next_to(face_a, DOWN, buff=0.5)
        label_b.next_to(face_b, DOWN, buff=0.5)

        # Initially position A and B at CENTER, close to each other
        # A at LEFT*1.5, B at RIGHT*1.5 (they overlap slightly in the middle)
        card_a.move_to(LEFT * 3.0)
        card_b.move_to(RIGHT * 1.5)

        # Add cards to scene and fade in (they appear large at center)
        self.add(card_a, card_b)
        self.play(FadeIn(card_a), FadeIn(card_b), run_time=0.6)

        self.wait(0.4)

        # STEP 2: Shrink and move A, B to the LEFT
        # Effect: "Extract" A and B from center, shrink them, and move left
        # This creates space on the right side for face C to appear
        #
        # Movement:
        #   A: (LEFT*1.5) → (LEFT*3.5 + UP*0.5)  [moves left and up slightly]
        #   B: (RIGHT*1.5) → (ORIGIN + UP*0.5)    [moves to center-left and up]
        #
        # Size: scale down to 70% (0.7) of original
        target_a_pos = LEFT * 3.5 + UP * 0.5
        target_b_pos = ORIGIN + UP * 0.5

        self.play(
            card_a.animate.scale(0.7).move_to(target_a_pos),
            card_b.animate.scale(0.7).move_to(target_b_pos),
            run_time=0.8
        )

        self.wait(0.3)

        # STEP 3: Show face C on the RIGHT
        # C appears at RIGHT side, same size as A and B after shrinking 
        # C represents a DIFFERENT person with SAME conditions as A
        face_c = get_face_image("face_C.png", height=2.5)
        face_c.scale(1.4)  # Same size of A and B after shrinking

        label_c = Tex(
            r"\begin{array}{l}"
            r"\text{C: same conditions,}\\"
            r"\text{different identity}"
            r"\end{array}",
            font_size=27,
            color=WHITE
        )

        card_c = Group(face_c, label_c)
        card_c.move_to(RIGHT * 3.5 + UP * 0.5)  # 
        label_c.next_to(face_c, DOWN, buff=0.5)

        # Fade in C with a simple animation
        self.add(card_c)
        self.play(FadeIn(card_c), run_time=0.5)

        self.wait(0.5)

        # Fade out part 2 title and subtitle
        self.play(FadeOut(part_2_title), FadeOut(part_2_subtitle), run_time=0.3)
        self.wait(0.3)

        # STEP 4: Show pixel vectors below each face
        # Create simplified illustrative pixel vectors to show raw pixel representation
        p_a = Tex(r"\mathbf{p}_A = [23,\ 41,\ 88,\ \cdots]", font_size=24)
        p_b = Tex(r"\mathbf{p}_B = [4,\ 12,\ 35,\ \cdots]", font_size=24)
        p_c = Tex(r"\mathbf{p}_C = [25,\ 39,\ 84,\ \cdots]", font_size=24)

        # Position vectors below each card
        p_a.next_to(card_a, DOWN, buff=0.8)
        p_b.next_to(card_b, DOWN, buff=0.8)
        p_c.next_to(card_c, DOWN, buff=0.8)

        # Show the notation label explaining the vector representation
        notation_label = Tex(r"\mathbf{p}=\operatorname{flatten}(\mathbf{I})", font_size=20, color=MUTED)
        notation_label.move_to(DOWN * 2.2)
        self.add(notation_label)

        dim_label = Tex(r"\mathbf{p}\in\mathbb{R}^{H\times W\times 3}", font_size=18, color=MUTED)
        dim_label.next_to(notation_label, DOWN, buff=0.1)

        # Animate: cards shift up slightly while pixel vectors and labels appear
        self.play(
            card_a.animate.shift(UP * 0.15).set_opacity(0.85),
            card_b.animate.shift(UP * 0.15).set_opacity(0.85),
            card_c.animate.shift(UP * 0.15).set_opacity(0.85),
            Write(p_a), Write(p_b), Write(p_c),
            Write(notation_label),
            Write(dim_label),
            run_time=0.6
        )

        # Add note showing that A and C have similar first pixel values
        closer_note = Tex(r"\text{(first entries of } \mathbf{p}_A \text{ and } \mathbf{p}_C \text{ are similar)}", font_size=16, color=MUTED)
        closer_note.move_to(DOWN * 3.8)
        self.add(closer_note)
        self.play(Write(closer_note), run_time=0.4)
        self.wait(0.6)

        # STEP 5: Create 2D coordinate plane (raw-pixel space)
        # Fade cards and vectors to 30% opacity as background for the plane
        self.play(
            card_a.animate.set_opacity(0.3),
            card_b.animate.set_opacity(0.3),
            card_c.animate.set_opacity(0.3),
            p_a.animate.set_opacity(0.3),
            p_b.animate.set_opacity(0.3),
            p_c.animate.set_opacity(0.3),
            notation_label.animate.set_opacity(0.3),
            dim_label.animate.set_opacity(0.3),
            closer_note.animate.set_opacity(0.3),
            run_time=0.5
        )

        # Create 2D coordinate plane title
        plane_title = Tex(r"\text{2D projection of raw-pixel space}", font_size=28)
        plane_title.move_to(UP * 3.8)
        self.add(plane_title)

        plane_subtitle = Tex(r"\text{conceptual view}", font_size=18, color=MUTED)
        plane_subtitle.next_to(plane_title, DOWN, buff=0.15)
        self.add(plane_subtitle)

        # Draw axes with generic pixel dimension labels
        axis_length = 3.5
        h_line = Line(LEFT * axis_length, RIGHT * axis_length, stroke_color=WHITE, stroke_width=1.5)
        v_line = Line(DOWN * axis_length, UP * axis_length, stroke_color=WHITE, stroke_width=1.5)
        h_line.move_to(ORIGIN)
        v_line.move_to(ORIGIN)

        # Axis labels (pixel dimensions, not identity/pose/lighting)
        axis_label_i = Tex(r"p_i", font_size=20)
        axis_label_i.next_to(h_line, RIGHT, buff=0.2)
        axis_label_j = Tex(r"p_j", font_size=20)
        axis_label_j.next_to(v_line, UP, buff=0.2)

        # Group and display the plane
        plane_group = VGroup(h_line, v_line, axis_label_i, axis_label_j, plane_title, plane_subtitle)
        self.add(plane_group)
        self.play(Write(plane_group), run_time=0.5)

        # STEP 6: Transform face cards into points on the 2D plane
        # Define positions on the 2D plane:
        #   A and B: far apart (same identity, different appearance)
        #   A and C: closer (different identity, similar conditions)
        #
        # Final layout:
        #       C (1.2, 0.2)
        #   A (-2.0, 0.3)
        #           B (-0.3, -1.5)
        point_a_pos = LEFT * 2.0 + UP * 0.3
        point_b_pos = LEFT * 0.3 + DOWN * 1.5
        point_c_pos = RIGHT * 1.2 + UP * 0.2

        # Create colored dots to represent each face
        dot_a = Dot(point_a_pos, color=CYAN, radius=0.12)
        dot_b = Dot(point_b_pos, color=CYAN, radius=0.12)
        dot_c = Dot(point_c_pos, color="#CC8855", radius=0.12)

        # Labels for each point
        point_label_a = Tex(r"A", font_size=22)
        point_label_b = Tex(r"B", font_size=22)
        point_label_c = Tex(r"C", font_size=22)
        point_label_a.next_to(dot_a, UP + LEFT, buff=0.1)
        point_label_b.next_to(dot_b, DOWN + RIGHT, buff=0.1)
        point_label_c.next_to(dot_c, UP + RIGHT, buff=0.1)

        # Shrink cards down to tiny dots and move them to point positions
        # This creates a visual effect of faces "collapsing" into points
        self.play(
            card_a.animate.scale(0.06).move_to(point_a_pos),
            card_b.animate.scale(0.06).move_to(point_b_pos),
            card_c.animate.scale(0.06).move_to(point_c_pos),
            run_time=0.7
        )

        # Fade in the dots at the point positions
        self.play(
            FadeIn(dot_a), FadeIn(dot_b), FadeIn(dot_c),
            Write(point_label_a), Write(point_label_b), Write(point_label_c),
            run_time=0.4
        )

        # STEP 7: Draw dashed lines showing distances between points
        # Draw dashed line between A and B (large distance - same identity)
        line_ab = DashedLine(point_a_pos, point_b_pos, stroke_color=WHITE, stroke_width=1.5)

        # Draw dashed line between A and C (small distance - different identity)
        line_ac = DashedLine(point_a_pos, point_c_pos, stroke_color=WHITE, stroke_width=1.5)

        # Animate the lines appearing
        self.play(Write(line_ab), Write(line_ac), run_time=0.4)

        # Add distance labels explaining the distances
        dist_ab_label = Tex(r"\text{same identity, large pixel distance}", font_size=18, color=CYAN)
        dist_ab_label.move_to((point_a_pos + point_b_pos) / 2 + DOWN * 0.4)
        dist_ab_label.shift(RIGHT * 0.5)

        dist_ac_label = Tex(r"\text{different identity, smaller pixel distance}", font_size=18, color="#CC8855")
        dist_ac_label.move_to((point_a_pos + point_c_pos) / 2 + UP * 0.35)

        self.play(Write(dist_ab_label), Write(dist_ac_label), run_time=0.4)
        self.wait(0.5)

        # STEP 8: Display the key conclusion
        # Show the main takeaway: raw pixel distance can be misleading
        conclusion1 = Tex(r"\textbf{Raw-pixel distance can be misleading.}", font_size=32)
        conclusion1.center()
        conclusion1.move_to(DOWN * 3.8)
        self.add(conclusion1)
        self.play(Write(conclusion1), run_time=0.5)
        self.wait(0.8)

        # Transform to a stronger statement
        conclusion1.generate_target()
        conclusion1.target.become(
            Tex(r"\textbf{Raw pixels do not preserve identity distance.}", font_size=32)
        )
        conclusion1.target.move_to(DOWN * 3.8)

        self.play(Transform(conclusion1, conclusion1.target), run_time=0.5)
        self.wait(0.8)

        # STEP 9: Store elements for Part 3
        # Store all part 2 elements for use in Part 3 (identity-aware representation)
        self.points_ab = VGroup(dot_a, dot_b, dot_c, line_ab, line_ac, point_label_a, point_label_b, point_label_c)
        self.dist_labels = VGroup(dist_ab_label, dist_ac_label)
        self.conclusion1 = conclusion1
        self.plane_group = plane_group

        # Store all part 2 elements including card groups
        self.all_part2_elements = [
            card_a, card_b, card_c,
            p_a, p_b, p_c, notation_label, dim_label, closer_note
        ]

        # Store individual references for Part 3 animation
        self.dot_a = dot_a
        self.dot_b = dot_b
        self.dot_c = dot_c
        self.point_label_a = point_label_a
        self.point_label_b = point_label_b
        self.point_label_c = point_label_c

    # =========================================================================
    # BEAT 0 - PART 3: Link to Next Chapter
    # =========================================================================

    def beat_0_part_3_central_question(self):
        """
        Transition from raw-pixel space to identity-aware representation.
        Shows that we need a new space where identity (not appearance) defines distance.
        """
        # STEP 1: Create identity-aware representation space (on the RIGHT)
        # Create second space labeled "Identity-aware representation"
        # This represents what we WANT: a space where identity distance is preserved
        new_space_title = Tex(r"\text{Identity-aware representation}", font_size=26)
        new_space_title.move_to(RIGHT * 4.5 + UP * 3.2)

        # Draw axes for the new space
        new_axis_length = 2.5
        new_h_line = Line(LEFT * new_axis_length, RIGHT * new_axis_length, stroke_color=WHITE, stroke_width=1.5)
        new_v_line = Line(DOWN * new_axis_length, UP * new_axis_length, stroke_color=WHITE, stroke_width=1.5)
        new_h_line.move_to(RIGHT * 4.5)
        new_v_line.move_to(RIGHT * 4.5)

        # Axis labels for feature dimensions
        new_label_1 = Tex(r"f_i", font_size=18)
        new_label_1.next_to(new_h_line, RIGHT, buff=0.15).shift(RIGHT * 4.5)
        new_label_2 = Tex(r"f_j", font_size=18)
        new_label_2.next_to(new_v_line, UP, buff=0.15).shift(RIGHT * 4.5)

        new_space_group = VGroup(new_h_line, new_v_line, new_label_1, new_label_2, new_space_title)

        # -------------------------------------------------------------------------
        # STEP 2: Define new positions for points (DESIRED behavior)
        # -------------------------------------------------------------------------
        # In identity-aware space:
        #   A and B should be CLOSE (same identity, despite different appearance)
        #   C should be FAR from A and B (different identity)
        #
        # Positions:
        #   A: (4.3, 0.3) - upper left of new space
        #   B: (4.5, -0.3) - lower left of new space (close to A)
        #   C: (6.5, 0.2) - far right (different identity)
        new_pos_a = RIGHT * 4.3 + UP * 0.3
        new_pos_b = RIGHT * 4.5 + DOWN * 0.3
        new_pos_c = RIGHT * 6.5 + UP * 0.2

        # Create new dots at desired positions
        new_dot_a = Dot(new_pos_a, color=CYAN, radius=0.12)
        new_dot_b = Dot(new_pos_b, color=CYAN, radius=0.12)
        new_dot_c = Dot(new_pos_c, color="#CC8855", radius=0.12)

        # Labels for new dots
        new_label_a = Tex(r"A", font_size=20)
        new_label_b = Tex(r"B", font_size=20)
        new_label_c = Tex(r"C", font_size=20)
        new_label_a.next_to(new_dot_a, UP + LEFT, buff=0.08)
        new_label_b.next_to(new_dot_b, DOWN + RIGHT, buff=0.08)
        new_label_c.next_to(new_dot_c, UP + RIGHT, buff=0.08)

        # -------------------------------------------------------------------------
        # STEP 3: Animate transition to new space
        # -------------------------------------------------------------------------
        # Show the new space appearing
        self.play(Write(new_space_group), run_time=0.5)
        self.wait(0.3)

        # Move existing points to new positions in identity-aware space
        # Points will animate from raw-pixel positions to identity-aware positions
        self.play(
            self.dot_a.animate.move_to(new_pos_a),
            self.dot_b.animate.move_to(new_pos_b),
            self.dot_c.animate.move_to(new_pos_c),
            self.point_label_a.animate.next_to(new_dot_a, UP + LEFT, buff=0.08),
            self.point_label_b.animate.next_to(new_dot_b, DOWN + RIGHT, buff=0.08),
            self.point_label_c.animate.next_to(new_dot_c, UP + RIGHT, buff=0.08),
            run_time=0.8
        )

        # -------------------------------------------------------------------------
        # STEP 4: Show relationship lines and annotations
        # -------------------------------------------------------------------------
        # Draw solid lines showing relationships in identity-aware space
        new_line_ab = Line(new_pos_a, new_pos_b, stroke_color=CYAN, stroke_width=2.0)  # A-B: close
        new_line_ac = Line(new_pos_a, new_pos_c, stroke_color="#CC8855", stroke_width=2.0)  # A-C: far
        new_line_bc = Line(new_pos_b, new_pos_c, stroke_color="#CC8855", stroke_width=2.0)  # B-C: far

        self.play(Write(new_line_ab), Write(new_line_ac), Write(new_line_bc), run_time=0.4)

        # Draw circle around A and B to show they form a cluster (same identity)
        center_ab = (new_pos_a + new_pos_b) / 2
        compactness_circle = Circle(radius=0.6, stroke_color=CYAN, stroke_width=2.0, fill_opacity=0)
        compactness_circle.move_to(center_ab)
        self.play(FadeIn(compactness_circle), run_time=0.3)

        # Draw arrow showing separation from A/B cluster to C
        separation_arrow = Arrow(
            center_ab + RIGHT * 0.5,
            new_pos_c + LEFT * 0.5,
            buff=0.1,
            stroke_color="#CC8855",
            stroke_width=2.0
        )
        self.play(Write(separation_arrow), run_time=0.3)

        # STEP 5: Show behavior labels
        # Label for same identity → close
        same_label = Tex(r"\text{same identity}", font_size=20, color=CYAN)
        same_arrow = Tex(r"\rightarrow", font_size=20, color=CYAN)
        same_arrow.next_to(same_label, RIGHT, buff=0.1)
        close_word = Tex(r"\text{close}", font_size=20, color=CYAN)
        close_word.next_to(same_arrow, RIGHT, buff=0.1)

        same_identity_group = VGroup(same_label, same_arrow, close_word)
        same_identity_group.move_to(DOWN * 3.5 + LEFT * 2.5)

        # Label for different identities → far apart
        different_label = Tex(r"\text{different identities}", font_size=20, color="#CC8855")
        different_arrow = Tex(r"\rightarrow", font_size=20, color="#CC8855")
        different_arrow.next_to(different_label, RIGHT, buff=0.1)
        far_word = Tex(r"\text{far apart}", font_size=20, color="#CC8855")
        far_word.next_to(different_arrow, RIGHT, buff=0.1)

        different_identity_group = VGroup(different_label, different_arrow, far_word)
        different_identity_group.move_to(DOWN * 3.5 + RIGHT * 2.5)

        self.play(Write(same_identity_group), Write(different_identity_group), run_time=0.4)

        # STEP 6: Display linking statement
        # Show the key message: we need representation where identity defines distance
        linking_statement = Tex(
            r"\textbf{We need a representation where identity,}",
            font_size=30
        )
        linking_statement2 = Tex(
            r"\textbf{not appearance, defines distance.}",
            font_size=30
        )
        linking_statement.center()
        linking_statement2.next_to(linking_statement, DOWN, buff=0.2)
        linking_statement.move_to(UP * 1.8)
        linking_statement2.move_to(UP * 1.3)

        self.play(Write(linking_statement), Write(linking_statement2), run_time=0.5)
        self.wait(1.0)

        # STEP 7: Fade out all elements for scene title
        # Prepare all elements for transition to Part 4 (scene title)
        fade_out_list = list(self.points_ab) + list(self.dist_labels) + [self.conclusion1, self.plane_group]
        fade_out_list.extend(self.all_part2_elements)
        fade_out_list.extend([
            new_space_group,
            new_dot_a, new_dot_b, new_dot_c,
            new_label_a, new_label_b, new_label_c,
            new_line_ab, new_line_ac, new_line_bc,
            compactness_circle, separation_arrow,
            same_identity_group, different_identity_group,
            linking_statement, linking_statement2
        ])

        self.play(*[FadeOut(obj) for obj in fade_out_list], run_time=0.6)
        self.wait(0.3)

        # Clear the grid for Part 4
        self.face_grid.set_opacity(0)

        self.play(*[FadeOut(obj) for obj in fade_out_list], run_time=0.6)
        self.wait(0.3)

        # Store for Part 4
        self.face_grid.set_opacity(0)  # Clear the grid

    # =========================================================================
    # BEAT 0 - PART 4: Scene Title
    # =========================================================================

    def beat_0_part_4_scene_title(self):
        """
        Display the scene title "Challenges" with subtitle and key points,
        then fade out to prepare for the next section.
        """
        # STEP 1: Display main title
        # Large bold title at the top center of the screen
        title = Tex(r"\textbf{Challenges}", font_size=72)
        title.center()
        title.move_to(UP * 1.5)
        self.add(title)
        self.play(Write(title), run_time=0.55)

        # STEP 2: Display subtitle
        # Subtitle explaining the theme of this scene
        subtitle = Tex(r"\text{Why Face Recognition Is Harder Than It Looks}", font_size=26, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.45)
        self.add(subtitle)
        self.play(Write(subtitle), run_time=0.4)

        # STEP 3: Draw accent line under subtitle
        # Cyan accent line to visually separate title from content
        line = Line(
            LEFT * 3.2,
            RIGHT * 3.2,
            stroke_color=CYAN,
            stroke_width=1.2,
            stroke_opacity=0.45
        )
        line.next_to(subtitle, DOWN, buff=0.35)
        self.add(line)
        self.play(Write(line), run_time=0.3)

        # STEP 4: Display key points (compact lines)
        # Three concise statements about the challenges
        compact1 = Tex(r"\text{Appearance changes.}", font_size=24)
        compact1.next_to(line, DOWN, buff=0.5)

        compact2 = Tex(r"\text{Mistakes have consequences.}", font_size=24)
        compact2.next_to(compact1, DOWN, buff=0.3)

        compact3 = Tex(r"\text{A better representation is needed.}", font_size=24)
        compact3.next_to(compact2, DOWN, buff=0.3)

        # Animate each line appearing
        self.play(Write(compact1), run_time=0.3)
        self.play(Write(compact2), run_time=0.3)
        self.play(Write(compact3), run_time=0.3)

        self.wait(1.2)

        # STEP 5: Fade out all title elements
        # Clear the screen for the next scene content
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(line),
            FadeOut(compact1),
            FadeOut(compact2),
            FadeOut(compact3),
            run_time=0.45
        )
        self.wait(0.3)

    # =========================================================================
    # (Future beats will be added here as separate methods)
    # =========================================================================
