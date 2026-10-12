# converters/media.py
import os
import shutil
import subprocess
from pathlib import Path
from . import ConversionResult

def is_ffmpeg_installed() -> bool:
    """Checks whether the FFmpeg binary is accessible in the system PATH."""
    return shutil.which("ffmpeg") is not None

def convert(input_path: str, output_format: str, output_dir: str) -> ConversionResult:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    fmt = output_format.lower().strip().lstrip(".")
    output_path = output_dir / f"{input_path.stem}.{fmt}"

    output_dir.mkdir(parents=True, exist_ok=True)

    if not is_ffmpeg_installed():
        return ConversionResult(
            status='error',
            error="FFmpeg is not installed or not found in system PATH. When running via Docker, FFmpeg is pre-installed automatically; on desktop, install FFmpeg (e.g., via winget install ffmpeg or ffmpeg.org)."
        )

    try:
        # Build ffmpeg command line directly or via ffmpeg-python
        # Direct subprocess gives clear stderr diagnostics and handles audio extraction
        cmd = ["ffmpeg", "-y", "-i", str(input_path)]

        audio_formats = {'mp3', 'wav', 'flac', 'ogg', 'm4a', 'aac'}
        video_formats = {'mp4', 'mkv', 'avi', 'mov', 'webm'}

        if fmt in audio_formats:
            # If extracting audio from video, or converting audio:
            if fmt == 'mp3':
                cmd.extend(["-vn", "-acodec", "libmp3lame", "-q:a", "2"])
            elif fmt == 'wav':
                cmd.extend(["-vn"])
            elif fmt == 'flac':
                cmd.extend(["-vn", "-acodec", "flac"])
            elif fmt == 'ogg':
                cmd.extend(["-vn", "-acodec", "libvorbis"])
            elif fmt in ('m4a', 'aac'):
                cmd.extend(["-vn", "-acodec", "aac"])
        elif fmt in video_formats:
            if fmt == 'webm':
                cmd.extend(["-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0", "-b:a", "128k", "-c:a", "libopus"])
            elif fmt == 'mp4':
                cmd.extend(["-c:v", "libx264", "-c:a", "aac"])

        cmd.append(str(output_path))

        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.returncode != 0:
            return ConversionResult(status='error', error=f"FFmpeg error: {process.stderr[-500:] if process.stderr else 'Unknown error'}")

        size = output_path.stat().st_size if output_path.exists() else None
        return ConversionResult(status='success', output_path=str(output_path), output_size=size)

    except Exception as e:
        return ConversionResult(status='error', error=str(e))