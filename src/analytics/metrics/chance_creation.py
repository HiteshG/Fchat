"""
Section 3: Chance Creation Analysis
Analyzes attacking patterns, final third entry, and shot quality
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def analyze_final_third_entry(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze how team enters final third
    """
    # Filter events that enter final third
    final_third_entries = events_df[
        (events_df['third_start'] != 'attacking_third') &
        (events_df['third_end'] == 'attacking_third')
    ] if 'third_start' in events_df.columns and 'third_end' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(final_third_entries) > 0:
        metrics['total_final_third_entries'] = len(final_third_entries)

        # Entry methods
        if 'event_type' in final_third_entries.columns:
            metrics['pass_entries'] = (final_third_entries['event_type'] == 'pass').sum()
            metrics['carry_entries'] = (final_third_entries['event_type'] == 'carry').sum()

        # Entry channels
        if 'channel_end' in final_third_entries.columns:
            channel_entries = final_third_entries['channel_end'].value_counts(normalize=True).to_dict()
            metrics['entry_channels'] = channel_entries

        # Success rate
        if 'lead_to_shot' in final_third_entries.columns:
            metrics['entry_to_shot_rate'] = final_third_entries['lead_to_shot'].mean()

    return metrics


def analyze_shot_creation(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze shot creation and quality
    """
    # Filter shots
    shots = events_df[events_df['lead_to_shot'] == True] if 'lead_to_shot' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(shots) > 0:
        metrics['total_shots'] = len(shots)

        # Shot locations
        if 'third_start' in shots.columns:
            metrics['shots_from_penalty_area'] = (shots['penalty_area_start'] == True).sum() if 'penalty_area_start' in shots.columns else 0

        # Expected threat
        if 'xthreat' in shots.columns:
            metrics['avg_xthreat_shot'] = shots['xthreat'].mean()
            metrics['total_xthreat'] = shots['xthreat'].sum()

        # Dangerous situations
        if 'dangerous' in shots.columns:
            metrics['dangerous_situations'] = shots['dangerous'].sum()
            metrics['dangerous_rate'] = shots['dangerous'].mean()

    return metrics


def analyze_passing_decisions(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compare actual decisions vs available options
    """
    possessions = events_df[events_df['event_type'] == 'player_possession'] if 'event_type' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(possessions) > 0:
        # Average passing options
        if 'n_passing_options' in possessions.columns:
            metrics['avg_passing_options'] = possessions['n_passing_options'].mean()

        # Dangerous options utilization
        if 'n_passing_options_dangerous_not_difficult' in possessions.columns:
            dangerous_options_available = possessions['n_passing_options_dangerous_not_difficult'] > 0
            if dangerous_options_available.sum() > 0:
                dangerous_chosen = possessions[dangerous_options_available]['player_targeted_dangerous'].sum() if 'player_targeted_dangerous' in possessions.columns else 0
                metrics['dangerous_option_utilization'] = dangerous_chosen / dangerous_options_available.sum()

        # Line-breaking options
        if 'n_passing_options_line_break' in possessions.columns:
            metrics['avg_line_break_options'] = possessions['n_passing_options_line_break'].mean()

    return metrics


def analyze_chance_creation(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze chance creation

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with chance creation metrics
    """
    results = {
        'section': 'Chance Creation',
        'metrics': {}
    }

    # Final third entry
    final_third_metrics = analyze_final_third_entry(events_df)
    results['metrics']['final_third_entry'] = final_third_metrics

    # Shot creation
    shot_metrics = analyze_shot_creation(events_df)
    results['metrics']['shot_creation'] = shot_metrics

    # Passing decisions
    decision_metrics = analyze_passing_decisions(events_df)
    results['metrics']['passing_decisions'] = decision_metrics

    return results
