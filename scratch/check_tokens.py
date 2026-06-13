import os
import sys

# Add working directory to path to import helpers
sys.path.append(os.path.abspath("."))

from generate_manim_scenes import parse_narration_csv, build_system_prompt, build_user_prompt, get_existing_decorations

scenes = parse_narration_csv()
scene = scenes[0]

skills_content = """
## Rule 1: ABSOLUTE TYPOGRAPHY — NO PLAIN TEXT
- Do NOT use `Text(...)`, plain system fonts, or any non-LaTeX text.
- Every piece of text MUST be written in LaTeX using `Tex(r"\\text{...}")`.
- Font sizes: Title=72, Subtitle=32, Label=24.
- Always use raw strings: `r"..."`.

## Rule 2: HYBRID VECTOR ASSETS — NO PRIMITIVE CODE FOR COMPLEX SHAPES
- Do NOT draw smartphones, laptops, padlocks, icons, or complex shapes using primitive shapes.
- Use `SVGMobject(asset_path("filename.svg"))` or the helper `white_svg("filename.svg", height)`.
- Always wrap asset filenames in `asset_path()`.

## Rule 3: ORTHOGRAPHIC CAMERA — ZERO CAMERA MODIFICATIONS
- Always extend `Scene`, never `ThreeDScene`. Do not orient or rotate the camera.
- To zoom or pan, scale or move the camera frame: `self.camera.frame.animate.scale(0.5)` or `self.camera.frame.animate.move_to(point)`.

## Rule 4: GRAPHIC PALETTE ONLY
- Use the palette from `scenes/utils.py`: CYAN = "#00D4FF", BLUE = "#4A7DFF", WHITE = "#F2F6FF", MUTED = "#8A94A6", DARK = "#0A0E14", PANEL = "#101722", GREEN = "#3EF7A0".

## Rule 5: MATH-FIRST STORYTELLING
- Use standard LaTeX equations and align them properly.

## Rule 6: SMOOTH CONTINUOUS ANIMATIONS
- Align animation times with the narration beat durations provided.
- Avoid static screens by adding loops, camera pans, and detailed steps.
"""

utils_content = """
# Color constants
CYAN = "#00D4FF"
BLUE = "#4A7DFF"
WHITE = "#F2F6FF"
MUTED = "#8A94A6"
DARK = "#0A0E14"
PANEL = "#101722"
GREEN = "#3EF7A0"

# Helper functions
def asset_path(filename: str) -> str: ... # Return absolute path to decorations/filename
def white_svg(filename: str, height: float) -> SVGMobject: ... # Load SVG as solid-white vector
def latex(text: str, size: int = 28, color=WHITE) -> Tex: ... # Styled LaTeX Tex element
def glow_copy(mob, color=CYAN, width=7, opacity=0.18) -> Mobject: ... # glowing copy of mob
def make_box(label_lines, width=2.35, height=1.28, stroke=CYAN, font_size=22) -> VGroup: ... # rounded box with lines
def make_vector(values, font_size=19) -> VGroup: ... # vector with brackets
def make_camera_icon() -> VGroup: ... # camera icon mobject
def make_abstract_face() -> VGroup: ... # face icon mobject
def make_landmarks() -> VGroup: ... # 5 landmarks dots
def make_pixel_grid(size=2.15, n=8) -> VGroup: ... # grid overlay
def make_neural_network() -> VGroup: ... # neural network
"""

sys_prompt = build_system_prompt(skills_content, utils_content)
existing_decorations = get_existing_decorations()
usr_prompt = build_user_prompt(scene, existing_decorations)

print(f"System Prompt characters: {len(sys_prompt)}")
print(f"User Prompt characters: {len(usr_prompt)}")
print(f"Total prompt characters: {len(sys_prompt) + len(usr_prompt)}")
print(f"Approximate tokens (chars/4): {(len(sys_prompt) + len(usr_prompt)) / 4:.1f}")
