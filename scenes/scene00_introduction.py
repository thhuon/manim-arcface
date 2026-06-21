from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 00 - Introduction
# Clear visual arc: same face images -> pixels -> latent identity -> open set.
# =============================================================================


class Scene00_Introduction(Scene):
    def construct(self):
        self.camera.background_color = DARK
        self.frame = self.camera.frame

        self.beat_a_same_identity_grid()
        self.clear_and_wait()
        self.beat_b_pixels_vs_identity()
        self.clear_and_wait()
        self.beat_c_latent_identity()
        self.clear_and_wait()
        self.beat_d_open_set_bridge()

    # -------------------------------------------------------------------------
    # Beat A - same identity, different images
    # -------------------------------------------------------------------------
    def beat_a_same_identity_grid(self):
        title = make_scene_title(
            "Same Identity, Different Images?",
            title_size=39,
        )

        face_files = [
            "face_1.png", "face_2.png", "face_3.png", "face_4.png",
            "face_5.png", "face_6.png", "face_7.png", "face_8.png",
            "face_9.png", "face_10.png", "face_11.png", "face_12.png",
            "face_13.png", "face_14.png", "face_15.png", "face_16.png",
            "face_17.png", "face_18.png", "face_19.png", "face_20.png",
            "face_21.png", "face_22.png", "face_23.png", "face_24.png"
        ]
        cards = Group(*[
            make_image_card(fname, width=1.28, height=1.42, show_frame=False)
            for fname in face_files
        ])
        cards.arrange_in_grid(4, 6, buff=0.13)
        cards.move_to(DOWN * 0.08)
        fit_to_bounds(cards, max_width=7.45, max_height=4.60)

        bottom_note = latex(r"\text{same person, different conditions}", size=24, color=GREEN)
        bottom_note.next_to(cards, DOWN, buff=0.20)

        layout = Group(cards, bottom_note)
        center_element_group(layout)
        layout.shift(DOWN * 0.18)

        human_label = VGroup(
            make_abstract_face().scale(0.45),
            latex(r"\text{human intuition}", size=24, color=CYAN),
        ).arrange(RIGHT, buff=0.18)
        human_label.next_to(cards, RIGHT, buff=0.32)
        fit_to_bounds(human_label, max_width=2.15)

        scan_line = Line(
            cards.get_left() + UP * cards.get_height() / 2,
            cards.get_right() + UP * cards.get_height() / 2,
            color=CYAN,
            stroke_width=3,
            stroke_opacity=0.65,
        )
        scan_line.shift(UP * 0.12)
        focus = cards[5].copy()
        focus.generate_target()
        focus.target.scale(1.16)
        focus.target.move_to(cards[5])

        self.play(FadeIn(title), run_time=0.55)
        self.play(
            LaggedStart(*[FadeIn(card, shift=0.14 * UP) for card in cards],
                        lag_ratio=0.045),
            run_time=1.6,
        )
        self.play(ShowPassingFlash(scan_line), run_time=1.0)
        self.play(
            MoveToTarget(focus),
            cards[5].animate.scale(1.08),
            run_time=0.36,
        )
        self.play(cards[5].animate.scale(1 / 1.08), FadeOut(focus), run_time=0.28)
        self.play(
            LaggedStart(*[
                card.animate.shift(0.06 * UP if i % 2 == 0 else 0.06 * DOWN)
                for i, card in enumerate(cards)
            ], lag_ratio=0.025),
            run_time=0.45,
        )
        self.play(
            LaggedStart(*[
                card.animate.shift(0.06 * DOWN if i % 2 == 0 else 0.06 * UP)
                for i, card in enumerate(cards)
            ], lag_ratio=0.025),
            run_time=0.45,
        )
        self.play(FadeIn(bottom_note), run_time=0.45)
        self.play(FadeIn(human_label, shift=0.15 * LEFT), run_time=0.55)
        self.play(
            bottom_note.animate.scale(1.06),
            run_time=0.32,
        )
        self.play(
            bottom_note.animate.scale(1 / 1.06),
            run_time=0.28,
        )
        self.wait(0.7)

    # -------------------------------------------------------------------------
    # Beat B - computer view: pixels change
    # -------------------------------------------------------------------------
    def beat_b_pixels_vs_identity(self):
        title = make_scene_title("A Computer Sees Numbers", title_size=39)

        # --- Phase 1: input thumbnails feeding the computer view ---
        face_files = ["face_3.png", "face_4.png", "face_5.png"]

        img_cards = Group()
        for fname in face_files:
            img_cards.add(make_image_card(
                fname, width=1.38, height=1.58, show_frame=False,
                stroke_color=WHITE, label_size=13, label_color=MUTED,
            ))
        img_cards.arrange(DOWN, buff=0.22)
        img_cards.move_to(LEFT * 5.45 + UP * 0.12)

        # --- Phase 2: pixel matrices centered and slightly larger ---
        matrices = VGroup()
        for fname in face_files:
            matrices.add(make_pixel_matrix_from_image(fname, n=8, side=1.72))
        matrices.arrange(RIGHT, buff=0.42)
        matrices.move_to(LEFT * 0.45 + UP * 0.42)

        computer_badge = make_badge(
            "Computer view: pixel values",
            color=CYAN, font_size=18, h_buff=0.22, v_buff=0.10,
        )
        computer_badge.next_to(matrices, UP, buff=0.22)

        # --- Phase 3: Zoomed numeric cells (right side) ---
        import os
        from PIL import Image as PILImage
        img_path = os.path.join(os.path.dirname(__file__), "decorations", face_files[0])
        pil_img = PILImage.open(img_path).convert("RGB")
        pw, ph = pil_img.size
        patch = pil_img.crop((pw // 2 - 18, ph // 2 - 18, pw // 2 + 18, ph // 2 + 18))
        patch = patch.resize((6, 6), PILImage.Resampling.BILINEAR)
        gray_vals = [[int(0.299 * r + 0.587 * g + 0.114 * b)
                      for r, g, b in [patch.getpixel((c, r)) for c in range(6)]] for r in range(6)]

        zoom_cells = VGroup()
        zoom_numbers = VGroup()
        cs = 0.34  # cell side
        cell_gap = 0.035
        for row in range(6):
            for col in range(6):
                cell = Square(side_length=cs, stroke_color=YELLOW, stroke_width=1.4,
                              fill_color=PANEL, fill_opacity=0.90)
                cell.move_to(
                    RIGHT * (col - 2.5) * (cs + cell_gap) +
                    UP * (2.5 - row) * (cs + cell_gap)
                )
                num = latex(str(gray_vals[row][col]), size=13, color=WHITE)
                num.move_to(cell)
                zoom_cells.add(cell)
                zoom_numbers.add(num)

        zoom_group = VGroup(zoom_cells, zoom_numbers)
        zoom_group.move_to(RIGHT * 4.65 + UP * 0.38)
        zoom_border = RoundedRectangle(
            width=zoom_group.get_width() + 0.20,
            height=zoom_group.get_height() + 0.20,
            corner_radius=0.10,
            stroke_color=YELLOW, stroke_width=1.8,
            fill_opacity=0,
        )
        zoom_border.move_to(zoom_group)

        zoom_label = latex(r"\text{actual pixel values}", size=15, color=YELLOW)
        zoom_label.next_to(zoom_border, DOWN, buff=0.10)

        # --- Phase 4: Pixel change marker (right side) ---
        counter = make_badge(
            "pixels changed",
            color=ORANGE,
            font_size=19,
            h_buff=0.22,
            v_buff=0.10,
        )
        counter.move_to(RIGHT * 4.65 + DOWN * 1.50)

        # --- Phase 5: Final statements (bottom) ---
        final_statement = latex(
            r"\text{Pixels change } \neq \text{ identity changes}",
            size=31, color=WHITE,
        )
        fit_to_bounds(final_statement, max_width=10.8)
        final_statement.move_to(DOWN * 2.52)

        bridge_line = latex(
            r"\text{So the model must learn stable identity, not raw pixels.}",
            size=20, color=MUTED,
        )
        fit_to_bounds(bridge_line, max_width=10.8)
        bridge_line.next_to(final_statement, DOWN, buff=0.16)

        image_to_matrix_arrow = make_flow_arrow(
            img_cards.get_right() + RIGHT * 0.12,
            matrices.get_left() + LEFT * 0.12,
            color=WHITE,
            stroke_width=2.0,
        )
        matrix_to_zoom_arrow = make_flow_arrow(
            matrices.get_right() + RIGHT * 0.12,
            zoom_border.get_left() + LEFT * 0.12,
            color=YELLOW,
            stroke_width=2.0,
        )
        zoom_to_counter_arrow = make_flow_arrow(
            zoom_border.get_bottom() + DOWN * 0.10,
            counter.get_top() + UP * 0.08,
            color=YELLOW,
            stroke_width=1.7,
        )

        # --- ANIMATIONS ---

        # Phase 1: input thumbnails -> computer pixel matrices
        self.play(FadeIn(title), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(c, shift=0.10 * RIGHT) for c in img_cards], lag_ratio=0.10),
            run_time=0.85,
        )
        scan_lines = VGroup(*[
            self._scan_line_for_card(c) for c in img_cards
        ])
        self.play(
            LaggedStart(*[ShowPassingFlash(sl) for sl in scan_lines], lag_ratio=0.20),
            run_time=0.85,
        )
        self.play(
            GrowArrow(image_to_matrix_arrow),
            LaggedStart(*[FadeIn(m, shift=0.18 * RIGHT) for m in matrices], lag_ratio=0.10),
            FadeIn(computer_badge, shift=0.08 * DOWN),
            run_time=1.0,
        )
        self.wait(0.5)

        # Phase 2: highlight cells -> show zoomed numeric values
        hi_indices = [row * 8 + col for row in range(2, 5) for col in range(2, 5)]
        hi_cells = VGroup(*[matrices[0][i] for i in hi_indices])
        self.play(
            LaggedStart(*[
                c.animate.set_stroke(color=YELLOW, width=1.5, opacity=0.85)
                for c in hi_cells
            ], lag_ratio=0.04), run_time=0.50,
        )
        self.play(
            LaggedStart(*[
                c.animate.set_stroke(color=WHITE, width=0.35, opacity=0.35)
                for c in hi_cells
            ], lag_ratio=0.04), run_time=0.40,
        )
        self.play(
            GrowArrow(matrix_to_zoom_arrow),
            LaggedStart(*[FadeIn(c, scale=1.2) for c in zoom_cells], lag_ratio=0.06),
            LaggedStart(*[FadeIn(n) for n in zoom_numbers], lag_ratio=0.06),
            FadeIn(zoom_border), FadeIn(zoom_label),
            run_time=0.90,
        )
        self.play(
            LaggedStart(*[n.animate.scale(1.12) for n in zoom_numbers], lag_ratio=0.05),
            run_time=0.35,
        )
        self.play(
            LaggedStart(*[n.animate.scale(1 / 1.12) for n in zoom_numbers], lag_ratio=0.05),
            run_time=0.25,
        )
        self.wait(0.5)

        # Phase 3: pixel marker with flashing cells and changing matrix values
        self.play(GrowArrow(zoom_to_counter_arrow), FadeIn(counter), run_time=0.55)

        flash_idx = [3, 8, 12, 17, 22, 27, 31, 38, 44, 51]
        flash_col = [RED, YELLOW, RED, YELLOW, RED, YELLOW, RED, YELLOW, RED, YELLOW]
        number_change_batches = [
            [(7, 241), (8, 225), (13, 198), (14, 172), (20, 164), (21, 150)],
            [(9, 236), (10, 214), (15, 189), (16, 166), (22, 142), (23, 127)],
            [(18, 207), (19, 191), (24, 176), (25, 153), (30, 132), (31, 118)],
        ]

        flash_cells_by_matrix = [
            [c for i, c in enumerate(mat) if i in flash_idx[:6]]
            for mat in matrices
        ]
        flash_colors_by_matrix = [
            [flash_col[flash_idx.index(i)] for i, _ in enumerate(mat) if i in flash_idx[:6]]
            for mat in matrices
        ]

        for batch in number_change_batches:
            self.play(counter.animate.scale(1.07), run_time=0.16)

            self.play(
                *[
                    LaggedStart(*[
                        c.animate.set_stroke(color=color, width=2.2, opacity=0.90)
                        for c, color in zip(cells, colors)
                    ], lag_ratio=0.025)
                    for cells, colors in zip(flash_cells_by_matrix, flash_colors_by_matrix)
                ],
                *[
                    Transform(
                        zoom_numbers[idx],
                        latex(str(value), size=13, color=ORANGE).move_to(zoom_cells[idx])
                    )
                    for idx, value in batch
                ],
                run_time=0.34,
            )
            self.play(
                *[
                    LaggedStart(*[
                        c.animate.set_stroke(color=WHITE, width=0.35, opacity=0.35)
                        for c in cells
                    ], lag_ratio=0.025)
                    for cells in flash_cells_by_matrix
                ],
                run_time=0.24,
            )

            self.play(counter.animate.scale(1 / 1.07), run_time=0.16)

        self.wait(0.5)

        # Phase 4: final statement
        self.play(FadeIn(final_statement), run_time=0.65)
        self.play(final_statement.animate.scale(1.06), run_time=0.22)
        self.play(final_statement.animate.scale(1 / 1.06), run_time=0.22)
        self.play(FadeIn(bridge_line), run_time=0.55)
        self.wait(1.0)

    def _scan_line_for_card(self, card):
        """Create a horizontal scan line positioned at the top of a card."""
        sl = Line(
            card.get_left() + UP * card.get_height() / 2,
            card.get_right() + UP * card.get_height() / 2,
            color=CYAN, stroke_width=2.5, stroke_opacity=0.60,
        )
        sl.move_to(card)
        return sl

    # -------------------------------------------------------------------------
    # Beat C - what identity is made from
    # -------------------------------------------------------------------------
    def beat_c_latent_identity(self):
        title = make_scene_title(
            "What Are We Actually Recognizing?",
            title_size=37,
        )

        face = ImageMobject(asset_path("face_normal.png"), height=3.45)
        face.move_to(LEFT * 2.35 + DOWN * 0.05)

        feature_specs = [
            (LEFT * 0.36 + UP * 0.54, "eyes", CYAN),
            (RIGHT * 0.03 + DOWN * 0.04, "nose", YELLOW),
            (RIGHT * 0.04 + DOWN * 0.62, "mouth", GREEN),
        ]
        features = VGroup()
        feature_tags = VGroup()
        for offset, label, color in feature_specs:
            marker = Dot(point=face.get_center() + offset, radius=0.075, color=color)
            ring = Circle(radius=0.17, stroke_color=color, stroke_width=1.7, fill_opacity=0)
            ring.move_to(marker)
            text = make_badge(label, color=color, font_size=18)
            text.next_to(marker, RIGHT, buff=0.22)
            features.add(VGroup(ring, marker))
            feature_tags.add(text)

        phase1 = Group(face, features, feature_tags)
        center_element_group(phase1, max_height=4.55)
        phase1.shift(DOWN * 0.18)

        similar_faces = Group(
            make_image_card("face_A.png", width=1.58, height=1.82, label="similar eyes", label_color=CYAN, label_size=17, show_frame=False),
            make_image_card("face_B.png", width=1.58, height=1.82, label="similar pose", label_color=YELLOW, label_size=17, show_frame=False),
            make_image_card("face_C.png", width=1.58, height=1.82, label="similar mouth", label_color=GREEN, label_size=17, show_frame=False),
        ).arrange(RIGHT, buff=0.72)
        similar_faces.move_to(DOWN * 0.12)

        no_single_feature = make_badge("one feature is not enough", color=RED, font_size=20)
        no_single_feature.next_to(similar_faces, DOWN, buff=0.34)

        phase2 = Group(similar_faces, no_single_feature)
        center_element_group(phase2, max_width=10.4, max_height=4.35)
        phase2.shift(DOWN * 0.15)

        face_final = ImageMobject(asset_path("face_normal.png"), height=3.20)
        face_final.move_to(LEFT * 3.80 + DOWN * 0.06)

        final_features = VGroup()
        for offset, _, color in feature_specs:
            marker = Dot(point=face_final.get_center() + offset * (3.20 / 3.45), radius=0.070, color=color)
            ring = Circle(radius=0.16, stroke_color=color, stroke_width=1.7, fill_opacity=0)
            ring.move_to(marker)
            final_features.add(VGroup(ring, marker))

        identity_dot = Dot(color=GREEN, radius=0.20)
        identity_ring = Circle(radius=0.54, stroke_color=GREEN, stroke_width=2.2, fill_opacity=0)
        identity = VGroup(identity_ring, identity_dot)
        identity.move_to(RIGHT * 4.15 + DOWN * 0.02)
        identity_label = latex(r"\text{latent identity}", size=25, color=GREEN)
        identity_label.next_to(identity, DOWN, buff=0.16)

        combo_label = make_badge("unique combination", color=GREEN, font_size=22)
        combo_label.move_to(RIGHT * 0.68 + DOWN * 0.02)

        feature_to_combo_arrows = VGroup(*[
            make_flow_arrow(
                feature.get_right() + RIGHT * 0.05,
                combo_label.get_left() + LEFT * 0.10,
                color=feature[1].get_color(),
                stroke_width=1.7,
            )
            for feature in final_features
        ])
        combo_to_identity_arrow = make_flow_arrow(
            combo_label.get_right() + RIGHT * 0.12,
            identity.get_left() + LEFT * 0.12,
            color=GREEN,
            stroke_width=2.1,
        )

        self.play(FadeIn(title), run_time=0.5)
        self.play(
            FadeIn(face, shift=0.12 * UP),
            LaggedStart(*[GrowFromCenter(feature) for feature in features], lag_ratio=0.16),
            run_time=0.75,
        )
        for feature, tag in zip(features, feature_tags):
            self.play(FadeIn(tag, shift=0.08 * LEFT), run_time=0.25)
            self.play(
                Flash(feature[1], color=feature[1].get_color(), flash_radius=0.34, run_time=0.42),
                ShowPassingFlashAround(tag, stroke_color=feature[1].get_color(), buff=0.06, run_time=0.42),
            )
        self.wait(0.35)

        self.play(
            FadeOut(face),
            FadeOut(features),
            FadeOut(feature_tags),
            run_time=0.45,
        )

        self.play(FadeIn(similar_faces, shift=0.16 * UP), run_time=0.65)
        for card in similar_faces:
            self.play(
                card.animate.scale(1.06),
                ShowPassingFlashAround(card, stroke_color=YELLOW, buff=0.08, run_time=0.48),
                run_time=0.48,
            )
            self.play(card.animate.scale(1 / 1.06), run_time=0.18)
        self.play(FadeIn(no_single_feature, shift=0.12 * UP), run_time=0.45)
        self.play(no_single_feature.animate.scale(1.08), run_time=0.18)
        self.play(no_single_feature.animate.scale(1 / 1.08), run_time=0.18)
        self.wait(0.35)

        self.play(
            FadeOut(similar_faces),
            FadeOut(no_single_feature),
            run_time=0.45,
        )

        self.play(
            FadeIn(face_final, shift=0.12 * UP),
            LaggedStart(*[GrowFromCenter(feature) for feature in final_features], lag_ratio=0.16),
            run_time=0.72,
        )
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in feature_to_combo_arrows], lag_ratio=0.10),
            FadeIn(combo_label, shift=0.12 * LEFT),
            run_time=0.75,
        )
        self.play(combo_label.animate.scale(1.07), run_time=0.20)
        self.play(combo_label.animate.scale(1 / 1.07), run_time=0.18)
        self.play(
            GrowArrow(combo_to_identity_arrow),
            FadeIn(identity),
            FadeIn(identity_label, shift=0.08 * UP),
            run_time=0.75,
        )
        self.play(identity.animate.scale(1.14), run_time=0.22)
        self.play(identity.animate.scale(1 / 1.14), run_time=0.22)
        self.wait(0.9)

    # -------------------------------------------------------------------------
    # Beat D - why not classify identities directly?
    # -------------------------------------------------------------------------
    def beat_d_open_set_bridge(self):
        title = make_scene_title(
            "Why Not Classify Identities Directly?",
            title_size=36,
        )

        # --- Phase 1: ordinary image classification has fixed classes ---
        img_input = make_badge("image", color=WHITE, font_size=20)
        img_input.move_to(LEFT * 4.35 + DOWN * 0.05)
        classifier = make_badge("classifier", color=CYAN, font_size=20)
        classifier.move_to(LEFT * 0.85 + DOWN * 0.05)
        fixed_classes = VGroup(
            make_badge("cat", color=BLUE, font_size=18),
            make_badge("dog", color=GREEN, font_size=18),
            make_badge("bird", color=ORANGE, font_size=18),
        ).arrange(DOWN, buff=0.18)
        fixed_classes.move_to(RIGHT * 3.35 + DOWN * 0.05)
        phase1_label = latex(r"\text{Image classification: known classes}", size=25, color=CYAN)
        phase1_label.move_to(UP * 1.68)
        fixed_note = latex(r"\text{the output set is fixed during training}", size=20, color=MUTED)
        fixed_note.move_to(DOWN * 1.55)
        phase1_arrows = VGroup(
            make_flow_arrow(img_input.get_right(), classifier.get_left(), color=WHITE, stroke_width=2.0),
            make_flow_arrow(classifier.get_right(), fixed_classes.get_left(), color=CYAN, stroke_width=2.0),
        )
        phase1 = Group(phase1_label, img_input, classifier, fixed_classes, fixed_note, phase1_arrows)
        center_element_group(phase1, max_width=11.3, max_height=4.30)

        # --- Phase 2: direct identity classification breaks when new people appear ---
        direct_label = latex(r"\text{Direct identity classifier}", size=25, color=YELLOW)
        direct_label.move_to(UP * 1.78)
        new_face = make_image_card(
            "face_scan.png",
            width=1.30,
            height=1.52,
            label="unseen face",
            label_color=YELLOW,
            label_size=16,
            show_frame=False,
        )
        new_face.move_to(LEFT * 4.40 + DOWN * 0.05)
        identity_classifier = make_badge("classifier", color=RED, font_size=20)
        identity_classifier.move_to(LEFT * 0.75 + DOWN * 0.05)
        known_identities = VGroup(
            make_badge("Person A", color=BLUE, font_size=18),
            make_badge("Person B", color=CYAN, font_size=18),
            make_badge("Person C", color=ORANGE, font_size=18),
        ).arrange(DOWN, buff=0.18)
        known_identities.move_to(RIGHT * 3.45 + UP * 0.30)
        forced_label = make_badge("must choose an old class", color=RED, font_size=17)
        forced_label.next_to(known_identities, DOWN, buff=0.26)
        new_identity_slot = make_badge("Person D?", color=YELLOW, font_size=18)
        new_identity_slot.move_to(RIGHT * 3.45 + DOWN * 1.70)
        no_slot_note = latex(r"\text{not in training classes}", size=17, color=YELLOW)
        no_slot_note.next_to(new_identity_slot, DOWN, buff=0.10)
        phase2_arrows = VGroup(
            make_flow_arrow(new_face.get_right(), identity_classifier.get_left(), color=WHITE, stroke_width=2.0),
            make_flow_arrow(identity_classifier.get_right(), known_identities.get_left(), color=RED, stroke_width=2.0),
        )
        phase2 = Group(
            direct_label,
            new_face,
            identity_classifier,
            known_identities,
            forced_label,
            new_identity_slot,
            no_slot_note,
            phase2_arrows,
        )
        center_element_group(phase2, max_width=11.4, max_height=4.55)

        # --- Phase 3: learn reusable identity representations instead ---
        rep_label = latex(r"\text{Face recognition learns a reusable representation}", size=25, color=GREEN)
        rep_label.move_to(UP * 1.82)
        any_face = make_image_card(
            "face_scan.png",
            width=1.10,
            height=1.30,
            label="any face",
            label_color=YELLOW,
            label_size=15,
            show_frame=False,
        )
        any_face.move_to(LEFT * 5.05 + DOWN * 0.10)
        network = make_neural_network().scale(0.78)
        network.move_to(LEFT * 2.38 + DOWN * 0.04)
        network_label = make_badge("network", color=CYAN, font_size=17)
        network_label.next_to(network, DOWN, buff=0.18)
        embedding = make_vector(["0.42", "-0.18", r"\cdots", "0.73"], font_size=15)
        embedding.move_to(RIGHT * 0.25 + DOWN * 0.02)
        embedding_label = make_badge("embedding", color=GREEN, font_size=17)
        embedding_label.next_to(embedding, DOWN, buff=0.18)

        space_center = RIGHT * 3.98 + DOWN * 0.02
        space_box = RoundedRectangle(
            width=2.55,
            height=2.18,
            corner_radius=0.10,
            stroke_color=GREEN,
            stroke_width=1.4,
            fill_color=PANEL,
            fill_opacity=0.18,
        )
        space_box.move_to(space_center)
        space_title = latex(r"\text{identity space}", size=18, color=GREEN)
        space_title.next_to(space_box, UP, buff=0.12)
        cluster_a = make_embedding_cluster(space_center + LEFT * 0.62 + UP * 0.42, BLUE, scale=0.62, count=4)
        cluster_b = make_embedding_cluster(space_center + RIGHT * 0.55 + UP * 0.16, CYAN, scale=0.62, count=4)
        cluster_c = make_embedding_cluster(space_center + LEFT * 0.12 + DOWN * 0.58, ORANGE, scale=0.56, count=3)
        new_dot = Dot(point=space_center + RIGHT * 0.74 + DOWN * 0.56, color=YELLOW, radius=0.095)
        new_dot_label = latex(r"\text{new}", size=15, color=YELLOW)
        new_dot_label.next_to(new_dot, RIGHT, buff=0.09)
        identity_space = VGroup(space_box, cluster_a, cluster_b, cluster_c, new_dot, new_dot_label, space_title)

        rep_statement = latex(
            r"\text{Learn identity features, not memorized names.}",
            size=25,
            color=WHITE,
        )
        rep_statement.move_to(DOWN * 2.02)
        rep_arrows = VGroup(
            make_flow_arrow(any_face.get_right(), network.get_left(), color=WHITE, stroke_width=1.9),
            make_flow_arrow(network.get_right(), embedding.get_left(), color=CYAN, stroke_width=1.9),
            make_flow_arrow(embedding.get_right(), space_box.get_left(), color=GREEN, stroke_width=1.9),
        )
        phase3 = Group(
            rep_label,
            any_face,
            network,
            network_label,
            embedding,
            embedding_label,
            identity_space,
            rep_statement,
            rep_arrows,
        )
        center_element_group(phase3, max_width=12.0, max_height=4.70)

        self.play(FadeIn(title), run_time=0.5)
        self.play(
            FadeIn(phase1_label),
            FadeIn(img_input),
            FadeIn(classifier),
            FadeIn(fixed_classes),
            run_time=0.65,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in phase1_arrows], lag_ratio=0.20),
            run_time=0.55,
        )
        self.play(FadeIn(fixed_note, shift=0.10 * UP), run_time=0.45)
        self.play(
            LaggedStart(*[ShowPassingFlashAround(c, stroke_color=CYAN, buff=0.05) for c in fixed_classes], lag_ratio=0.12),
            run_time=0.75,
        )
        self.wait(0.35)

        self.play(FadeOut(phase1), run_time=0.45)
        self.play(
            FadeIn(direct_label),
            FadeIn(new_face),
            FadeIn(identity_classifier),
            FadeIn(known_identities),
            run_time=0.65,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in phase2_arrows], lag_ratio=0.18),
            run_time=0.60,
        )
        self.play(
            FadeIn(forced_label, shift=0.10 * UP),
            ShowPassingFlashAround(known_identities, stroke_color=RED, buff=0.08),
            run_time=0.65,
        )
        self.play(WiggleOutThenIn(new_face, run_time=0.60))
        self.play(FadeIn(new_identity_slot), FadeIn(no_slot_note), run_time=0.45)
        self.play(ShowPassingFlashAround(new_identity_slot, stroke_color=YELLOW, buff=0.06), run_time=0.55)
        self.wait(0.35)

        self.play(FadeOut(phase2), run_time=0.45)
        self.play(FadeIn(rep_label), FadeIn(any_face), run_time=0.55)
        self.play(GrowArrow(rep_arrows[0]), FadeIn(network), FadeIn(network_label), run_time=0.65)
        self.play(
            ShowPassingFlashAround(network, stroke_color=CYAN, buff=0.08),
            run_time=0.55,
        )
        self.play(GrowArrow(rep_arrows[1]), FadeIn(embedding), FadeIn(embedding_label), run_time=0.65)
        self.play(GrowArrow(rep_arrows[2]), FadeIn(identity_space), run_time=0.75)
        self.play(new_dot.animate.scale(1.25), run_time=0.25)
        self.play(new_dot.animate.scale(1 / 1.25), run_time=0.25)
        self.play(FadeIn(rep_statement), run_time=0.60)
        self.play(rep_statement.animate.scale(1.05), run_time=0.20)
        self.play(rep_statement.animate.scale(1 / 1.05), run_time=0.20)
        self.wait(0.9)

    def clear_and_wait(self):
        clear_scene(self, run_time=0.65, wait_time=0.35)

    def make_particles_from_group(self, group, count=20, color=CYAN, radius=0.03):
        points = self.sample_points_from_group(group, count)
        return VGroup(*[
            Dot(point=point, radius=radius, color=color)
            for point in points
        ])

    def sample_points_from_group(self, group, count):
        left = group.get_left()[0]
        right = group.get_right()[0]
        bottom = group.get_bottom()[1]
        top = group.get_top()[1]
        points = []
        for i in range(count):
            alpha = 0 if count == 1 else i / (count - 1)
            x = interpolate(left, right, (i % 7) / 6)
            y = interpolate(bottom, top, (int(alpha * 11) % 5) / 4)
            points.append(np.array([x, y, 0]))
        return points
