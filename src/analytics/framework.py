"""
Phase 2: Metrics Engine Framework
Orchestrates parallel computation of all metrics with progress tracking
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from pathlib import Path
import pickle
import hashlib

# Import all metric modules
from .metrics import (
    analyze_team_identity,
    analyze_possession_buildup,
    analyze_chance_creation,
    analyze_defensive_structure,
    analyze_transitions,
    analyze_tactical_intelligence,
    analyze_individual_players,
    analyze_team_chemistry,
    analyze_efficiency,
    analyze_set_pieces,
    analyze_momentum,
    analyze_consistency,
    analyze_training_focus,
    analyze_opponent_exploitation
)


class MetricsEngine:
    """
    Metrics computation engine with parallel processing, caching, and progress tracking
    """

    def __init__(self, cache_dir: str = "data/cache"):
        """
        Initialize metrics engine

        Args:
            cache_dir: Directory for caching computed metrics
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Define all 14 sections with their compute functions
        self.sections = [
            {
                'id': 'team_identity',
                'name': 'Team Identity & Setup',
                'icon': '🧩',
                'function': analyze_team_identity,
                'weight': 1
            },
            {
                'id': 'possession',
                'name': 'Possession & Build-Up',
                'icon': '⚙️',
                'function': analyze_possession_buildup,
                'weight': 1
            },
            {
                'id': 'chance_creation',
                'name': 'Chance Creation',
                'icon': '⚡',
                'function': analyze_chance_creation,
                'weight': 1
            },
            {
                'id': 'defensive_structure',
                'name': 'Defensive Structure',
                'icon': '🛡️',
                'function': analyze_defensive_structure,
                'weight': 1
            },
            {
                'id': 'transitions',
                'name': 'Transitions',
                'icon': '🔄',
                'function': analyze_transitions,
                'weight': 1
            },
            {
                'id': 'tactical_intelligence',
                'name': 'Tactical Intelligence',
                'icon': '🧠',
                'function': analyze_tactical_intelligence,
                'weight': 1
            },
            {
                'id': 'individual_players',
                'name': 'Individual Players',
                'icon': '👤',
                'function': analyze_individual_players,
                'weight': 1
            },
            {
                'id': 'team_chemistry',
                'name': 'Team Chemistry',
                'icon': '🤝',
                'function': analyze_team_chemistry,
                'weight': 1
            },
            {
                'id': 'efficiency',
                'name': 'Efficiency',
                'icon': '📊',
                'function': analyze_efficiency,
                'weight': 1
            },
            {
                'id': 'set_pieces',
                'name': 'Set-Pieces',
                'icon': '⚽',
                'function': analyze_set_pieces,
                'weight': 1
            },
            {
                'id': 'momentum',
                'name': 'Momentum',
                'icon': '📈',
                'function': analyze_momentum,
                'weight': 1
            },
            {
                'id': 'consistency',
                'name': 'Consistency',
                'icon': '🎯',
                'function': analyze_consistency,
                'weight': 1
            },
            {
                'id': 'training_focus',
                'name': 'Training Focus',
                'icon': '💪',
                'function': analyze_training_focus,
                'weight': 1
            },
            {
                'id': 'opponent_exploitation',
                'name': 'Opponent Exploitation',
                'icon': '🎲',
                'function': analyze_opponent_exploitation,
                'weight': 1
            }
        ]

    def _generate_cache_key(self, events_df: pd.DataFrame, phases_df: pd.DataFrame = None, team_id: str = None) -> str:
        """
        Generate unique cache key based on data
        """
        # Use data shape and sample values for hashing
        key_string = f"{len(events_df)}_{events_df.columns.tolist()}"

        if phases_df is not None:
            key_string += f"_{len(phases_df)}_{phases_df.columns.tolist()}"

        if team_id:
            key_string += f"_{team_id}"

        return hashlib.md5(key_string.encode()).hexdigest()

    def _load_from_cache(self, cache_key: str) -> Dict[str, Any]:
        """
        Load metrics from cache if available
        """
        cache_file = self.cache_dir / f"{cache_key}.pkl"

        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)

                # Check if cache is recent (less than 1 hour old)
                cache_age = time.time() - cache_file.stat().st_mtime
                if cache_age < 3600:  # 1 hour
                    return cached_data
            except Exception as e:
                print(f"Cache load error: {e}")

        return None

    def _save_to_cache(self, cache_key: str, data: Dict[str, Any]):
        """
        Save metrics to cache
        """
        cache_file = self.cache_dir / f"{cache_key}.pkl"

        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Cache save error: {e}")

    def compute_section(self, section: Dict[str, Any], events_df: pd.DataFrame, phases_df: pd.DataFrame = None) -> Dict[str, Any]:
        """
        Compute metrics for a single section
        """
        try:
            start_time = time.time()

            # Execute the metric function
            result = section['function'](events_df, phases_df)

            # Add metadata
            result['id'] = section['id']
            result['name'] = section['name']
            result['icon'] = section['icon']
            result['computation_time'] = time.time() - start_time
            result['status'] = 'success'

            return result

        except Exception as e:
            return {
                'id': section['id'],
                'name': section['name'],
                'icon': section['icon'],
                'section': section['name'],
                'status': 'error',
                'error': str(e),
                'metrics': {}
            }

    def compute_all_metrics(
        self,
        events_df: pd.DataFrame,
        phases_df: pd.DataFrame = None,
        team_id: str = None,
        use_cache: bool = True,
        progress_callback: Callable[[int, int, str], None] = None
    ) -> Dict[str, Any]:
        """
        Compute all metrics in parallel with progress tracking

        Args:
            events_df: Events dataframe
            phases_df: Phases dataframe (optional)
            team_id: Team identifier (optional)
            use_cache: Whether to use caching
            progress_callback: Callback function for progress updates (current, total, message)

        Returns:
            Dictionary with all computed metrics
        """
        # Check cache first
        if use_cache:
            cache_key = self._generate_cache_key(events_df, phases_df, team_id)
            cached_results = self._load_from_cache(cache_key)

            if cached_results is not None:
                if progress_callback:
                    progress_callback(len(self.sections), len(self.sections), "Loaded from cache")
                return cached_results

        # Initialize results
        results = {
            'team_id': team_id,
            'sections': {},
            'summary': {
                'total_sections': len(self.sections),
                'total_events': len(events_df),
                'total_phases': len(phases_df) if phases_df is not None else 0,
                'computation_start': time.time()
            }
        }

        # Parallel computation using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all tasks
            future_to_section = {
                executor.submit(self.compute_section, section, events_df, phases_df): section
                for section in self.sections
            }

            # Process completed tasks
            completed = 0
            for future in as_completed(future_to_section):
                section = future_to_section[future]

                try:
                    section_result = future.result()
                    results['sections'][section['id']] = section_result

                    completed += 1

                    # Progress callback
                    if progress_callback:
                        progress_callback(
                            completed,
                            len(self.sections),
                            f"Completed: {section['name']}"
                        )

                except Exception as e:
                    results['sections'][section['id']] = {
                        'id': section['id'],
                        'name': section['name'],
                        'icon': section['icon'],
                        'status': 'error',
                        'error': str(e),
                        'metrics': {}
                    }
                    completed += 1

                    if progress_callback:
                        progress_callback(
                            completed,
                            len(self.sections),
                            f"Error in: {section['name']}"
                        )

        # Add summary statistics
        results['summary']['computation_end'] = time.time()
        results['summary']['total_time'] = results['summary']['computation_end'] - results['summary']['computation_start']
        results['summary']['successful_sections'] = sum(1 for s in results['sections'].values() if s.get('status') == 'success')
        results['summary']['failed_sections'] = sum(1 for s in results['sections'].values() if s.get('status') == 'error')

        # Save to cache
        if use_cache:
            self._save_to_cache(cache_key, results)

        return results

    def get_section_list(self) -> List[Dict[str, Any]]:
        """
        Get list of all sections with metadata
        """
        return [
            {
                'id': s['id'],
                'name': s['name'],
                'icon': s['icon']
            }
            for s in self.sections
        ]

    def clear_cache(self):
        """
        Clear all cached metrics
        """
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()
