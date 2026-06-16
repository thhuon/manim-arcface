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

# Preview (display in window, no file saved)
python3 -m manimlib scenes/scene00_introduction.py Scene00Introduction

# Render and save video (default: 720p)
python3 -m manimlib -w scenes/scene00_introduction.py Scene00Introduction

# Render 480p (fast, for testing)
python3 -m manimlib -w -l scenes/scene00_introduction.py Scene00Introduction

# Render 720p
python3 -m manimlib -w -m scenes/scene00_introduction.py Scene00Introduction

# Render 1080p (recommended for final output)
python3 -m manimlib -w --hd scenes/scene00_introduction.py Scene00Introduction

# Render 4K (ultra high quality)
python3 -m manimlib -w --uhd scenes/scene00_introduction.py Scene00Introduction

# Presenter mode (wait for spacebar between animations)
python3 -m manimlib -p scenes/scene00_introduction.py Scene00Introduction

# Save final frame only (fast testing)
python3 -m manimlib -s scenes/scene00_introduction.py Scene00Introduction

# Export as GIF
python3 -m manimlib -i scenes/scene00_introduction.py Scene00Introduction

# Start from animation N (e.g., animation 5)
python3 -m manimlib -w -n 5 scenes/scene00_introduction.py Scene00Introduction

# Custom resolution (e.g., 720)
python3 -m manimlib -w -r 720 scenes/scene00_introduction.py Scene00Introduction

# Custom FPS
python3 -m manimlib -w --fps 30 scenes/scene00_introduction.py Scene00Introduction

# List all scenes in a file
python3 -m manimlib scenes/scene00_introduction.py

# Using venv
cd /home/hg/source/manim-arcface-2
source venv/bin/activate
python -m manimlib -w scenes/scene00_introduction.py Scene00Introduction
```

### Choosing Video Quality

| Quality | Resolution | Use Case | Render Time |
|---------|-----------|----------|-------------|
| **480p** (`-l`) | 854×480 | Quick testing, draft review | ~1x |
| **720p** (`-m`) | 1280×720 | Preview, internal review | ~2x |
| **1080p** (`--hd`) | 1920×1080 | **Recommended for final output** | ~4x |
| **4K** (`--uhd`) | 3840×2160 | Maximum quality, large displays | ~8x+ |

**Recommendations:**
- **Development/Testing**: Use `-l` (480p) for fast iteration during coding
- **Review**: Use `-m` (720p) for scene-by-scene review
- **Final Output**: Use `--hd` (1080p) for YouTube/presentations
- **4K**: Only for large displays or if you have powerful GPU

### Video Output Directory

Rendered videos are saved in:
```
videos/<SceneClass>/
└── <Quality>/
    └── <SceneClass>.mp4
```

Example: `videos/Scene00Introduction/480p15/Scene00Introduction.mp4`

### Useful Flags

| Flag | Description |
|------|-------------|
| `-w` | Write to file (save video) |
| `-s` | Save final frame only (no animation) |
| `-n <num>` | Start at animation number |
| `-o` | Write and open result |
| `-p` | Presenter mode |
| `-l` | Low quality (480p) |
| `-m` | Medium quality (720p) |
| `--hd` | High quality (1080p) |
| `--uhd` | Ultra high quality (4K) |
| `-r <px>` | Custom resolution |
| `--fps <n>` | Custom FPS |
| `-i` | Export as GIF |

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
