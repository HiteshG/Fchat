"""
Knowledge Bank Generator for SkillCorner Dataset
Generates comprehensive field documentation for downstream tasks
"""

import pandas as pd
import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class KnowledgeBank:
    """
    Knowledge Bank for documenting dataset fields and their properties
    """

    def __init__(self):
        self.metadata_fields = {}
        self.tracking_fields = {}
        self.events_fields = {}
        self.phases_fields = {}
        self.enriched_tracking_fields = {}
        self.created_at = datetime.now().isoformat()

    def analyze_metadata(self, metadata_file_path: str) -> Dict[str, Any]:
        """
        Analyze metadata file and extract field information

        Args:
            metadata_file_path: Path to metadata JSON file

        Returns:
            Dictionary with metadata field information
        """
        with open(metadata_file_path, "r") as f:
            data = json.load(f)

        # Critical fields as per specification
        critical_fields = [
            "id",
            "date_time",
            "competition_edition.competition.name",
            "players",
            "pitch_length",
            "pitch_width"
        ]

        # Extract all fields from the metadata
        df = pd.json_normalize(data, max_level=3)

        self.metadata_fields = {
            "critical_fields": critical_fields,
            "all_fields": df.columns.tolist(),
            "field_types": {col: str(df[col].dtype) for col in df.columns},
            "sample_values": {col: self._get_sample_value(df[col]) for col in df.columns},
            "description": "Match metadata containing team information, player details, competition info, and pitch dimensions"
        }

        # Extract player fields
        if "players" in data:
            player_sample = data["players"][0] if data["players"] else {}
            player_fields = self._flatten_dict(player_sample)

            self.metadata_fields["player_fields"] = {
                "fields": list(player_fields.keys()),
                "description": "Player-specific information including identity, position, playing time, and statistics"
            }

        return self.metadata_fields

    def analyze_tracking(self, tracking_file_path: str) -> Dict[str, Any]:
        """
        Analyze tracking file and extract field information

        Args:
            tracking_file_path: Path to tracking JSONL file

        Returns:
            Dictionary with tracking field information
        """
        # Read first few lines to analyze structure
        tracking_data = []
        with open(tracking_file_path, "r") as f:
            for i, line in enumerate(f):
                if i < 10:  # Read first 10 lines for analysis
                    tracking_data.append(json.loads(line))
                else:
                    break

        if not tracking_data:
            return {}

        # Critical fields as per specification
        critical_fields = ["frame", "timestamp", "period", "ball_data", "player_data"]

        # Extract top-level fields
        sample = tracking_data[0]
        top_level_fields = list(sample.keys())

        # Extract ball_data fields
        ball_fields = list(sample.get("ball_data", {}).keys())

        # Extract player_data fields
        player_data_sample = sample.get("player_data", [{}])[0]
        player_data_fields = list(player_data_sample.keys())

        self.tracking_fields = {
            "critical_fields": critical_fields,
            "top_level_fields": top_level_fields,
            "ball_data_fields": ball_fields,
            "player_data_fields": player_data_fields,
            "description": "Frame-by-frame tracking data showing positions of all players and the ball",
            "frequency": "10 frames per second (0.1s intervals)",
            "field_descriptions": {
                "frame": "Frame number in the match",
                "timestamp": "Time in match (HH:MM:SS.ms format)",
                "period": "Match period (1 or 2)",
                "ball_data": {
                    "x": "Ball x-coordinate (meters)",
                    "y": "Ball y-coordinate (meters)",
                    "z": "Ball z-coordinate/height (meters)",
                    "is_detected": "Whether ball was detected in this frame"
                },
                "player_data": {
                    "x": "Player x-coordinate (meters)",
                    "y": "Player y-coordinate (meters)",
                    "player_id": "Unique player identifier linking to metadata",
                    "is_detected": "Whether player was detected in this frame"
                },
                "possession": {
                    "player_id": "ID of player in possession",
                    "group": "Team in possession"
                }
            }
        }

        return self.tracking_fields

    def analyze_phases(self, phases_file_path: str) -> Dict[str, Any]:
        """
        Analyze phases file and extract field information

        Args:
            phases_file_path: Path to phases CSV file

        Returns:
            Dictionary with phases field information
        """
        df = pd.read_csv(phases_file_path, nrows=10)

        # All phase fields as per specification
        phase_fields = [
            'index', 'match_id', 'frame_start', 'frame_end', 'time_start', 'time_end',
            'minute_start', 'second_start', 'duration', 'period', 'attacking_side_id',
            'team_in_possession_id', 'attacking_side', 'team_in_possession_shortname',
            'n_player_possessions_in_phase', 'team_possession_loss_in_phase',
            'team_possession_lead_to_goal', 'team_possession_lead_to_shot',
            'team_in_possession_phase_type', 'team_in_possession_phase_type_id',
            'team_out_of_possession_phase_type', 'team_out_of_possession_phase_type_id',
            'x_start', 'y_start', 'channel_id_start', 'channel_start', 'third_id_start',
            'third_start', 'penalty_area_start', 'x_end', 'y_end', 'channel_id_end',
            'channel_end', 'third_id_end', 'third_end', 'penalty_area_end',
            'team_in_possession_width_start', 'team_in_possession_width_end',
            'team_in_possession_length_start', 'team_in_possession_length_end',
            'team_out_of_possession_width_start', 'team_out_of_possession_width_end',
            'team_out_of_possession_length_start', 'team_out_of_possession_length_end'
        ]

        self.phases_fields = {
            "all_fields": df.columns.tolist(),
            "field_types": {col: str(df[col].dtype) for col in df.columns},
            "sample_values": {col: self._get_sample_value(df[col]) for col in df.columns},
            "description": "Phase of play data capturing attacking and defending team phases",
            "key_concepts": {
                "phase_type": "Type of play phase (e.g., build-up, progression, attack)",
                "possession": "Team in possession during the phase",
                "spatial_info": "Starting and ending positions with pitch zones",
                "team_shape": "Width and length of team formations"
            }
        }

        return self.phases_fields

    def analyze_events(self, events_file_path: str) -> Dict[str, Any]:
        """
        Analyze events file and extract field information

        Args:
            events_file_path: Path to events CSV file

        Returns:
            Dictionary with events field information
        """
        df = pd.read_csv(events_file_path, nrows=10)

        # Core event categories
        event_categories = {
            "identification": ["event_id", "index", "match_id"],
            "temporal": ["frame_start", "frame_end", "time_start", "time_end", "minute_start", "second_start", "duration", "period"],
            "event_type": ["event_type_id", "event_type", "event_subtype_id", "event_subtype"],
            "player_info": ["player_id", "player_name", "player_position_id", "player_position"],
            "spatial": ["x_start", "y_start", "x_end", "y_end", "channel_start", "channel_end", "third_start", "third_end"],
            "passing": ["pass_distance", "pass_angle", "pass_direction", "pass_outcome", "high_pass"],
            "tactical": ["phase_index", "team_in_possession_phase_type", "n_passing_options", "line_break"],
            "advanced_metrics": ["xpass_completion", "xthreat", "speed_avg", "distance_covered"]
        }

        self.events_fields = {
            "all_fields": df.columns.tolist(),
            "field_types": {col: str(df[col].dtype) for col in df.columns},
            "sample_values": {col: self._get_sample_value(df[col]) for col in df.columns},
            "event_categories": event_categories,
            "description": "Detailed event-level data including passes, shots, defensive actions, and advanced metrics",
            "total_fields": len(df.columns)
        }

        return self.events_fields

    def analyze_enriched_tracking(self, enriched_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze enriched tracking data and extract field information

        Args:
            enriched_df: Enriched tracking dataframe

        Returns:
            Dictionary with enriched tracking field information
        """
        self.enriched_tracking_fields = {
            "all_fields": enriched_df.columns.tolist(),
            "field_types": {col: str(enriched_df[col].dtype) for col in enriched_df.columns},
            "total_fields": len(enriched_df.columns),
            "total_rows": len(enriched_df),
            "description": "Enriched tracking data combining frame-by-frame positions with player metadata",
            "source": "Merged from tracking data and metadata",
            "key_features": {
                "temporal_resolution": "10 FPS",
                "spatial_info": "Player and ball coordinates",
                "player_context": "Team, position, playing time",
                "tactical_context": "Direction of play, home/away designation"
            }
        }

        return self.enriched_tracking_fields

    def _flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
        """Flatten nested dictionary"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def _get_sample_value(self, series: pd.Series) -> Any:
        """Get a sample non-null value from series"""
        non_null = series.dropna()
        if len(non_null) > 0:
            value = non_null.iloc[0]
            # Convert to string if it's a complex type
            if isinstance(value, (dict, list)):
                return str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            return value
        return None

    def generate_knowledge_bank(
        self,
        metadata_path: Optional[str] = None,
        tracking_path: Optional[str] = None,
        events_path: Optional[str] = None,
        phases_path: Optional[str] = None,
        enriched_df: Optional[pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """
        Generate complete knowledge bank from all available datasets

        Args:
            metadata_path: Path to metadata file
            tracking_path: Path to tracking file
            events_path: Path to events file
            phases_path: Path to phases file
            enriched_df: Enriched tracking dataframe

        Returns:
            Complete knowledge bank dictionary
        """
        knowledge_bank = {
            "created_at": self.created_at,
            "version": "1.0",
            "description": "SkillCorner Dataset Field Documentation and Knowledge Bank"
        }

        if metadata_path:
            knowledge_bank["metadata"] = self.analyze_metadata(metadata_path)

        if tracking_path:
            knowledge_bank["tracking"] = self.analyze_tracking(tracking_path)

        if events_path:
            knowledge_bank["events"] = self.analyze_events(events_path)

        if phases_path:
            knowledge_bank["phases"] = self.analyze_phases(phases_path)

        if enriched_df is not None:
            knowledge_bank["enriched_tracking"] = self.analyze_enriched_tracking(enriched_df)

        return knowledge_bank

    def save_knowledge_bank(self, knowledge_bank: Dict[str, Any], output_path: str):
        """
        Save knowledge bank to JSON file

        Args:
            knowledge_bank: Knowledge bank dictionary
            output_path: Path to save the JSON file
        """
        # Convert any non-serializable types
        def convert_types(obj):
            if isinstance(obj, (pd.Series, pd.DataFrame)):
                return obj.to_dict()
            return obj

        with open(output_path, 'w') as f:
            json.dump(knowledge_bank, f, indent=2, default=convert_types)

    def get_field_info(self, dataset: str, field_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific field

        Args:
            dataset: Dataset name (metadata, tracking, events, phases, enriched_tracking)
            field_name: Field name

        Returns:
            Field information or None if not found
        """
        dataset_mapping = {
            "metadata": self.metadata_fields,
            "tracking": self.tracking_fields,
            "events": self.events_fields,
            "phases": self.phases_fields,
            "enriched_tracking": self.enriched_tracking_fields
        }

        fields = dataset_mapping.get(dataset, {})
        all_fields = fields.get("all_fields", [])

        if field_name in all_fields:
            return {
                "field_name": field_name,
                "dataset": dataset,
                "data_type": fields.get("field_types", {}).get(field_name),
                "sample_value": fields.get("sample_values", {}).get(field_name)
            }

        return None
