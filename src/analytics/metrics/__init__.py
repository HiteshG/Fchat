"""
Analytics Metrics Module
Contains all 14 tactical analysis sections
"""

from .team_identity import analyze_team_identity
from .possession import analyze_possession_buildup
from .chance_creation import analyze_chance_creation
from .defense import analyze_defensive_structure
from .transitions import analyze_transitions
from .intelligence import analyze_tactical_intelligence
from .players import analyze_individual_players
from .chemistry import analyze_team_chemistry
from .efficiency import analyze_efficiency
from .set_pieces import analyze_set_pieces
from .momentum import analyze_momentum
from .consistency import analyze_consistency
from .training import analyze_training_focus
from .opponent import analyze_opponent_exploitation

__all__ = [
    'analyze_team_identity',
    'analyze_possession_buildup',
    'analyze_chance_creation',
    'analyze_defensive_structure',
    'analyze_transitions',
    'analyze_tactical_intelligence',
    'analyze_individual_players',
    'analyze_team_chemistry',
    'analyze_efficiency',
    'analyze_set_pieces',
    'analyze_momentum',
    'analyze_consistency',
    'analyze_training_focus',
    'analyze_opponent_exploitation',
]
