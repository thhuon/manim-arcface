Manim is an engine for precise programmatic animations, designed for creating explanatory math videos.

For educational and academic purposes.

## Installation

Manim runs on Python 3.7 or higher.

System requirements are [FFmpeg](https://ffmpeg.org/), [OpenGL](https://www.opengl.org/) and [LaTeX](https://www.latex-project.org) (optional, if you want to use LaTeX).


### Directly

```sh
pip install -e .
```

For more options, take a look at the [Using manim](#using-manim) sections further below.

If you want to hack on manimlib itself, clone this repository and in that directory execute:

```sh
pip install -e .
```


### Mac OSX

1. Install FFmpeg and LaTeX using homebrew.

2. If you are using an ARM-based processor, install Cairo.

3. Install manim using pip.

## Using manim

Look through the [example scenes](https://3b1b.github.io/manim/getting_started/example_scenes.html) to see examples of the library's syntax, animation types and object types.

When running in the CLI, some useful flags include:
* `-w` to write the scene to a file
* `-o` to write the scene to a file and open the result
* `-s` to skip to the end and just show the final frame.
    * `-so` will save the final frame to an image and show it
* `-n <number>` to skip ahead to the `n`'th animation of a scene.
* `-f` to make the playback window fullscreen

Take a look at custom_config.yml for further configuration.

### Documentation
Documentation is in progress.