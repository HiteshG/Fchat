Football Tactical Intelligence Platform - Part 1 Specification

Version: 1.0
Last Updated: 2025
Purpose: Blueprint for building an AI-powered football match analysis system with Streamlit

After the creation of enriched_tracking_data, remove the option to view or download. 

Now we want to auto-generate comprehensive tactical analysis report

STEP 2: Match Report Dashboard                     │
│  ├─ Executive Summary                               │
│  ├─ 14 Collapsible Analysis Sections               │
│  │   ├─ Team Identity & Setup                      │
│  │   ├─ Possession & Build-Up                      │
│  │   ├─ Chance Creation                            │
│  │   ├─ Defensive Structure                        │
│  │   ├─ Transitions                                │
│  │   ├─ Tactical Intelligence                      │
│  │   ├─ Individual Players                         │
│  │   ├─ Team Chemistry                             │
│  │   ├─ Efficiency                                 │
│  │   ├─ Set-Pieces                                 │
│  │   ├─ Momentum                                   │
│  │   ├─ Consistency                                │
│  │   ├─ Training Focus                             │
│  │   └─ Opponent Exploitation                      │
│  ├─ Interactive Visualizations (Plotly)            │
│  ├─ Key Moments (auto-generated video clips)       │
│  └─ Export Options (PDF/HTML/PPTX)         

Metric Computation (30-60 seconds)

FRAMEWORK SECTIONS: COMPLETE METRICS

A) Tactical Analysis Functions
pythondef calculate_phase_effectiveness(df, team_id):
    """
    Returns success metrics for each phase
    """
    results = df.groupby('team_in_possession_phase_type').agg({
        'team_possession_lead_to_shot': 'mean',
        'team_possession_lead_to_goal': 'mean',
        'team_possession_loss_in_phase': 'mean',
        'duration': 'mean',
        'n_player_possessions_in_phase': 'mean'
    })
    return results

def analyze_pressing_chains(events_df):
    """
    Analyze pressing effectiveness
    """
    pressing = events_df[events_df['pressing_chain'] == True]
    
    metrics = {
        'total_chains': pressing['pressing_chain_index'].nunique(),
        'avg_chain_length': pressing['pressing_chain_length'].mean(),
        'regain_rate': (pressing['pressing_chain_end_type'] == 'regain').mean(),
        'disruption_rate': (pressing['pressing_chain_end_type'] == 'disruption').mean(),
        'danger_stopped_rate': pressing['stop_possession_danger'].mean()
    }
    return metrics

def identify_line_breaking_patterns(events_df):
    """
    Where and how are we breaking lines
    """
    line_breaks = events_df[
        (events_df['first_line_break'] == True) | 
        (events_df['last_line_break'] == True)
    ]
    
    return line_breaks.groupby(['player_name', 'player_position']).agg({
        'first_line_break': 'sum',
        'last_line_break': 'sum',
        'furthest_line_break': lambda x: x.value_counts(),
        'pass_direction': lambda x: x.value_counts()
    })
B) Decision Quality Analysis
pythondef analyze_passing_decisions(events_df):
    """
    Compare actual decisions vs available options
    """
    possessions = events_df[events_df['event_type'] == 'player_possession']
    
    # For each possession, compare what was done vs what was available
    decisions = []
    
    for idx, possession in possessions.iterrows():
        decision = {
            'event_id': possession['event_id'],
            'player_name': possession['player_name'],
            'end_type': possession['end_type'],
            
            # What was available
            'n_passing_options': possession['n_passing_options'],
            'n_dangerous_options': possession['n_passing_options_dangerous_difficult'] + 
                                   possession['n_passing_options_dangerous_not_difficult'],
            'n_line_breaking_options': possession['n_passing_options_line_break'],
            
            # What was chosen
            'targeted_dangerous': possession.get('player_targeted_dangerous'),
            'line_break_achieved': possession['first_line_break'] or possession['last_line_break'],
            'pass_outcome': possession['pass_outcome']
        }
        
        # Flag suboptimal decisions
        if decision['n_dangerous_options'] > 0 and not decision['targeted_dangerous']:
            decision['missed_dangerous_option'] = True
            
        decisions.append(decision)
    
    return pd.DataFrame(decisions)
    
📐 Section 1: Team Identity & Setup

🧩 1. TEAM IDENTITY & SETUP
A. Formation & Structure
Critical Metrics:
python# Dynamic Formation Analysis
def analyze_formation_fluidity(events_df):
    """
    Use positional data to understand formation changes
    """
    metrics = {
        # Vertical compactness
        'team_length_avg_buildup': events_df[
            events_df['team_in_possession_phase_type'] == 'build_up'
        ]['team_in_possession_length_start'].mean(),
        
        'team_length_avg_create': events_df[
            events_df['team_in_possession_phase_type'] == 'create'
        ]['team_in_possession_length_start'].mean(),
        
        'team_length_avg_finish': events_df[
            events_df['team_in_possession_phase_type'] == 'finish'
        ]['team_in_possession_length_start'].mean(),
        
        # Horizontal width
        'team_width_avg_buildup': events_df[
            events_df['team_in_possession_phase_type'] == 'build_up'
        ]['team_in_possession_width_start'].mean(),
        
        'team_width_avg_create': events_df[
            events_df['team_in_possession_phase_type'] == 'create'
        ]['team_in_possession_width_start'].mean(),
        
        # Shape change rate
        'length_change_per_phase': (
            events_df.groupby('phase_index')['team_in_possession_length_start']
            .std().mean()
        ),
        
        # Width asymmetry detection
        'channel_usage_asymmetry': analyze_channel_asymmetry(events_df)
    }
    return metrics

def analyze_channel_asymmetry(events_df):
    """
    Detect if team has asymmetric structure (e.g., inverted fullback)
    """
    # Count events by channel and player position
    channel_usage = events_df.groupby(['player_position', 'channel_start']).size()
    
    # For fullbacks specifically
    lb_channels = channel_usage.get(('LB', slice(None)), pd.Series())
    rb_channels = channel_usage.get(('RB', slice(None)), pd.Series())
    
    # Calculate how often LB goes wide vs tucking in (center/half-space)
    lb_wide_rate = lb_channels.get('wide_left', 0) / lb_channels.sum() if lb_channels.sum() > 0 else 0
    rb_wide_rate = rb_channels.get('wide_right', 0) / rb_channels.sum() if rb_channels.sum() > 0 else 0
    
    return {
        'lb_wide_rate': lb_wide_rate,
        'rb_wide_rate': rb_wide_rate,
        'fullback_asymmetry': abs(lb_wide_rate - rb_wide_rate)
    }
Advanced Shape Analysis:
pythondef phase_transition_shape_analysis(events_df):
    """
    How shape morphs between phases
    """
    # Group by consecutive phase transitions
    events_df['phase_changed'] = (
        events_df['team_in_possession_phase_type'] != 
        events_df['team_in_possession_phase_type'].shift(1)
    )
    
    transitions = events_df[events_df['phase_changed'] == True].copy()
    
    # Calculate shape changes at transition moments
    transitions['length_delta'] = (
        transitions['team_in_possession_length_end'] - 
        transitions['team_in_possession_length_start']
    )
    
    transitions['width_delta'] = (
        transitions['team_in_possession_width_end'] - 
        transitions['team_in_possession_width_start']
    )
    
    # Analyze by transition type
    shape_changes = transitions.groupby([
        'team_in_possession_phase_type',
        'current_team_in_possession_previous_phase_type'
    ]).agg({
        'length_delta': 'mean',
        'width_delta': 'mean',
        'duration': 'mean'  # How long transition takes
    })
    
    return shape_changes
B. Roles & Responsibilities
Critical Metrics:
pythondef analyze_player_role_clarity(events_df):
    """
    Measure how consistently players operate in defined spaces/roles
    """
    player_metrics = []
    
    for player_id in events_df['player_id'].unique():
        player_data = events_df[events_df['player_id'] == player_id]
        
        # Spatial consistency
        channel_distribution = player_data['channel_start'].value_counts(normalize=True)
        third_distribution = player_data['third_start'].value_counts(normalize=True)
        
        # Role clarity = entropy (lower = more consistent positioning)
        channel_entropy = -sum(p * np.log(p) for p in channel_distribution if p > 0)
        third_entropy = -sum(p * np.log(p) for p in third_distribution if p > 0)
        
        # Phase involvement pattern
        phase_involvement = player_data.groupby('team_in_possession_phase_type').size()
        
        # Detect role type based on patterns
        role_indicators = {
            'build_up_rate': phase_involvement.get('build_up', 0) / len(player_data),
            'create_rate': phase_involvement.get('create', 0) / len(player_data),
            'finish_rate': phase_involvement.get('finish', 0) / len(player_data),
            
            # Progressive tendency
            'avg_delta_to_defensive_line': player_data['delta_to_last_defensive_line_start'].mean(),
            'forward_movement_rate': (player_data['trajectory_direction'] == 'forward').mean(),
            
            # Support vs penetration
            'avg_location_to_ball': player_data['location_to_player_in_possession_id_start'].value_counts(normalize=True),
            'runs_behind_rate': (player_data['event_subtype'] == 'behind').sum() / len(player_data),
            
            # Spatial consistency scores
            'channel_consistency': 1 - (channel_entropy / np.log(5)),  # Normalized
            'third_consistency': 1 - (third_entropy / np.log(3))
        }
        
        player_metrics.append({
            'player_id': player_id,
            'player_name': player_data['player_name'].iloc[0],
            'position': player_data['player_position'].iloc[0],
            **role_indicators
        })
    
    return pd.DataFrame(player_metrics)
Position Optimization Analysis:
pythondef analyze_position_optimization(events_df):
    """
    Are players in positions that maximize their strengths?
    """
    # For each player, compare performance in different zones
    player_zone_performance = []
    
    for player_id in events_df['player_id'].unique():
        player_data = events_df[events_df['player_id'] == player_id]
        
        # Group by zone combinations
        zone_performance = player_data.groupby(['channel_start', 'third_start']).agg({
            'pass_outcome': lambda x: (x == 'successful').mean() if len(x) > 0 else 0,
            'lead_to_shot': 'mean',
            'dangerous': 'mean',
            'xthreat': 'mean',
            'event_id': 'count'  # Sample size
        }).reset_index()
        
        zone_performance['player_id'] = player_id
        zone_performance['player_name'] = player_data['player_name'].iloc[0]
        
        # Identify optimal zones (highest threat generation)
        zone_performance['performance_score'] = (
            zone_performance['xthreat'] * 0.4 +
            zone_performance['lead_to_shot'] * 0.3 +
            zone_performance['dangerous'] * 0.3
        )
        
        player_zone_performance.append(zone_performance)
    
    all_zones = pd.concat(player_zone_performance)
    
    # Compare actual usage vs optimal zones
    for player_id in events_df['player_id'].unique():
        player_zones = all_zones[all_zones['player_id'] == player_id]
        
        # Find best performing zones
        best_zones = player_zones.nlargest(3, 'performance_score')[['channel_start', 'third_start']]
        
        # Calculate how often they're actually in those zones
        actual_usage = player_zones['event_id'].sum()
        optimal_usage = player_zones.nlargest(3, 'performance_score')['event_id'].sum()
        
        optimization_rate = optimal_usage / actual_usage if actual_usage > 0 else 0
        
    return all_zones, optimization_rate

⚙️ 2. POSSESSION & BUILD-UP PLAY
A. Build-Up Patterns
Critical Metrics:
pythondef deep_buildup_analysis(events_df):
    """
    Comprehensive build-up pattern analysis
    """
    buildup_phases = events_df[events_df['team_in_possession_phase_type'] == 'build_up']
    
    metrics = {
        # Progression method
        'short_pass_buildup_rate': (
            buildup_phases['pass_range'] == 'short'
        ).mean(),
        
        'long_ball_rate': (
            buildup_phases['pass_range'] == 'long'
        ).mean(),
        
        # Direct to 'direct' phase transition (bypass midfield)
        'bypass_to_direct_phase': (
            buildup_phases['current_team_in_possession_next_phase_type'] == 'direct'
        ).mean(),
        
        # Line-breaking efficiency
        'buildup_line_breaks': buildup_phases.groupby('player_in_possession_id').agg({
            'first_line_break': 'sum',
            'second_last_line_break': 'sum',
            'last_line_break': 'sum',
            'furthest_line_break': lambda x: x.value_counts()
        }),
        
        # Progression speed
        'avg_buildup_duration': buildup_phases['duration'].mean(),
        'passes_before_exit': buildup_phases.groupby('phase_index')['event_id'].count().mean(),
        
        # Carries vs passes for progression
        'carry_progression_rate': (buildup_phases['carry'] == True).mean(),
        'carry_distance_avg': buildup_phases[buildup_phases['carry'] == True]['distance_covered'].mean(),
        
        # Third entry patterns
        'buildup_to_middle_third': (
            (buildup_phases['third_start'] == 'defensive_third') &
            (buildup_phases['third_end'] == 'middle_third')
        ).mean(),
        
        'buildup_to_final_third': (
            (buildup_phases['third_start'] == 'defensive_third') &
            (buildup_phases['third_end'] == 'attacking_third')
        ).mean(),
        
        # Success rate
        'buildup_success_rate': 1 - buildup_phases['team_possession_loss_in_phase'].mean(),
        'buildup_to_shot_rate': buildup_phases['lead_to_shot'].mean(),
        
        # Channel preference during build-up
        'buildup_channel_usage': buildup_phases['channel_start'].value_counts(normalize=True),
        
        # Opposition context
        'buildup_vs_high_block': buildup_phases[
            buildup_phases['team_out_of_possession_phase_type'] == 'high_block'
        ]['team_possession_loss_in_phase'].mean()
    }
    
    return metrics
Build-Up Sequence Analysis:
pythondef analyze_buildup_sequences(events_df):
    """
    Detailed sequence patterns during build-up
    """
    buildup_phases = events_df[events_df['team_in_possession_phase_type'] == 'build_up']
    
    # Group by phase_index to get sequences
    sequences = []
    
    for phase_idx in buildup_phases['phase_index'].unique():
        phase_events = buildup_phases[buildup_phases['phase_index'] == phase_idx].sort_values('index')
        
        if len(phase_events) == 0:
            continue
            
        sequence = {
            'phase_index': phase_idx,
            'total_passes': len(phase_events),
            'duration': phase_events['duration'].sum(),
            'players_involved': phase_events['player_id'].nunique(),
            
            # Spatial progression
            'x_progression': phase_events['x_end'].iloc[-1] - phase_events['x_start'].iloc[0],
            'y_movement': abs(phase_events['y_end'].iloc[-1] - phase_events['y_start'].iloc[0]),
            
            # Pattern identification
            'channel_switches': (phase_events['channel_start'] != phase_events['channel_start'].shift(1)).sum(),
            'backward_passes': (phase_events['pass_direction'] == 'backward').sum(),
            'forward_passes': (phase_events['pass_direction'] == 'forward').sum(),
            
            # Line breaks achieved
            'lines_broken': phase_events[['first_line_break', 'second_last_line_break', 'last_line_break']].any(axis=1).sum(),
            
            # Starting structure
            'start_channel': phase_events['channel_start'].iloc[0],
            'start_position': phase_events['player_position'].iloc[0],
            
            # Outcome
            'successful': not phase_events['team_possession_loss_in_phase'].iloc[-1],
            'led_to_shot': phase_events['lead_to_shot'].any(),
            'end_phase_type': phase_events['current_team_in_possession_next_phase_type'].iloc[-1],
            
            # Pressure context
            'started_under_pressure': phase_events['xloss_player_possession_start'].iloc[0],
            'avg_passing_options': phase_events['n_passing_options'].mean(),
            
            # Key progressive actions
            'progressive_carries': (phase_events['carry'] == True).sum(),
            'progressive_passes': (
                (phase_events['pass_ahead'] == True) | 
                (phase_events['first_line_break'] == True)
            ).sum()
        }
        
        sequences.append(sequence)
    
    sequences_df = pd.DataFrame(sequences)
    
    # Identify common successful patterns
    successful_sequences = sequences_df[sequences_df['successful'] == True]
    
    # Cluster similar sequences
    from sklearn.cluster import KMeans
    
    features_for_clustering = successful_sequences[[
        'total_passes', 'x_progression', 'channel_switches', 
        'backward_passes', 'forward_passes', 'progressive_carries'
    ]].fillna(0)
    
    if len(features_for_clustering) > 5:
        kmeans = KMeans(n_clusters=min(5, len(features_for_clustering)), random_state=42)
        successful_sequences['pattern_cluster'] = kmeans.fit_predict(features_for_clustering)
    
    return sequences_df, successful_sequences
B. Player Involvement
Critical Metrics:
pythondef buildup_player_roles(events_df):
    """
    Identify who does what in build-up
    """
    buildup = events_df[events_df['team_in_possession_phase_type'] == 'build_up']
    
    player_roles = []
    
    for player_id in buildup['player_id'].unique():
        player_buildup = buildup[buildup['player_id'] == player_id]
        
        role_metrics = {
            'player_id': player_id,
            'player_name': player_buildup['player_name'].iloc[0],
            'position': player_buildup['player_position'].iloc[0],
            
            # Involvement rate
            'buildup_involvements': len(player_buildup),
            'buildup_involvements_per_phase': len(player_buildup) / buildup['phase_index'].nunique(),
            
            # Initiator role
            'phases_initiated': (player_buildup['first_player_possession_in_team_possession'] == True).sum(),
            'initiation_rate': (player_buildup['first_player_possession_in_team_possession'] == True).mean(),
            
            # Progression contribution
            'line_breaks_made': (
                player_buildup['first_line_break'] | 
                player_buildup['last_line_break']
            ).sum(),
            'progressive_passes': (player_buildup['pass_ahead'] == True).sum(),
            'progressive_carries': (player_buildup['carry'] == True).sum(),
            'avg_x_progression': (player_buildup['x_end'] - player_buildup['x_start']).mean(),
            
            # Safety role
            'backward_passes': (player_buildup['pass_direction'] == 'backward').sum(),
            'safe_passing_rate': (
                player_buildup['difficult_pass_target'] == False
            ).mean() if 'difficult_pass_target' in player_buildup else 0,
            
            # Link role (between lines)
            'avg_location_to_ball': player_buildup['location_to_player_in_possession_id_start'].mode()[0] if len(player_buildup) > 0 else None,
            'receives_between_lines': (
                (player_buildup['inside_defensive_shape_start'] == False) &
                (player_buildup['third_start'] == 'middle_third')
            ).sum(),
            
            # Pressure handling
            'pass_success_under_pressure': player_buildup[
                player_buildup['xloss_player_possession_start'] > 0.3
            ]['pass_outcome'].apply(lambda x: x == 'successful').mean() if len(player_buildup) > 0 else 0,
            
            # Option provision as off-ball player
            'times_available_as_option': buildup[
                buildup['player_targeted_id'] == player_id
            ].shape[0],
            'reception_success_rate': buildup[
                buildup['player_targeted_id'] == player_id
            ]['received'].mean() if buildup[buildup['player_targeted_id'] == player_id].shape[0] > 0 else 0
        }
        
        player_roles.append(role_metrics)
    
    roles_df = pd.DataFrame(player_roles)
    
    # Classify players into archetypes
    roles_df['archetype'] = roles_df.apply(classify_buildup_archetype, axis=1)
    
    return roles_df

def classify_buildup_archetype(row):
    """
    Classify player's build-up role
    """
    if row['initiation_rate'] > 0.5 and row['position'] in ['GK', 'CB', 'LCB', 'RCB']:
        return 'build_up_initiator'
    elif row['line_breaks_made'] > 3 and row['progressive_passes'] > 5:
        return 'line_breaker'
    elif row['receives_between_lines'] > 5:
        return 'link_player'
    elif row['progressive_carries'] > 3:
        return 'ball_carrier'
    elif row['backward_passes'] > row['progressive_passes']:
        return 'recycler'
    else:
        return 'rotation_player'
C. Under Pressure
Critical Metrics:
pythondef pressure_resistance_analysis(events_df):
    """
    How team handles being pressed
    """
    # High pressure situations (xloss > 0.3 or opponent high block)
    high_pressure = events_df[
        (events_df['xloss_player_possession_start'] > 0.3) |
        (events_df['team_out_of_possession_phase_type'] == 'high_block')
    ]
    
    normal_pressure = events_df[
        (events_df['xloss_player_possession_start'] <= 0.3) &
        (events_df['team_out_of_possession_phase_type'] != 'high_block')
    ]
    
    metrics = {
        # Success rate comparison
        'pass_success_high_pressure': (high_pressure['pass_outcome'] == 'successful').mean(),
        'pass_success_normal_pressure': (normal_pressure['pass_outcome'] == 'successful').mean(),
        'pressure_impact': (
            (normal_pressure['pass_outcome'] == 'successful').mean() -
            (high_pressure['pass_outcome'] == 'successful').mean()
        ),
        
        # Tactical response to pressure
        'long_ball_under_pressure_rate': (
            high_pressure['pass_range'] == 'long'
        ).mean(),
        'long_ball_normal_rate': (
            normal_pressure['pass_range'] == 'long'
        ).mean(),
        
        # Carry response
        'carry_under_pressure': (high_pressure['carry'] == True).mean(),
        'carry_normal': (normal_pressure['carry'] == True).mean(),
        
        # Forward momentum creation
        'forward_momentum_under_pressure': (high_pressure['forward_momentum'] == True).mean(),
        
        # Players targeted by press
        'most_pressed_players': high_pressure['player_id'].value_counts().head(5),
        'press_target_success_rate': high_pressure.groupby('player_id')['pass_outcome'].apply(
            lambda x: (x == 'successful').mean()
        ),
        
        # Available options under pressure
        'avg_options_under_pressure': high_pressure['n_passing_options'].mean(),
        'avg_options_normal': normal_pressure['n_passing_options'].mean(),
        
        # Quality of options under pressure
        'dangerous_options_under_pressure_rate': (
            high_pressure['n_passing_options_dangerous_not_difficult'] > 0
        ).mean(),
        
        # Defensive line breaking under pressure
        'line_breaks_under_pressure': (
            high_pressure['first_line_break'] | high_pressure['last_line_break']
        ).mean(),
        
        # Turnover rate
        'turnover_under_pressure': high_pressure['team_possession_loss_in_phase'].mean(),
        'turnover_normal': normal_pressure['team_possession_loss_in_phase'].mean()
    }
    
    return metrics, high_pressure, normal_pressure


## Instructions 

Double check that while creating metrics you are using proper metrics from 

#### Phase of Play Data file
Phase file is csv file. 

Phases of play capture which phase the attacking and defending team are in concurrently.Phases of play are only defined when the ball is in play. When the ball is out of play there is no phase of play.  Each in-possession phase directly corresponds to an out-of-possession phase.


Phase file have following fields :
'index',
'match_id',
'frame_start',
'frame_end',
'time_start',
'time_end',
'minute_start',
'second_start',
'duration',
'period',
'attacking_side_id',
'team_in_possession_id',
'attacking_side',
'team_in_possession_shortname',
'n_player_possessions_in_phase',
'team_possession_loss_in_phase',
'team_possession_lead_to_goal',
'team_possession_lead_to_shot',
'team_in_possession_phase_type',
'team_in_possession_phase_type_id',
'team_out_of_possession_phase_type',
'team_out_of_possession_phase_type_id',
'x_start',
'y_start',
'channel_id_start',
'channel_start',
'third_id_start',
'third_start',
'penalty_area_start',
'x_end',
'y_end',
'channel_id_end',
'channel_end',
'third_id_end',
'third_end',
'penalty_area_end',
'team_in_possession_width_start',
'team_in_possession_width_end',
'team_in_possession_length_start',
'team_in_possession_length_end',
'team_out_of_possession_width_start',
'team_out_of_possession_width_end',
'team_out_of_possession_length_start',
'team_out_of_possession_length_end'


#### Events 

Events file have all these fields :

['event_id',
 'index',
 'match_id',
 'frame_start',
 'frame_end',
 'frame_physical_start',
 'time_start',
 'time_end',
 'minute_start',
 'second_start',
 'duration',
 'period',
 'attacking_side_id',
 'attacking_side',
 'event_type_id',
 'event_type',
 'event_subtype_id',
 'event_subtype',
 'player_id',
 'player_name',
 'player_position_id',
 'player_position',
 'player_in_possession_id',
 'player_in_possession_name',
 'player_in_possession_position_id',
 'player_in_possession_position',
 'team_id',
 'team_shortname',
 'x_start',
 'y_start',
 'channel_id_start',
 'channel_start',
 'third_id_start',
 'third_start',
 'penalty_area_start',
 'x_end',
 'y_end',
 'channel_id_end',
 'channel_end',
 'third_id_end',
 'third_end',
 'penalty_area_end',
 'associated_player_possession_event_id',
 'associated_player_possession_frame_start',
 'associated_player_possession_frame_end',
 'associated_player_possession_end_type_id',
 'associated_player_possession_end_type',
 'associated_off_ball_run_event_id',
 'associated_off_ball_run_subtype_id',
 'associated_off_ball_run_subtype',
 'game_state_id',
 'game_state',
 'team_score',
 'opponent_team_score',
 'phase_index',
 'player_possession_phase_index',
 'first_player_possession_in_team_possession',
 'last_player_possession_in_team_possession',
 'lead_to_different_phase',
 'issued_from_different_phase',
 'n_player_possessions_in_phase',
 'team_possession_loss_in_phase',
 'team_in_possession_phase_type_id',
 'team_in_possession_phase_type',
 'team_out_of_possession_phase_type_id',
 'team_out_of_possession_phase_type',
 'current_team_in_possession_next_phase_type_id',
 'current_team_in_possession_next_phase_type',
 'current_team_out_of_possession_next_phase_type_id',
 'current_team_out_of_possession_next_phase_type',
 'current_team_in_possession_previous_phase_type_id',
 'current_team_in_possession_previous_phase_type',
 'current_team_out_of_possession_previous_phase_type_id',
 'current_team_out_of_possession_previous_phase_type',
 'game_interruption_before_id',
 'game_interruption_before',
 'game_interruption_after_id',
 'game_interruption_after',
 'lead_to_shot',
 'lead_to_goal',
 'distance_covered',
 'trajectory_angle',
 'trajectory_direction_id',
 'trajectory_direction',
 'in_to_out',
 'out_to_in',
 'speed_avg',
 'speed_avg_band_id',
 'speed_avg_band',
 'separation_start',
 'separation_end',
 'separation_gain',
 'last_defensive_line_x_start',
 'last_defensive_line_x_end',
 'delta_to_last_defensive_line_start',
 'delta_to_last_defensive_line_end',
 'delta_to_last_defensive_line_gain',
 'last_defensive_line_height_start',
 'last_defensive_line_height_end',
 'last_defensive_line_height_gain',
 'inside_defensive_shape_start',
 'inside_defensive_shape_end',
 'start_type_id',
 'start_type',
 'end_type_id',
 'end_type',
 'consecutive_on_ball_engagements',
 'one_touch',
 'quick_pass',
 'carry',
 'forward_momentum',
 'is_header',
 'hand_pass',
 'initiate_give_and_go',
 'pass_angle_received',
 'pass_direction_received_id',
 'pass_direction_received',
 'pass_distance_received',
 'pass_range_received_id',
 'pass_range_received',
 'pass_outcome_id',
 'pass_outcome',
 'targeted_passing_option_event_id',
 'high_pass',
 'player_targeted_id',
 'player_targeted_name',
 'player_targeted_position_id',
 'player_targeted_position',
 'player_targeted_x_pass',
 'player_targeted_y_pass',
 'player_targeted_channel_pass_id',
 'player_targeted_channel_pass',
 'player_targeted_third_pass_id',
 'player_targeted_third_pass',
 'player_targeted_penalty_area_pass',
 'player_targeted_x_reception',
 'player_targeted_y_reception',
 'player_targeted_channel_reception_id',
 'player_targeted_channel_reception',
 'player_targeted_third_reception_id',
 'player_targeted_third_reception',
 'player_targeted_penalty_area_reception',
 'player_targeted_distance_to_goal_start',
 'player_targeted_distance_to_goal_end',
 'player_targeted_angle_to_goal_start',
 'player_targeted_angle_to_goal_end',
 'player_targeted_average_speed',
 'player_targeted_speed_avg_band_id',
 'player_targeted_speed_avg_band',
 'speed_difference',
 'player_targeted_xpass_completion',
 'player_targeted_difficult_pass_target',
 'player_targeted_xthreat',
 'player_targeted_dangerous',
 'n_passing_options',
 'n_off_ball_runs',
 'n_passing_options_line_break',
 'n_passing_options_first_line_break',
 'n_passing_options_second_last_line_break',
 'n_passing_options_last_line_break',
 'n_passing_options_ahead',
 'n_passing_options_dangerous_difficult',
 'n_passing_options_dangerous_not_difficult',
 'n_passing_options_not_dangerous_not_difficult',
 'n_passing_options_not_dangerous_difficult',
 'n_passing_options_at_start',
 'n_passing_options_at_end',
 'n_passing_options_ahead_at_start',
 'n_passing_options_ahead_at_end',
 'n_teammates_ahead_end',
 'n_teammates_ahead_start',
 'n_player_targeted_opponents_ahead_start',
 'n_player_targeted_opponents_ahead_end',
 'n_player_targeted_teammates_ahead_start',
 'n_player_targeted_teammates_ahead_end',
 'n_player_targeted_teammates_within_5m_start',
 'n_player_targeted_teammates_within_5m_end',
 'n_player_targeted_opponents_within_5m_start',
 'n_player_targeted_opponents_within_5m_end',
 'organised_defense',
 'defensive_structure',
 'n_defensive_lines',
 'first_line_break',
 'first_line_break_type_id',
 'first_line_break_type',
 'second_last_line_break',
 'second_last_line_break_type_id',
 'second_last_line_break_type',
 'last_line_break',
 'last_line_break_type_id',
 'last_line_break_type',
 'furthest_line_break_id',
 'furthest_line_break',
 'furthest_line_break_type_id',
 'furthest_line_break_type',
 'interplayer_distance',
 'interplayer_distance_range_id',
 'interplayer_distance_range',
 'interplayer_distance_start',
 'interplayer_distance_end',
 'interplayer_distance_min',
 'interplayer_distance_start_physical',
 'close_at_player_possession_start',
 'interplayer_angle',
 'interplayer_direction_id',
 'interplayer_direction',
 'angle_of_engagement',
 'goal_side_start',
 'goal_side_end',
 'pass_distance',
 'pass_range_id',
 'pass_range',
 'pass_angle',
 'pass_direction_id',
 'pass_direction',
 'pass_ahead',
 'n_opponents_ahead_player_in_possession_pass_moment',
 'n_opponents_ahead_pass_reception',
 'n_opponents_bypassed',
 'location_to_player_in_possession_id_start',
 'location_to_player_in_possession_start',
 'location_to_player_in_possession_id_end',
 'location_to_player_in_possession_end',
 'distance_to_player_in_possession_start',
 'distance_to_player_in_possession_end',
 'player_in_possession_x_start',
 'player_in_possession_y_start',
 'player_in_possession_channel_id_start',
 'player_in_possession_channel_start',
 'player_in_possession_third_id_start',
 'player_in_possession_third_start',
 'player_in_possession_penalty_area_start',
 'player_in_possession_x_end',
 'player_in_possession_y_end',
 'player_in_possession_channel_id_end',
 'player_in_possession_channel_end',
 'player_in_possession_third_id_end',
 'player_in_possession_third_end',
 'player_in_possession_penalty_area_end',
 'targeted',
 'received',
 'received_in_space',
 'dangerous',
 'difficult_pass_target',
 'xthreat',
 'xpass_completion',
 'passing_option_score',
 'predicted_passing_option',
 'peak_passing_option_frame',
 'passing_option_at_player_possession_start',
 'n_simultaneous_runs',
 'give_and_go',
 'intended_run_behind',
 'push_defensive_line',
 'break_defensive_line',
 'passing_option_at_start',
 'n_simultaneous_passing_options',
 'passing_option_at_pass_moment',
 'n_opponents_ahead_end',
 'n_opponents_ahead_start',
 'n_opponents_overtaken',
 'pressing_chain',
 'pressing_chain_length',
 'pressing_chain_end_type_id',
 'pressing_chain_end_type',
 'pressing_chain_index',
 'index_in_pressing_chain',
 'simultaneous_defensive_engagement_same_target',
 'simultaneous_defensive_engagement_same_target_rank',
 'affected_line_breaking_passing_option_id',
 'affected_line_break_id',
 'affected_line_break',
 'affected_line_breaking_passing_option_attempted',
 'affected_line_breaking_passing_option_xthreat',
 'affected_line_breaking_passing_option_dangerous',
 'affected_line_breaking_passing_option_run_subtype_id',
 'affected_line_breaking_passing_option_run_subtype',
 'possession_danger',
 'beaten_by_possession',
 'beaten_by_movement',
 'stop_possession_danger',
 'reduce_possession_danger',
 'force_backward',
 'xloss_player_possession_start',
 'xloss_player_possession_end',
 'xloss_player_possession_max',
 'xshot_player_possession_start',
 'xshot_player_possession_end',
 'xshot_player_possession_max',
 'is_player_possession_start_matched',
 'is_player_possession_end_matched',
 'is_previous_pass_matched',
 'is_pass_reception_matched',
 'fully_extrapolated']

 #### enriched_data_tracking 

 Fields:
    'x',
    'y',
    'player_id',
    'is_detected',
    'frame',
    'timestamp',
    'period',
    'possession_player_id',
    'possession_group',
    'ball_x',
    'ball_y',
    'ball_z',
    'is_detected_ball',
    'match_id',
    'start_time',
    'end_time',
    'match_name',
    'date_time',
    'home_team.name',
    'away_team.name',
    'home_away_player',
    'id',
    'short_name',
    'number',
    'team_id',
    'team_name',
    'player_role.position_group',
    'total_time',
    'player_role.name',
    'player_role.acronym',
    'is_gk',
    'direction_player_1st_half',
    'direction_player_2nd_half'



Report Dashboard Layout
python# Step 3: Report Dashboard
st.header("📊 Match Analysis Report")

# Executive Summary
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Possession", "58%", "+3%")
    with col2:
        st.metric("Shots", "14", "+5")
    with col3:
        st.metric("xG", "1.8", "+0.4")
    with col4:
        st.metric("Pressing Success", "62%", "+8%")

# Collapsible Sections
sections = {
    "Team Identity & Setup": section_1_content,
    "Possession & Build-Up": section_2_content,
    # ... all 14 sections
}

for section_name, content_func in sections.items():
    with st.expander(f"📌 {section_name}"):
        content_func()
Chat Interface
python# Step 4: Chat Interface
st.header("💬 Chat with Your Match Data")

# Quick questions
st.subheader("💡 Quick Questions")
cols = st.columns(3)
for i, (question, template) in enumerate(QUICK_QUESTIONS.items()):
    with cols[i % 3]:
        if st.button(question, key=f"quick_{i}"):
            process_quick_question(template)

# Chat history
for message in st.session_state.chat_history:
    if message['role'] == 'user':
        st.chat_message("user").write(message['content'])
    else:
        with st.chat_message("assistant"):
            st.write(message['text'])
            
            # Display metrics
            if 'metrics' in message:
                cols = st.columns(len(message['metrics']))
                for i, (metric, value) in enumerate(message['metrics'].items()):
                    cols[i].metric(metric, value)
            
            # Display video clips
            if 'video_clips' in message:
                st.subheader("🎬 Key Moments")
                for i, clip in enumerate(message['video_clips']):
                    st.video(clip['path'])
                    st.caption(f"{clip['title']} - {clip['description']}")

# Input
user_input = st.chat_input("Ask anything about the match...")
if user_input:
    # Process query...

## PROJECT STRUCTURE
```

Put all the analytics processing into one folder. 

│   │
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── metrics/
│   │   │   ├── __init__.py
│   │   │   ├── team_identity.py
│   │   │   ├── possession.py
│   │   │   ├── chance_creation.py
│   │   │   ├── defense.py
│   │   │   ├── transitions.py
│   │   │   ├── intelligence.py
│   │   │   ├── players.py
│   │   │   ├── chemistry.py
│   │   │   ├── efficiency.py
│   │   │   ├── set_pieces.py
│   │   │   ├── momentum.py
│   │   │   ├── consistency.py
│   │   │   ├── training.py
│   │   │   └── opponent.py
│   │   ├── framework.py
│   │   └── insights.py
│   │
│   ├── video/
│   │   ├── __init__.py
│   │   ├── clip_generator.py
│   │   ├── annotator.py
│   │   └── renderer.py
│   │
│   ├── chat/
│   │   ├── __init__.py
│   │   ├── query_processor.py
│   │   ├── template_matcher.py
│   │   ├── llm_interface.py
│   │   └── response_generator.py
│   │
│   ├── report/
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   ├── pdf_export.py
│   │   └── html_export.py
│   │
│   └── ui/
│       ├── __init__.py
│       ├── components.py
│       ├── upload_page.py
│       ├── analysis_page.py
│       ├── report_page.py
│       └── chat_page.py
│
├── clips/                         # Generated videos
│   └── match_{id}/
│
└── outputs/                       # Exported reports
    ├── pdfs/
    ├── html/
    └── pptx/
```

Phase 2: Metrics Engine 
- [ ] Implement all section metrics
- [ ] Parallel computation
- [ ] Progress tracking
- [ ] Cache system

Phase 3: Report Dashboard 
- [ ] collapsible sections
- [ ] Interactive charts
- [ ] Metric cards
- [ ] Export functionality

### Phase 4: Video System 
- [ ] Frame-based clip extraction
- [ ] mplsoccer annotations
- [ ] ffmpeg rendering
- [ ] Video player component

Performance

Use DuckDB for analytical queries (10x faster than pandas)
Cache expensive computations
Parallelize independent metric calculations
Lazy-load video generation (only on demand)

Video Generation

Pre-generate clips for report (top 15 moments)
Generate chat clips on-demand
Cache generated clips (reuse if same frames requested)
