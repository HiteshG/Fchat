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
from src.data_processing.knowledge_bank import KnowledgeBank

# Configure Streamlit page
st.set_page_config(
    page_title="Football Tactical Intelligence Platform",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Color scheme as per specification
COLORS = {
    "primary": "#00A85D",
    "secondary": "#1D73E8",
    "accent": "#00D8B0",
    "success": "#4CAF50",
    "warning": "#FFB300",
    "danger": "#D32F2F",
    "neutral": "#6E6E6E",
    "background": "#FFFFFF",
    "text": "#212121"
}

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
if 'knowledge_bank' not in st.session_state:
    st.session_state.knowledge_bank = None
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {}
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False


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
    # Progress stages
    progress_stages = [
        (10, "Loading metadata..."),
        (25, "Processing tracking data..."),
        (50, "Creating enriched tracking data..."),
        (70, "Generating knowledge bank..."),
        (90, "Finalizing analysis..."),
        (100, "Analysis complete!")
    ]

    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        for progress, message in progress_stages:
            status_text.text(f"⚙️ {message}")
            progress_bar.progress(progress)

            if progress == 25:
                # Create enriched tracking data
                enriched_df = create_enriched_tracking_data(
                    tracking_path,
                    metadata_path,
                    match_id
                )
                st.session_state.enriched_data = enriched_df

            elif progress == 70:
                # Generate knowledge bank
                kb = KnowledgeBank()
                knowledge_bank = kb.generate_knowledge_bank(
                    metadata_path=metadata_path,
                    tracking_path=tracking_path,
                    events_path=events_path,
                    phases_path=phases_path,
                    enriched_df=st.session_state.enriched_data
                )
                st.session_state.knowledge_bank = knowledge_bank

                # Save knowledge bank
                kb_output_path = "data/cache/knowledge_bank.json"
                os.makedirs("data/cache", exist_ok=True)
                kb.save_knowledge_bank(knowledge_bank, kb_output_path)

            time.sleep(0.3)

        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        st.session_state.processing_complete = True

    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")
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
            ["Upload Data", "View Enriched Data", "Knowledge Bank"],
            index=0
        )

        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This platform processes SkillCorner match data to generate:
        - Enriched tracking data
        - Comprehensive field documentation
        - Knowledge bank for downstream tasks
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
                        st.info("👈 Navigate to 'View Enriched Data' or 'Knowledge Bank' in the sidebar")
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

    # Page: View Enriched Data
    elif page == "View Enriched Data":
        st.header("📊 Enriched Tracking Data")

        if st.session_state.enriched_data is not None:
            enriched_df = st.session_state.enriched_data

            # Display summary statistics
            st.subheader("📈 Dataset Summary")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Rows", f"{len(enriched_df):,}")
            with col2:
                st.metric("Total Columns", len(enriched_df.columns))
            with col3:
                st.metric("Unique Players", enriched_df['player_id'].nunique())
            with col4:
                st.metric("Unique Frames", enriched_df['frame'].nunique())

            st.markdown("---")

            # Display match information
            if len(enriched_df) > 0:
                st.subheader("⚽ Match Information")
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Match:** {enriched_df['match_name'].iloc[0]}")
                    st.write(f"**Date:** {enriched_df['date_time'].iloc[0]}")

                with col2:
                    st.write(f"**Home Team:** {enriched_df['home_team.name'].iloc[0]}")
                    st.write(f"**Away Team:** {enriched_df['away_team.name'].iloc[0]}")

            st.markdown("---")

            # Display data
            st.subheader("🔍 Data Preview")

            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                period_filter = st.selectbox(
                    "Filter by Period",
                    ["All"] + sorted(enriched_df['period'].unique().tolist())
                )
            with col2:
                team_filter = st.selectbox(
                    "Filter by Team",
                    ["All"] + sorted(enriched_df['team_name'].unique().tolist())
                )

            # Apply filters
            filtered_df = enriched_df.copy()
            if period_filter != "All":
                filtered_df = filtered_df[filtered_df['period'] == period_filter]
            if team_filter != "All":
                filtered_df = filtered_df[filtered_df['team_name'] == team_filter]

            # Display filtered data
            st.dataframe(
                filtered_df.head(1000),
                use_container_width=True,
                height=400
            )

            st.info(f"Showing first 1000 rows of {len(filtered_df):,} filtered rows")

            # Download options
            st.markdown("---")
            st.subheader("💾 Download Data")

            col1, col2 = st.columns(2)

            with col1:
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="enriched_tracking_data.csv",
                    mime="text/csv"
                )

            with col2:
                # Save to parquet for efficiency
                parquet_path = "data/processed/enriched_tracking_data.parquet"
                os.makedirs("data/processed", exist_ok=True)
                enriched_df.to_parquet(parquet_path)
                st.success(f"✅ Data saved to {parquet_path}")

        else:
            st.warning("⚠️ No enriched data available. Please upload and process data first.")
            st.info("👈 Go to 'Upload Data' page to get started")

    # Page: Knowledge Bank
    elif page == "Knowledge Bank":
        st.header("📚 Knowledge Bank")
        st.markdown("Comprehensive field documentation for all datasets")

        if st.session_state.knowledge_bank is not None:
            kb = st.session_state.knowledge_bank

            # Overview
            st.subheader("📋 Overview")
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Created:** {kb.get('created_at', 'N/A')}")
                st.write(f"**Version:** {kb.get('version', 'N/A')}")

            with col2:
                datasets = [k for k in kb.keys() if k not in ['created_at', 'version', 'description']]
                st.write(f"**Datasets:** {len(datasets)}")
                st.write(f"**Datasets:** {', '.join(datasets)}")

            st.markdown("---")

            # Display each dataset
            for dataset_name in ['metadata', 'tracking', 'events', 'phases', 'enriched_tracking']:
                if dataset_name in kb:
                    dataset_info = kb[dataset_name]

                    with st.expander(f"📊 {dataset_name.replace('_', ' ').title()}", expanded=False):
                        st.markdown(f"**Description:** {dataset_info.get('description', 'N/A')}")

                        # Display fields
                        if 'all_fields' in dataset_info:
                            st.markdown(f"**Total Fields:** {len(dataset_info['all_fields'])}")

                            # Show fields in a searchable format
                            search = st.text_input(
                                f"Search fields in {dataset_name}",
                                key=f"search_{dataset_name}"
                            )

                            fields = dataset_info['all_fields']
                            if search:
                                fields = [f for f in fields if search.lower() in f.lower()]

                            if fields:
                                st.write(f"**Fields ({len(fields)}):**")
                                # Display in columns for better readability
                                n_cols = 3
                                cols = st.columns(n_cols)
                                for i, field in enumerate(fields):
                                    with cols[i % n_cols]:
                                        st.write(f"• {field}")
                            else:
                                st.warning("No fields match your search")

                        # Display critical fields if available
                        if 'critical_fields' in dataset_info:
                            st.markdown("**Critical Fields:**")
                            for field in dataset_info['critical_fields']:
                                st.write(f"🔑 {field}")

            # Download knowledge bank
            st.markdown("---")
            st.subheader("💾 Download Knowledge Bank")

            kb_json = json.dumps(kb, indent=2)
            st.download_button(
                label="📥 Download Knowledge Bank (JSON)",
                data=kb_json,
                file_name="knowledge_bank.json",
                mime="application/json"
            )

        else:
            st.warning("⚠️ Knowledge bank not generated yet. Please upload and process data first.")
            st.info("👈 Go to 'Upload Data' page to get started")


if __name__ == "__main__":
    main()
