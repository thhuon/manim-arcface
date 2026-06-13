#!/usr/bin/env python3
import os
import sys
import re
import csv
import asyncio
import subprocess
import argparse
from pathlib import Path
import edge_tts

def get_scene_files():
    scenes_dir = Path("scenes")
    if not scenes_dir.exists():
        print("Error: 'scenes' directory not found.", file=sys.stderr)
        sys.exit(1)
    
    # Match scene00_*.py through scene99_*.py
    scene_pattern = re.compile(r"^scene(\d+).*\.py$")
    files = []
    for f in scenes_dir.iterdir():
        if f.is_file():
            m = scene_pattern.match(f.name)
            if m:
                files.append((int(m.group(1)), f))
    # Sort by scene ID number
    files.sort(key=lambda x: x[0])
    return files

def extract_classname(filepath):
    content = filepath.read_text()
    match = re.search(r"class\s+(\w+)\(Scene\):", content)
    if match:
        return match.group(1)
    return None

def parse_narration_csv(filepath="narration.csv"):
    scenes = {}
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found!", file=sys.stderr)
        sys.exit(1)
        
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if not row or len(row) < 5:
                continue
            scene_id_str = row[0].strip()
            if not scene_id_str:
                continue
            try:
                scene_id = int(scene_id_str)
            except ValueError:
                continue
            
            narration = row[4].strip()
            if scene_id not in scenes:
                scenes[scene_id] = []
            if narration:
                scenes[scene_id].append(narration)
                
    # Join the narrations for each scene into a single block of text
    joined_scenes = {}
    for scene_id, text_list in scenes.items():
        joined_scenes[scene_id] = " ".join(text_list)
    return joined_scenes

def chunk_text(text, max_chars=800):
    # Split by sentence boundaries, maintaining the punctuation
    sentences = re.split(r'(?<=[.?!])\s+', text)
    chunks = []
    current_chunk = []
    current_len = 0
    for sentence in sentences:
        if current_len + len(sentence) > max_chars:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_len = len(sentence)
        else:
            current_chunk.append(sentence)
            current_len += len(sentence) + 1  # +1 for space
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

async def save_with_retry(text, voice, path, retries=5, delay=3.0):
    for attempt in range(retries):
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(path))
            # Wait a small delay after a successful request to be polite to the API
            await asyncio.sleep(0.5)
            return
        except Exception as e:
            if attempt == retries - 1:
                raise e
            print(f"    ⚠️ TTS request failed (attempt {attempt+1}/{retries}). Retrying in {delay}s... (Error: {e})")
            await asyncio.sleep(delay)
            delay *= 2.0

async def generate_tts(text, output_path, voice):
    # If the text is short, generate it directly in one request
    if len(text) <= 800:
        await save_with_retry(text, voice, output_path)
        return

    # For long narrations, chunk the text to bypass the API limit
    chunks = chunk_text(text, max_chars=800)
    print(f"  Text is long ({len(text)} chars). Splitting into {len(chunks)} chunks for TTS...")
    
    temp_files = []
    for idx, chunk in enumerate(chunks):
        chunk_path = output_path.with_name(f"{output_path.stem}_chunk_{idx}.mp3")
        await save_with_retry(chunk, voice, chunk_path)
        temp_files.append(chunk_path)
    
    # Concatenate the audio chunks using ffmpeg
    concat_file = output_path.with_name("audio_concat_list.txt")
    with open(concat_file, "w") as f:
        for tf in temp_files:
            escaped_path = str(tf.resolve()).replace("'", "'\\''")
            f.write(f"file '{escaped_path}'\n")
            
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(output_path)
    ]
    
    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Clean up temp files
    if concat_file.exists():
        concat_file.unlink()
    for tf in temp_files:
        if tf.exists():
            tf.unlink()

def get_duration(filepath):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(filepath)
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Warning: Failed to get duration of {filepath}: {e}")
        return 0.0

def merge_video_audio(video_path, audio_path, output_path):
    video_dur = get_duration(video_path)
    audio_dur = get_duration(audio_path)
    
    print(f"  Video duration: {video_dur:.2f}s")
    print(f"  Audio duration: {audio_dur:.2f}s")
    
    # If audio is longer, pad/extend the video's last frame to match audio duration
    diff = audio_dur - video_dur
    if diff > 0.1:
        print(f"  Audio is longer by {diff:.2f}s. Cloning last frame to pad video.")
        # tpad=stop_mode=clone will repeat the last frame for stop_duration seconds
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-vf", f"tpad=stop_mode=clone:stop_duration={diff}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output_path)
        ]
    else:
        print("  Video is longer or equal to audio. Direct merging without re-encoding video.")
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest", # End when the shortest stream ends (in case video is way longer and we want it to align)
            str(output_path)
        ]
        
    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

async def main_async():
    parser = argparse.ArgumentParser(description="Render ManimGL scenes with neural TTS voiceovers and combine them.")
    parser.add_argument("-d", "--draft", action="store_true", help="Render in draft/low quality (480p15) for fast preview compilation.")
    parser.add_argument("-o", "--output-dir", default="output", help="Directory where the final combined video will be saved.")
    parser.add_argument("--skip-render", action="store_true", help="Skip rendering new files; only stitch currently existing renders.")
    parser.add_argument("--voice", default="en-US-AndrewNeural", help="Microsoft Edge Neural TTS voice (e.g. en-US-AndrewNeural, en-US-GuyNeural, en-US-AvaNeural).")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create directories for audio and intermediate voiced clips
    audio_dir = Path("videos") / "audio"
    voiced_dir = Path("videos") / "temp_voiced"
    audio_dir.mkdir(parents=True, exist_ok=True)
    voiced_dir.mkdir(parents=True, exist_ok=True)

    scene_files = get_scene_files()
    if not scene_files:
        print("No scene files found matching scenes/scene*.py", file=sys.stderr)
        sys.exit(1)
        
    print(f"Found {len(scene_files)} scenes to process.")

    # Parse narration
    narrations = parse_narration_csv()
    
    render_list = []
    for scene_id, filepath in scene_files:
        classname = extract_classname(filepath)
        if not classname:
            print(f"Warning: Could not extract Scene class name from {filepath}. Skipping.")
            continue
        
        narration_text = narrations.get(scene_id, "")
        expected_video = Path("videos") / f"{classname}.mp4"
        expected_audio = audio_dir / f"scene_{scene_id:02d}.mp3"
        voiced_video = voiced_dir / f"scene_{scene_id:02d}_voiced.mp4"
        
        render_list.append({
            "id": scene_id,
            "filepath": filepath,
            "classname": classname,
            "video_path": expected_video,
            "audio_path": expected_audio,
            "voiced_path": voiced_video,
            "narration": narration_text
        })

    # Render step
    if not args.skip_render:
        os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"
        
        for idx, item in enumerate(render_list):
            print("\n" + "="*80)
            print(f"RENDERING SCENE {idx+1}/{len(render_list)}: {item['classname']} ({item['filepath']})")
            print("="*80)
            
            cmd = [sys.executable, "-m", "manimlib", str(item["filepath"]), item["classname"], "-w"]
            if args.draft:
                cmd.append("-l")
                
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError:
                print(f"\n❌ Error rendering scene: {item['classname']}")
                choice = input("Failed to render this scene. Do you want to continue stitching anyway? (y/n): ").strip().lower()
                if choice not in ('y', 'yes'):
                    sys.exit(1)

    # Voiceover Generation & Audio Alignment step
    print("\n" + "="*80)
    print("GENERATING NEURAL TTS VOICEOVERS & ALIGNING VIDEOS")
    print("="*80)
    
    valid_voiced_videos = []
    
    for item in render_list:
        print(f"\nProcessing Scene {item['id']:02d}: {item['classname']}")
        
        # 1. Check if video exists
        if not item["video_path"].exists():
            print(f"  ⚠️ Video render file not found: {item['video_path']}. Skipping voiceover integration.")
            continue
            
        # 2. Generate audio if narration exists
        if item["narration"]:
            print(f"  Generating voiceover (voice: {args.voice})...")
            # Remove existing audio file to force regeneration of narration
            if item["audio_path"].exists():
                item["audio_path"].unlink()
            await generate_tts(item["narration"], item["audio_path"], args.voice)
            
            # 3. Merge audio and video
            print("  Merging audio and video...")
            try:
                merge_video_audio(item["video_path"], item["audio_path"], item["voiced_path"])
                valid_voiced_videos.append(item["voiced_path"])
            except Exception as e:
                print(f"  ❌ Error merging video and audio: {e}")
        else:
            print("  No narration text found for this scene. Using silent source video.")
            # If no audio, just use the rendered video directly
            valid_voiced_videos.append(item["video_path"])

    if not valid_voiced_videos:
        print("\n❌ No voiced scene videos found. Concat aborted.", file=sys.stderr)
        sys.exit(1)

    # Stitch step using FFMPEG concat demuxer
    print("\n" + "="*80)
    print(f"STITCHING {len(valid_voiced_videos)} VOICED BEATS INTO FINAL MOVIE")
    print("="*80)

    concat_file = Path("concat_voiced_list.txt")
    with open(concat_file, "w") as f:
        for video_path in valid_voiced_videos:
            escaped_path = str(video_path.resolve()).replace("'", "'\\''")
            f.write(f"file '{escaped_path}'\n")

    suffix = "_voiced_draft" if args.draft else "_voiced"
    final_output = output_dir / f"final_video{suffix}.mp4"
    
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
        print(f"\n🎉 SUCCESS! Full voiced video saved to:")
        print(f"👉 {final_output.resolve()}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ FFMPEG concatenation failed: {e}", file=sys.stderr)
    finally:
        if concat_file.exists():
            concat_file.unlink()

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
