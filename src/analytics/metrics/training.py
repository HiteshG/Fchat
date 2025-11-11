"""
Section 13: Training Focus Analysis
Identifies areas for training improvement
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List


def identify_weakness_areas(events_df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Identify key weakness areas
    """
    weaknesses = []

    # Analyze pass completion
    if 'pass_outcome' in events_df.columns:
        pass_accuracy = (events_df['pass_outcome'] == 'successful').mean()
        if pass_accuracy < 0.75:
            weaknesses.append({
                'area': 'Passing Accuracy',
                'value': pass_accuracy,
                'recommendation': 'Focus on passing drills and ball retention exercises'
            })

    # Analyze pressure handling
    if 'xloss_player_possession_start' in events_df.columns and 'pass_outcome' in events_df.columns:
        high_pressure = events_df[events_df['xloss_player_possession_start'] > 0.3]
        if len(high_pressure) > 0:
            pressure_success = (high_pressure['pass_outcome'] == 'successful').mean()
            if pressure_success < 0.65:
                weaknesses.append({
                    'area': 'Pressure Resistance',
                    'value': pressure_success,
                    'recommendation': 'Implement high-pressure situational training'
                })

    # Analyze final third effectiveness
    if 'third_start' in events_df.columns and 'lead_to_shot' in events_df.columns:
        final_third = events_df[events_df['third_start'] == 'attacking_third']
        if len(final_third) > 0:
            final_third_efficiency = final_third['lead_to_shot'].mean()
            if final_third_efficiency < 0.15:
                weaknesses.append({
                    'area': 'Final Third Efficiency',
                    'value': final_third_efficiency,
                    'recommendation': 'Work on finishing and final third decision-making'
                })

    # Analyze defensive transitions
    if 'team_possession_loss_in_phase' in events_df.columns:
        turnover_rate = events_df['team_possession_loss_in_phase'].mean()
        if turnover_rate > 0.3:
            weaknesses.append({
                'area': 'Ball Retention',
                'value': 1 - turnover_rate,
                'recommendation': 'Practice ball retention and defensive transition drills'
            })

    return {'weaknesses': weaknesses}


def identify_strength_areas(events_df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Identify key strength areas to maintain
    """
    strengths = []

    # Line-breaking ability
    if 'first_line_break' in events_df.columns and 'last_line_break' in events_df.columns:
        line_breaks = (events_df['first_line_break'] | events_df['last_line_break']).sum()
        total_actions = len(events_df)
        line_break_rate = line_breaks / total_actions if total_actions > 0 else 0

        if line_break_rate > 0.2:
            strengths.append({
                'area': 'Line-Breaking',
                'value': line_break_rate,
                'recommendation': 'Continue developing progressive passing patterns'
            })

    # Build-up play
    if 'team_in_possession_phase_type' in events_df.columns:
        buildup = events_df[events_df['team_in_possession_phase_type'] == 'build_up']
        if len(buildup) > 0 and 'team_possession_loss_in_phase' in buildup.columns:
            buildup_success = 1 - buildup['team_possession_loss_in_phase'].mean()
            if buildup_success > 0.8:
                strengths.append({
                    'area': 'Build-Up Play',
                    'value': buildup_success,
                    'recommendation': 'Maintain build-up patterns in training sessions'
                })

    return {'strengths': strengths}


def suggest_training_priorities(events_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Suggest prioritized training focus areas
    """
    priorities = []

    # Priority 1: Most critical weakness
    weaknesses = identify_weakness_areas(events_df)['weaknesses']
    if weaknesses:
        # Sort by severity (lower value = higher priority)
        sorted_weaknesses = sorted(weaknesses, key=lambda x: x['value'])
        if sorted_weaknesses:
            priorities.append({
                'priority': 1,
                'focus': sorted_weaknesses[0]['area'],
                'reason': f"Current level: {sorted_weaknesses[0]['value']:.2%}",
                'action': sorted_weaknesses[0]['recommendation']
            })

    # Priority 2: Player-specific development
    if 'player_id' in events_df.columns and 'pass_outcome' in events_df.columns:
        player_pass_rates = events_df.groupby('player_id').apply(
            lambda x: (x['pass_outcome'] == 'successful').mean()
        )
        if len(player_pass_rates) > 0:
            struggling_players = player_pass_rates[player_pass_rates < 0.7]
            if len(struggling_players) > 0:
                priorities.append({
                    'priority': 2,
                    'focus': 'Individual Player Development',
                    'reason': f"{len(struggling_players)} players below 70% pass accuracy",
                    'action': 'Implement individual technical training programs'
                })

    # Priority 3: Tactical awareness
    if 'n_passing_options_dangerous_not_difficult' in events_df.columns:
        dangerous_available = events_df[events_df['n_passing_options_dangerous_not_difficult'] > 0]
        if len(dangerous_available) > 0 and 'player_targeted_dangerous' in dangerous_available.columns:
            utilization = (dangerous_available['player_targeted_dangerous'] == True).mean()
            if utilization < 0.6:
                priorities.append({
                    'priority': 3,
                    'focus': 'Tactical Decision Making',
                    'reason': f"Only {utilization:.1%} utilization of dangerous passing options",
                    'action': 'Focus on game intelligence and decision-making drills'
                })

    return priorities


def analyze_training_focus(events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Main function to analyze training focus areas

    Args:
        events_df: Events dataframe
        phases_df: Phases dataframe (optional)

    Returns:
        Dictionary with training focus recommendations
    """
    results = {
        'section': 'Training Focus',
        'metrics': {}
    }

    # Identify weaknesses
    weakness_metrics = identify_weakness_areas(events_df)
    results['metrics']['weaknesses'] = weakness_metrics

    # Identify strengths
    strength_metrics = identify_strength_areas(events_df)
    results['metrics']['strengths'] = strength_metrics

    # Training priorities
    priorities = suggest_training_priorities(events_df)
    results['metrics']['priorities'] = priorities

    return results
