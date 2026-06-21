# Understanding ArcFace: The Geometry Behind Modern Face Recognition

An educational animation project for the **Pattern Recognition** course, explaining ArcFace's additive angular margin loss through visual and intuitive animations.

---

## Course Project Requirements

This project fulfills the following course requirements:

- **Content Alignment**: Explains ArcFace algorithm, a core topic in Pattern Recognition (face recognition and metric learning)
- **Clear Methodology**: Visualizes the mathematical approach with verifiable geometric interpretations
- **Aesthetic Investment**: Custom-designed visuals with cinematic quality and smooth animations
- **Real Dataset Evaluation**: Includes performance evaluation results on actual face recognition datasets
- **Minimum Duration**: 8 minutes (exceeds 5-minute requirement)
- **Original Content**: All content created manually without generative AI

**Bonus Elements**: Real-world applications including smartphone unlock, security systems, and medical diagnostics.

---

## Project Overview

| Item | Value |
|------|-------|
| **Framework** | ManimGL (3b1b version) |
| **Style** | 3Blue1Brown — cinematic, geometric, intuition-first |
| **Duration** | ~15 minutes (8 scenes) |
| **Purpose** | Explain ArcFace's additive angular margin loss visually |
| **Audience** | Undergrad CS students with basic ML knowledge |

---

## Video Content Overview

This video explains how modern face recognition systems work, with a focus on the **ArcFace** algorithm. The content is structured as follows:

### Scene 0: Introduction
**Beats:** A - Same Identity Different Images → B - Computer Sees Numbers → C - What Are We Recognizing → D - Open-Set Bridge
Contrasts human instant recognition with computer pixel-level view. Introduces the concept of latent identity — the hidden pattern behind millions of pixels — and bridges to the question of why face recognition cannot simply classify identities by name.

### Scene 1: Face Recognition Pipeline
**Beats:** Overview → Stage 1: Input Image → Stage 2: Detection & Alignment → Stage 3: Feature Extraction → Stage 4: Matching/Verification → Final Recap
Four-stage pipeline: Input Image → Detection & Alignment → Feature Extraction → Matching/Verification. Shows how raw pixels become an embedding vector and then an identity decision.

### Scene 2: Challenges
**Beats:** A - Good Embedding Space → B - Intra-Class Variation → C - Inter-Class Similarity → D - Why Accuracy Matters → E - Open-Set Transition
Three core challenges of face recognition: intra-class variation (same person, different conditions), inter-class similarity (different people, similar faces), and open-set recognition (unseen identities). Introduces the two goals: compact clusters and wide margins.

### Scene 3: Embedding Space
**Beats:** A - Manual Grouping → B - Network Learns to Place Faces → C - Distances Carry Meaning → D - Embedding Space Is Learned → E - What Objective Shapes The Space
How neural networks turn face images into geometric points. Introduces the embedding space concept: coordinates matter less than relative geometry. Shows how training shapes the space through backpropagation.

### Scene 4: Softmax
**Beats:** A - Embedding Space Transition (bridge) → B - Loss Function Introduction → C - How Softmax Works → D - Softmax Limitations
Loss function introduction: how Softmax classifies by comparing embeddings against class weight vectors. Geometric interpretation with decision boundaries. Key limitation: Softmax only requires being on the correct side of the boundary — it does not enforce compact clusters or wide separation.

### Scene 5: Evolution
**Beats:** A - Milestones (FaceNet → SphereFace → CosFace → ArcFace)
Timeline of face recognition milestones: FaceNet (Triplet Loss, 2015), SphereFace (Multiplicative Angular Margin, 2017), CosFace (Additive Cosine Margin, 2018), ArcFace (Additive Angular Margin, 2018). Bridges to the ArcFace Mechanism scene.

### Scene 6: ArcFace Mechanism
**Beats:** 1 - ArcFace Formula → 2 - Why Angular Distance → 3 - 2D Comparison (Softmax vs ArcFace) → 4 - Angular Margin Geometric View → 5 - Normalisation → 6 - Formula Step by Step → 7 - Boundary Shift → 8 - Hypersphere Embedding Space
The core scene. Explains normalization (L2 on embeddings and weights), why angular distance matters on the unit hypersphere, the full ArcFace formula `cos(θ + m)`, boundary shifting effect, and the geometric meaning of additive angular margin.

### Scene 7: Closing
**Beats:** A - Real-World Applications → B - Final Closing
Real-world applications (Smartphones, Banking, Airports, Social Networks, Medical). Final closing: from pixels → geometry → identity. "From pixels → geometry → identity."

---

## Technical Specifications

| Item | Value |
|------|-------|
| Resolution | 1920×1080 (1080p) |
| FPS | 60fps |
| Total Duration | ~15 minutes (8 scenes) |
| Output | `.mp4` via FFmpeg |
| Camera | 3D-enabled for hypersphere scenes (Scene 6) |

---

## Project Structure

```
manim-arcface-2/
├── scenes/                        # Video scene implementations
│   ├── __init__.py
│   ├── utils.py                   # Shared utilities (colors, shapes, helpers)
│   ├── scene00_introduction.py     # Scene 0: Introduction
│   ├── scene01_pipeline.py        # Scene 1: Face Recognition Pipeline
│   ├── scene02_challenges.py      # Scene 2: Challenges
│   ├── scene03_embedding_space.py # Scene 3: Embedding Space
│   ├── scene04_softmax.py         # Scene 4: Softmax
│   ├── scene05_evolution.py       # Scene 5: Evolution
│   ├── scene06_arcface_mechanism.py # Scene 6: ArcFace Mechanism
│   └── scene07_closing.py        # Scene 7: Closing
├── videos/                       # Rendered output
├── datasets/                     # Evaluation datasets
├── evaluation/                   # Evaluation scripts and results
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

Render all 8 scenes with a single command each. Replace `-w -l` with your desired quality flag.

### Preview All Scenes (480p — fast, for development)

```bash
# Scene 0: Introduction
python3 -m manimlib scenes/scene00_introduction.py Scene00Introduction -l

# Scene 1: Face Recognition Pipeline
python3 -m manimlib scenes/scene01_pipeline.py Scene01_Pipeline -l

# Scene 2: Challenges
python3 -m manimlib scenes/scene02_challenges.py Scene02_Challenges -l

# Scene 3: Embedding Space
python3 -m manimlib scenes/scene03_embedding_space.py Scene03_EmbeddingSpace -l

# Scene 4: Softmax
python3 -m manimlib scenes/scene04_softmax.py Scene04_Softmax -l

# Scene 5: Evolution
python3 -m manimlib scenes/scene05_evolution.py Scene05_Evolution -l

# Scene 6: ArcFace Mechanism
python3 -m manimlib scenes/scene06_arcface_mechanism.py Scene06_ArcFaceMechanism -l

# Scene 7: Closing
python3 -m manimlib scenes/scene07_closing.py Scene07_Closing -l
```

### Preview All Scenes (720p — recommended for review)

```bash
python3 -m manimlib scenes/scene00_introduction.py Scene00_Introduction -m
python3 -m manimlib scenes/scene01_pipeline.py Scene01_Pipeline -m
python3 -m manimlib scenes/scene02_challenges.py Scene02_Challenges -m
python3 -m manimlib scenes/scene03_embedding_space.py Scene03_EmbeddingSpace -m
python3 -m manimlib scenes/scene04_softmax.py Scene04_Softmax -m
python3 -m manimlib scenes/scene05_evolution.py Scene05_Evolution -m
python3 -m manimlib scenes/scene06_arcface_mechanism.py Scene06_ArcFaceMechanism -m
python3 -m manimlib scenes/scene07_closing.py Scene07_Closing -m
```

### Render All Scenes (1080p — for final output)

```bash
python3 -m manimlib -w --hd scenes/scene00_introduction.py Scene00_Introduction
python3 -m manimlib -w --hd scenes/scene01_pipeline.py Scene01_Pipeline
python3 -m manimlib -w --hd scenes/scene02_challenges.py Scene02_Challenges
python3 -m manimlib -w --hd scenes/scene03_embedding_space.py Scene03_EmbeddingSpace
python3 -m manimlib -w --hd scenes/scene04_softmax.py Scene04_Softmax
python3 -m manimlib -w --hd scenes/scene05_evolution.py Scene05_Evolution
python3 -m manimlib -w --hd scenes/scene06_arcface_mechanism.py Scene06_ArcFaceMechanism
python3 -m manimlib -w --hd scenes/scene07_closing.py Scene07_Closing
```

### Render All Scenes (4K — maximum quality)

```bash
python3 -m manimlib -w --uhd scenes/scene00_introduction.py Scene00_Introduction
python3 -m manimlib -w --uhd scenes/scene01_pipeline.py Scene01_Pipeline
python3 -m manimlib -w --uhd scenes/scene02_challenges.py Scene02_Challenges
python3 -m manimlib -w --uhd scenes/scene03_embedding_space.py Scene03_EmbeddingSpace
python3 -m manimlib -w --uhd scenes/scene04_softmax.py Scene04_Softmax
python3 -m manimlib -w --uhd scenes/scene05_evolution.py Scene05_Evolution
python3 -m manimlib -w --uhd scenes/scene06_arcface_mechanism.py Scene06_ArcFaceMechanism
python3 -m manimlib -w --uhd scenes/scene07_closing.py Scene07_Closing
```

### Presenter Mode (wait for spacebar between animations)

```bash
python3 -m manimlib -p scenes/scene00_introduction.py Scene00_Introduction
python3 -m manimlib -p scenes/scene01_pipeline.py Scene01_Pipeline
python3 -m manimlib -p scenes/scene02_challenges.py Scene02_Challenges
python3 -m manimlib -p scenes/scene03_embedding_space.py Scene03_EmbeddingSpace
python3 -m manimlib -p scenes/scene04_softmax.py Scene04_Softmax
python3 -m manimlib -p scenes/scene05_evolution.py Scene05_Evolution
python3 -m manimlib -p scenes/scene06_arcface_mechanism.py Scene06_ArcFaceMechanism
python3 -m manimlib -p scenes/scene07_closing.py Scene07_Closing
```

### Start from Animation N (skip first N animations)

```bash
python3 -m manimlib -w -l -n 5 scenes/scene06_arcface_mechanism.py Scene06_ArcFaceMechanism
```

### List All Scenes in a File

```bash
python3 -m manimlib scenes/scene00_introduction.py
python3 -m manimlib scenes/scene01_pipeline.py
python3 -m manimlib scenes/scene02_challenges.py
python3 -m manimlib scenes/scene03_embedding_space.py
python3 -m manimlib scenes/scene04_softmax.py
python3 -m manimlib scenes/scene05_evolution.py
python3 -m manimlib scenes/scene06_arcface_mechanism.py
python3 -m manimlib scenes/scene07_closing.py
```

### Using Virtual Environment

```bash
cd /home/hg/source/manim-arcface-2
source venv/bin/activate
python -m manimlib -w --hd scenes/scene00_introduction.py Scene00Introduction
```

---

## Quality Reference

| Flag | Quality | Resolution | Use Case |
|------|---------|-----------|----------|
| `-l` | Low | 480p | Fast testing during development |
| `-m` | Medium | 720p | Preview, internal review |
| `--hd` | High | 1080p | **Recommended for final output** |
| `--uhd` | Ultra | 4K | Large displays, maximum quality |

**Recommendations:**
- **Development/Testing**: Use `-l` (480p) for fast iteration
- **Review**: Use `-m` (720p) for scene-by-scene review
- **Final Output**: Use `--hd` (1080p) for YouTube/presentations
- **4K**: Only for large displays or powerful GPU

---

## Useful Flags Reference

| Flag | Description |
|------|-------------|
| `-w` | Write to file (save video) |
| `-l` | Low quality (480p) |
| `-m` | Medium quality (720p) |
| `--hd` | High quality (1080p) |
| `--uhd` | Ultra high quality (4K) |
| `-s` | Save final frame only (no animation) |
| `-n <num>` | Start at animation number |
| `-o` | Write and open result |
| `-p` | Presenter mode (wait for spacebar) |
| `-r <px>` | Custom resolution |
| `--fps <n>` | Custom FPS |
| `-i` | Export as GIF |

---

## Video Output Directory

Rendered videos are saved in:

```
videos/<SceneClass>/
└── <Quality>/
    └── <SceneClass>.mp4
```

Example: `videos/Scene00Introduction/480p15/Scene00Introduction.mp4`
