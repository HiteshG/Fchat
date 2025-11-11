"""
Section 14: Opponent Exploitation Analysis
Analyzes how to exploit opponent weaknesses
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List


def identify_opponent_vulnerabilities(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Identify opponent defensive vulnerabilities
    """
    vulnerabilities = []

    # Analyze successful attacks by zone
    if 'channel_start' in events_df.columns and 'lead_to_shot' in events_df.columns:
        channel_success = events_df.groupby('channel_start')['lead_to_shot'].agg(['sum', 'mean', 'count'])

        # Find most successful channels
        if len(channel_success) > 0:
            best_channel = channel_success['mean'].idxmax() if channel_success['mean'].max() > 0 else None
            if best_channel:
                success_rate = channel_success.loc[best_channel, 'mean']
                vulnerabilities.append({
                    'area': f'Vulnerable Channel: {best_channel}',
                    'success_rate': success_rate,
                    'recommendation': f'Target {best_channel} channel with increased frequency'
                })

    # Analyze opponent pressing weaknesses
    if 'team_out_of_possession_phase_type' in events_df.columns and 'pass_outcome' in events_df.columns:
        for phase in ['high_block', 'mid_block', 'low_block']:
            phase_data = events_df[events_df['team_out_of_possession_phase_type'] == phase]
            if len(phase_data) > 0:
                success_vs_phase = (phase_data['pass_outcome'] == 'successful').mean()
                if 'team_possession_loss_in_phase' in phase_data.columns:
                    retention_vs_phase = 1 - phase_data['team_possession_loss_in_phase'].mean()

                    if retention_vs_phase > 0.75:  # Strong performance against this phase
                        vulnerabilities.append({
                            'area': f'Effective vs {phase}',
                            'success_rate': retention_vs_phase,
                            'recommendation': f'Continue exploiting opponent {phase} with current tactics'
                        })

    return {'vulnerabilities': vulnerabilities}


def analyze_successful_patterns(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze patterns that led to success
    """
    patterns = []

    # Successful build-up patterns
    if 'team_in_possession_phase_type' in events_df.columns and 'lead_to_shot' in events_df.columns:
        successful_phases = events_df[events_df['lead_to_shot'] == True]

        if len(successful_phases) > 0:
            # Phase type distribution for successful attacks
            phase_dist = successful_phases['team_in_possession_phase_type'].value_counts(normalize=True).to_dict()

            for phase, rate in phase_dist.items():
                if rate > 0.3:  # Significant contribution
                    patterns.append({
                        'pattern': f'Success through {phase}',
                        'frequency': rate,
                        'recommendation': f'Emphasize {phase} phase in attack'
                    })

    # Successful passing patterns
    if 'pass_range' in events_df.columns and 'lead_to_shot' in events_df.columns:
        shots = events_df[events_df['lead_to_shot'] == True]
        if len(shots) > 0:
            # What pass types led to shots
            pass_types_to_shots = shots['pass_range'].value_counts(normalize=True).to_dict()

            top_pass_type = max(pass_types_to_shots.items(), key=lambda x: x[1]) if pass_types_to_shots else None
            if top_pass_type:
                patterns.append({
                    'pattern': f'Shots via {top_pass_type[0]} passes',
                    'frequency': top_pass_type[1],
                    'recommendation': f'Continue using {top_pass_type[0]} passes to create chances'
                })

    return {'patterns': patterns}


def suggest_tactical_adjustments(events_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Suggest tactical adjustments to exploit opponent
    """
    adjustments = []

    # Analyze opponent defensive line
    if 'last_defensive_line_height_start' in events_df.columns:
        avg_line_height = events_df['last_defensive_line_height_start'].mean()

        if avg_line_height > 60:  # High defensive line
            adjustments.append({
                'adjustment': 'Exploit High Defensive Line',
                'reason': f'Opponent average defensive line at {avg_line_height:.1f}m',
                'tactic': 'Increase through balls and runs in behind'
            })
        elif avg_line_height < 40:  # Low defensive line
            adjustments.append({
                'adjustment': 'Break Down Low Block',
                'reason': f'Opponent sits deep at {avg_line_height:.1f}m',
                'tactic': 'Use width and patient build-up to create openings'
            })

    # Analyze pressing intensity
    if 'pressing_chain' in events_df.columns:
        pressing_events = events_df[events_df['pressing_chain'] == True]
        pressing_rate = len(pressing_events) / len(events_df) if len(events_df) > 0 else 0

        if pressing_rate > 0.2:
            adjustments.append({
                'adjustment': 'Counter Aggressive Press',
                'reason': f'Opponent pressing {pressing_rate:.1%} of possessions',
                'tactic': 'Quick one-touch passing and long balls to bypass press'
            })
        elif pressing_rate < 0.1:
            adjustments.append({
                'adjustment': 'Exploit Passive Defense',
                'reason': f'Opponent rarely presses ({pressing_rate:.1%})',
                'tactic': 'Build patiently and create overloads in advanced areas'
            })

    # Width exploitation
    if 'channel_start' in events_df.columns:
        wide_actions = events_df[events_df['channel_start'].isin(['wide_left', 'wide_right'])]
        wide_rate = len(wide_actions) / len(events_df) if len(events_df) > 0 else 0

        if 'pass_outcome' in wide_actions.columns and len(wide_actions) > 0:
            wide_success = (wide_actions['pass_outcome'] == 'successful').mean()
            if wide_success > 0.75:
                adjustments.append({
                    'adjustment': 'Increase Width',
                    'reason': f'{wide_success:.1%} success rate in wide areas',
                    'tactic': 'Utilize wingers and fullbacks more frequently'
                })

    return adjustments


def analyze_opponent_exploitation(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze opponent exploitation opportunities

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with opponent exploitation analysis
    """
    results = {
        'section': 'Opponent Exploitation',
        'metrics': {}
    }

    # Identify vulnerabilities
    vulnerability_metrics = identify_opponent_vulnerabilities(events_df)
    results['metrics']['vulnerabilities'] = vulnerability_metrics

    # Successful patterns
    pattern_metrics = analyze_successful_patterns(events_df)
    results['metrics']['successful_patterns'] = pattern_metrics

    # Tactical adjustments
    adjustments = suggest_tactical_adjustments(events_df)
    results['metrics']['tactical_adjustments'] = adjustments

    return results
