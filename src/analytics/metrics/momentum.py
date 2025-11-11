"""
Section 11: Momentum Analysis
Analyzes game momentum and performance over time
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List


def analyze_performance_by_period(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze performance across different periods
    """
    metrics = {}

    if 'period' in events_df.columns:
        for period in events_df['period'].unique():
            period_data = events_df[events_df['period'] == period]

            period_metrics = {
                'total_actions': len(period_data),
            }

            if 'lead_to_shot' in period_data.columns:
                period_metrics['shots'] = period_data['lead_to_shot'].sum()

            if 'xthreat' in period_data.columns:
                period_metrics['total_xthreat'] = period_data['xthreat'].sum()

            if 'team_possession_loss_in_phase' in period_data.columns:
                period_metrics['possession_loss_rate'] = period_data['team_possession_loss_in_phase'].mean()

            metrics[f'period_{period}'] = period_metrics

    return metrics


def analyze_momentum_shifts(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Identify momentum shifts in the match
    """
    metrics = {}

    # Analyze by time windows (15-minute intervals)
    if 'minute_start' in events_df.columns:
        events_df = events_df.copy()
        events_df['time_window'] = (events_df['minute_start'] // 15) * 15

        windows = []
        for window in sorted(events_df['time_window'].unique()):
            window_data = events_df[events_df['time_window'] == window]

            window_metrics = {
                'time_window': f"{int(window)}-{int(window+15)} min",
                'actions': len(window_data),
            }

            if 'xthreat' in window_data.columns:
                window_metrics['xthreat'] = window_data['xthreat'].sum()

            if 'lead_to_shot' in window_data.columns:
                window_metrics['shots'] = window_data['lead_to_shot'].sum()

            windows.append(window_metrics)

        metrics['time_windows'] = windows

        # Identify best and worst periods
        if windows:
            if any('xthreat' in w for w in windows):
                best_window = max(windows, key=lambda x: x.get('xthreat', 0))
                worst_window = min(windows, key=lambda x: x.get('xthreat', 0))
                metrics['strongest_period'] = best_window['time_window']
                metrics['weakest_period'] = worst_window['time_window']

    return metrics


def analyze_game_state_performance(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze performance in different game states (winning, drawing, losing)
    """
    metrics = {}

    if 'team_score' in events_df.columns and 'opponent_team_score' in events_df.columns:
        events_df = events_df.copy()

        # Determine game state
        events_df['game_state_type'] = events_df.apply(
            lambda row: 'winning' if row['team_score'] > row['opponent_team_score']
            else ('losing' if row['team_score'] < row['opponent_team_score'] else 'drawing'),
            axis=1
        )

        for state in ['winning', 'drawing', 'losing']:
            state_data = events_df[events_df['game_state_type'] == state]

            if len(state_data) > 0:
                state_metrics = {
                    'actions': len(state_data),
                }

                if 'lead_to_shot' in state_data.columns:
                    state_metrics['shots'] = state_data['lead_to_shot'].sum()

                if 'pass_outcome' in state_data.columns:
                    state_metrics['pass_accuracy'] = (state_data['pass_outcome'] == 'successful').mean()

                metrics[state] = state_metrics

    return metrics


def analyze_momentum(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze momentum

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with momentum metrics
    """
    results = {
        'section': 'Momentum',
        'metrics': {}
    }

    # Performance by period
    period_metrics = analyze_performance_by_period(events_df)
    results['metrics']['by_period'] = period_metrics

    # Momentum shifts
    shift_metrics = analyze_momentum_shifts(events_df)
    results['metrics']['shifts'] = shift_metrics

    # Game state performance
    game_state_metrics = analyze_game_state_performance(events_df)
    results['metrics']['by_game_state'] = game_state_metrics

    return results
