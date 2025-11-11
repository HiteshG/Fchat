"""
Section 9: Efficiency Analysis
Analyzes conversion rates and goal efficiency
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def analyze_conversion_efficiency(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze shot to goal conversion
    """
    metrics = {}

    # Shots analysis
    if 'lead_to_shot' in events_df.columns:
        shot_events = events_df[events_df['lead_to_shot'] == True]
        metrics['total_shots'] = len(shot_events)

        if 'lead_to_goal' in shot_events.columns:
            goals = shot_events[shot_events['lead_to_goal'] == True]
            metrics['total_goals'] = len(goals)
            metrics['conversion_rate'] = len(goals) / len(shot_events) if len(shot_events) > 0 else 0

        # xG analysis
        if 'xshot_player_possession_max' in shot_events.columns:
            metrics['total_xg'] = shot_events['xshot_player_possession_max'].sum()
            metrics['avg_xg_per_shot'] = shot_events['xshot_player_possession_max'].mean()

    return metrics


def analyze_possession_efficiency(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Analyze how efficiently possession is converted to chances
    """
    metrics = {}

    # Use phases if available
    if phases_df is not None and len(phases_df) > 0:
        metrics['total_possessions'] = len(phases_df)

        if 'team_possession_lead_to_shot' in phases_df.columns:
            metrics['possession_to_shot_rate'] = phases_df['team_possession_lead_to_shot'].mean()

        if 'team_possession_lead_to_goal' in phases_df.columns:
            metrics['possession_to_goal_rate'] = phases_df['team_possession_lead_to_goal'].mean()

        if 'duration' in phases_df.columns:
            metrics['avg_possession_duration'] = phases_df['duration'].mean()
    else:
        # Fallback to events analysis
        if 'phase_index' in events_df.columns:
            total_phases = events_df['phase_index'].nunique()
            metrics['total_possessions'] = total_phases

            if 'lead_to_shot' in events_df.columns:
                phases_with_shots = events_df[events_df['lead_to_shot'] == True]['phase_index'].nunique()
                metrics['possession_to_shot_rate'] = phases_with_shots / total_phases if total_phases > 0 else 0

    return metrics


def analyze_final_third_efficiency(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze efficiency in final third
    """
    final_third = events_df[events_df['third_start'] == 'attacking_third'] if 'third_start' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(final_third) > 0:
        metrics['final_third_actions'] = len(final_third)

        if 'lead_to_shot' in final_third.columns:
            metrics['final_third_to_shot_rate'] = final_third['lead_to_shot'].mean()

        if 'pass_outcome' in final_third.columns:
            metrics['final_third_pass_accuracy'] = (final_third['pass_outcome'] == 'successful').mean()

        if 'team_possession_loss_in_phase' in final_third.columns:
            metrics['final_third_retention_rate'] = 1 - final_third['team_possession_loss_in_phase'].mean()

    return metrics


def analyze_efficiency(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze efficiency

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with efficiency metrics
    """
    results = {
        'section': 'Efficiency',
        'metrics': {}
    }

    # Conversion efficiency
    conversion_metrics = analyze_conversion_efficiency(events_df)
    results['metrics']['conversion'] = conversion_metrics

    # Possession efficiency
    possession_metrics = analyze_possession_efficiency(events_df, phases_df)
    results['metrics']['possession'] = possession_metrics

    # Final third efficiency
    final_third_metrics = analyze_final_third_efficiency(events_df)
    results['metrics']['final_third'] = final_third_metrics

    return results
