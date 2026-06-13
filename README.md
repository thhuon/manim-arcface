# Understanding ArcFace: The Geometry Behind Modern Face Recognition

An educational animation project for the **Pattern Recognition** course, explaining ArcFace's additive angular margin loss through visual and intuitive animations.

---

## Course Project Requirements

This project fulfills the following course requirements:

- **Content Alignment**: Explains ArcFace algorithm, a core topic in Pattern Recognition (face recognition and metric learning)
- **Clear Methodology**: Visualizes the mathematical approach with verifiable geometric interpretations
- **Aesthetic Investment**: Custom-designed visuals with cinematic quality and smooth animations
- **Real Dataset Evaluation**: Includes performance evaluation results on actual face recognition datasets
- **Minimum Duration**: 9 minutes (exceeds 5-minute requirement)
- **Original Content**: All content created manually without generative AI

**Bonus Elements**: Real-world applications including smartphone unlock, security systems, and medical diagnostics.

---

## Project Overview

| Item | Value |
|------|-------|
| **Framework** | ManimGL |
| **Style** | Cinematic, geometric, intuition-first |
| **Duration** | ~9 minutes (12 scenes) |
| **Purpose** | Explain ArcFace's additive angular margin loss visually |
| **Audience** | Undergrad CS students with basic ML knowledge |

---

## Video Content Overview

This video explains how modern face recognition systems work, with a focus on the **ArcFace** algorithm. The content is structured as follows:

### Scene 1: Introduction
Opening scene showing how computers represent faces as mathematical vectors, transitioning from human intuition to computational representation.

### Scene 2: Hook
Real-world statistics on face recognition usage (billions of devices daily) and the significance of ArcFace as the gold standard since 2019, adopted by Apple, Google, and major tech companies.

### Scene 3: Pipeline
- **Part A - Human vs Computer**: Contrasts how humans instantly recognize faces versus how computers process pixels
- **Part B - 4-Step Pipeline**: Face Detection → Feature Extraction → Embedding → Verification workflow

### Scene 4: Challenges
- **Part A - Variability**: Same person appears differently under various conditions (lighting, angles, expressions, accessories)
- **Part B - Why Accuracy Matters**: Real-world applications requiring high accuracy (Face ID, security cameras, eKYC)

### Scene 5: Embedding Space
- **Part A - City Map Analogy**: Similar architecture grouped together, analogous to face feature organization
- **Part B - Embedding Concept**: Face images transformed into embedding vectors, clustered by similarity in geometric space

### Scene 6: Softmax Introduction
Introduction to softmax loss function:
- Formula: \( p(y=class) = \frac{\exp(W \cdot x + b)}{\sum \exp(W \cdot x + b)} \)
- 2D visualization with decision boundaries
- Probability distribution across classes

### Scene 7: Softmax Limitation
- **Part A - Classroom Analogy**: Groups sitting too close can easily be confused
- **Part B - Overlapping Clusters**: Decision boundaries too fuzzy, boundary points easily misclassified
- **Part C - Safe Margin**: Need for larger separation between identities

### Scene 8: Evolution Timeline
Evolution of face recognition methods:
- **2015 - FaceNet**: Triplet loss for learning similarity
- **2017 - SphereFace**: Angular margin introduction
- **2018 - CosFace**: Direct cosine similarity optimization
- **2019 - ArcFace**: Combined advantages, became industry standard

### Scene 9: ArcFace Core (Most Important)
- **Part A - Abstract Introduction**: How ArcFace amplifies differences between faces
- **Part B - Why Angle**: Angular distance is more stable than Euclidean distance under varying conditions
- **Part C - Visual Comparison**: Side-by-side softmax vs ArcFace
- **Part D - 3D Hypersphere**: How margin pushes points farther on the unit sphere

### Scene 10: Why It Works
Split-screen comparison showing:
- Left: Softmax with close clusters and fuzzy boundaries
- Right: ArcFace with separated clusters and clear boundaries
- Angular distance measurement demonstrating improved discrimination

### Scene 11: Applications
Real-world applications: smartphone Face ID, ATM authentication, airport automation, social media tagging, medical genetics.

### Scene 12: Closing
Pullback from embedding space to network architecture, summarizing the geometric interpretation of face recognition.

---

## Technical Specifications

| Item | Value |
|------|-------|
| Resolution | 1920×1080 (1080p) |
| FPS | 60fps |
| Output | `.mp4` via FFmpeg |
| Camera | 3D-enabled for hypersphere scenes (Scenes 8-9) |

---

## Project Structure

```
manim-arcface/
├── manimlib/                  # ManimGL core library
├── scenes/                    # Video scene implementations
│   ├── scene01_intro.py
│   ├── scene02_hook.py
│   ├── scene03_pipeline.py
│   ├── scene04_challenges.py
│   ├── scene05_embedding_space.py
│   ├── scene06_softmax_intro.py
│   ├── scene07_softmax_limitation.py
│   ├── scene08_evolution.py
│   ├── scene09_arcface_core.py
│   ├── scene10_why_it_works.py
│   ├── scene11_applications.py
│   └── scene12_closing.py
├── main.py                    # Scene orchestrator
├── videos/                    # Rendered output
├── datasets/                  # Evaluation datasets
├── evaluation/                # Evaluation scripts and results
└── requirements.txt
```

---

## Video Resources

| Resource | Status |
|----------|--------|
| Final Video | [Link to be added] |
| Presentation Slides | [Link to be added] |
| Evaluation Dataset | [Link to be added] |
| Evaluation Results | [Link to be added] |

---

## Installation

Manim runs on Python 3.7 or higher.

System requirements: [FFmpeg](https://ffmpeg.org/), [OpenGL](https://www.opengl.org/), and [LaTeX](https://www.latex-project.org) (optional, for LaTeX rendering).

### Linux

```sh
# Install system dependencies
sudo apt update
sudo apt install ffmpeg libopenblas-dev libxrender-dev libxkbcommon-dev libxxf86vm-dev libsm6 libgl1-mesa-glx

# Install LaTeX (optional)
sudo apt install texlive-latex-base texlive-fonts-recommended texlive-extra-utils

# Install manim
pip install -e .
```

### Windows

1. Install [FFmpeg](https://ffmpeg.org/download.html#windows-builds)
2. Install a LaTeX distribution ([MiKTeX](https://miktex.org/download) recommended)
3. Install Python dependencies:

```sh
pip install -e .
```

### macOS

```sh
# Install dependencies via Homebrew
brew install ffmpeg mactex

# Install manim
pip install -e .
```

---

## Render Commands

Render videos using **ManimGL**:

```bash
manimgl scenes/<scene_file>.py <SceneClass> -w -q <quality>
```

### Quality Flags

| Flag | Quality |
|------|---------|
| `l` | Low (480p) |
| `m` | Medium (720p) |
| `h` | High (1080p) |
| `p` | Production |

### All Scenes

```bash
# Scene 00 - Introduction
manimgl scenes/scene00_introduction.py Scene00Introduction -w

# Scene 01 - Human vs Computer
manimgl scenes/scene01_human_vs_computer.py Scene01_HumanVsComputer -w

# Scene 02 - Face Recognition Pipeline
manimgl scenes/scene02_face_recognition_pipeline.py Scene02_FaceRecognitionPipeline -w

# Scene 03 - Challenges
manimgl scenes/scene03_challenges.py Scene03_Challenges -w
```

### Useful Flags

| Flag | Description |
|------|-------------|
| `-w` | Write to file |
| `-s` | Preview only (skip to end) |
| `-n <num>` | Start at animation number |
| `-o` | Write and open result |

---

## Using Manim

Render a specific scene:

```sh
manimgl scenes/scene09_arcface_core.py ArcFaceCore -w
```

Useful flags:
* `-w` to write the scene to a file
* `-o` to write and open the result
* `-s` to skip to the final frame
* `-n <number>` to skip ahead to a specific animation

### Render and Stitch All Scenes into a Full Video

We have provided two scripts at the root of the project to automate rendering and stitching:

#### 1. Silent Video Compilation (`render_all_scenes.py`)
Automates rendering all 30 scenes in order and stitching them into a single continuous video:

* **Render All (Draft/Preview Quality)**:
  ```sh
  python render_all_scenes.py -d
  ```
* **Render All (Production Quality)**:
  ```sh
  python render_all_scenes.py
  ```
* **Stitch Existing Renders Only**:
  ```sh
  python render_all_scenes.py --skip-render
  ```

#### 2. Voiced Video Compilation (`render_with_voice.py`)
Generates high-quality neural voiceovers (using Microsoft Edge's Neural TTS) for each scene's narration, automatically aligns/extends the video duration (holding the final frame if the voiceover is longer), and merges them into a final narrated video:

* **Render and Voice All (Draft/Preview Quality)**:
  ```sh
  python render_with_voice.py -d
  ```
* **Render and Voice All (Production Quality)**:
  ```sh
  python render_with_voice.py
  ```
* **Voice and Stitch Existing Renders Only (Extremely Fast)**:
  If you have already rendered the scenes and just want to generate/add voiceovers and stitch them together:
  ```sh
  python render_with_voice.py --skip-render
  ```
* **Custom Neural Voices**:
  By default, it uses `en-US-AndrewNeural`. You can specify a different voice (e.g., `en-US-AvaNeural` for a female narrator or `en-US-GuyNeural` for a male narrator):
  ```sh
  python render_with_voice.py --voice en-US-AvaNeural
  ```
