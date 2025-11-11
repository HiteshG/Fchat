"""
Section 5: Transitions Analysis
Analyzes transition speed and effectiveness
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def analyze_counter_attacks(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze counter-attacking patterns
    """
    # Identify counter-attacks (quick transitions)
    counter_attacks = events_df[
        (events_df['current_team_in_possession_previous_phase_type'].isin(['regain', 'turnover'])) &
        (events_df['team_in_possession_phase_type'] == 'direct')
    ] if 'current_team_in_possession_previous_phase_type' in events_df.columns and 'team_in_possession_phase_type' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(counter_attacks) > 0:
        metrics['total_counter_attacks'] = counter_attacks['phase_index'].nunique() if 'phase_index' in counter_attacks.columns else len(counter_attacks)

        # Speed metrics
        if 'duration' in counter_attacks.columns:
            metrics['avg_counter_duration'] = counter_attacks['duration'].mean()

        # Success metrics
        if 'lead_to_shot' in counter_attacks.columns:
            metrics['counter_to_shot_rate'] = counter_attacks['lead_to_shot'].mean()

        if 'lead_to_goal' in counter_attacks.columns:
            metrics['counter_to_goal_rate'] = counter_attacks['lead_to_goal'].mean()

        # Distance covered
        if 'distance_covered' in counter_attacks.columns:
            metrics['avg_counter_distance'] = counter_attacks['distance_covered'].sum() / metrics.get('total_counter_attacks', 1)

    return metrics


def analyze_transition_speed(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze speed of transitions
    """
    # Filter transition moments
    transitions = events_df[
        events_df['lead_to_different_phase'] == True
    ] if 'lead_to_different_phase' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(transitions) > 0:
        metrics['total_transitions'] = len(transitions)

        # Duration analysis
        if 'duration' in transitions.columns:
            metrics['avg_transition_duration'] = transitions['duration'].mean()

        # Forward momentum in transitions
        if 'forward_momentum' in transitions.columns:
            metrics['forward_momentum_rate'] = (transitions['forward_momentum'] == True).mean()

        # Speed bands
        if 'speed_avg_band' in transitions.columns:
            speed_dist = transitions['speed_avg_band'].value_counts(normalize=True).to_dict()
            metrics['transition_speed_distribution'] = speed_dist

    return metrics


def analyze_defensive_transitions(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze defensive transition effectiveness
    """
    # Quick defensive response after losing possession
    defensive_transitions = events_df[
        (events_df['team_possession_loss_in_phase'] == True)
    ] if 'team_possession_loss_in_phase' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(defensive_transitions) > 0:
        metrics['total_defensive_transitions'] = len(defensive_transitions)

        # Immediate pressure application
        if 'pressing_chain' in events_df.columns:
            # Count pressing actions immediately after loss
            metrics['immediate_press_rate'] = 0.5  # Placeholder - needs more complex logic

    return metrics


def analyze_transitions(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze transitions

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with transition metrics
    """
    results = {
        'section': 'Transitions',
        'metrics': {}
    }

    # Counter-attacks
    counter_metrics = analyze_counter_attacks(events_df)
    results['metrics']['counter_attacks'] = counter_metrics

    # Transition speed
    speed_metrics = analyze_transition_speed(events_df)
    results['metrics']['transition_speed'] = speed_metrics

    # Defensive transitions
    defensive_metrics = analyze_defensive_transitions(events_df)
    results['metrics']['defensive_transitions'] = defensive_metrics

    return results
