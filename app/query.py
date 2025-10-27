"""Adapter to expose the helper functions used by the app, backed by
the Experta-based knowledge module (`experta_kb`).

This file intentionally only supports the Experta backend. The older Prolog
subprocess-based code has been removed as part of the migration.
"""
from typing import List, Dict, Any

try:
    from experta_kb import (
        recommend_trip as experta_recommend_trip,
        get_city_coords as experta_get_city_coords,
        get_attractions as experta_get_attractions,
        get_all_cities as experta_get_all_cities,
        city_exists as experta_city_exists,
    )
except Exception as e:
    raise ImportError(
        "Experta-based knowledge module not available. Install 'experta' and ensure"
        " 'experta_kb.py' exists in app/ folder."
    ) from e


def recommend_trip_py(season: str, budget: str, start: str = 'colombo', end: str = 'ella') -> List[Dict[str, Any]]:
    """Return route recommendations via the Experta KB."""
    return experta_recommend_trip(season, budget, start, end)


get_city_coords = experta_get_city_coords
get_attractions = experta_get_attractions
get_all_cities = experta_get_all_cities
city_exists = experta_city_exists
