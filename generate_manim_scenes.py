#!/usr/bin/env python3
"""
ManimGL Scene and Asset Generator
This script automates the generation of ManimGL scenes and custom PNG assets
from a narration CSV file using the Groq API with Llama 3.3.
It features a self-healing loop that verifies compilation using a low-res test compile.
"""

import os
import sys
import json
import csv
import subprocess
import urllib.request
import urllib.error
import argparse
import re
import time
import asyncio
import tempfile
import edge_tts

# =============================================================================
# AUTO-DEPENDENCY SETUP
# =============================================================================
def install_dependencies():
    """Ensure groq and python-dotenv are installed in the environment."""
    required = ["groq", "python-dotenv"]
    missing = []
    for pkg in required:
        try:
            if pkg == "python-dotenv":
                import dotenv
            else:
                import groq
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("Dependencies successfully installed.")
        except Exception as e:
            print(f"Warning: Could not install dependencies via pip: {e}")
            print(f"Please install manually: pip install {' '.join(missing)}")

# Run installation of dependencies
install_dependencies()

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

# =============================================================================
# UTILITIES & HELPERS
# =============================================================================
def to_pascal_case(text):
    """Convert a phrase to PascalCase (e.g. 'Why Angle' -> 'WhyAngle')."""
    clean = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    words = re.split(r'[\s_-]+', clean)
    return "".join(word.capitalize() for word in words if word)

def to_snake_case(text):
    """Convert a phrase to snake_case (e.g. 'Why Angle' -> 'why_angle')."""
    clean = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    words = re.split(r'[\s_-]+', clean)
    return "_".join(word.lower() for word in words if word)

def get_scene_descriptive_name(scene):
    """Generate a clean, descriptive name for a scene using name and subscene."""
    name = scene.get("name", "").strip()
    subscene = ""
    if scene.get("beats"):
        subscene = scene["beats"][0].get("subscene", "").strip()
        # Strip prefixes like "A. ", "B. ", "1. ", "Part A: "
        subscene = re.sub(r'^[A-Za-z0-9\s]+:\s*', '', subscene)
        subscene = re.sub(r'^[A-Z0-9]\.\s*', '', subscene)
        
    if not name:
        return subscene if subscene else f"Scene{scene['id']}"
        
    if subscene and subscene.lower() not in name.lower():
        return f"{name} {subscene}"
        
    return name

def get_file_content(path):
    """Safely read and return file contents."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def clean_python_code(code):
    """Clean Python code by stripping comments and docstrings to save tokens."""
    lines = []
    in_docstring = False
    docstring_char = None
    
    for line in code.splitlines():
        stripped = line.strip()
        if not in_docstring:
            if stripped.startswith('"""') or stripped.startswith("'''"):
                in_docstring = True
                docstring_char = stripped[:3]
                if stripped.count(docstring_char) == 2 and len(stripped) > 3:
                    in_docstring = False
                continue
        else:
            if docstring_char in stripped:
                in_docstring = False
            continue
            
        if stripped.startswith("#"):
            continue
        if not stripped:
            continue
        if "#" in line:
            if not ('"' in line or "'" in line):
                line = line.split("#")[0]
        lines.append(line.rstrip())
        
    return "\n".join(lines)

def clean_markdown(text):
    """Clean Markdown text by removing HTML comments and excessive blank lines."""
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("<!--") or stripped.endswith("-->"):
            continue
        lines.append(line)
    return "\n".join(lines)

def get_existing_decorations():
    """List all files in scenes/decorations to provide LLM context."""
    dec_dir = os.path.join("scenes", "decorations")
    if os.path.exists(dec_dir):
        files = [f for f in os.listdir(dec_dir) if os.path.isfile(os.path.join(dec_dir, f))]
        face_files = [f for f in files if f.startswith("face_") and f[5:-4].isdigit()]
        non_face_files = [f for f in files if f not in face_files]
        if face_files:
            non_face_files.append("face_1.png to face_48.png")
        return sorted(non_face_files)
    return []

# =============================================================================
# NARRATION PARSER
# =============================================================================
async def compute_narration_duration(text, voice="en-US-AndrewNeural", retries=3):
    if not text.strip():
        return 0.0
    
    temp_fd, temp_path = tempfile.mkstemp(suffix=".mp3")
    os.close(temp_fd)
    
    for attempt in range(retries):
        try:
            communicate = edge_tts.Communicate(text, voice)
            await asyncio.wait_for(communicate.save(temp_path), timeout=5.0)
            
            # Get duration using ffprobe
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                temp_path
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            dur = float(result.stdout.strip())
            return dur
        except Exception as e:
            if attempt == retries - 1:
                # Fallback heuristic: approx 15 chars per second (about 150 words per minute)
                return max(1.0, len(text) / 15.0)
            await asyncio.sleep(1.0 * (attempt + 1))
        finally:
            if os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
    return max(1.0, len(text) / 15.0)

def get_narration_duration(text, voice="en-US-AndrewNeural"):
    try:
        return asyncio.run(compute_narration_duration(text, voice))
    except Exception:
        return max(1.0, len(text) / 15.0)

def parse_narration_csv(filepath="narration.csv"):
    """Parse narration.csv and group rows by Scene ID (#) with duration calculation."""
    scenes = {}
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found in the current folder!")
        sys.exit(1)
        
    print("Pre-calculating narration durations for all beats...")
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        
        for row in reader:
            if not row or len(row) < 7:
                continue
            
            scene_id_str = row[0].strip()
            if not scene_id_str:
                continue
            
            try:
                scene_id = int(scene_id_str)
            except ValueError:
                continue
            
            scene_name = row[1].strip()
            subscene = row[2].strip()
            notes = row[3].strip()
            narration = row[4].strip()
            camera = row[5].strip()
            transition = row[6].strip()
            
            if scene_id not in scenes:
                scenes[scene_id] = {
                    "id": scene_id,
                    "name": scene_name,
                    "beats": []
                }
            
            # Split narration by double newlines to make multiple beats if there are paragraph breaks
            raw_paras = [p.strip() for p in narration.split("\n\n") if p.strip()]
            if not raw_paras:
                raw_paras = [narration]
                
            for idx, para in enumerate(raw_paras):
                scenes[scene_id]["beats"].append({
                    "subscene": f"{subscene} (Part {idx+1})" if (subscene and len(raw_paras) > 1) else subscene,
                    "notes": notes if idx == 0 else "",
                    "narration": para,
                    "duration": 0.0,
                    "camera": camera if idx == 0 else "",
                    "transition": transition if idx == len(raw_paras) - 1 else ""
                })
            
    return scenes

def format_scene_context(scene):
    """Format the beats of a scene into a string for the prompt."""
    context = f"Scene ID: {scene['id']}\nScene Name: {scene['name']}\n\nBeats:\n"
    for i, beat in enumerate(scene["beats"]):
        context += f"Beat {i+1}:\n"
        if beat["subscene"]:
            context += f"  Subscene/Part: {beat['subscene']}\n"
        if beat["notes"]:
            context += f"  Notes: {beat['notes']}\n"
        if beat["narration"]:
            context += f"  Narration: {beat['narration']}\n"
            context += f"  Narration Audio Duration: {beat['duration']:.2f} seconds\n"
        if beat["camera"]:
            context += f"  Camera Movement: {beat['camera']}\n"
        if beat["transition"]:
            context += f"  Transition: {beat['transition']}\n"
        context += "\n"
    return context

# =============================================================================
# COMPILER TEST & HEALING
# =============================================================================
def test_compile(filepath, classname):
    """Test compile a scene using a low-res single frame render (-s flag)."""
    # Prepend software rendering to avoid GPU errors
    cmd = [sys.executable, "-m", "manimlib", "-w", "-l", filepath, classname, "-s"]
    env = os.environ.copy()
    env["LIBGL_ALWAYS_SOFTWARE"] = "1"
    
    print(f"Testing compilation of class '{classname}' in '{filepath}'...")
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            timeout=40
        )
        if result.returncode == 0:
            return True, ""
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Compilation timed out after 40 seconds."
    except Exception as e:
        return False, f"Failed to start compiler subprocess: {e}"

# =============================================================================
# API INTERACTION
# =============================================================================
def build_system_prompt(skills_content, utils_content):
    """Create the base system prompt with guidelines and library context."""
    return f"""You are an expert Python developer and animator specializing in ManimGL (3b1b version).
Your task is to write perfect, high-quality, bug-free python scripts for educational animations explaining the ArcFace face recognition algorithm.

---
### CRITICAL RULES TO PREVENT COMPILATION ERRORS:
1. Do NOT use hallucinated classes, functions, or camera properties:
   - Do NOT use `SceneTransition()` or any custom transition class. Use standard animations like `self.play(FadeIn(...))` or `self.play(FadeOut(...))`.
   - Do NOT use `self.camera.zoom_in`, `self.camera.zoom`, or `self.camera.set_zoom`. In ManimGL, camera zoom/pan is done by changing the camera frame scale or position (e.g. `self.play(self.camera.frame.animate.scale(0.5))` or `self.play(self.camera.frame.animate.move_to(point))`).
   - Do NOT use `Create` (always use `ShowCreation`).
   - Do NOT use `Write(Text(...))` (always use `Write(Tex(...))`).
   - Do NOT use custom external modules that are not standard.
   - For image and SVG loading, ALWAYS wrap the filename in the `asset_path()` helper! For example: `SVGMobject(asset_path("filename.svg"))`.

---
### MANIMGL CODING GUIDELINES & STYLE RULES
You must follow these rules strictly. Any violation will make the code fail to compile or look unprofessional!

{skills_content}

---
### REUSABLE HELPERS (from scenes/utils.py)
You can import and use any of these constants and helper functions from `scenes.utils`:
{utils_content}
"""

def build_user_prompt(scene, existing_decorations):
    """Create the scene-specific user prompt."""
    scene_context = format_scene_context(scene)
    decorations_str = ", ".join(existing_decorations)
    desc_name = get_scene_descriptive_name(scene)
    classname = f"Scene{scene['id']:02d}_{to_pascal_case(desc_name)}"
    
    return f"""### SCENE TO ANIMATE
{scene_context}

### EXPECTED CLASS NAME
The generated class name MUST be: `{classname}`

### EXISTING DECORATIONS (in scenes/decorations/)
Use these assets if they fit the narration, but DO NOT assume other assets exist.
CRITICAL: You MUST wrap the filename in `asset_path()` helper to load these files!
Example: `SVGMobject(asset_path("devices.svg"))` or `ImageMobject(asset_path("face_A.png"))`.
[{decorations_str}]

### DETAILED INSTRUCTIONS:
1. **Pacing and Timing Alignment (CRITICAL)**:
   - For each Beat in this scene, you are provided with the exact `Narration Audio Duration` in seconds.
   - The animations you write for that Beat MUST be paced and slowed down so they span the entire duration of that beat's audio.
   - Do NOT play all animations quickly and then sit on a static screen.
   - To achieve perfect pacing:
     a. Divide your `construct` code into logical sections corresponding to each Beat.
     b. For each section, calculate the total duration of the animations (`run_time` parameters in your `self.play()` calls) and wait times (`self.wait()` calls).
     c. Ensure that the total duration of each section matches the `Narration Audio Duration` for that beat.
        For example, if Beat 1 has a duration of 35.88 seconds, and your animations in Beat 1 take 10 seconds of runtime, you must add `self.wait(25.88)` spread out or at the end of Beat 1.
     d. Spread the wait times and animations out naturally! For example, instead of doing `self.wait(25.88)` at the very end, do smaller waits like `self.wait(5.0)` between key animations in that Beat to keep the visual pacing aligned with the voice.
     e. Keep elements visible on screen! Do NOT call `FadeOut` or clear elements at the end of a beat if the narration for the next beat refers to them or builds upon them. Keep them on screen so the user can read/view them.
     f. The entire scene MUST NOT fade out to black until the very end of the final beat.
     
2. **Dynamic Animations and Visual Diversity**:
   - The user complained that "video play and it finish fast and then last screen of the scene stay until audio finish".
   - You MUST add more intermediate animations, steps, and visual movements so that the video is constantly alive and active, showing exactly what is being narrated at that moment.
   - For example: instead of fading in a diagram all at once, fade in its parts step-by-step.
   - Introduce subtle animations like glowing elements, moving pointers, data flow animations (e.g., small circles traveling along lines), pulsed scaling effects, or highlighting specific nodes/labels as they are discussed in the narration text.
   - If there is a wait time, use small, subtle loop animations (like self.play(Transform(...), run_time=...)) or sub-animations to keep the canvas alive, or slow down the existing animations (e.g. increase run_time of complex transitions to 2.5s or 3.0s).

3. **Prefer Vector Drawings and Existing Assets**:
   - Construct diagrams and icons directly inside ManimGL using standard vector shapes (Circle, Rectangle, Line, Arrow, etc.) or reuse existing SVG assets (devices.svg, lock.svg, face-id.svg, etc.) from the decorations list. This is 100% preferred over generating raster images.
   - ALWAYS load local SVGs using: `SVGMobject(asset_path("filename.svg"))`. Do NOT write `SVGMobject("filename.svg")` as it will fail!
   - ALWAYS load local PNGs using: `ImageMobject(asset_path("filename.png"))`. Do NOT write `ImageMobject("filename.png")` as it will fail!

4. **Asset Generation Code (`asset_generator_code`)**:
   - ONLY generate a custom PNG asset via PIL/matplotlib if you need a complex statistical plot, chart, or data visualization that cannot be easily built in Manim.
   - If generating a PNG, save it to `scenes/decorations/filename.png` with a transparent background.
   - If no custom external PNG is needed, set this to an empty string.

5. **ManimGL Code (`manim_code`)**:
   - Write the complete python code for the ManimGL class `{classname}` (extending `Scene`, or `ThreeDScene` if the scene specifically requires 3D).
   - Must import `from manimlib import *` and `from scenes.utils import *`.
   - Adhere strictly to the styling guidelines: LaTeX ONLY (no plain Text), no hardcoded absolute coords (except ORIGIN), use VGroup/Group correctly (remember: ImageMobject is NOT a VMobject, so use `Group` instead of `VGroup` when containerizing combinations of ImageMobjects and VMobjects to avoid crashes), use `ShowCreation` (not `Create`), make it look slow, clean, and elegant.

You must return a JSON object with this exact structure:
{{
  "asset_generation_explanation": "Explain what PNG assets are needed and how they are generated.",
  "asset_generator_code": "Python code using PIL/matplotlib to generate assets.",
  "manim_scene_explanation": "Explain the design of the ManimGL animation.",
  "manim_code": "Complete ManimGL Scene Python code."
}}
"""

def call_groq_api(api_key, messages, max_retries=4, backoff_seconds=30):
    """Call Groq API using standard urllib to avoid dependency conflicts, with retry and multi-model fallback."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # Ordered list of models to fall back through in case of rate limits, TPD limits, or payload size limits
    models = [
        "qwen/qwen3-32b",
        "llama-3.1-8b-instant",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "llama-3.3-70b-versatile",
        "openai/gpt-oss-20b"
    ]
    
    def extract_json(text):
        import re
        # Strip <think>...</think> reasoning blocks from reasoning models
        text_clean = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
        
        try:
            return json.loads(text_clean)
        except Exception:
            pass
            
        # Try finding markdown code block
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text_clean, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except Exception:
                pass
                
        # Try finding first brace and last brace
        first_brace = text_clean.find("{")
        last_brace = text_clean.rfind("}")
        if first_brace != -1 and last_brace != -1:
            try:
                return json.loads(text_clean[first_brace:last_brace+1].strip())
            except Exception:
                pass
        return None

    # We iterate over the models to find one that works
    for model in models:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 1200
        }
        # Only use json_object response format for models that officially support it
        if "llama" in model:
            payload["response_format"] = {"type": "json_object"}
            
        data = json.dumps(payload).encode("utf-8")
        
        # Sleep to avoid hitting Groq RPM/TPM limits
        time.sleep(10)
        print(f"  Trying model: {model}...")
        
        for attempt in range(1, max_retries + 1):
            req = urllib.request.Request(url, data=data, method="POST")
            req.add_header("Content-Type", "application/json")
            req.add_header("Authorization", f"Bearer {api_key}")
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            try:
                with urllib.request.urlopen(req) as response:
                    res_body = response.read().decode("utf-8")
                    res_json = json.loads(res_body)
                    content = res_json["choices"][0]["message"]["content"]
                    parsed_json = extract_json(content)
                    if parsed_json is not None:
                        return parsed_json
                    else:
                        print("  Warning: Model response did not contain valid JSON. Content was:")
                        print("-" * 50)
                        print(content)
                        print("-" * 50)
            except urllib.error.HTTPError as e:
                err_body = ""
                try:
                    err_body = e.read().decode("utf-8")
                except Exception:
                    pass
                
                # If rate-limited (429), or request too large (413), or payload issues
                if e.code == 429:
                    if "TPD" in err_body or "daily limit" in err_body or "tokens per day" in err_body:
                        print(f"    Model {model} hit daily limit (TPD). Falling back to next model immediately...")
                        break
                    
                    if model != models[-1]:
                        print(f"    Rate limit (429) hit for model {model}. Falling back to next model immediately...")
                        break
                    else:
                        print(f"    Rate limit (429) hit for model {model} (last fallback).")
                        if attempt < max_retries:
                            wait_time = backoff_seconds * attempt
                            print(f"    Retrying in {wait_time} seconds (attempt {attempt}/{max_retries})...")
                            time.sleep(wait_time)
                            continue
                        else:
                            print(f"    Max retries reached for model {model}.")
                            break
                elif e.code == 413 or "TPM" in err_body or "TPD" in err_body or "too large" in err_body:
                    print(f"    Model {model} hit token/size limit or bad request. Details: {err_body}. Falling back to next model...")
                    break
                else:
                    print(f"    HTTP Error {e.code} for model {model}. Details: {err_body}. Falling back to next model...")
                    break
            except Exception as e:
                print(f"    Error calling Groq API with {model}: {e}. Falling back to next model...")
                break
                
    print("Error: All fallback models failed or were rate-limited.")
    return None

# =============================================================================
# MAIN PIPELINE
# =============================================================================
def generate_scene(scene, api_key, system_prompt, force=False):
    """Execute the generation and self-healing loop for a single scene."""
    scene_id = scene["id"]
    desc_name = get_scene_descriptive_name(scene)
    scene_name_clean = to_snake_case(desc_name)
    filename = f"scene{scene_id:02d}_{scene_name_clean}.py"
    filepath = os.path.join("scenes", filename)
    classname = f"Scene{scene_id:02d}_{to_pascal_case(desc_name)}"
    
    # Check if scene file already exists
    if os.path.exists(filepath) and not force:
        print(f"Scene {scene_id:02d} ({filepath}) already exists. Skipping. Use --overwrite to force.")
        return True
        
    # Lazy calculate durations on-the-fly for the scene we are generating
    print(f"Calculating narration durations for Scene {scene_id:02d} beats...")
    for idx, beat in enumerate(scene["beats"]):
        beat["duration"] = get_narration_duration(beat["narration"])
        print(f"  Beat {idx+1}: {beat['narration'][:45]}... ({beat['duration']:.2f}s)")
    
    print(f"\n=============================================================================")
    print(f"GENERATING SCENE {scene_id:02d}: {scene['name']}")
    print(f"=============================================================================")
    
    existing_decorations = get_existing_decorations()
    user_prompt = build_user_prompt(scene, existing_decorations)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        print(f"Attempt {attempt}/{max_attempts} calling Groq API...")
        response = call_groq_api(api_key, messages)
        
        if not response:
            print("Failed to get response from Groq. Aborting scene generation.")
            return False
            
        asset_explanation = response.get("asset_generation_explanation", "")
        asset_code = response.get("asset_generator_code", "")
        manim_explanation = response.get("manim_scene_explanation", "")
        manim_code = response.get("manim_code", "")
        
        # 1. Run Asset Generation
        if asset_code.strip():
            print(f"Asset explanation: {asset_explanation}")
            print("Running asset generator code...")
            os.makedirs(os.path.join("scenes", "decorations"), exist_ok=True)
            try:
                # Execute asset generation code in local namespace
                namespace = {}
                exec(asset_code, globals(), namespace)
                print("Asset generation complete!")
            except Exception as e:
                print(f"Warning: Asset generator code failed: {e}")
                # We do not fail the loop just for asset code, since the manim code might still work
                
        # 2. Write Manim Code to File
        print(f"Writing ManimGL code to {filepath}...")
        os.makedirs("scenes", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(manim_code)
            
        # 3. Test Compile
        compiled, error_msg = test_compile(filepath, classname)
        if compiled:
            print(f"SUCCESS: Scene {scene_id:02d} compiled successfully!")
            print(f"Design details: {manim_explanation}")
            return True
        else:
            print(f"\n❌ Compilation Failed on Attempt {attempt}!")
            print(f"Error details:\n{error_msg}\n")
            
            if attempt == max_attempts:
                print("Max compilation attempts reached. Please fix the file manually.")
                return False
                
            print("Initiating Self-Healing feedback loop...")
            healing_prompt = f"""The code you generated failed to compile. Here is the compilation error output:
```
{error_msg}
```

Please identify and fix the compiler error. Common issues:
- Using Manim Community classes/methods instead of ManimGL (e.g. use `ShowCreation` instead of `Create`, check parameters of `Arrow`, `Brace`, `Tex`, etc.).
- Incorrect layout alignments.
- Undefined variables or naming mismatches.

Regenerate the complete corrected code and respond in the same JSON format."""
            
            # Reset messages to a clean 4-message context to prevent token count accumulation
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": json.dumps(response)},
                {"role": "user", "content": healing_prompt}
            ]

    return False

# =============================================================================
# CLI RUNNER
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="Generate ManimGL scenes and assets from narration.csv using Groq API.")
    parser.add_argument("--scene", type=int, help="ID of a specific scene to generate.")
    parser.add_argument("--all", action="store_true", help="Generate all missing scenes.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing scene files.")
    parser.add_argument("--list", action="store_true", help="List all parsed scenes from narration.csv.")
    args = parser.parse_args()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable is not set!")
        print("Please check your .env file or export the variable: export GROQ_API_KEY=your_key")
        sys.exit(1)

    # Parse CSV
    scenes = parse_narration_csv()
    
    if args.list:
        print("Parsed Scenes from narration.csv:")
        for idx in sorted(scenes.keys()):
            scene = scenes[idx]
            beats_cnt = len(scene["beats"])
            print(f"  [{idx:02d}] {scene['name']} ({beats_cnt} beat(s))")
        sys.exit(0)

    # Ensure scenes and decorations dirs exist
    os.makedirs(os.path.join("scenes", "decorations"), exist_ok=True)

    # Load prompt context
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
- CRITICAL: Do NOT confuse helper functions (like `make_neural_network()`, `make_box()`, `make_vector()`, `make_camera_icon()`, `make_abstract_face()`, `make_landmarks()`, `make_pixel_grid()`) with SVG files. Do NOT try to load `neural_network.svg` or `box.svg`. Call the python helper function directly (e.g. `nn = make_neural_network()`).

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
    
    system_prompt = build_system_prompt(skills_content, utils_content)

    if args.scene is not None:
        if args.scene not in scenes:
            print(f"Error: Scene ID {args.scene} not found in narration.csv!")
            sys.exit(1)
        generate_scene(scenes[args.scene], api_key, system_prompt, force=args.overwrite)
    elif args.all:
        print(f"Starting generation for all scenes. Overwrite={args.overwrite}")
        success_cnt = 0
        fail_cnt = 0
        for idx in sorted(scenes.keys()):
            # Skip scenes 0-3 by default unless overwrite is specified, to preserve existing manual work
            if idx <= 3 and not args.overwrite:
                continue
            
            success = generate_scene(scenes[idx], api_key, system_prompt, force=args.overwrite)
            if success:
                success_cnt += 1
            else:
                fail_cnt += 1
            
            # Sleep between scenes to avoid rate limits
            if idx < max(scenes.keys()):
                print("Sleeping 5 seconds to prevent rate limits between scenes...")
                time.sleep(5.0)
                
        print(f"\nBatch Generation Summary:")
        print(f"  Successfully Generated: {success_cnt}")
        print(f"  Failed to Compile: {fail_cnt}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
