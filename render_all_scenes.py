#!/usr/bin/env python3
import os
import sys
import re
import subprocess
import argparse
from pathlib import Path

def get_scene_files():
    scenes_dir = Path("scenes")
    if not scenes_dir.exists():
        print("Error: 'scenes' directory not found.", file=sys.stderr)
        sys.exit(1)
    
    # Match scene00_*.py through scene99_*.py
    scene_pattern = re.compile(r"^scene\d+.*\.py$")
    files = [f for f in scenes_dir.iterdir() if f.is_file() and scene_pattern.match(f.name)]
    # Sort alphanumerically to ensure chronological order
    files.sort(key=lambda x: x.name)
    return files

def extract_classname(filepath):
    content = filepath.read_text()
    match = re.search(r"class\s+(\w+)\(Scene\):", content)
    if match:
        return match.group(1)
    return None

def main():
    parser = argparse.ArgumentParser(description="Render all ManimGL scenes and combine them into a single video.")
    parser.add_argument("-d", "--draft", action="store_true", help="Render in draft/low quality (480p15) for fast preview compilation.")
    parser.add_argument("-o", "--output-dir", default="output", help="Directory where the final combined video will be saved.")
    parser.add_argument("--skip-render", action="store_true", help="Skip rendering new files; only stitch currently existing renders.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    scene_files = get_scene_files()
    if not scene_files:
        print("No scene files found matching scenes/scene*.py", file=sys.stderr)
        sys.exit(1)
        
    print(f"Found {len(scene_files)} scenes to process.")

    render_list = []
    failed_scenes = []

    # Prepare rendering info
    for filepath in scene_files:
        classname = extract_classname(filepath)
        if not classname:
            print(f"Warning: Could not extract Scene class name from {filepath}. Skipping.")
            continue
        
        expected_video = Path("videos") / f"{classname}.mp4"
        render_list.append({
            "filepath": str(filepath),
            "classname": classname,
            "video_path": expected_video
        })

    # Render step
    if not args.skip_render:
        # Enforce software rendering to avoid driver/GPU initialization issues
        os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"
        
        for idx, item in enumerate(render_list):
            print("\n" + "="*80)
            print(f"RENDERING SCENE {idx+1}/{len(render_list)}: {item['classname']} ({item['filepath']})")
            print("="*80)
            
            cmd = [sys.executable, "-m", "manimlib", item["filepath"], item["classname"], "-w"]
            if args.draft:
                cmd.append("-l")
                
            try:
                # Run the render process and stream output to console
                result = subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError:
                print(f"\n❌ Error rendering scene: {item['classname']}")
                failed_scenes.append(item['classname'])
                # Ask user if they want to continue
                choice = input("Failed to render this scene. Do you want to continue stitching anyway? (y/n): ").strip().lower()
                if choice not in ('y', 'yes'):
                    sys.exit(1)

    # Filter out files that don't exist (e.g. if skipped or failed)
    valid_videos = []
    for item in render_list:
        if item["video_path"].exists():
            valid_videos.append(item["video_path"])
        else:
            print(f"Warning: Expected video output not found: {item['video_path']}")

    if not valid_videos:
        print("\n❌ No successfully rendered videos found. Concat aborted.", file=sys.stderr)
        sys.exit(1)

    # Stitch step using FFMPEG concat demuxer (lossless, instant merging)
    print("\n" + "="*80)
    print(f"STITCHING {len(valid_videos)} VIDEO BEATS INTO FINAL MOVIE")
    print("="*80)

    concat_file = Path("concat_list.txt")
    with open(concat_file, "w") as f:
        for video_path in valid_videos:
            # Escape single quotes in path if any
            escaped_path = str(video_path.resolve()).replace("'", "'\\''")
            f.write(f"file '{escaped_path}'\n")

    suffix = "_draft" if args.draft else ""
    final_output = output_dir / f"final_video{suffix}.mp4"
    
    # Run FFMPEG concatenation
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(final_output)
    ]
    
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"\n🎉 SUCCESS! Full consolidated video saved to:")
        print(f"👉 {final_output.resolve()}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ FFMPEG concatenation failed: {e}", file=sys.stderr)
    finally:
        # Cleanup
        if concat_file.exists():
            concat_file.unlink()

if __name__ == "__main__":
    main()
