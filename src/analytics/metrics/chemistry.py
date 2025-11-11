"""
Section 8: Team Chemistry Analysis
Analyzes player combinations and team cohesion
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def analyze_passing_networks(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze passing connections between players
    """
    # Filter successful passes
    passes = events_df[
        (events_df['event_type'] == 'pass') &
        (events_df['pass_outcome'] == 'successful')
    ] if 'event_type' in events_df.columns and 'pass_outcome' in events_df.columns else pd.DataFrame()

    metrics = {}

    if len(passes) > 0 and 'player_id' in passes.columns and 'player_targeted_id' in passes.columns:
        # Count passes between players
        pass_combinations = passes.groupby(['player_id', 'player_targeted_id']).size().reset_index(name='count')

        if len(pass_combinations) > 0:
            # Top combinations
            top_combos = pass_combinations.nlargest(10, 'count')

            # Add player names if available
            if 'player_name' in passes.columns and 'player_targeted_name' in passes.columns:
                combo_details = []
                for _, row in top_combos.iterrows():
                    passer = passes[passes['player_id'] == row['player_id']]['player_name'].iloc[0] if len(passes[passes['player_id'] == row['player_id']]) > 0 else "Unknown"
                    receiver = passes[passes['player_id'] == row['player_targeted_id']]['player_name'].iloc[0] if len(passes[passes['player_id'] == row['player_targeted_id']]) > 0 else "Unknown"
                    combo_details.append({
                        'passer': passer,
                        'receiver': receiver,
                        'passes': int(row['count'])
                    })
                metrics['top_passing_combinations'] = combo_details

            metrics['total_unique_combinations'] = len(pass_combinations)

    return metrics


def analyze_player_clusters(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Identify which players work together frequently
    """
    metrics = {}

    # Analyze simultaneous passing options
    if 'n_simultaneous_passing_options' in events_df.columns:
        metrics['avg_simultaneous_options'] = events_df['n_simultaneous_passing_options'].mean()

    # Give and go patterns
    if 'give_and_go' in events_df.columns:
        give_and_gos = events_df[events_df['give_and_go'] == True]
        metrics['total_give_and_gos'] = len(give_and_gos)

        if len(give_and_gos) > 0 and 'player_id' in give_and_gos.columns:
            top_give_and_go_players = give_and_gos['player_id'].value_counts().head(5).to_dict()
            metrics['top_give_and_go_players'] = top_give_and_go_players

    return metrics


def analyze_team_cohesion(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Measure overall team cohesion
    """
    metrics = {}

    # Players per phase involvement
    if 'phase_index' in events_df.columns and 'player_id' in events_df.columns:
        players_per_phase = events_df.groupby('phase_index')['player_id'].nunique().mean()
        metrics['avg_players_per_phase'] = players_per_phase

    # Distribution of touches
    if 'player_id' in events_df.columns:
        touches_distribution = events_df['player_id'].value_counts()
        if len(touches_distribution) > 0:
            # Calculate coefficient of variation (lower = more even distribution)
            cv = touches_distribution.std() / touches_distribution.mean()
            metrics['touch_distribution_balance'] = 1 / (1 + cv)  # Normalize to 0-1 scale

    return metrics


def analyze_team_chemistry(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze team chemistry

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with team chemistry metrics
    """
    results = {
        'section': 'Team Chemistry',
        'metrics': {}
    }

    # Passing networks
    network_metrics = analyze_passing_networks(events_df)
    results['metrics']['passing_networks'] = network_metrics

    # Player clusters
    cluster_metrics = analyze_player_clusters(events_df)
    results['metrics']['player_clusters'] = cluster_metrics

    # Team cohesion
    cohesion_metrics = analyze_team_cohesion(events_df)
    results['metrics']['team_cohesion'] = cohesion_metrics

    return results
