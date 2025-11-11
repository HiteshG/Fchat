"""
Football Tactical Intelligence Platform
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import json
import os
import time
from pathlib import Path

# Import custom modules
from src.data_processing.preprocessing import (
    create_enriched_tracking_data,
    get_enriched_data_info
)
from src.analytics.framework import MetricsEngine
from src.ui.report_page import render_match_report, render_export_options

# Configure Streamlit page
st.set_page_config(
    page_title="Football Tactical Intelligence Platform",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SkillCorner Color scheme
from src.analytics.colors import SKILLCORNER_COLORS

COLORS = SKILLCORNER_COLORS

# Custom CSS
st.markdown(f"""
<style>
    .main {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
    }}
    .stButton>button {{
        background-color: {COLORS['primary']};
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }}
    .stButton>button:hover {{
        background-color: {COLORS['accent']};
    }}
    .success-box {{
        background-color: {COLORS['success']};
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }}
    .info-box {{
        background-color: {COLORS['secondary']};
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }}
    h1, h2, h3 {{
        color: {COLORS['text']};
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'enriched_data' not in st.session_state:
    st.session_state.enriched_data = None
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {}
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'metrics_results' not in st.session_state:
    st.session_state.metrics_results = None
if 'events_df' not in st.session_state:
    st.session_state.events_df = None
if 'phases_df' not in st.session_state:
    st.session_state.phases_df = None


def save_uploaded_file(uploaded_file, directory: str) -> str:
    """
    Save uploaded file to specified directory

    Args:
        uploaded_file: Streamlit uploaded file object
        directory: Directory to save the file

    Returns:
        Path to saved file
    """
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def process_data(metadata_path, tracking_path, events_path, phases_path, match_id):
    """
    Process uploaded data and create enriched tracking data

    Args:
        metadata_path: Path to metadata file
        tracking_path: Path to tracking file
        events_path: Path to events file
        phases_path: Path to phases file
        match_id: Match identifier
    """
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        # Stage 1: Load data
        status_text.text("⚙️ Loading metadata...")
        progress_bar.progress(10)

        # Create enriched tracking data
        enriched_df = create_enriched_tracking_data(
            tracking_path,
            metadata_path,
            match_id
        )
        st.session_state.enriched_data = enriched_df

        status_text.text("⚙️ Loading events and phases data...")
        progress_bar.progress(25)

        # Load events and phases
        events_df = pd.read_csv(events_path)
        phases_df = pd.read_csv(phases_path)

        st.session_state.events_df = events_df
        st.session_state.phases_df = phases_df

        # Stage 2: Compute metrics
        status_text.text("⚙️ Computing tactical metrics...")
        progress_bar.progress(40)

        # Initialize metrics engine
        metrics_engine = MetricsEngine()

        # Progress callback for metrics computation
        def metrics_progress(current, total, message):
            percent = 40 + int((current / total) * 50)  # 40-90%
            progress_bar.progress(percent)
            status_text.text(f"⚙️ {message} ({current}/{total})")

        # Compute all metrics with progress tracking
        metrics_results = metrics_engine.compute_all_metrics(
            events_df,
            phases_df,
            team_id=match_id,
            use_cache=True,
            progress_callback=metrics_progress
        )

        st.session_state.metrics_results = metrics_results

        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        st.session_state.processing_complete = True

    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        progress_bar.empty()
        status_text.empty()


def main():
    """Main application"""

    # Title
    st.title("⚽ Football Tactical Intelligence Platform")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("📋 Navigation")
        page = st.radio(
            "Select Page",
            ["Upload Data", "Match Analysis Report"],
            index=0
        )

        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This platform processes SkillCorner match data to generate:
        - Comprehensive tactical analysis
        - Interactive match reports
        - Advanced metrics dashboard
        """)

    # Page: Upload Data
    if page == "Upload Data":
        st.header("📂 Step 1: Upload Match Data")
        st.markdown("Upload all four required files to begin analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Match Information")
            metadata_file = st.file_uploader(
                "📄 Match Metadata (JSON)",
                type=['json'],
                help="Contains match info, team data, and player details"
            )

            tracking_file = st.file_uploader(
                "📍 Tracking Data (JSONL)",
                type=['jsonl'],
                help="Frame-by-frame player and ball positions"
            )

        with col2:
            st.subheader("Event & Phase Data")
            events_file = st.file_uploader(
                "⚡ Events Data (CSV)",
                type=['csv'],
                help="Match events including passes, shots, and tackles"
            )

            phases_file = st.file_uploader(
                "🔄 Phases of Play (CSV)",
                type=['csv'],
                help="Team possession and phase information"
            )

        # Match ID input
        st.markdown("---")
        match_id = st.text_input(
            "🆔 Match ID",
            value="match_001",
            help="Unique identifier for this match"
        )

        # Check if all files are uploaded
        all_files_uploaded = all([
            metadata_file,
            tracking_file,
            events_file,
            phases_file
        ])

        if all_files_uploaded:
            st.success("✅ All files uploaded successfully!")

            # Process button
            if st.button("🔍 Process Data", type="primary"):
                with st.spinner("Processing data..."):
                    # Save uploaded files
                    metadata_path = save_uploaded_file(metadata_file, "data/uploads")
                    tracking_path = save_uploaded_file(tracking_file, "data/uploads")
                    events_path = save_uploaded_file(events_file, "data/uploads")
                    phases_path = save_uploaded_file(phases_file, "data/uploads")

                    # Store paths in session state
                    st.session_state.uploaded_files = {
                        'metadata': metadata_path,
                        'tracking': tracking_path,
                        'events': events_path,
                        'phases': phases_path
                    }

                    # Process data
                    process_data(
                        metadata_path,
                        tracking_path,
                        events_path,
                        phases_path,
                        match_id
                    )

                    if st.session_state.processing_complete:
                        st.balloons()
                        st.success("🎉 Data processing completed successfully!")
                        st.info("👈 Navigate to 'Match Analysis Report' in the sidebar to view comprehensive analysis")
        else:
            st.warning("⚠️ Please upload all four required files to continue")

            # Show which files are missing
            missing = []
            if not metadata_file:
                missing.append("Metadata (JSON)")
            if not tracking_file:
                missing.append("Tracking Data (JSONL)")
            if not events_file:
                missing.append("Events Data (CSV)")
            if not phases_file:
                missing.append("Phases Data (CSV)")

            if missing:
                st.error(f"Missing files: {', '.join(missing)}")

    # Page: Match Analysis Report
    elif page == "Match Analysis Report":
        if st.session_state.metrics_results is None:
            st.warning("⚠️ No analysis available. Please upload and process data first.")
            st.info("👈 Go to 'Upload Data' page to get started")
        else:
            # Render the match report
            render_match_report(
                st.session_state.metrics_results,
                st.session_state.events_df,
                st.session_state.phases_df
            )

            # Export options
            render_export_options(st.session_state.metrics_results)


if __name__ == "__main__":
    main()
