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
        return [f for f in os.listdir(dec_dir) if os.path.isfile(os.path.join(dec_dir, f))]
    return []

# =============================================================================
# NARRATION PARSER
# =============================================================================
def parse_narration_csv(filepath="narration.csv"):
    """Parse narration.csv and group rows by Scene ID (#)."""
    scenes = {}
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found in the current folder!")
        sys.exit(1)
        
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
            
            # Add beat
            scenes[scene_id]["beats"].append({
                "subscene": subscene,
                "notes": notes,
                "narration": narration,
                "camera": camera,
                "transition": transition
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
1. **Prefer Vector Drawings and Existing Assets**:
   - Construct diagrams and icons directly inside ManimGL using standard vector shapes (Circle, Rectangle, Line, Arrow, etc.) or reuse existing SVG assets (devices.svg, lock.svg, face-id.svg, etc.) from the decorations list. This is 100% preferred over generating raster images.
   - ALWAYS load local SVGs using: `SVGMobject(asset_path("filename.svg"))`. Do NOT write `SVGMobject("filename.svg")` as it will fail!
   - ALWAYS load local PNGs using: `ImageMobject(asset_path("filename.png"))`. Do NOT write `ImageMobject("filename.png")` as it will fail!
   
2. **Asset Generation Code (`asset_generator_code`)**:
   - ONLY generate a custom PNG asset via PIL/matplotlib if you need a complex statistical plot, chart, or data visualization that cannot be easily built in Manim.
   - If generating a PNG, save it to `scenes/decorations/filename.png` with a transparent background.
   - If no custom external PNG is needed (highly recommended for icons/simple shapes), set this to an empty string.

3. **ManimGL Code (`manim_code`)**:
   - Write the complete python code for the ManimGL class `{classname}` (extending `Scene`, or `ThreeDScene` if the scene specifically requires 3D).
   - Must import `from manimlib import *` and `from scenes.utils import *`.
   - Adhere strictly to the styling guidelines: LaTeX ONLY (no plain Text), no hardcoded absolute coords (except ORIGIN), use VGroup/Group correctly (remember: ImageMobject is NOT a VMobject, so use `Group` instead of `VGroup` when containerizing combinations of ImageMobjects and VMobjects to avoid crashes), use `ShowCreation` (not `Create`), make it look slow, clean, and elegant.
   - Ensure the duration matches the narration speed (wait times, transitions).

You must return a JSON object with this exact structure:
{{
  "asset_generation_explanation": "Explain what PNG assets are needed and how they are generated.",
  "asset_generator_code": "Python code using PIL/matplotlib to generate assets.",
  "manim_scene_explanation": "Explain the design of the ManimGL animation.",
  "manim_code": "Complete ManimGL Scene Python code."
}}
"""

def call_groq_api(api_key, messages, max_retries=4, backoff_seconds=30):
    """Call Groq API using standard urllib to avoid dependency conflicts, with retry on rate limits."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": messages,
        "temperature": 0.1,
        "response_format": {"type": "json_object"}
    }
    
    data = json.dumps(payload).encode("utf-8")
    
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
                return json.loads(content)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                err_body = ""
                try:
                    err_body = e.read().decode("utf-8")
                except Exception:
                    pass
                if attempt == max_retries:
                    print(f"Rate limit hit (429). Max retries reached. Details: {err_body}")
                    return None
                wait_time = backoff_seconds * attempt
                print(f"Rate limit hit (429). Details: {err_body}")
                print(f"Retrying in {wait_time} seconds (attempt {attempt}/{max_retries})...")
                time.sleep(wait_time)
                continue
                
            print(f"Groq API HTTP Error: {e.code} - {e.reason}")
            try:
                err_body = e.read().decode("utf-8")
                print(f"Error details: {err_body}")
            except Exception:
                pass
            return None
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return None
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
    skills_content = clean_markdown(get_file_content(os.path.join(".cursor", "skills", "skills.md")))
    utils_content = clean_python_code(get_file_content(os.path.join("scenes", "utils.py")))
    
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
                print("Sleeping 15 seconds to prevent rate limits between scenes...")
                time.sleep(15)
                
        print(f"\nBatch Generation Summary:")
        print(f"  Successfully Generated: {success_cnt}")
        print(f"  Failed to Compile: {fail_cnt}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
