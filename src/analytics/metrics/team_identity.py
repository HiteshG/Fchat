"""
Section 1: Team Identity & Setup Analysis
Analyzes formation, structure, and player roles
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def analyze_formation_fluidity(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Use positional data to understand formation changes
    """
    metrics = {}

    # Vertical compactness by phase
    for phase_type in ['build_up', 'create', 'finish']:
        phase_data = events_df[events_df['team_in_possession_phase_type'] == phase_type]
        if len(phase_data) > 0:
            metrics[f'team_length_avg_{phase_type}'] = phase_data['team_in_possession_length_start'].mean()
            metrics[f'team_width_avg_{phase_type}'] = phase_data['team_in_possession_width_start'].mean()

    # Shape change rate
    if 'phase_index' in events_df.columns:
        metrics['length_change_per_phase'] = events_df.groupby('phase_index')['team_in_possession_length_start'].std().mean()

    # Channel usage asymmetry
    channel_metrics = analyze_channel_asymmetry(events_df)
    metrics.update(channel_metrics)

    return metrics


def analyze_channel_asymmetry(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Detect if team has asymmetric structure (e.g., inverted fullback)
    """
    metrics = {}

    # Count events by channel and player position
    if 'player_position' in events_df.columns and 'channel_start' in events_df.columns:
        channel_usage = events_df.groupby(['player_position', 'channel_start']).size()

        # For fullbacks specifically
        lb_channels = channel_usage.get('LB', pd.Series())
        rb_channels = channel_usage.get('RB', pd.Series())

        # Calculate how often LB goes wide vs tucking in
        if len(lb_channels) > 0:
            lb_wide_rate = lb_channels.get('wide_left', 0) / lb_channels.sum() if lb_channels.sum() > 0 else 0
        else:
            lb_wide_rate = 0

        if len(rb_channels) > 0:
            rb_wide_rate = rb_channels.get('wide_right', 0) / rb_channels.sum() if rb_channels.sum() > 0 else 0
        else:
            rb_wide_rate = 0

        metrics['lb_wide_rate'] = lb_wide_rate
        metrics['rb_wide_rate'] = rb_wide_rate
        metrics['fullback_asymmetry'] = abs(lb_wide_rate - rb_wide_rate)

    return metrics


def analyze_player_role_clarity(events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Measure how consistently players operate in defined spaces/roles
    """
    player_metrics = []

    for player_id in events_df['player_id'].unique():
        if pd.isna(player_id):
            continue

        player_data = events_df[events_df['player_id'] == player_id]

        if len(player_data) == 0:
            continue

        # Spatial consistency
        if 'channel_start' in player_data.columns:
            channel_distribution = player_data['channel_start'].value_counts(normalize=True)
            channel_entropy = -sum(p * np.log(p) for p in channel_distribution if p > 0) if len(channel_distribution) > 0 else 0
        else:
            channel_entropy = 0

        if 'third_start' in player_data.columns:
            third_distribution = player_data['third_start'].value_counts(normalize=True)
            third_entropy = -sum(p * np.log(p) for p in third_distribution if p > 0) if len(third_distribution) > 0 else 0
        else:
            third_entropy = 0

        # Phase involvement pattern
        if 'team_in_possession_phase_type' in player_data.columns:
            phase_involvement = player_data.groupby('team_in_possession_phase_type').size()
            build_up_rate = phase_involvement.get('build_up', 0) / len(player_data)
            create_rate = phase_involvement.get('create', 0) / len(player_data)
            finish_rate = phase_involvement.get('finish', 0) / len(player_data)
        else:
            build_up_rate = create_rate = finish_rate = 0

        # Get player info
        player_name = player_data['player_name'].iloc[0] if 'player_name' in player_data.columns else f"Player {player_id}"
        position = player_data['player_position'].iloc[0] if 'player_position' in player_data.columns else "Unknown"

        player_metrics.append({
            'player_id': player_id,
            'player_name': player_name,
            'position': position,
            'build_up_rate': build_up_rate,
            'create_rate': create_rate,
            'finish_rate': finish_rate,
            'channel_consistency': 1 - (channel_entropy / np.log(5)) if channel_entropy > 0 else 1,
            'third_consistency': 1 - (third_entropy / np.log(3)) if third_entropy > 0 else 1,
            'total_actions': len(player_data)
        })

    return pd.DataFrame(player_metrics)


def analyze_team_identity(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze team identity and setup

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with team identity metrics
    """
    results = {
        'section': 'Team Identity & Setup',
        'metrics': {}
    }

    # Formation fluidity
    formation_metrics = analyze_formation_fluidity(events_df)
    results['metrics']['formation'] = formation_metrics

    # Player roles
    player_roles = analyze_player_role_clarity(events_df)
    results['metrics']['player_roles'] = player_roles.to_dict('records') if not player_roles.empty else []

    # Summary statistics
    results['metrics']['summary'] = {
        'total_players': events_df['player_id'].nunique() if 'player_id' in events_df.columns else 0,
        'total_actions': len(events_df),
        'unique_positions': events_df['player_position'].nunique() if 'player_position' in events_df.columns else 0
    }

    return results
