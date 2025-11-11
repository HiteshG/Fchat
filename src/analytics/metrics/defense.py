"""
Section 4: Defensive Structure Analysis
Analyzes defensive organization, pressing, and engagement
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def analyze_pressing_chains(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze pressing effectiveness
    """
    pressing = events_df[events_df['pressing_chain'] == True] if 'pressing_chain' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(pressing) > 0:
        metrics['total_pressing_actions'] = len(pressing)

        if 'pressing_chain_index' in pressing.columns:
            metrics['total_chains'] = pressing['pressing_chain_index'].nunique()

        if 'pressing_chain_length' in pressing.columns:
            metrics['avg_chain_length'] = pressing['pressing_chain_length'].mean()

        if 'pressing_chain_end_type' in pressing.columns:
            metrics['regain_rate'] = (pressing['pressing_chain_end_type'] == 'regain').mean()
            metrics['disruption_rate'] = (pressing['pressing_chain_end_type'] == 'disruption').mean()

        if 'stop_possession_danger' in pressing.columns:
            metrics['danger_stopped_rate'] = pressing['stop_possession_danger'].mean()

    return metrics


def analyze_defensive_line_height(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze defensive line positioning
    """
    metrics = {}

    if 'last_defensive_line_x_start' in events_df.columns:
        metrics['avg_defensive_line_height'] = events_df['last_defensive_line_x_start'].mean()
        metrics['defensive_line_std'] = events_df['last_defensive_line_x_start'].std()

    if 'last_defensive_line_height_start' in events_df.columns:
        metrics['avg_line_height'] = events_df['last_defensive_line_height_start'].mean()

    # Defensive line by phase
    if 'team_out_of_possession_phase_type' in events_df.columns:
        for phase in ['high_block', 'mid_block', 'low_block']:
            phase_data = events_df[events_df['team_out_of_possession_phase_type'] == phase]
            if len(phase_data) > 0 and 'last_defensive_line_x_start' in phase_data.columns:
                metrics[f'defensive_line_height_{phase}'] = phase_data['last_defensive_line_x_start'].mean()

    return metrics


def analyze_defensive_engagements(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze defensive player engagements
    """
    # Filter defensive events
    defensive_events = events_df[events_df['event_type'].isin(['defensive_engagement', 'tackle', 'interception'])] if 'event_type' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(defensive_events) > 0:
        metrics['total_defensive_actions'] = len(defensive_events)

        # Success rate
        if 'end_type' in defensive_events.columns:
            metrics['defensive_success_rate'] = (defensive_events['end_type'] == 'successful').mean()

        # By location
        if 'third_start' in defensive_events.columns:
            location_dist = defensive_events['third_start'].value_counts(normalize=True).to_dict()
            metrics['defensive_actions_by_third'] = location_dist

    return metrics


def analyze_defensive_structure(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze defensive structure

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with defensive metrics
    """
    results = {
        'section': 'Defensive Structure',
        'metrics': {}
    }

    # Pressing analysis
    pressing_metrics = analyze_pressing_chains(events_df)
    results['metrics']['pressing'] = pressing_metrics

    # Defensive line
    line_metrics = analyze_defensive_line_height(events_df)
    results['metrics']['defensive_line'] = line_metrics

    # Defensive engagements
    engagement_metrics = analyze_defensive_engagements(events_df)
    results['metrics']['engagements'] = engagement_metrics

    return results
