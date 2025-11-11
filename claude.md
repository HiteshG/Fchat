Football Tactical Intelligence Platform - Part 1 Specification

Version: 1.0
Last Updated: 2025
Purpose: Blueprint for building an AI-powered football match analysis system with Streamlit

## Table Content
Application Overview
Architecture Diagram
Data Schemas 
Data Processing Pipeline

APPLICATION OVERVIEW
Goal: Build a Streamlit application where coaches and analysts can:
Upload SkillCorner match data (4 files: metadata, tracking, events, phases)

#### Metdata file
Metadata file have following fields :
critical fields: "id", "date_time", "competition_edition.competition.name", "players", "pitch_legth", "pitch_width"

"players" array is a structured snapshot of all players participating in a specific football match, capturing:
Who they are — identity, name, team, gender, etc.
What position they play — tactical role like “Center Forward (CF)” or “Right Back (RB)”.
How long they played — total minutes, when they entered/left, time per half.
What they did (summary) — goals, cards, injuries, etc.
Tracking references — linking them to tracking data objects (so their on-field x/y coordinates can be mapped).

Sample file with all the fields :
{"id":1886347,"home_team_score":2,"away_team_score":0,"date_time":"2024-11-30T04:00:00Z","stadium":{"id":3811,"name":"Mount Smart Stadium","city":"Auckland","capacity":25000},"home_team":{"id":4177,"name":"Auckland FC","short_name":"Auckland FC","acronym":"AUC"},"home_team_kit":{"id":14025,"team_id":4177,"season":{"id":95,"start_year":2024,"end_year":2025,"name":"2024/2025"},"name":"Home","jersey_color":"#2800f0","number_color":"#ffffff"},"away_team":{"id":1805,"name":"Newcastle United Jets FC","short_name":"Newcastle","acronym":"NEW"},"away_team_kit":{"id":10376,"team_id":1805,"season":{"id":29,"start_year":2024,"end_year":2024,"name":"2024"},"name":"away","jersey_color":"#ffffff","number_color":"#000000"},"home_team_coach":null,"away_team_coach":null,"home_team_playing_time":{"minutes_tip":31.13,"minutes_otip":22.2},"away_team_playing_time":{"minutes_tip":22.2,"minutes_otip":31.13},"competition_edition":{"id":870,"competition":{"id":61,"area":"AUS","name":"A-League","gender":"male","age_group":"adult"},"season":{"id":95,"start_year":2024,"end_year":2025,"name":"2024/2025"},"name":"AUS - A-League - 2024/2025"},"match_periods":[{"period":1,"name":"period_1","start_frame":10,"end_frame":27790,"duration_frames":27780,"duration_minutes":46.3},{"period":2,"name":"period_2","start_frame":27800,"end_frame":59060,"duration_frames":31260,"duration_minutes":52.1}],"competition_round":{"id":611,"name":"Round 6","round_number":6,"potential_overtime":false},"referees":[],"players":[{"player_role":{"id":15,"position_group":"Center Forward","name":"Center Forward","acronym":"CF"},"start_time":"00:00:00","end_time":"01:25:21","number":10,"yellow_card":0,"red_card":0,"injured":false,"goal":0,"own_goal":0,"playing_time":{"total":{"minutes_tip":29.55,"minutes_otip":18.76,"start_frame":10,"end_frame":52009,"minutes_played":86.65,"minutes_played_regular_time":86.65},"by_period":[{"name":"period_1","minutes_tip":18.21,"minutes_otip":11.03,"start_frame":10,"end_frame":27790,"minutes_played":46.3},{"name":"period_2","minutes_tip":11.34,"minutes_otip":7.73,"start_frame":27800,"end_frame":52009,"minutes_played":40.35}]},"team_player_id":1507965,"team_id":4177,"id":38673,"first_name":"Guillermo Luis","last_name":"May Bartesaghi","short_name":"G. May","birthday":"1998-03-11","trackable_object":39794,"gender":"male"}],"status":"closed","home_team_side":["right_to_left","left_to_right"],"ball":{"trackable_object":55},"pitch_length":104,"pitch_width":68}

#### Tracking file
Tracking file is multi-line json file. 

Tracking file have following fields :
critical fields: "frame", "timestamp", "period", "ball_data", "player_data"

Tracking data represents:
Where every player is (x, y coordinates)
Where the ball is (x, y, z)

"player_data" array
Each object here represents one player’s position at this exact timestamp:
x, y: player coordinates on the pitch (in meters).
player_id: links to the "players" dataset you shared earlier (so you know who this is).
is_detected: whether tracking successfully identified them in this frame (false = missing or occluded).
So in this frame, all 22 players have their approximate locations, with a few not detected (maybe behind others or off-camera).

Sample of tracking data:
{"frame": 11, "timestamp": "00:00:00.10", "period": 1, "ball_data": {"x": 0.54, "y": 0.08, "z": 0.22, "is_detected": true}, "possession": {"player_id": null, "group": null}, "image_corners_projection": {"x_top_left": -52.37, "y_top_left": 39.0, "x_bottom_left": -23.18, "y_bottom_left": -36.89, "x_bottom_right": 22.69, "y_bottom_right": -36.7, "x_top_right": 50.74, "y_top_right": 39.0}, "player_data": [{"x": -39.86, "y": -0.13, "player_id": 51009, "is_detected": false}, {"x": -19.23, "y": -9.23, "player_id": 176224, "is_detected": true}, {"x": -21.82, "y": 0.43, "player_id": 51649, "is_detected": true}, {"x": -1.14, "y": -32.57, "player_id": 50983, "is_detected": true}, {"x": -18.98, "y": 15.73, "player_id": 735578, "is_detected": true}, {"x": -7.37, "y": 7.13, "player_id": 50978, "is_detected": true}, {"x": -9.48, "y": -5.08, "player_id": 735574, "is_detected": true}, {"x": -2.29, "y": 7.33, "player_id": 795507, "is_detected": false}, {"x": -0.84, "y": -20.66, "player_id": 795505, "is_detected": true}, {"x": -1.82, "y": 18.78, "player_id": 735573, "is_detected": true}, {"x": 1.24, "y": 0.74, "player_id": 966120, "is_detected": true}, {"x": 40.65, "y": 0.24, "player_id": 285188, "is_detected": false}, {"x": 17.92, "y": 5.42, "player_id": 51667, "is_detected": true}, {"x": 16.81, "y": -3.7, "player_id": 33697, "is_detected": true}, {"x": 17.09, "y": 14.62, "player_id": 51713, "is_detected": true}, {"x": 17.57, "y": -13.63, "player_id": 133498, "is_detected": true}, {"x": 11.58, "y": 6.69, "player_id": 14736, "is_detected": true}, {"x": 10.13, "y": -2.22, "player_id": 23418, "is_detected": true}, {"x": 0.98, "y": 18.84, "player_id": 133501, "is_detected": false}, {"x": 7.78, "y": -16.35, "player_id": 965685, "is_detected": true}, {"x": 0.44, "y": -8.39, "player_id": 50951, "is_detected": true}, {"x": 2.61, "y": 9.91, "player_id": 38673, "is_detected": true}]}
{"frame": 12, "timestamp": "00:00:00.20", "period": 1, "ball_data": {"x": 0.57, "y": -0.07, "z": 0.19, "is_detected": true}, "possession": {"player_id": null, "group": null}, "image_corners_projection": {"x_top_left": -52.11, "y_top_left": 39.0, "x_bottom_left": -23.09, "y_bottom_left": -36.74, "x_bottom_right": 22.58, "y_bottom_right": -36.58, "x_top_right": 50.48, "y_top_right": 39.0}, "player_data": [{"x": -40.06, "y": -0.18, "player_id": 51009, "is_detected": false}, {"x": -19.24, "y": -9.27, "player_id": 176224, "is_detected": true}, {"x": -21.81, "y": 0.4, "player_id": 51649, "is_detected": true}, {"x": -1.13, "y": -32.66, "player_id": 50983, "is_detected": true}, {"x": -19.07, "y": 15.73, "player_id": 735578, "is_detected": true}, {"x": -7.32, "y": 7.14, "player_id": 50978, "is_detected": true}, {"x": -9.46, "y": -5.15, "player_id": 735574, "is_detected": true}, {"x": -2.09, "y": 7.39, "player_id": 795507, "is_detected": false}, {"x": -0.9, "y": -20.64, "player_id": 795505, "is_detected": true}, {"x": -1.8, "y": 18.77, "player_id": 735573, "is_detected": true}, {"x": 1.22, "y": 0.61, "player_id": 966120, "is_detected": true}, {"x": 40.83, "y": 0.24, "player_id": 285188, "is_detected": false}, {"x": 17.98, "y": 5.34, "player_id": 51667, "is_detected": true}, {"x": 16.83, "y": -3.72, "player_id": 33697, "is_detected": true}, {"x": 17.13, "y": 14.55, "player_id": 51713, "is_detected": true}, {"x": 17.59, "y": -13.66, "player_id": 133498, "is_detected": true}, {"x": 11.46, "y": 6.66, "player_id": 14736, "is_detected": true}, {"x": 10.09, "y": -2.31, "player_id": 23418, "is_detected": true}, {"x": 1.05, "y": 18.74, "player_id": 133501, "is_detected": false}, {"x": 7.8, "y": -16.43, "player_id": 965685, "is_detected": true}, {"x": 0.48, "y": -8.49, "player_id": 50951, "is_detected": true}, {"x": 2.56, "y": 9.87, "player_id": 38673, "is_detected": true}]}
{"frame": 13, "timestamp": "00:00:00.30", "period": 1, "ball_data": {"x": 0.56, "y": -0.07, "z": 0.14, "is_detected": true}, "possession": {"player_id": null, "group": null}, "image_corners_projection": {"x_top_left": -52.02, "y_top_left": 39.0, "x_bottom_left": -23.09, "y_bottom_left": -36.67, "x_bottom_right": 22.54, "y_bottom_right": -36.51, "x_top_right": 50.28, "y_top_right": 39.0}, "player_data": [{"x": -40.24, "y": -0.22, "player_id": 51009, "is_detected": false}, {"x": -19.25, "y": -9.31, "player_id": 176224, "is_detected": true}, {"x": -21.8, "y": 0.36, "player_id": 51649, "is_detected": true}, {"x": -1.12, "y": -32.74, "player_id": 50983, "is_detected": true}, {"x": -19.16, "y": 15.73, "player_id": 735578, "is_detected": true}, {"x": -7.28, "y": 7.14, "player_id": 50978, "is_detected": true}, {"x": -9.45, "y": -5.2, "player_id": 735574, "is_detected": true}, {"x": -1.91, "y": 7.45, "player_id": 795507, "is_detected": false}, {"x": -0.95, "y": -20.62, "player_id": 795505, "is_detected": true}, {"x": -1.76, "y": 18.76, "player_id": 735573, "is_detected": true}, {"x": 1.19, "y": 0.51, "player_id": 966120, "is_detected": true}, {"x": 40.98, "y": 0.24, "player_id": 285188, "is_detected": false}, {"x": 18.04, "y": 5.26, "player_id": 51667, "is_detected": true}, {"x": 16.86, "y": -3.73, "player_id": 33697, "is_detected": true}, {"x": 17.17, "y": 14.48, "player_id": 51713, "is_detected": true}, {"x": 17.6, "y": -13.68, "player_id": 133498, "is_detected": true}, {"x": 11.34, "y": 6.63, "player_id": 14736, "is_detected": true}, {"x": 10.06, "y": -2.39, "player_id": 23418, "is_detected": true}, {"x": 1.11, "y": 18.63, "player_id": 133501, "is_detected": false}, {"x": 7.83, "y": -16.51, "player_id": 965685, "is_detected": true}, {"x": 0.51, "y": -8.57, "player_id": 50951, "is_detected": true}, {"x": 2.5, "y": 9.83, "player_id": 38673, "is_detected": true}]}


Now using tracking data and metadata, we have to create new dataframe called "enrich_tracking_data":
Following code - 

def time_to_seconds(time_str):
    if time_str is None:
        return 90 * 60  # 120 minutes = 7200 seconds
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

# Read tracking data 
raw_data = pd.read_json(
    f"{tracking_data_file_path}.jsonl", lines=True
)

raw_df = pd.json_normalize(
    raw_data.to_dict("records"),
    "player_data",
    ["frame", "timestamp", "period", "possession", "ball_data"],
)

# Extract 'player_id' and 'group from the 'possession' dictionary
raw_df["possession_player_id"] = raw_df["possession"].apply(
    lambda x: x.get("player_id")
)
raw_df["possession_group"] = raw_df["possession"].apply(lambda x: x.get("group"))


# (Optional) Expand the ball_data with json_normalize
raw_df[["ball_x", "ball_y", "ball_z", "is_detected_ball"]] = pd.json_normalize(
    raw_df.ball_data
)

# (Optional) Drop the original 'possession' column if you no longer need it
raw_df = raw_df.drop(columns=["possession", "ball_data"])

# Add the match_id identifier to your dataframe
raw_df["match_id"] = match_id
tracking_df = raw_df.copy()

# Reading metadata file 
file_path = f"{metadata_file_path}.json"

with open(file_path, "r") as f:
    raw_match_data = json.load(f)

# The output has nested json elements. We process them
raw_match_df = pd.json_normalize(raw_match_data, max_level=2)
raw_match_df["home_team_side"] = raw_match_df["home_team_side"].astype(str)

players_df = pd.json_normalize(
    raw_match_df.to_dict("records"),
    record_path="players",
    meta=[
        "home_team_score",
        "away_team_score",
        "date_time",
        "home_team_side",
        "home_team.name",
        "home_team.id",
        "away_team.name",
        "away_team.id",
    ],  # data we keep
)


# Take only players who played and create their total time
players_df = players_df[
    ~((players_df.start_time.isna()) & (players_df.end_time.isna()))
]
players_df["total_time"] = players_df["end_time"].apply(time_to_seconds) - players_df[
    "start_time"
].apply(time_to_seconds)

# Create a flag for GK
players_df["is_gk"] = players_df["player_role.acronym"] == "GK"

# Add a flag if the given player is home or away
players_df["match_name"] = (
    players_df["home_team.name"] + " vs " + players_df["away_team.name"]
)


# Add a flag if the given player is home or away
players_df["home_away_player"] = np.where(
    players_df.team_id == players_df["home_team.id"], "Home", "Away"
)

# Create flag from player
players_df["team_name"] = np.where(
    players_df.team_id == players_df["home_team.id"],
    players_df["home_team.name"],
    players_df["away_team.name"],
)

# Figure out sides
players_df[["home_team_side_1st_half", "home_team_side_2nd_half"]] = (
    players_df["home_team_side"]
    .astype(str)
    .str.strip("[]")
    .str.replace("'", "")
    .str.split(", ", expand=True)
)
# Clean up sides
players_df["direction_player_1st_half"] = np.where(
    players_df.home_away_player == "Home",
    players_df.home_team_side_1st_half,
    players_df.home_team_side_2nd_half,
)
players_df["direction_player_2nd_half"] = np.where(
    players_df.home_away_player == "Home",
    players_df.home_team_side_2nd_half,
    players_df.home_team_side_1st_half,
)

# Clean up and keep the columns that we want to keep about

columns_to_keep = [
    "start_time",
    "end_time",
    "match_name",
    "date_time",
    "home_team.name",
    "away_team.name",
    "id",
    "short_name",
    "number",
    "team_id",
    "team_name",
    "player_role.position_group",
    "total_time",
    "player_role.name",
    "player_role.acronym",
    "is_gk",
    "direction_player_1st_half",
    "direction_player_2nd_half",
]
players_df = players_df[columns_to_keep]

enriched_tracking_data = tracking_df.merge(
    players_df, left_on=["player_id"], right_on=["id"]
)

Finally show the option to view this enriched_tracking_data to user. By clicking view data.


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


### UI/UX SPECIFICATIONS
Color Scheme
pythonCOLORS = {
    "primary":   "#00A85D",   # a vivid green (inspired by their green icon variant)
    "secondary": "#1D73E8",   # a bold blue (matching their blue-accent graphics)
    "accent":     "#00D8B0",   # teal/bright green-blue for highlights
    "success":    "#4CAF50",   # your same green success colour (works well)
    "warning":    "#FFB300",   # amber for warnings
    "danger":     "#D32F2F",   # deep red for errors/danger
    "neutral":    "#6E6E6E",   # mid-grey for neutral/text secondary
    "background": "#FFFFFF",   # white background for clean UI
    "text":       "#212121"    # dark text
}

SEVERITY_COLORS = {
    "HIGH": COLORS["danger"],
    "MEDIUM": COLORS["warning"],
    "LOW": COLORS["success"]
}
Streamlit Layout
python# Step 1: Upload Page
st.title("⚽ Football Tactical Intelligence Platform")
st.header("📂 Step 1: Upload Match Data")

col1, col2 = st.columns(2)
with col1:
    metadata_file = st.file_uploader("Match Metadata (JSON)", type=['json'])
    tracking_file = st.file_uploader("Tracking Data (CSV/JSONL)", type=['csv', 'jsonl'])

with col2:
    events_file = st.file_uploader("Dynamic Events (CSV)", type=['csv'])
    phases_file = st.file_uploader("Phase of Play (CSV)", type=['csv'])

if all([metadata_file, tracking_file, events_file, phases_file]):
    st.success("✅ All files uploaded!")
    if st.button("🔍 Process", type="primary"):
        # Trigger processing...

Progress Bar Animation
python# Step 2: Analysis Progress
progress_stages = [
    (10, "Computing basic statistics..."),
    (20, "Analyzing formations and shape..."),
    (40, "Calculating possession metrics..."),
    (60, "Processing defensive actions..."),
    (80, "Generating tactical insights..."),
    (100, "Analysis complete!")
]

progress_bar = st.progress(0)
status_text = st.empty()

for progress, message in progress_stages:
    progress_bar.progress(progress)
    status_text.text(f"⚙️ {message}")
    time.sleep(0.5)  # Replace with actual computation
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

TECHNICAL STACK
Requirements.txt
txt# Core
streamlit>=1.30.0
pandas>=2.0.0
numpy>=1.24.0

# Database
duckdb>=0.9.0

# Visualization
plotly>=5.17.0
mplsoccer>=1.3.0
matplotlib>=3.7.0

# Video
opencv-python>=4.8.0
ffmpeg-python>=0.2.0

# LLM
anthropic>=0.18.0

# Analytics
scikit-learn>=1.3.0
scipy>=1.11.0

# Utilities
python-dotenv>=1.0.0
```

---

## PROJECT STRUCTURE
```
football-intelligence-platform/
├── app.py                          # Main Streamlit app
├── requirements.txt
├── README.md
├── .env                            # API keys
│
├── config/
│   ├── metric_templates.json      # Pre-defined templates
│   ├── question_templates.json    # Chat quick questions
│   └── ui_config.yaml             # UI settings
│
├── data/
│   ├── uploads/                   # User uploads
│   ├── processed/                 # Standardized data
│   └── cache/                     # Computed metrics
│
├── src/
│   ├── __init__.py
│   │
│   ├── data_processing/
│   │   ├── __init__.py
│   │   ├── ingestion.py
│   │   ├── preprocessing.py
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


## QUICK START GUIDE

### For Claude Code

**First Prompt:**
```
I want to build a football tactical intelligence platform using Streamlit.

Complete specification is in this file: [attach claude.md]

Let's start with Phase 1: Core Data Pipeline.

Create:
1. Project structure (all folders)
2. requirements.txt
3. Basic Streamlit app with file upload interface
4. Data uploading module with pre-processing steps

Use the schemas from the spec. Show me the upload UI first.

Performance

Use DuckDB for analytical queries (10x faster than pandas)
Cache expensive computations
Parallelize independent metric calculations
Lazy-load video generation (only on demand)

Video Generation

Pre-generate clips for report (top 15 moments)
Generate chat clips on-demand
Cache generated clips (reuse if same frames requested)
