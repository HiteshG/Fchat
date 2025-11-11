"""
Section 12: Consistency Analysis
Analyzes performance consistency and reliability
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def analyze_pass_consistency(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze passing consistency across the match
    """
    metrics = {}

    if 'pass_outcome' in events_df.columns and 'minute_start' in events_df.columns:
        # Group by 15-minute windows
        events_df = events_df.copy()
        events_df['time_window'] = (events_df['minute_start'] // 15) * 15

        window_accuracies = []
        for window in sorted(events_df['time_window'].unique()):
            window_data = events_df[events_df['time_window'] == window]
            if len(window_data) > 0:
                accuracy = (window_data['pass_outcome'] == 'successful').mean()
                window_accuracies.append(accuracy)

        if len(window_accuracies) > 1:
            metrics['pass_accuracy_std'] = np.std(window_accuracies)
            metrics['pass_accuracy_consistency'] = 1 - (np.std(window_accuracies) / np.mean(window_accuracies)) if np.mean(window_accuracies) > 0 else 0

    return metrics


def analyze_phase_consistency(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Analyze consistency in different phases of play
    """
    metrics = {}

    if 'team_in_possession_phase_type' in events_df.columns:
        for phase_type in ['build_up', 'create', 'finish']:
            phase_data = events_df[events_df['team_in_possession_phase_type'] == phase_type]

            if len(phase_data) > 0:
                phase_metrics = {}

                if 'pass_outcome' in phase_data.columns:
                    phase_metrics['pass_accuracy'] = (phase_data['pass_outcome'] == 'successful').mean()

                if 'team_possession_loss_in_phase' in phase_data.columns:
                    phase_metrics['retention_rate'] = 1 - phase_data['team_possession_loss_in_phase'].mean()

                metrics[f'{phase_type}_consistency'] = phase_metrics

    return metrics


def analyze_player_consistency(events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze individual player consistency
    """
    player_consistency = []

    for player_id in events_df['player_id'].unique():
        if pd.isna(player_id):
            continue

        player_data = events_df[events_df['player_id'] == player_id]

        if len(player_data) < 10:  # Need minimum sample size
            continue

        player_name = player_data['player_name'].iloc[0] if 'player_name' in player_data.columns else f"Player {player_id}"
        position = player_data['player_position'].iloc[0] if 'player_position' in player_data.columns else "Unknown"

        consistency_metrics = {
            'player_id': player_id,
            'player_name': player_name,
            'position': position,
            'total_actions': len(player_data),
        }

        # Pass completion consistency
        if 'pass_outcome' in player_data.columns and 'minute_start' in player_data.columns:
            # Split into halves
            first_half = player_data[player_data['period'] == 1] if 'period' in player_data.columns else pd.DataFrame()
            second_half = player_data[player_data['period'] == 2] if 'period' in player_data.columns else pd.DataFrame()

            if len(first_half) > 0 and len(second_half) > 0:
                first_half_accuracy = (first_half['pass_outcome'] == 'successful').mean()
                second_half_accuracy = (second_half['pass_outcome'] == 'successful').mean()

                consistency_metrics['first_half_pass_accuracy'] = first_half_accuracy
                consistency_metrics['second_half_pass_accuracy'] = second_half_accuracy
                consistency_metrics['pass_accuracy_consistency'] = 1 - abs(first_half_accuracy - second_half_accuracy)

        player_consistency.append(consistency_metrics)

    return pd.DataFrame(player_consistency)


def analyze_consistency(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze consistency

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with consistency metrics
    """
    results = {
        'section': 'Consistency',
        'metrics': {}
    }

    # Pass consistency
    pass_metrics = analyze_pass_consistency(events_df)
    results['metrics']['passing'] = pass_metrics

    # Phase consistency
    phase_metrics = analyze_phase_consistency(events_df, phases_df)
    results['metrics']['by_phase'] = phase_metrics

    # Player consistency
    player_metrics = analyze_player_consistency(events_df)
    results['metrics']['players'] = player_metrics.to_dict('records') if not player_metrics.empty else []

    return results
