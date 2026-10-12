# converters/registry.py
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from . import ConversionResult
from converters import tabular, images, documents, media, data

# Category Registry with inputs, allowed outputs, and recommended target formats
REGISTRY = {
    "tabular": {
        "title": "Tabular & Spreadsheets",
        "icon": "📊",
        "description": "Convert datasets between Excel, CSV, JSON, and Parquet",
        "inputs": [".csv", ".tsv", ".xlsx", ".xls", ".parquet"],
        "outputs": ["CSV", "XLSX", "JSON", "PARQUET", "TSV", "HTML"],
        "module": tabular,
        "recommendations": {
            ".csv": [
                {"format": "XLSX", "badge": "Popular", "reason": "Open in Microsoft Excel or Google Sheets"},
                {"format": "PARQUET", "badge": "High Perf", "reason": "Compressed columnar format for data science"},
                {"format": "JSON", "badge": "API", "reason": "Standard web and API data structure"}
            ],
            ".tsv": [
                {"format": "CSV", "badge": "Standard", "reason": "Universal comma-separated format"},
                {"format": "XLSX", "badge": "Popular", "reason": "Interactive spreadsheet workbook"}
            ],
            ".xlsx": [
                {"format": "CSV", "badge": "Universal", "reason": "Lightweight, plain-text spreadsheet"},
                {"format": "JSON", "badge": "API", "reason": "Machine-readable record array"},
                {"format": "PARQUET", "badge": "Optimized", "reason": "Fast, compressed columnar storage"}
            ],
            ".xls": [
                {"format": "XLSX", "badge": "Modern", "reason": "Upgrade legacy Excel to modern .xlsx"},
                {"format": "CSV", "badge": "Universal", "reason": "Plain-text data export"}
            ],
            ".parquet": [
                {"format": "CSV", "badge": "Standard", "reason": "Human-readable plain text export"},
                {"format": "XLSX", "badge": "Popular", "reason": "Open in Microsoft Excel"},
                {"format": "JSON", "badge": "API", "reason": "Standard JSON records export"}
            ]
        }
    },
    "images": {
        "title": "Images & Graphics",
        "icon": "🖼️",
        "description": "Convert images between web, photo, and print formats",
        "inputs": [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".ico", ".tiff", ".tif", ".gif"],
        "outputs": ["PNG", "JPG", "WEBP", "PDF", "ICO", "BMP", "TIFF"],
        "module": images,
        "recommendations": {
            ".png": [
                {"format": "WEBP", "badge": "Web Best", "reason": "Up to 30% smaller size with high quality"},
                {"format": "JPG", "badge": "Popular", "reason": "Universal compatibility for photos"},
                {"format": "PDF", "badge": "Document", "reason": "Print-ready single page document"}
            ],
            ".jpg": [
                {"format": "WEBP", "badge": "Optimized", "reason": "Next-gen web performance"},
                {"format": "PNG", "badge": "Lossless", "reason": "Lossless editing without compression artifacts"},
                {"format": "PDF", "badge": "Document", "reason": "Export photo to PDF"}
            ],
            ".jpeg": [
                {"format": "WEBP", "badge": "Optimized", "reason": "Next-gen web performance"},
                {"format": "PNG", "badge": "Lossless", "reason": "Lossless editing without compression artifacts"},
                {"format": "PDF", "badge": "Document", "reason": "Export photo to PDF"}
            ],
            ".webp": [
                {"format": "PNG", "badge": "Compatible", "reason": "Universal support across all legacy software"},
                {"format": "JPG", "badge": "Photo", "reason": "Standard photo format"}
            ],
            ".bmp": [
                {"format": "PNG", "badge": "Recommended", "reason": "Significantly smaller lossless compression"},
                {"format": "JPG", "badge": "Popular", "reason": "Universal small photo file"}
            ],
            ".tiff": [
                {"format": "PNG", "badge": "Lossless", "reason": "Web-friendly lossless format"},
                {"format": "JPG", "badge": "Photo", "reason": "Compressed lightweight photo"},
                {"format": "PDF", "badge": "Document", "reason": "Standard document format"}
            ],
            ".tif": [
                {"format": "PNG", "badge": "Lossless", "reason": "Web-friendly lossless format"},
                {"format": "JPG", "badge": "Photo", "reason": "Compressed lightweight photo"},
                {"format": "PDF", "badge": "Document", "reason": "Standard document format"}
            ],
            ".ico": [
                {"format": "PNG", "badge": "Universal", "reason": "High-res transparent image"},
                {"format": "WEBP", "badge": "Web", "reason": "Modern web icon"}
            ],
            ".gif": [
                {"format": "PNG", "badge": "Standard", "reason": "Extract still frame with transparency"},
                {"format": "WEBP", "badge": "Modern", "reason": "Modern optimized image"}
            ]
        }
    },
    "documents": {
        "title": "Documents & Text",
        "icon": "📄",
        "description": "Convert Word, PDF, Markdown, HTML, and Text documents",
        "inputs": [".docx", ".doc", ".pdf", ".md", ".markdown", ".html", ".txt"],
        "outputs": ["PDF", "DOCX", "TXT", "HTML", "MD"],
        "module": documents,
        "recommendations": {
            ".docx": [
                {"format": "PDF", "badge": "Standard", "reason": "Fixed-layout non-editable distribution document"},
                {"format": "TXT", "badge": "Clean", "reason": "Extract clean unformatted plain text"},
                {"format": "MD", "badge": "Notes", "reason": "Convert into clean developer Markdown"}
            ],
            ".doc": [
                {"format": "DOCX", "badge": "Modern", "reason": "Upgrade legacy Word format to modern DOCX"},
                {"format": "PDF", "badge": "Standard", "reason": "Non-editable standard PDF"}
            ],
            ".pdf": [
                {"format": "DOCX", "badge": "Editable", "reason": "Convert fixed PDF back into editable Word document"},
                {"format": "TXT", "badge": "Extract", "reason": "Instant plain text extraction"}
            ],
            ".md": [
                {"format": "HTML", "badge": "Web Ready", "reason": "Render styled web page from Markdown"},
                {"format": "DOCX", "badge": "Office", "reason": "Generate Microsoft Word document"},
                {"format": "PDF", "badge": "Print", "reason": "Formatted PDF document"}
            ],
            ".markdown": [
                {"format": "HTML", "badge": "Web Ready", "reason": "Render styled web page from Markdown"},
                {"format": "DOCX", "badge": "Office", "reason": "Generate Microsoft Word document"},
                {"format": "PDF", "badge": "Print", "reason": "Formatted PDF document"}
            ],
            ".html": [
                {"format": "MD", "badge": "Clean", "reason": "Convert webpage to lightweight Markdown"},
                {"format": "DOCX", "badge": "Office", "reason": "Open styled content in Microsoft Word"}
            ],
            ".txt": [
                {"format": "DOCX", "badge": "Office", "reason": "Wrap text into standard Word document"},
                {"format": "HTML", "badge": "Web", "reason": "HTML web document with preformatted text"},
                {"format": "MD", "badge": "Docs", "reason": "Markdown document"}
            ]
        }
    },
    "media": {
        "title": "Audio & Video",
        "icon": "🎬",
        "description": "Convert media files and extract audio tracks",
        "inputs": [".mp4", ".mkv", ".avi", ".mov", ".webm", ".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"],
        "outputs": ["MP4", "MKV", "WEBM", "MP3", "WAV", "FLAC", "OGG"],
        "module": media,
        "recommendations": {
            ".mp4": [
                {"format": "MP3", "badge": "Extract Audio", "reason": "Extract audio track from video file"},
                {"format": "WEBM", "badge": "Web Video", "reason": "Open web video format for HTML5"},
                {"format": "MKV", "badge": "Container", "reason": "Matroska container with subtitle support"}
            ],
            ".mkv": [
                {"format": "MP4", "badge": "Universal", "reason": "Standard video playable on all devices"},
                {"format": "MP3", "badge": "Extract Audio", "reason": "Extract audio soundtrack"}
            ],
            ".mov": [
                {"format": "MP4", "badge": "Universal", "reason": "Convert Apple QuickTime to standard MP4"},
                {"format": "MP3", "badge": "Extract Audio", "reason": "Extract audio track"}
            ],
            ".avi": [
                {"format": "MP4", "badge": "Modern", "reason": "High-efficiency modern MP4 video"},
                {"format": "MP3", "badge": "Extract Audio", "reason": "Extract audio soundtrack"}
            ],
            ".webm": [
                {"format": "MP4", "badge": "Universal", "reason": "Universal device compatibility"},
                {"format": "MP3", "badge": "Extract Audio", "reason": "Extract audio track"}
            ],
            ".mp3": [
                {"format": "WAV", "badge": "Uncompressed", "reason": "Uncompressed PCM audio for editing"},
                {"format": "OGG", "badge": "Open Codec", "reason": "Open-source audio for games and apps"},
                {"format": "FLAC", "badge": "Lossless", "reason": "Lossless audio format"}
            ],
            ".wav": [
                {"format": "MP3", "badge": "Compact", "reason": "Compressed universal audio player format"},
                {"format": "FLAC", "badge": "Lossless", "reason": "Compressed without loss of studio audio quality"}
            ],
            ".flac": [
                {"format": "MP3", "badge": "Compatible", "reason": "Universal audio playable anywhere"},
                {"format": "WAV", "badge": "Studio", "reason": "Raw uncompressed PCM audio"}
            ],
            ".ogg": [
                {"format": "MP3", "badge": "Universal", "reason": "Universal playback compatibility"},
                {"format": "WAV", "badge": "Studio", "reason": "Uncompressed audio"}
            ],
            ".m4a": [
                {"format": "MP3", "badge": "Universal", "reason": "Universal playback compatibility"},
                {"format": "WAV", "badge": "Studio", "reason": "Uncompressed audio"}
            ],
            ".aac": [
                {"format": "MP3", "badge": "Universal", "reason": "Universal playback compatibility"},
                {"format": "WAV", "badge": "Studio", "reason": "Uncompressed audio"}
            ]
        }
    },
    "data": {
        "title": "Structured Data & Config",
        "icon": "⚡",
        "description": "Convert configuration and data files between JSON, YAML, and TOML",
        "inputs": [".json", ".yaml", ".yml", ".toml"],
        "outputs": ["JSON", "YAML", "TOML", "CSV"],
        "module": data,
        "recommendations": {
            ".json": [
                {"format": "YAML", "badge": "Clean Config", "reason": "Human-friendly readable configuration syntax"},
                {"format": "TOML", "badge": "Config", "reason": "Strict key-value configuration file"},
                {"format": "CSV", "badge": "Tabular", "reason": "Flatten array records into a spreadsheet"}
            ],
            ".yaml": [
                {"format": "JSON", "badge": "Universal", "reason": "Standard JSON for APIs and parsers"},
                {"format": "TOML", "badge": "Config", "reason": "Standard configuration format"}
            ],
            ".yml": [
                {"format": "JSON", "badge": "Universal", "reason": "Standard JSON for APIs and parsers"},
                {"format": "TOML", "badge": "Config", "reason": "Standard configuration format"}
            ],
            ".toml": [
                {"format": "JSON", "badge": "Universal", "reason": "Standard JSON format"},
                {"format": "YAML", "badge": "Human-Friendly", "reason": "Clean readable configuration syntax"}
            ]
        }
    }
}

def get_category_key_for_extension(ext: str) -> Optional[str]:
    """Finds which category key handles the given file extension."""
    norm_ext = ext.lower().strip()
    if not norm_ext.startswith("."):
        norm_ext = f".{norm_ext}"
        
    for cat_key, cat_data in REGISTRY.items():
        if norm_ext in cat_data["inputs"]:
            return cat_key
    return None

def get_supported_outputs(ext: str) -> List[str]:
    """Returns list of allowed output format strings for an extension (e.g. ['PNG', 'JPG', 'WEBP'])."""
    cat_key = get_category_key_for_extension(ext)
    if not cat_key:
        return []
    
    norm_ext = ext.lower().strip().lstrip(".")
    all_outputs = list(REGISTRY[cat_key]["outputs"])
    # Filter out same format as input
    return [fmt for fmt in all_outputs if fmt.lower() != norm_ext]

def get_recommendations(ext: str) -> List[Dict[str, str]]:
    """Returns recommended format recommendations with rationale badges for the given extension."""
    cat_key = get_category_key_for_extension(ext)
    if not cat_key:
        return []

    norm_ext = ext.lower().strip()
    if not norm_ext.startswith("."):
        norm_ext = f".{norm_ext}"

    cat_data = REGISTRY[cat_key]
    recs = cat_data.get("recommendations", {}).get(norm_ext)
    if recs:
        return recs

    # Default fallback: pick the first 3 valid outputs
    allowed = get_supported_outputs(norm_ext)
    return [{"format": fmt, "badge": "Suggested", "reason": f"Convert to {fmt}"} for fmt in allowed[:3]]

def convert_file(input_path: str, output_format: str, output_dir: str) -> ConversionResult:
    """Dispatches conversion to the appropriate converter module."""
    ext = Path(input_path).suffix.lower()
    cat_key = get_category_key_for_extension(ext)
    if not cat_key:
        return ConversionResult(status='error', error=f"Unsupported file extension '{ext}'.")

    converter_module = REGISTRY[cat_key]["module"]
    return converter_module.convert(
        input_path=input_path,
        output_format=output_format,
        output_dir=output_dir
    )

def check_system_tools() -> Dict[str, Dict[str, any]]:
    """Checks the availability of external binaries needed for conversions."""
    pandoc_path = shutil.which("pandoc")
    ffmpeg_path = shutil.which("ffmpeg")
    libreoffice_path = shutil.which("libreoffice") or shutil.which("soffice")

    return {
        "pandoc": {
            "name": "Pandoc Document Engine",
            "available": pandoc_path is not None,
            "path": pandoc_path,
            "purpose": "Markdown, HTML, DOCX bidirectional conversion"
        },
        "ffmpeg": {
            "name": "FFmpeg Audio/Video Engine",
            "available": ffmpeg_path is not None,
            "path": ffmpeg_path,
            "purpose": "Audio & Video transcoding and audio extraction"
        },
        "libreoffice": {
            "name": "LibreOffice Headless Engine",
            "available": libreoffice_path is not None,
            "path": libreoffice_path,
            "purpose": "DOCX to PDF native Linux/Docker rendering"
        }
    }
