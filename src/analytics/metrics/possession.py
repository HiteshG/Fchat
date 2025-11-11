"""
Section 2: Possession & Build-Up Play Analysis
Analyzes build-up patterns, player involvement, and pressure resistance
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple


def deep_buildup_analysis(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Comprehensive build-up pattern analysis
    """
    buildup_phases = events_df[events_df['team_in_possession_phase_type'] == 'build_up']

    if len(buildup_phases) == 0:
        return {}

    metrics = {
        # Progression method
        'short_pass_buildup_rate': (buildup_phases['pass_range'] == 'short').mean() if 'pass_range' in buildup_phases.columns else 0,
        'long_ball_rate': (buildup_phases['pass_range'] == 'long').mean() if 'pass_range' in buildup_phases.columns else 0,

        # Direct to 'direct' phase transition
        'bypass_to_direct_phase': (buildup_phases['current_team_in_possession_next_phase_type'] == 'direct').mean() if 'current_team_in_possession_next_phase_type' in buildup_phases.columns else 0,

        # Progression speed
        'avg_buildup_duration': buildup_phases['duration'].mean() if 'duration' in buildup_phases.columns else 0,

        # Carries vs passes for progression
        'carry_progression_rate': (buildup_phases['carry'] == True).mean() if 'carry' in buildup_phases.columns else 0,
        'carry_distance_avg': buildup_phases[buildup_phases['carry'] == True]['distance_covered'].mean() if 'carry' in buildup_phases.columns and 'distance_covered' in buildup_phases.columns else 0,

        # Success rate
        'buildup_success_rate': 1 - buildup_phases['team_possession_loss_in_phase'].mean() if 'team_possession_loss_in_phase' in buildup_phases.columns else 0,
        'buildup_to_shot_rate': buildup_phases['lead_to_shot'].mean() if 'lead_to_shot' in buildup_phases.columns else 0,

        # Total build-up phases
        'total_buildup_phases': buildup_phases['phase_index'].nunique() if 'phase_index' in buildup_phases.columns else 0,
    }

    # Channel preference during build-up
    if 'channel_start' in buildup_phases.columns:
        channel_usage = buildup_phases['channel_start'].value_counts(normalize=True).to_dict()
        metrics['buildup_channel_usage'] = channel_usage

    return metrics


def buildup_player_roles(events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify who does what in build-up
    """
    buildup = events_df[events_df['team_in_possession_phase_type'] == 'build_up']

    if len(buildup) == 0:
        return pd.DataFrame()

    player_roles = []

    for player_id in buildup['player_id'].unique():
        if pd.isna(player_id):
            continue

        player_buildup = buildup[buildup['player_id'] == player_id]

        if len(player_buildup) == 0:
            continue

        player_name = player_buildup['player_name'].iloc[0] if 'player_name' in player_buildup.columns else f"Player {player_id}"
        position = player_buildup['player_position'].iloc[0] if 'player_position' in player_buildup.columns else "Unknown"

        role_metrics = {
            'player_id': player_id,
            'player_name': player_name,
            'position': position,

            # Involvement rate
            'buildup_involvements': len(player_buildup),
            'buildup_involvements_per_phase': len(player_buildup) / buildup['phase_index'].nunique() if 'phase_index' in buildup.columns and buildup['phase_index'].nunique() > 0 else 0,

            # Progression contribution
            'progressive_passes': (player_buildup['pass_ahead'] == True).sum() if 'pass_ahead' in player_buildup.columns else 0,
            'progressive_carries': (player_buildup['carry'] == True).sum() if 'carry' in player_buildup.columns else 0,

            # Pass success under pressure
            'pass_success_rate': (player_buildup['pass_outcome'] == 'successful').mean() if 'pass_outcome' in player_buildup.columns else 0,
        }

        player_roles.append(role_metrics)

    return pd.DataFrame(player_roles)


def pressure_resistance_analysis(events_df: pd.DataFrame) -> Tuple[Dict[str, Any], pd.DataFrame, pd.DataFrame]:
    """
    How team handles being pressed
    """
    # High pressure situations
    high_pressure = events_df[
        (events_df['xloss_player_possession_start'] > 0.3) |
        (events_df['team_out_of_possession_phase_type'] == 'high_block')
    ] if 'xloss_player_possession_start' in events_df.columns and 'team_out_of_possession_phase_type' in events_df.columns else pd.DataFrame()

    normal_pressure = events_df[
        (events_df['xloss_player_possession_start'] <= 0.3) &
        (events_df['team_out_of_possession_phase_type'] != 'high_block')
    ] if 'xloss_player_possession_start' in events_df.columns and 'team_out_of_possession_phase_type' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(high_pressure) > 0 and len(normal_pressure) > 0:
        # Success rate comparison
        if 'pass_outcome' in events_df.columns:
            metrics['pass_success_high_pressure'] = (high_pressure['pass_outcome'] == 'successful').mean()
            metrics['pass_success_normal_pressure'] = (normal_pressure['pass_outcome'] == 'successful').mean()
            metrics['pressure_impact'] = metrics['pass_success_normal_pressure'] - metrics['pass_success_high_pressure']

        # Tactical response to pressure
        if 'pass_range' in events_df.columns:
            metrics['long_ball_under_pressure_rate'] = (high_pressure['pass_range'] == 'long').mean()
            metrics['long_ball_normal_rate'] = (normal_pressure['pass_range'] == 'long').mean()

        # Turnover rate
        if 'team_possession_loss_in_phase' in events_df.columns:
            metrics['turnover_under_pressure'] = high_pressure['team_possession_loss_in_phase'].mean()
            metrics['turnover_normal'] = normal_pressure['team_possession_loss_in_phase'].mean()

    return metrics, high_pressure, normal_pressure


def analyze_possession_buildup(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze possession and build-up play

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with possession metrics
    """
    results = {
        'section': 'Possession & Build-Up Play',
        'metrics': {}
    }

    # Build-up analysis
    buildup_metrics = deep_buildup_analysis(events_df)
    results['metrics']['buildup'] = buildup_metrics

    # Player roles in build-up
    player_roles = buildup_player_roles(events_df)
    results['metrics']['player_roles'] = player_roles.to_dict('records') if not player_roles.empty else []

    # Pressure resistance
    pressure_metrics, _, _ = pressure_resistance_analysis(events_df)
    results['metrics']['pressure_resistance'] = pressure_metrics

    return results
