"""
Section 10: Set-Pieces Analysis
Analyzes set-piece effectiveness and patterns
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def analyze_set_piece_situations(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze set-piece situations and outcomes
    """
    # Filter set-piece events
    set_pieces = events_df[
        events_df['game_interruption_before'].isin(['corner_kick', 'free_kick', 'throw_in', 'penalty'])
    ] if 'game_interruption_before' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(set_pieces) > 0:
        metrics['total_set_pieces'] = len(set_pieces)

        # By type
        if 'game_interruption_before' in set_pieces.columns:
            set_piece_types = set_pieces['game_interruption_before'].value_counts().to_dict()
            metrics['set_piece_types'] = set_piece_types

        # Success rate
        if 'lead_to_shot' in set_pieces.columns:
            metrics['set_piece_to_shot_rate'] = set_pieces['lead_to_shot'].mean()

        if 'lead_to_goal' in set_pieces.columns:
            metrics['set_piece_to_goal_rate'] = set_pieces['lead_to_goal'].mean()

        # Delivery analysis
        if 'pass_range' in set_pieces.columns:
            delivery_types = set_pieces['pass_range'].value_counts(normalize=True).to_dict()
            metrics['delivery_types'] = delivery_types

    return metrics


def analyze_corner_kicks(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Detailed corner kick analysis
    """
    corners = events_df[
        events_df['game_interruption_before'] == 'corner_kick'
    ] if 'game_interruption_before' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(corners) > 0:
        metrics['total_corners'] = len(corners)

        if 'lead_to_shot' in corners.columns:
            metrics['corners_to_shot'] = corners['lead_to_shot'].sum()
            metrics['corners_to_shot_rate'] = corners['lead_to_shot'].mean()

        if 'lead_to_goal' in corners.columns:
            metrics['corners_to_goal'] = corners['lead_to_goal'].sum()

        # Delivery zones
        if 'channel_end' in corners.columns:
            delivery_zones = corners['channel_end'].value_counts().to_dict()
            metrics['corner_delivery_zones'] = delivery_zones

    return metrics


def analyze_free_kicks(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Detailed free kick analysis
    """
    free_kicks = events_df[
        events_df['game_interruption_before'] == 'free_kick'
    ] if 'game_interruption_before' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(free_kicks) > 0:
        metrics['total_free_kicks'] = len(free_kicks)

        # Categorize by location
        if 'third_start' in free_kicks.columns:
            location_dist = free_kicks['third_start'].value_counts().to_dict()
            metrics['free_kick_locations'] = location_dist

        # Dangerous free kicks (attacking third)
        dangerous_fks = free_kicks[free_kicks['third_start'] == 'attacking_third'] if 'third_start' in free_kicks.columns else pd.DataFrame()
        if len(dangerous_fks) > 0:
            metrics['dangerous_free_kicks'] = len(dangerous_fks)

            if 'lead_to_shot' in dangerous_fks.columns:
                metrics['dangerous_fk_to_shot_rate'] = dangerous_fks['lead_to_shot'].mean()

    return metrics


def analyze_set_pieces(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze set-pieces

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with set-piece metrics
    """
    results = {
        'section': 'Set-Pieces',
        'metrics': {}
    }

    # Overall set-piece analysis
    set_piece_metrics = analyze_set_piece_situations(events_df)
    results['metrics']['overall'] = set_piece_metrics

    # Corner kicks
    corner_metrics = analyze_corner_kicks(events_df)
    results['metrics']['corners'] = corner_metrics

    # Free kicks
    free_kick_metrics = analyze_free_kicks(events_df)
    results['metrics']['free_kicks'] = free_kick_metrics

    return results
