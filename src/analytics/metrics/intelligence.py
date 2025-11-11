"""
Section 6: Tactical Intelligence Analysis
Analyzes decision-making quality and line-breaking patterns
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def identify_line_breaking_patterns(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Where and how team breaks defensive lines
    """
    line_breaks = events_df[
        (events_df['first_line_break'] == True) |
        (events_df['last_line_break'] == True)
    ] if 'first_line_break' in events_df.columns and 'last_line_break' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(line_breaks) > 0:
        metrics['total_line_breaks'] = len(line_breaks)

        if 'first_line_break' in line_breaks.columns:
            metrics['first_line_breaks'] = line_breaks['first_line_break'].sum()

        if 'last_line_break' in line_breaks.columns:
            metrics['last_line_breaks'] = line_breaks['last_line_break'].sum()

        # Line break methods
        if 'furthest_line_break_type' in line_breaks.columns:
            methods = line_breaks['furthest_line_break_type'].value_counts(normalize=True).to_dict()
            metrics['line_break_methods'] = methods

        # By player position
        if 'player_position' in line_breaks.columns:
            position_breaks = line_breaks.groupby('player_position').size().to_dict()
            metrics['line_breaks_by_position'] = position_breaks

    return metrics


def analyze_decision_quality(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze quality of passing decisions
    """
    possessions = events_df[events_df['event_type'] == 'player_possession'] if 'event_type' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(possessions) > 0:
        # Dangerous option utilization
        if 'n_passing_options_dangerous_not_difficult' in possessions.columns:
            dangerous_available = possessions[possessions['n_passing_options_dangerous_not_difficult'] > 0]
            if len(dangerous_available) > 0:
                if 'player_targeted_dangerous' in dangerous_available.columns:
                    metrics['dangerous_option_chosen_rate'] = (dangerous_available['player_targeted_dangerous'] == True).mean()

        # Progressive option selection
        if 'n_passing_options_ahead' in possessions.columns and 'pass_ahead' in possessions.columns:
            progressive_available = possessions[possessions['n_passing_options_ahead'] > 0]
            if len(progressive_available) > 0:
                metrics['progressive_option_chosen_rate'] = (progressive_available['pass_ahead'] == True).mean()

        # Decision success rate
        if 'pass_outcome' in possessions.columns:
            metrics['decision_success_rate'] = (possessions['pass_outcome'] == 'successful').mean()

    return metrics


def analyze_spatial_awareness(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze spatial awareness and positioning
    """
    metrics = {}

    # Positioning relative to defensive line
    if 'delta_to_last_defensive_line_start' in events_df.columns:
        metrics['avg_positioning_vs_defensive_line'] = events_df['delta_to_last_defensive_line_start'].mean()

    # Runs behind defense
    if 'event_subtype' in events_df.columns:
        runs_behind = events_df[events_df['event_subtype'] == 'behind']
        metrics['total_runs_behind'] = len(runs_behind)

        if len(runs_behind) > 0 and 'targeted' in runs_behind.columns:
            metrics['runs_behind_targeted_rate'] = (runs_behind['targeted'] == True).mean()

    return metrics


def analyze_tactical_intelligence(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze tactical intelligence

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with tactical intelligence metrics
    """
    results = {
        'section': 'Tactical Intelligence',
        'metrics': {}
    }

    # Line-breaking patterns
    line_break_metrics = identify_line_breaking_patterns(events_df)
    results['metrics']['line_breaking'] = line_break_metrics

    # Decision quality
    decision_metrics = analyze_decision_quality(events_df)
    results['metrics']['decision_quality'] = decision_metrics

    # Spatial awareness
    spatial_metrics = analyze_spatial_awareness(events_df)
    results['metrics']['spatial_awareness'] = spatial_metrics

    return results
