# 🔄 OmniConverter — Universal File Converter

> **A powerful, modern, cross-platform file converter designed for effortless file transformation, smart format recommendations, and seamless Docker sharing.**

---

## ✨ Features

- **🎯 Smart Format Recommendations**: Automatically inspects the uploaded file extension and MIME structure to recommend the best, highest-performing conversion formats with clear rationale badges (e.g. *Web Best*, *Lossless*, *Editable*, *High Perf*).
- **🌐 Dual-Interface Design**:
  - **Modern Streamlit Web App (`streamlit_app.py`)**: Glassmorphism UI, drag-and-drop file uploader, batch conversion, instant download & ZIP bundling, real-time progress, and diagnostics.
  - **CustomTkinter Desktop App (`main.py`)**: Native desktop window with dark/light mode toggle, drag-and-drop, format pill picker, and local folder integration.
- **🐳 1-Command Docker Sharing**: Containerized with all native conversion binaries (`ffmpeg`, `pandoc`, `libreoffice`) bundled, allowing you to share the app with anyone on Windows, macOS, or Linux without asking them to install complex system dependencies.
- **📦 Multi-Category Support**:
  - **Images & Graphics**: PNG, JPG, JPEG, WEBP, BMP, ICO, TIFF, GIF, PDF
  - **Tabular & Spreadsheets**: CSV, XLSX, XLS, JSON, Parquet, TSV, HTML
  - **Documents & Text**: Word (DOCX/DOC), PDF, Markdown, HTML, Plain Text
  - **Media (Audio & Video)**: MP4, MKV, AVI, MOV, WEBM, MP3, WAV, FLAC, OGG, M4A, AAC
  - **Structured Data & Config**: JSON, YAML, TOML, flattened CSV
- **📜 Conversion History**: Unified JSON history tracker that records conversions across both desktop and web sessions.
- **🔧 System Diagnostics**: Built-in health check page that detects host binaries and confirms engine availability.

---

## 🚀 Quick Start with Docker (Recommended for Sharing)

Docker packages all external libraries (FFmpeg for media transcoding, Pandoc for documents, and LibreOffice for headless DOCX-to-PDF rendering) in a single portable container.

### Option A: Using Docker Compose
```bash
docker compose up --build
```
Then open your browser at **[http://localhost:8501](http://localhost:8501)**.

### Option B: Using Standalone Docker
```bash
# 1. Build Docker image
docker build -t omni-file-converter .

# 2. Run the container
docker run -p 8501:8501 --name omni-converter omni-file-converter
```

---

## 💻 Running Locally (Without Docker)

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Launch the Web Application
```bash
streamlit run streamlit_app.py
```
*or via the main runner:*
```bash
python main.py --web
```

### 3. Launch the Desktop Application
```bash
python main.py
```

> **Note on Local Binaries**:
> - Image conversions, tabular data, and structured configurations run using pure Python dependencies.
> - For video/audio transcoding, ensure `ffmpeg` is installed in your system PATH (or use the Docker container where FFmpeg is included).
> - For markdown/pandoc conversions, install `pandoc` or rely on the Docker build.

---

## 📋 Supported Formats Matrix

| Category | Input Formats | Converts To | Top Recommended Formats |
| :--- | :--- | :--- | :--- |
| **🖼️ Images** | `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.ico`, `.tiff`, `.gif` | PNG, JPG, WEBP, PDF, ICO, BMP, TIFF | `WEBP` (Web Best), `JPG` (Photo), `PDF` (Document) |
| **📊 Tabular** | `.csv`, `.tsv`, `.xlsx`, `.xls`, `.parquet` | CSV, XLSX, JSON, PARQUET, TSV, HTML | `XLSX` (Spreadsheet), `PARQUET` (Fast), `JSON` (API) |
| **📄 Documents** | `.docx`, `.doc`, `.pdf`, `.md`, `.html`, `.txt` | DOCX, PDF, TXT, HTML, MD | `PDF` (Print), `DOCX` (Editable Word), `TXT` (Clean Text) |
| **🎬 Media** | `.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`, `.mp3`, `.wav`, `.flac`, `.ogg` | MP4, MKV, WEBM, MP3, WAV, FLAC, OGG | `MP3` (Extract Audio), `WEBM` (Web Video), `WAV` (Studio) |
| **⚡ Structured Data** | `.json`, `.yaml`, `.yml`, `.toml` | JSON, YAML, TOML, CSV | `YAML` (Clean Config), `JSON` (API), `TOML` (Config) |

---

## 📁 Project Architecture

```
File Converter/
├── Dockerfile                  # Production container definition (Python 3.11 + FFmpeg + Pandoc + LibreOffice)
├── docker-compose.yml          # 1-command startup configuration
├── .dockerignore               # Build context filter
├── requirements.txt            # Python dependencies (Streamlit, CustomTkinter, Pandas, Pillow, etc.)
├── main.py                     # Unified entry point (Desktop GUI or --web)
├── streamlit_app.py            # Modern Streamlit web application
│
├── converters/                 # Core conversion modules
│   ├── __init__.py             # ConversionResult dataclass
│   ├── registry.py             # Central format catalog, dispatcher, and recommendation engine
│   ├── images.py               # Image processing & PDF/ICO generation (Pillow)
│   ├── tabular.py              # Spreadsheet & dataset conversion (Pandas, PyArrow, OpenPyXL)
│   ├── documents.py            # Document processing (PyMuPDF, python-docx, pdf2docx, Pandoc)
│   ├── media.py                # Audio/Video transcoding & audio extraction (FFmpeg)
│   └── data.py                 # Structured data conversion (JSON, YAML, TOML)
│
├── app/                        # CustomTkinter desktop interface
│   ├── window.py               # Main TkinterDnD window
│   ├── sidebar.py              # Navigation sidebar with dark/light mode toggle
│   ├── config_manager.py       # Configuration reader & writer
│   ├── history_manager.py      # Conversion history logger (shared with web app)
│   ├── pages/
│   │   ├── convert.py          # Drag-and-drop conversion page
│   │   ├── history.py          # Visual history log
│   │   ├── supported.py        # Supported formats overview
│   │   └── settings.py         # Output folder and system diagnostics
│   └── components/
│       ├── dropzone.py         # File dropzone with OS click-to-browse
│       ├── format_picker.py    # Recommended pills + dropdown selector
│       └── progress.py         # Animated progress bar
│
└── tests/                      # Automated test suite
    ├── __init__.py
    └── test_converters.py      # End-to-end tests for all converter engines
```

---

## 🧪 Running Tests

Run the automated test suite with:
```bash
python -m unittest tests.test_converters
```

---

## 🤝 Sharing & Deployment Tips

1. **ZIP Archive**: Zip this folder and send it to anyone with Docker installed. All they need to do is run:
   ```bash
   docker compose up --build
   ```
2. **Publish to Docker Hub**:
   ```bash
   docker build -t yourusername/omni-file-converter:latest .
   docker push yourusername/omni-file-converter:latest
   ```
   Users can then run it anywhere using:
   ```bash
   docker run -d -p 8501:8501 yourusername/omni-file-converter:latest
   ```

---

## 🛠️ Upgrading & Extending

To add a new format or category:
1. Implement the conversion logic in a module inside `converters/`.
2. Register the extension and recommendations in `converters/registry.py`.
3. Both the **Streamlit Web UI** and **CustomTkinter Desktop UI** will automatically update their options, recommendation pills, and documentation matrix without requiring UI code changes!
