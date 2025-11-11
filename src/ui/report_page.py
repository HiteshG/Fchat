"""
Phase 3: Report Dashboard Page
Displays comprehensive match analysis with collapsible sections and interactive charts
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any
from .components import charts
from ..analytics.colors import SKILLCORNER_COLORS


def render_executive_summary(metrics_results: Dict[str, Any], events_df: pd.DataFrame, phases_df: pd.DataFrame = None):
    """
    Render executive summary with key metrics
    """
    st.markdown("### 📋 Executive Summary")

    # Extract key metrics from different sections
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Possession metric
        if 'possession' in metrics_results['sections']:
            possession_metrics = metrics_results['sections']['possession']['metrics']
            buildup_metrics = possession_metrics.get('buildup', {})
            success_rate = buildup_metrics.get('buildup_success_rate', 0) * 100
            st.metric(
                "Build-Up Success",
                f"{success_rate:.1f}%",
                delta=None,
                help="Percentage of successful build-up phases"
            )
        else:
            st.metric("Build-Up Success", "N/A")

    with col2:
        # Shot creation metric
        if 'chance_creation' in metrics_results['sections']:
            chance_metrics = metrics_results['sections']['chance_creation']['metrics']
            shot_metrics = chance_metrics.get('shot_creation', {})
            total_shots = shot_metrics.get('total_shots', 0)
            st.metric(
                "Total Shots",
                f"{total_shots}",
                delta=None,
                help="Total shots created during the match"
            )
        else:
            st.metric("Total Shots", "N/A")

    with col3:
        # xThreat metric
        if 'chance_creation' in metrics_results['sections']:
            chance_metrics = metrics_results['sections']['chance_creation']['metrics']
            shot_metrics = chance_metrics.get('shot_creation', {})
            total_xthreat = shot_metrics.get('total_xthreat', 0)
            st.metric(
                "Total xThreat",
                f"{total_xthreat:.2f}",
                delta=None,
                help="Total expected threat generated"
            )
        else:
            st.metric("Total xThreat", "N/A")

    with col4:
        # Pressing success metric
        if 'defensive_structure' in metrics_results['sections']:
            defense_metrics = metrics_results['sections']['defensive_structure']['metrics']
            pressing_metrics = defense_metrics.get('pressing', {})
            regain_rate = pressing_metrics.get('regain_rate', 0) * 100
            st.metric(
                "Pressing Success",
                f"{regain_rate:.1f}%",
                delta=None,
                help="Percentage of pressing actions leading to regains"
            )
        else:
            st.metric("Pressing Success", "N/A")

    st.markdown("---")


def render_section_team_identity(section_data: Dict[str, Any]):
    """
    Render Team Identity & Setup section
    """
    metrics = section_data.get('metrics', {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Formation Fluidity")

        formation_metrics = metrics.get('formation', {})
        if formation_metrics:
            # Display formation metrics
            data = {}
            for key, value in formation_metrics.items():
                if isinstance(value, (int, float)):
                    data[key.replace('_', ' ').title()] = value

            if data:
                fig = charts.create_bar_chart(data, "Formation Metrics")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No formation data available")

    with col2:
        st.markdown("#### Player Role Distribution")

        player_roles = metrics.get('player_roles', [])
        if player_roles and len(player_roles) > 0:
            # Show top players by consistency
            df = pd.DataFrame(player_roles)
            if 'channel_consistency' in df.columns:
                top_consistent = df.nlargest(5, 'channel_consistency')[['player_name', 'position', 'channel_consistency']]
                st.dataframe(top_consistent, use_container_width=True)
        else:
            st.info("No player role data available")

    # Summary stats
    summary = metrics.get('summary', {})
    if summary:
        st.markdown("#### Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Players", summary.get('total_players', 0))
        with col2:
            st.metric("Total Actions", summary.get('total_actions', 0))
        with col3:
            st.metric("Unique Positions", summary.get('unique_positions', 0))


def render_section_possession(section_data: Dict[str, Any]):
    """
    Render Possession & Build-Up section
    """
    metrics = section_data.get('metrics', {})

    st.markdown("#### Build-Up Patterns")

    buildup_metrics = metrics.get('buildup', {})
    if buildup_metrics:
        col1, col2 = st.columns(2)

        with col1:
            # Build-up success metrics
            gauge_data = {
                'Success Rate': buildup_metrics.get('buildup_success_rate', 0) * 100,
                'Shot Rate': buildup_metrics.get('buildup_to_shot_rate', 0) * 100,
            }

            for label, value in gauge_data.items():
                fig = charts.create_metric_gauge(value, label)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Progression methods
            progression_data = {
                'Short Pass Rate': buildup_metrics.get('short_pass_buildup_rate', 0) * 100,
                'Long Ball Rate': buildup_metrics.get('long_ball_rate', 0) * 100,
                'Carry Rate': buildup_metrics.get('carry_progression_rate', 0) * 100,
            }

            fig = charts.create_bar_chart(progression_data, "Progression Methods (%)")
            st.plotly_chart(fig, use_container_width=True)

    # Pressure resistance
    st.markdown("#### Pressure Resistance")

    pressure_metrics = metrics.get('pressure_resistance', {})
    if pressure_metrics:
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Pass Success (High Pressure)",
                f"{pressure_metrics.get('pass_success_high_pressure', 0) * 100:.1f}%"
            )
            st.metric(
                "Turnover Rate (High Pressure)",
                f"{pressure_metrics.get('turnover_under_pressure', 0) * 100:.1f}%"
            )

        with col2:
            st.metric(
                "Pass Success (Normal)",
                f"{pressure_metrics.get('pass_success_normal_pressure', 0) * 100:.1f}%"
            )
            st.metric(
                "Pressure Impact",
                f"{pressure_metrics.get('pressure_impact', 0) * 100:.1f}%"
            )


def render_section_generic(section_data: Dict[str, Any]):
    """
    Generic section renderer for sections without custom rendering
    """
    metrics = section_data.get('metrics', {})

    if not metrics:
        st.info("No metrics available for this section")
        return

    # Display all metrics in a structured way
    for key, value in metrics.items():
        st.markdown(f"#### {key.replace('_', ' ').title()}")

        if isinstance(value, dict):
            # Display dictionary as metrics or chart
            numeric_values = {k: v for k, v in value.items() if isinstance(v, (int, float))}

            if numeric_values:
                # Show as bar chart if multiple values
                if len(numeric_values) > 1:
                    fig = charts.create_bar_chart(numeric_values, key.replace('_', ' ').title())
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # Show as single metric
                    for k, v in numeric_values.items():
                        st.metric(k.replace('_', ' ').title(), f"{v:.2f}")
            else:
                # Show as JSON
                st.json(value)

        elif isinstance(value, list):
            # Display list as dataframe if it contains dictionaries
            if value and isinstance(value[0], dict):
                df = pd.DataFrame(value)
                st.dataframe(df, use_container_width=True)
            else:
                st.write(value)

        elif isinstance(value, (int, float)):
            st.metric(key.replace('_', ' ').title(), f"{value:.2f}")

        else:
            st.write(value)


def render_match_report(metrics_results: Dict[str, Any], events_df: pd.DataFrame, phases_df: pd.DataFrame = None):
    """
    Render complete match analysis report

    Args:
        metrics_results: Computed metrics from MetricsEngine
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)
    """
    st.header("📊 Match Analysis Report")

    # Executive Summary
    render_executive_summary(metrics_results, events_df, phases_df)

    # Computation summary
    with st.expander("ℹ️ Computation Info"):
        summary = metrics_results.get('summary', {})
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Sections", summary.get('total_sections', 0))
        with col2:
            st.metric("Successful", summary.get('successful_sections', 0))
        with col3:
            st.metric("Computation Time", f"{summary.get('total_time', 0):.2f}s")

    st.markdown("---")

    # All 14 sections in collapsible expanders
    sections = metrics_results.get('sections', {})

    for section_id, section_data in sections.items():
        icon = section_data.get('icon', '📌')
        name = section_data.get('name', section_id)
        status = section_data.get('status', 'unknown')

        # Render section in expander
        with st.expander(f"{icon} {name}", expanded=False):
            if status == 'error':
                st.error(f"Error computing metrics: {section_data.get('error', 'Unknown error')}")
            else:
                # Custom rendering for specific sections
                if section_id == 'team_identity':
                    render_section_team_identity(section_data)
                elif section_id == 'possession':
                    render_section_possession(section_data)
                else:
                    # Generic rendering for other sections
                    render_section_generic(section_data)

                # Show computation time
                comp_time = section_data.get('computation_time', 0)
                st.caption(f"⏱️ Computed in {comp_time:.2f}s")


def render_export_options(metrics_results: Dict[str, Any]):
    """
    Render export options for the report
    """
    st.markdown("---")
    st.subheader("💾 Export Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Export as PDF", help="Export report as PDF"):
            st.info("PDF export feature coming soon!")

    with col2:
        if st.button("🌐 Export as HTML", help="Export report as HTML"):
            st.info("HTML export feature coming soon!")

    with col3:
        # JSON export (implemented)
        import json

        json_data = json.dumps(metrics_results, indent=2, default=str)
        st.download_button(
            label="📊 Download JSON",
            data=json_data,
            file_name="match_analysis.json",
            mime="application/json"
        )
