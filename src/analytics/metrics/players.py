"""
Section 7: Individual Players Analysis
Analyzes individual player performance and contributions
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def analyze_player_performance(events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Comprehensive individual player performance metrics
    """
    player_stats = []

    for player_id in events_df['player_id'].unique():
        if pd.isna(player_id):
            continue

        player_data = events_df[events_df['player_id'] == player_id]

        if len(player_data) == 0:
            continue

        player_name = player_data['player_name'].iloc[0] if 'player_name' in player_data.columns else f"Player {player_id}"
        position = player_data['player_position'].iloc[0] if 'player_position' in player_data.columns else "Unknown"

        stats = {
            'player_id': player_id,
            'player_name': player_name,
            'position': position,
            'total_actions': len(player_data),
        }

        # Passing metrics
        if 'pass_outcome' in player_data.columns:
            passes = player_data[player_data['event_type'] == 'pass'] if 'event_type' in player_data.columns else player_data
            if len(passes) > 0:
                stats['total_passes'] = len(passes)
                stats['pass_completion_rate'] = (passes['pass_outcome'] == 'successful').mean()

        # Progressive actions
        if 'pass_ahead' in player_data.columns:
            stats['progressive_passes'] = (player_data['pass_ahead'] == True).sum()

        if 'carry' in player_data.columns:
            stats['progressive_carries'] = (player_data['carry'] == True).sum()

        # Line breaks
        if 'first_line_break' in player_data.columns:
            stats['line_breaks'] = (player_data['first_line_break'] | player_data['last_line_break']).sum() if 'last_line_break' in player_data.columns else 0

        # Threat creation
        if 'xthreat' in player_data.columns:
            stats['total_xthreat'] = player_data['xthreat'].sum()
            stats['avg_xthreat_per_action'] = player_data['xthreat'].mean()

        if 'lead_to_shot' in player_data.columns:
            stats['shot_assists'] = player_data['lead_to_shot'].sum()

        # Defensive actions
        if 'pressing_chain' in player_data.columns:
            stats['pressing_actions'] = (player_data['pressing_chain'] == True).sum()

        player_stats.append(stats)

    return pd.DataFrame(player_stats)


def identify_key_players(player_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Identify key players by different metrics
    """
    key_players = {}

    if len(player_df) > 0:
        # Most influential
        if 'total_xthreat' in player_df.columns:
            top_threat = player_df.nlargest(5, 'total_xthreat')[['player_name', 'total_xthreat']].to_dict('records')
            key_players['top_threat_creators'] = top_threat

        # Most progressive
        if 'progressive_passes' in player_df.columns:
            top_progressive = player_df.nlargest(5, 'progressive_passes')[['player_name', 'progressive_passes']].to_dict('records')
            key_players['top_progressive_players'] = top_progressive

        # Best pass completion
        if 'pass_completion_rate' in player_df.columns:
            # Filter players with at least 20 passes
            qualified = player_df[player_df.get('total_passes', 0) >= 20]
            if len(qualified) > 0:
                top_passers = qualified.nlargest(5, 'pass_completion_rate')[['player_name', 'pass_completion_rate']].to_dict('records')
                key_players['most_accurate_passers'] = top_passers

    return key_players


def analyze_individual_players(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze individual players

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with player metrics
    """
    results = {
        'section': 'Individual Players',
        'metrics': {}
    }

    # Player performance
    player_performance = analyze_player_performance(events_df)
    results['metrics']['all_players'] = player_performance.to_dict('records') if not player_performance.empty else []

    # Key players
    key_players = identify_key_players(player_performance)
    results['metrics']['key_players'] = key_players

    return results
