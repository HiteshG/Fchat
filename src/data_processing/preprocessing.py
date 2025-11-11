"""
Data preprocessing module for SkillCorner dataset
Creates enriched tracking data by merging tracking data with player metadata
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, Any, Optional


def time_to_seconds(time_str: Optional[str]) -> float:
    """
    Convert time string (HH:MM:SS) to seconds

    Args:
        time_str: Time string in format HH:MM:SS

    Returns:
        Time in seconds
    """
    if time_str is None:
        return 90 * 60  # 90 minutes = 5400 seconds
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s


def process_tracking_data(tracking_file_path: str, match_id: str) -> pd.DataFrame:
    """
    Process tracking data from JSONL file

    Args:
        tracking_file_path: Path to tracking JSONL file
        match_id: Match identifier

    Returns:
        Processed tracking dataframe
    """
    # Read tracking data (multi-line JSON file)
    raw_data = pd.read_json(tracking_file_path, lines=True)

    # Normalize JSON structure
    raw_df = pd.json_normalize(
        raw_data.to_dict("records"),
        "player_data",
        ["frame", "timestamp", "period", "possession", "ball_data"],
    )

    # Extract 'player_id' and 'group' from the 'possession' dictionary
    raw_df["possession_player_id"] = raw_df["possession"].apply(
        lambda x: x.get("player_id") if isinstance(x, dict) else None
    )
    raw_df["possession_group"] = raw_df["possession"].apply(
        lambda x: x.get("group") if isinstance(x, dict) else None
    )

    # Expand the ball_data with json_normalize
    raw_df[["ball_x", "ball_y", "ball_z", "is_detected_ball"]] = pd.json_normalize(
        raw_df.ball_data
    )

    # Drop the original 'possession' and 'ball_data' columns
    raw_df = raw_df.drop(columns=["possession", "ball_data"])

    # Add the match_id identifier
    raw_df["match_id"] = match_id

    return raw_df


def process_metadata(metadata_file_path: str) -> pd.DataFrame:
    """
    Process metadata JSON file and extract player information

    Args:
        metadata_file_path: Path to metadata JSON file

    Returns:
        Processed players dataframe
    """
    # Reading metadata file
    with open(metadata_file_path, "r") as f:
        raw_match_data = json.load(f)

    # The output has nested json elements. We process them
    raw_match_df = pd.json_normalize(raw_match_data, max_level=2)
    raw_match_df["home_team_side"] = raw_match_df["home_team_side"].astype(str)

    # Extract players information
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
        ],
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

    # Add match name
    players_df["match_name"] = (
        players_df["home_team.name"] + " vs " + players_df["away_team.name"]
    )

    # Add a flag if the given player is home or away
    players_df["home_away_player"] = np.where(
        players_df.team_id == players_df["home_team.id"], "Home", "Away"
    )

    # Create team name flag
    players_df["team_name"] = np.where(
        players_df.team_id == players_df["home_team.id"],
        players_df["home_team.name"],
        players_df["away_team.name"],
    )

    # Figure out sides for each half
    players_df[["home_team_side_1st_half", "home_team_side_2nd_half"]] = (
        players_df["home_team_side"]
        .astype(str)
        .str.strip("[]")
        .str.replace("'", "")
        .str.split(", ", expand=True)
    )

    # Clean up sides - direction player is attacking in each half
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

    # Keep only relevant columns
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

    return players_df


def create_enriched_tracking_data(
    tracking_file_path: str,
    metadata_file_path: str,
    match_id: str
) -> pd.DataFrame:
    """
    Create enriched tracking data by merging tracking data with player metadata

    Args:
        tracking_file_path: Path to tracking JSONL file
        metadata_file_path: Path to metadata JSON file
        match_id: Match identifier

    Returns:
        Enriched tracking dataframe
    """
    # Process tracking data
    tracking_df = process_tracking_data(tracking_file_path, match_id)

    # Process metadata
    players_df = process_metadata(metadata_file_path)

    # Merge tracking data with player metadata
    enriched_tracking_data = tracking_df.merge(
        players_df, left_on=["player_id"], right_on=["id"]
    )

    return enriched_tracking_data


def get_enriched_data_info(enriched_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get information about the enriched tracking data

    Args:
        enriched_df: Enriched tracking dataframe

    Returns:
        Dictionary with dataset information
    """
    info = {
        "total_rows": len(enriched_df),
        "total_columns": len(enriched_df.columns),
        "column_names": enriched_df.columns.tolist(),
        "match_id": enriched_df["match_id"].iloc[0] if len(enriched_df) > 0 else None,
        "match_name": enriched_df["match_name"].iloc[0] if len(enriched_df) > 0 else None,
        "unique_players": enriched_df["player_id"].nunique(),
        "unique_frames": enriched_df["frame"].nunique(),
        "periods": sorted(enriched_df["period"].unique().tolist()),
        "data_types": enriched_df.dtypes.to_dict(),
    }

    return info
