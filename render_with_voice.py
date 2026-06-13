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
from PIL import Image, ImageDraw, ImageFont

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
    match = re.search(r"class\s+(\w+)\s*\(\s*(?:ThreeD)?Scene\s*\)", content)
    if match:
        return match.group(1)
    return None

def parse_narration_csv(filepath="narration.csv"):
    """
    Parse narration.csv and return a dictionary mapping scene_id to a dict of:
    {
        "name": scene_name,
        "subscene": subscene,
        "narration": combined_narration
    }
    """
    scenes_data = {}
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
            
            scene_name = row[1].strip()
            subscene = row[2].strip()
            narration = row[4].strip()
            
            if scene_id not in scenes_data:
                scenes_data[scene_id] = {
                    "name": scene_name,
                    "subscene": subscene,
                    "narrations_list": []
                }
            
            # Update name/subscene if empty from previous rows
            if not scenes_data[scene_id]["name"] and scene_name:
                scenes_data[scene_id]["name"] = scene_name
            if not scenes_data[scene_id]["subscene"] and subscene:
                scenes_data[scene_id]["subscene"] = subscene
                
            if narration:
                scenes_data[scene_id]["narrations_list"].append(narration)
                
    # Join list into single block
    final_narrations = {}
    for scene_id, data in scenes_data.items():
        final_narrations[scene_id] = {
            "name": data["name"],
            "subscene": data["subscene"],
            "narration": " ".join(data["narrations_list"])
        }
    return final_narrations

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

def get_video_properties(filepath):
    cmd_v = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-of", "csv=p=0",
        str(filepath)
    ]
    cmd_a = [
        "ffprobe", "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=sample_rate",
        "-of", "csv=p=0",
        str(filepath)
    ]
    
    width, height, fps = 854, 480, 30.0
    sample_rate = 24000
    
    try:
        res_v = subprocess.run(cmd_v, stdout=subprocess.PIPE, text=True, check=True)
        parts = res_v.stdout.strip().split(",")
        if len(parts) >= 3:
            width = int(parts[0])
            height = int(parts[1])
            fps_str = parts[2]
            if "/" in fps_str:
                n, d = fps_str.split("/")
                fps = float(n) / float(d)
            else:
                fps = float(fps_str)
    except Exception as e:
        print(f"Warning: Failed to get video properties for {filepath}: {e}")
        
    try:
        res_a = subprocess.run(cmd_a, stdout=subprocess.PIPE, text=True, check=True)
        val = res_a.stdout.strip()
        if val:
            sample_rate = int(val)
    except Exception as e:
        # Expected if silent video has no audio
        pass
        
    return width, height, fps, sample_rate

def generate_title_card(width, height, scene_num, scene_name, subscene, output_path):
    bg_color = (10, 14, 20)  # #0A0E14
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    line_y = int(height * 0.85)
    line_thickness = max(2, int(height * 0.005))
    draw.line(
        [(int(width * 0.1), line_y), (int(width * 0.9), line_y)],
        fill=(0, 212, 255),  # Cyan
        width=line_thickness
    )
    
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    font_title, font_subtitle, font_tag = None, None, None
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font_title = ImageFont.truetype(fp, int(height * 0.07))
                font_subtitle = ImageFont.truetype(fp, int(height * 0.045))
                font_tag = ImageFont.truetype(fp, int(height * 0.03))
                break
            except Exception:
                pass
                
    if font_title is None:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        
    draw.text(
        (width // 2, int(height * 0.35)),
        f"CHAPTER {scene_num:02d}",
        fill=(62, 247, 160),  # Green
        font=font_tag,
        anchor="mm"
    )
    
    draw.text(
        (width // 2, int(height * 0.45)),
        scene_name,
        fill=(242, 246, 255),  # White
        font=font_title,
        anchor="mm"
    )
    
    if subscene:
        draw.text(
            (width // 2, int(height * 0.58)),
            subscene,
            fill=(138, 148, 166),  # Muted
            font=font_subtitle,
            anchor="mm"
        )
        
    image.save(output_path)

def make_title_video(image_path, audio_sample_rate, video_fps, duration, output_path):
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"anullsrc=r={audio_sample_rate}:cl=mono",
        "-loop", "1", "-i", str(image_path),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-r", str(video_fps),
        str(output_path)
    ]
    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def merge_video_audio(video_path, audio_path, output_path):
    video_dur = get_duration(video_path)
    audio_dur = get_duration(audio_path)
    
    print(f"  Video duration: {video_dur:.2f}s")
    print(f"  Audio duration: {audio_dur:.2f}s")
    
    if video_dur <= 0 or audio_dur <= 0:
        print("  Error: Zero duration detected. Direct copying.")
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-map", "0:v",
            "-map", "1:a",
            "-c:v", "copy",
            "-c:a", "aac",
            str(output_path)
        ]
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return

    _, _, fps, _ = get_video_properties(video_path)
    factor = audio_dur / video_dur
    MAX_SLOW = 1.5  # never slow video by more than 1.5x (keeps motion natural)
    
    if factor <= MAX_SLOW:
        # Safe range: stretch video speed to match audio
        print(f"  Stretching video by {factor:.3f}x to match audio.")
        fade_start = max(0.0, audio_dur - 1.0)
        filter_str = (
            f"[0:v]setpts={factor}*PTS,fps={fps},"
            f"fade=t=out:st={fade_start}:d=1.0[v]"
        )
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-filter_complex", filter_str,
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{audio_dur:.3f}",
            str(output_path)
        ]
    else:
        # Audio is much longer: play video normally then freeze last frame
        print(f"  Audio {factor:.2f}x longer — playing video normally then freezing last frame.")
        pad_dur = audio_dur - video_dur
        fade_start = max(0.0, audio_dur - 1.0)
        filter_str = (
            f"[0:v]fps={fps},"
            f"tpad=stop_mode=clone:stop_duration={pad_dur:.3f},"
            f"fade=t=out:st={fade_start}:d=1.0[v]"
        )
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-filter_complex", filter_str,
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{audio_dur:.3f}",
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

    # Parse narration full data
    narrations = parse_narration_csv()
    
    render_list = []
    for scene_id, filepath in scene_files:
        classname = extract_classname(filepath)
        if not classname:
            print(f"Warning: Could not extract Scene class name from {filepath}. Skipping.")
            continue
        
        scene_data = narrations.get(scene_id, {"name": f"Scene {scene_id}", "subscene": "", "narration": ""})
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
            "name": scene_data["name"],
            "subscene": scene_data["subscene"],
            "narration": scene_data["narration"]
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
    print("GENERATING NEURAL TTS VOICEOVERS & ALIGNING VIDEOS (SCENE-WISE TRANSITIONS)")
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
                temp_voiced = voiced_dir / f"scene_{item['id']:02d}_temp_voiced.mp4"
                merge_video_audio(item["video_path"], item["audio_path"], temp_voiced)
                
                # Extract properties from temp_voiced
                width, height, fps, sample_rate = get_video_properties(temp_voiced)
                
                title_img = voiced_dir / f"scene_{item['id']:02d}_title.png"
                title_video = voiced_dir / f"scene_{item['id']:02d}_title.mp4"
                
                # Draw title card
                print(f"  Creating Chapter Title Slide: CHAPTER {item['id']:02d} - '{item['name']}'...")
                generate_title_card(width, height, item["id"], item["name"], item["subscene"], title_img)
                make_title_video(title_img, sample_rate, fps, 2.0, title_video)
                
                # Concat Title Slide + Voiced Video
                concat_list_file = voiced_dir / f"scene_{item['id']:02d}_concat.txt"
                with open(concat_list_file, "w") as f:
                    f.write(f"file '{title_video.resolve()}'\n")
                    f.write(f"file '{temp_voiced.resolve()}'\n")
                
                ffmpeg_concat_cmd = [
                    "ffmpeg", "-y",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", str(concat_list_file),
                    "-c", "copy",
                    str(item["voiced_path"])
                ]
                subprocess.run(ffmpeg_concat_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Cleanup temp files
                if temp_voiced.exists(): temp_voiced.unlink()
                if title_img.exists(): title_img.unlink()
                if title_video.exists(): title_video.unlink()
                if concat_list_file.exists(): concat_list_file.unlink()
                
                valid_voiced_videos.append(item["voiced_path"])
            except Exception as e:
                print(f"  ❌ Error merging video and audio: {e}")
        else:
            print("  No narration text found for this scene. Using source video directly.")
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
