# streamlit_app.py
import io
import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from datetime import datetime

import streamlit as st

from converters.registry import (
    REGISTRY,
    get_category_key_for_extension,
    get_supported_outputs,
    get_recommendations,
    convert_file,
    check_system_tools
)
from app.history_manager import log_conversion, get_history, clear_history
from app.config_manager import get_config

# --- Page Configuration ---
st.set_page_config(
    page_title="OmniConverter | Universal File Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .hero-container {
        padding: 1.6rem 2rem;
        background: linear-gradient(135deg, rgba(31, 83, 141, 0.15) 0%, rgba(47, 165, 114, 0.12) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(8px);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.3rem;
        background: linear-gradient(120deg, #38bdf8 0%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 0;
    }

    .badge-pill {
        display: inline-block;
        background: #1e293b;
        color: #38bdf8;
        border: 1px solid #0284c7;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        text-transform: uppercase;
        margin-right: 0.5rem;
    }
    .format-tag {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
        margin-right: 0.6rem;
    }
    .rec-reason {
        font-size: 0.85rem;
        color: #94a3b8;
    }

    .category-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
    }
    .pill-blue {
        display: inline-block;
        background: rgba(30, 64, 175, 0.4);
        color: #60a5fa;
        border: 1px solid rgba(96, 165, 250, 0.3);
        border-radius: 6px;
        padding: 0.2rem 0.55rem;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    .pill-green {
        display: inline-block;
        background: rgba(6, 95, 70, 0.4);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 6px;
        padding: 0.2rem 0.55rem;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    .pill-red {
        display: inline-block;
        background: rgba(153, 27, 27, 0.4);
        color: #f87171;
        border: 1px solid rgba(248, 113, 113, 0.3);
        border-radius: 6px;
        padding: 0.2rem 0.55rem;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

def format_file_size(size_bytes: int) -> str:
    """Formats bytes into human readable size."""
    if not size_bytes or size_bytes < 0:
        return "0 B"
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def reset_converter_state():
    """Resets all conversion keys in session state without reloading the server."""
    keys_to_clear = ["uploader_key", "target_format", "last_converted_files", "conversion_results", "conversion_error"]
    for k in keys_to_clear:
        if k in st.session_state:
            del st.session_state[k]
    # Increment uploader key to wipe the file uploader widget
    st.session_state["uploader_counter"] = st.session_state.get("uploader_counter", 0) + 1
    st.rerun()

if "uploader_counter" not in st.session_state:
    st.session_state["uploader_counter"] = 0

# --- Sidebar Navigation ---
st.sidebar.markdown("""
<div style="text-align: center; padding: 0.8rem 0;">
    <h2 style="margin: 0; font-size: 1.4rem; font-weight: 800;">🔄 OmniConverter</h2>
    <p style="color: #64748b; font-size: 0.82rem; margin-top: 0.2rem;">Universal File Conversion Engine</p>
</div>
""", unsafe_allow_html=True)

nav_selection = st.sidebar.radio(
    "Navigation",
    ["⚡ Convert Files", "📋 Formats Matrix", "📜 Conversion History", "🔧 System Status", "🐳 Docker & Sharing"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Quick Refresh Button on Sidebar
if st.sidebar.button("🔄 Reset App State", use_container_width=True, help="Clears current file and resets app to default ready state"):
    reset_converter_state()

st.sidebar.caption("🚀 **Dockerized & Cross-Platform**")
st.sidebar.caption("Supports Documents, Images, Spreadsheets, Media, and Data.")

# ==========================================
# PAGE 1: CONVERT FILES
# ==========================================
if nav_selection == "⚡ Convert Files":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">OmniConverter Engine</div>
        <p class="hero-subtitle">Upload any file to discover intelligent conversion recommendations and export to your target format instantly.</p>
    </div>
    """, unsafe_allow_html=True)

    # Top Controls Bar with Reset Button
    top_col1, top_col2 = st.columns([6, 1.2])
    with top_col2:
        if st.button("🔄 Clear / Reset", use_container_width=True, help="Clear file and reset state"):
            reset_converter_state()

    # Dynamic key ensures reset button truly clears uploaded files
    uploader_key = f"file_uploader_{st.session_state['uploader_counter']}"

    uploaded_files = st.file_uploader(
        "Choose file(s) to convert",
        accept_multiple_files=True,
        key=uploader_key,
        help="Upload images, spreadsheets, documents, audio, video, or data files"
    )

    if uploaded_files:
        first_file = uploaded_files[0]
        ext = Path(first_file.name).suffix.lower()
        cat_key = get_category_key_for_extension(ext)

        # File Overview Card
        total_size = sum(f.size for f in uploaded_files)
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("Files Selected", f"{len(uploaded_files)} file{'s' if len(uploaded_files) > 1 else ''}")
        with col_info2:
            st.metric("Input Format", ext.upper() if ext else "Unknown")
        with col_info3:
            st.metric("Total Size", format_file_size(total_size))

        if not cat_key:
            st.error(f"❌ Unsupported format **{ext}**. Check the Formats Matrix in the sidebar for supported types.")
            if st.button("🔄 Try Another File", type="secondary"):
                reset_converter_state()
        else:
            cat_data = REGISTRY[cat_key]
            allowed_outputs = get_supported_outputs(ext)
            recommendations = get_recommendations(ext)

            st.markdown(f"#### 📁 Category: **{cat_data.get('icon', '')} {cat_data['title']}**")

            # --- Target Format Selection ---
            st.markdown("### 1. Select Target Format")

            # Recommendation Cards
            if recommendations:
                st.markdown("**✨ Recommended for your file:**")
                rec_cols = st.columns(min(len(recommendations), 3))
                
                if "target_format" not in st.session_state or st.session_state.target_format not in allowed_outputs:
                    st.session_state.target_format = recommendations[0]["format"]

                for idx, rec in enumerate(recommendations[:3]):
                    with rec_cols[idx]:
                        is_selected = st.session_state.target_format == rec["format"]
                        card_border = "#38bdf8" if is_selected else "rgba(148, 163, 184, 0.2)"
                        st.markdown(f"""
                        <div style="border: 2px solid {card_border}; border-radius: 12px; padding: 0.9rem; background: rgba(30, 41, 59, 0.4); margin-bottom: 0.5rem;">
                            <span class="badge-pill">{rec.get('badge', 'Suggested')}</span>
                            <span class="format-tag">{rec['format']}</span>
                            <div class="rec-reason" style="margin-top: 0.4rem;">{rec['reason']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"Pick {rec['format']}", key=f"btn_rec_{rec['format']}", use_container_width=True):
                            st.session_state.target_format = rec["format"]
                            st.rerun()

            # All Allowed Formats dropdown
            default_index = 0
            if "target_format" in st.session_state and st.session_state.target_format in allowed_outputs:
                default_index = allowed_outputs.index(st.session_state.target_format)

            selected_format = st.selectbox(
                "Or choose from all available output formats:",
                options=allowed_outputs,
                index=default_index,
                help="Select target format to convert to"
            )
            st.session_state.target_format = selected_format

            st.markdown("---")
            st.markdown(f"### 2. Ready to Convert to **.{selected_format.lower()}**")

            btn_col1, btn_col2 = st.columns([5, 1.2])
            with btn_col1:
                convert_clicked = st.button("⚡ Convert Now", type="primary", use_container_width=True)
            with btn_col2:
                if st.button("Cancel & Clear", use_container_width=True):
                    reset_converter_state()

            if convert_clicked:
                progress_bar = st.progress(0, text="Initializing conversion...")
                results = []
                temp_dir = tempfile.mkdtemp(prefix="omniconvert_")
                output_files = []

                try:
                    for i, up_file in enumerate(uploaded_files):
                        progress_val = int(((i) / len(uploaded_files)) * 100)
                        progress_bar.progress(progress_val, text=f"Converting {up_file.name} to {selected_format}...")

                        # Save uploaded file to temp disk
                        input_temp_path = Path(temp_dir) / up_file.name
                        with open(input_temp_path, "wb") as f:
                            f.write(up_file.getbuffer())

                        # Execute conversion with fail-safe isolation
                        try:
                            res = convert_file(
                                input_path=str(input_temp_path),
                                output_format=selected_format,
                                output_dir=temp_dir
                            )
                        except Exception as unhandled_err:
                            from converters import ConversionResult
                            res = ConversionResult(status='error', error=f"Engine error: {unhandled_err}")
                        
                        log_conversion(
                            input_path=up_file.name,
                            output_format=selected_format,
                            status=res.status,
                            output_path=res.output_path,
                            size_bytes=res.output_size
                        )

                        results.append((up_file.name, res))
                        if res.status == 'success' and res.output_path:
                            output_files.append(Path(res.output_path))

                    progress_bar.progress(100, text="Conversion finished!")

                    successful = [r for r in results if r[1].status == 'success']
                    failed = [r for r in results if r[1].status == 'error']

                    if failed:
                        st.error(f"⚠️ {len(failed)} file(s) encountered an issue:")
                        for fname, res in failed:
                            st.write(f"- **{fname}**: {res.error}")
                        
                        # Prominent Fail-Safe Refresh Button
                        st.markdown("""
                        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 10px; padding: 1rem; margin: 1rem 0;">
                            <strong>💡 What to do next:</strong> Click the button below to reset the converter and try another file or format without restarting the app.
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("🔄 Reset Converter & Try Again", type="primary"):
                            reset_converter_state()

                    if successful:
                        st.success(f"🎉 Successfully converted {len(successful)} of {len(uploaded_files)} file(s) to **{selected_format}**!")

                        st.markdown("### 3. Download Converted Files")
                        
                        if len(output_files) == 1:
                            out_p = output_files[0]
                            with open(out_p, "rb") as f:
                                file_data = f.read()
                            
                            st.download_button(
                                label=f"⬇️ Download {out_p.name} ({format_file_size(len(file_data))})",
                                data=file_data,
                                file_name=out_p.name,
                                mime="application/octet-stream",
                                type="primary",
                                use_container_width=True
                            )
                        elif len(output_files) > 1:
                            zip_buffer = io.BytesIO()
                            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                                for out_p in output_files:
                                    zip_file.write(out_p, arcname=out_p.name)
                            zip_buffer.seek(0)
                            
                            zip_name = f"converted_{selected_format.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                            st.download_button(
                                label=f"📦 Download All {len(output_files)} Files as ZIP ({format_file_size(len(zip_buffer.getvalue()))})",
                                data=zip_buffer,
                                file_name=zip_name,
                                mime="application/zip",
                                type="primary",
                                use_container_width=True
                            )

                            with st.expander("Or download files individually:"):
                                for out_p in output_files:
                                    with open(out_p, "rb") as f:
                                        data = f.read()
                                    st.download_button(
                                        label=f"⬇️ {out_p.name} ({format_file_size(len(data))})",
                                        data=data,
                                        file_name=out_p.name,
                                        key=f"dl_{out_p.name}"
                                    )

                        # Conversion complete action buttons
                        st.markdown("---")
                        if st.button("🔄 Convert Another File", use_container_width=True):
                            reset_converter_state()

                except Exception as overall_e:
                    st.error(f"❌ An error occurred during processing: {overall_e}")
                    if st.button("🔄 Reset App & Clear Error", type="primary"):
                        reset_converter_state()

    else:
        st.info("👆 Drag and drop or browse files above to begin. The engine will detect the file type and highlight the best recommended formats.")

# ==========================================
# PAGE 2: FORMATS MATRIX & LIMITATIONS
# ==========================================
elif nav_selection == "📋 Formats Matrix":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Supported Formats & Matrix</div>
        <p class="hero-subtitle">Comprehensive compatibility catalog across all conversion engines.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_supported, tab_unsupported = st.tabs(["✅ Supported Formats", "❌ Unsupported / Incompatible Conversions"])

    with tab_supported:
        for cat_key, cat_data in REGISTRY.items():
            with st.container():
                st.markdown(f"""
                <div class="category-card">
                    <h3 style="margin: 0 0 0.4rem 0;">{cat_data.get('icon', '📁')} {cat_data['title']}</h3>
                    <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 1rem;">{cat_data['description']}</p>
                    <div>
                        <span style="font-weight: 600; color: #94a3b8; font-size: 0.85rem; margin-right: 0.5rem;">INPUT FORMATS:</span>
                        {" ".join([f'<span class="pill-blue">{inp.upper()}</span>' for inp in cat_data['inputs']])}
                    </div>
                    <div style="margin-top: 0.6rem;">
                        <span style="font-weight: 600; color: #94a3b8; font-size: 0.85rem; margin-right: 0.5rem;">CONVERTS TO:</span>
                        {" ".join([f'<span class="pill-green">{out.upper()}</span>' for out in cat_data['outputs']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                recs = cat_data.get("recommendations", {})
                if recs:
                    with st.expander(f"View Recommendations for {cat_data['title']}"):
                        for ext, rec_list in recs.items():
                            st.markdown(f"**From `{ext}`:**")
                            for r in rec_list:
                                st.markdown(f"- ➔ **{r['format']}** ({r.get('badge', '')}): *{r['reason']}*")

    with tab_unsupported:
        st.markdown("""
        ### What Conversions Are NOT Possible (And Why)

        A file converter **transcodes** existing data between compatible formats. It does **not** synthesize or create data from scratch. Here are conversions that cannot be performed:

        ---

        #### 1. 🚫 Cross-Domain Incompatible Conversions
        | Requested Conversion | Why It's Impossible | What Would Be Needed Instead |
        | :--- | :--- | :--- |
        | **Video (`MP4`) ➔ Spreadsheet (`XLSX`)** | Video frames have no tabular rows/columns. | Computer Vision OCR to extract text from video frames. |
        | **Image (`PNG`) ➔ Audio (`MP3`)** | Pixels cannot be translated to sound waves directly. | Image description / Text-to-Speech AI. |
        | **Audio (`MP3`) ➔ Word (`DOCX`)** | Converting spoken voice to text requires transcription. | Speech-to-Text AI (e.g., Whisper AI model). |
        | **Document (`PDF`) ➔ Audio (`MP3`)** | Reading documents aloud requires voice synthesis. | Text-to-Speech (TTS) engine. |

        ---

        #### 2. 🚫 Executables & System Binaries
        - **`.exe`, `.dll`, `.bin`, `.iso`, `.sys`**: Machine code compiled for specific CPU architectures cannot be converted into documents, images, or media.

        ---

        #### 3. 🚫 Password-Protected / Encrypted Files
        - **Locked PDFs or encrypted spreadsheets**: Cannot be read without the decryption key.

        ---

        #### 4. 🚫 Proprietary CAD & 3D Models
        - **`.psd` (Photoshop layers), `.blend` (Blender), `.dwg` (AutoCAD), `.step`**: Require proprietary vector/mesh rasterizers.

        > **How the app handles these:** If an unsupported file is uploaded, OmniConverter immediately displays an **"Unsupported Format"** banner, prevents any crash, and allows you to pick another file with one click.
        """)

# ==========================================
# PAGE 3: HISTORY
# ==========================================
elif nav_selection == "📜 Conversion History":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Conversion History</div>
        <p class="hero-subtitle">Track your recent conversions across web and desktop sessions.</p>
    </div>
    """, unsafe_allow_html=True)

    col_h1, col_h2 = st.columns([6, 1])
    with col_h2:
        if st.button("🗑️ Clear", use_container_width=True):
            clear_history()
            st.rerun()

    history_data = get_history()

    if not history_data:
        st.info("No conversions logged yet. Convert your first file to see history entries here!")
    else:
        for item in history_data:
            status_color = "#34d399" if item.get('status') == 'success' else "#f87171"
            status_text = "SUCCESS" if item.get('status') == 'success' else "FAILED"
            orig = item.get('original_ext', '').upper()
            targ = item.get('target_ext', '').upper()
            
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.5); border-left: 4px solid {status_color}; border-radius: 8px; padding: 0.8rem 1.2rem; margin-bottom: 0.6rem; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 600; font-size: 1rem; color: #f8fafc;">{item.get('filename', 'Unknown')}</div>
                    <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 0.2rem;">
                        <span class="pill-blue">{orig}</span> ➔ <span class="pill-green">{targ}</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <span style="color: {status_color}; font-weight: 700; font-size: 0.85rem;">{status_text}</span>
                    <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.2rem;">{item.get('date', '')} {item.get('time', '')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# PAGE 4: SYSTEM STATUS
# ==========================================
elif nav_selection == "🔧 System Status":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">System Status & Diagnostics</div>
        <p class="hero-subtitle">Checks availability of external conversion utilities in the current host or container.</p>
    </div>
    """, unsafe_allow_html=True)

    tools = check_system_tools()
    for key, info in tools.items():
        status_icon = "✅" if info["available"] else "⚠️"
        status_color = "#34d399" if info["available"] else "#f59e0b"
        status_badge = "Available in PATH" if info["available"] else "Not installed in local host"

        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0;">{status_icon} {info['name']}</h4>
                <span style="color: {status_color}; font-weight: 700; font-size: 0.85rem;">{status_badge}</span>
            </div>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem; margin-bottom: 0.3rem;">{info['purpose']}</p>
            <div style="font-family: monospace; font-size: 0.8rem; color: #64748b;">
                Path: {info['path'] if info['path'] else 'None (uses Docker image or pure-Python fallback)'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.info("💡 **Docker Note:** When running inside Docker, all utilities (Pandoc, FFmpeg, and LibreOffice) are pre-installed into the image.")

# ==========================================
# PAGE 5: DOCKER & SHARING GUIDE
# ==========================================
elif nav_selection == "🐳 Docker & Sharing":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Docker & Sharing Guide</div>
        <p class="hero-subtitle">How to run, containerize, and share OmniConverter with anyone effortlessly.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🚀 1. Run with Docker Compose (Recommended)
    You can spin up the full web application with all native engines pre-installed with a single command:
    ```bash
    docker compose up --build
    ```
    Then open your browser at:
    `http://localhost:8501`

    ---

    ### 🐳 2. Build & Run Standalone Docker Image
    ```bash
    # Build container image
    docker build -t omni-file-converter .

    # Run on port 8501
    docker run -d -p 8501:8501 --name converter omni-file-converter
    ```

    ---

    ### 🤝 3. How to Share with Others
    - **Share the Repository / Zip**: Send the project folder to anyone with Docker installed. They simply type `docker compose up` and have the entire app running in their browser.
    - **Publish to Docker Hub**:
      ```bash
      docker tag omni-file-converter yourusername/omni-file-converter:latest
      docker push yourusername/omni-file-converter:latest
      ```
      Anyone can then run it with:
      ```bash
      docker run -p 8501:8501 yourusername/omni-file-converter:latest
      ```

    ---

    ### 💻 4. Running Locally without Docker
    - **Web Application**:
      ```bash
      streamlit run streamlit_app.py
      ```
    - **Desktop GUI Application**:
      ```bash
      python main.py
      ```
    """)
