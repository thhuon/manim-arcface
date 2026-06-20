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
| **Duration** | ~13 minutes (9 scenes) |
| **Purpose** | Explain ArcFace's additive angular margin loss visually |
| **Audience** | Undergrad CS students with basic ML knowledge |

---

## Video Content Overview

This video explains how modern face recognition systems work, with a focus on the **ArcFace** algorithm. The content is structured as follows:

### Scene 1: Introduction
Opening scene showing multiple photos of the same person under different conditions. Contrasts human instant recognition vs computer pixel-level view. Introduces latent identity and open-set recognition.

### Scene 2: Face Recognition Pipeline
Four-stage pipeline: Input Image → Detection & Alignment → Feature Extraction → Matching/Verification. Explains how raw pixels become an identity decision.

### Scene 3: Challenges
Why face recognition is hard: intra-class variation (same person, different conditions), inter-class similarity (different people, similar faces), real-world use cases requiring stable/accurate/robust embeddings, and open-set recognition.

### Scene 4: Variability
4×3 grid showing the same person under 12 different conditions (lighting, pose, expression, occlusion). Real-world application cards: Phone Unlock, Security Camera, eKYC with stability/accuracy/robustness badges.

### Scene 5: Embedding Space
Transition scene showing embedding clusters forming on a 2D plane. Bridges from Challenges to Softmax.

### Scene 6: Softmax
Introduction to the softmax loss function: formula, geometric interpretation with weight vectors and decision boundaries, limitations (only cares about correct side → loose clusters), and the need for angular margin constraints.

### Scene 7: ArcFace Core
Most important scene: evolution timeline (FaceNet → SphereFace → CosFace → ArcFace), full ArcFace formula with angular margin `cos(θ + m)`, why angular distance matters, normalization, 2D comparison, boundary shifting, and hypersphere view.

### Scene 8: ArcFace vs CosFace
Comparison table, triplet loss challenges vs ArcFace advantages, side-by-side cluster comparison, robustness under difficult conditions, and summary of what ArcFace changes (network unchanged, loss improved, embedding structure much better).

### Scene 9: Closing
Real-world applications (Smartphones, Banking, Airports, Social Networks, Medical). Final hypersphere visualization with tight embedding clusters. "From pixels → geometry → identity."

---

## Technical Specifications

| Item | Value |
|------|-------|
| Resolution | 1920×1080 (1080p) |
| FPS | 60fps |
| Total Duration | ~13 minutes (9 scenes) |
| Output | `.mp4` via FFmpeg |
| Camera | 3D-enabled for hypersphere scenes (Scenes 6-7) |

---

## Project Structure

```
manim-arcface/
├── manimlib/                  # ManimGL core library
├── scenes/                    # Video scene implementations
│   ├── __init__.py
│   ├── utils.py              # Shared utilities (colors, shapes, helpers)
│   ├── scene00_introduction.py    # Scene 0: Introduction (hook, latent identity, open-set)
│   ├── scene01_human_vs_computer.py # Scene 1: Face Recognition Pipeline (4 stages)
│   ├── scene02_face_recognition_pipeline.py # Scene 2: Challenges (embedding quality, intra/inter-class)
│   ├── scene03_challenges.py     # Scene 3: Variability grid + Why accuracy matters
│   ├── scene04_embedding_space.py  # Scene 4: Embedding space transition
│   ├── scene05_softmax.py         # Scene 5: Softmax intro, concept, limitations
│   ├── scene06_arcface_core.py   # Scene 6: ArcFace Core (timeline, formula, hypersphere)
│   ├── scene07_arcface_vs_cosface.py # Scene 7: ArcFace vs CosFace comparison
│   ├── scene08_closing.py         # Scene 8: Applications + closing reveal
│   └── scene09_embedding_transition.py # Scene 9: Embedding transition to ArcFace
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
python3 -m manimlib scenes/<scene_file>.py <SceneClass> [-w] [-l|-m|--hd|--uhd]
```

### Quality Flags

| Flag | Quality |
|------|---------|
| `l` | Low (480p) |
| `m` | Medium (720p) |
| `h` | High (1080p) |
| `p` | Production |

# Preview (display in window, no file saved)
python3 -m manimlib scenes/scene00_introduction.py Scene00_Introduction

# Render and save video (default: 720p)
python3 -m manimlib -w scenes/scene00_introduction.py Scene00_Introduction

# Render 480p (fast, for testing)
python3 -m manimlib -w -l scenes/scene00_introduction.py Scene00_Introduction

# Render 720p
python3 -m manimlib -w -m scenes/scene00_introduction.py Scene00_Introduction

# Render 1080p (recommended for final output)
python3 -m manimlib -w --hd scenes/scene00_introduction.py Scene00_Introduction

# Render 4K (ultra high quality)
python3 -m manimlib -w --uhd scenes/scene00_introduction.py Scene00_Introduction

# Presenter mode (wait for spacebar between animations)
python3 -m manimlib -p scenes/scene00_introduction.py Scene00_Introduction

# Save final frame only (fast testing)
python3 -m manimlib -s scenes/scene00_introduction.py Scene00_Introduction

# Export as GIF
python3 -m manimlib -i scenes/scene00_introduction.py Scene00_Introduction

# Start from animation N (e.g., animation 5)
python3 -m manimlib -w -n 5 scenes/scene00_introduction.py Scene00_Introduction

# Custom resolution (e.g., 720)
python3 -m manimlib -w -r 720 scenes/scene00_introduction.py Scene00_Introduction

# Custom FPS
python3 -m manimlib -w --fps 30 scenes/scene00_introduction.py Scene00_Introduction

# List all scenes in a file
python3 -m manimlib scenes/scene00_introduction.py

# Using venv
cd /home/hg/source/manim-arcface-2
source venv/bin/activate
python -m manimlib -w scenes/scene00_introduction.py Scene00_Introduction
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
python3 -m manimlib -w -l scenes/scene00_introduction.py Scene00Introduction      # 0: Introduction
python3 -m manimlib -w -l scenes/scene01_pipeline.py Scene01_Pipeline              # 1: Pipeline
python3 -m manimlib -w -l scenes/scene02_challenges.py Scene02_Challenges          # 2: Challenges
python3 -m manimlib -w -l scenes/scene03_embedding_space.py Scene03_EmbeddingSpace  # 3: Embedding Space
python3 -m manimlib -w -l scenes/scene04_softmax.py Scene04_Softmax                # 4: Softmax
python3 -m manimlib -w -l scenes/scene05_evolution.py Scene05_Evolution             # 5: Evolution
python3 -m manimlib -w -l scenes/scene06_arcface_mechanism.py Scene06_ArcFaceMechanism  # 6: ArcFace Mechanism
python3 -m manimlib -w -l scenes/scene07_closing.py Scene07_Closing                # 7: Closing
```

Useful flags:
* `-w` to write the scene to a file
* `-l` for low quality (480p, fast testing)
* `-m` for medium quality (720p)
* `--hd` for high quality (1080p)
* `-s` to skip to the final frame
* `-n <number>` to skip ahead to a specific animation
* `-p` for presenter mode (wait for spacebar)
