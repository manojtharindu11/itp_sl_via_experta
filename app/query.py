"""Adapter to expose the helper functions used by the app, backed by
the modular Experta-based knowledge system.

This file uses the new modular structure:
- app.kb.entities: Domain models (City, Connection, Enums)
- app.kb.data: Knowledge base facts
- app.kb.rules: Expert system rules
- app.kb.algorithms: Pathfinding algorithms
- app.experta_kb_v2: Integration layer
"""
from typing import List, Dict, Any

try:
    from app.experta_kb import (
        recommend_trip as experta_recommend_trip,
        get_city_coords as experta_get_city_coords,
        get_attractions as experta_get_attractions,
        get_all_cities as experta_get_all_cities,
        city_exists as experta_city_exists,
    )
except Exception as e:
    raise ImportError(
        "Experta-based knowledge module not available. Install 'experta' and ensure"
        " the modular KB structure exists in app/kb/ folder."
    ) from e


def recommend_trip_py(season: str, budget: str, start: str = 'colombo', end: str = 'ella') -> List[Dict[str, Any]]:
    """Return route recommendations via the Experta KB."""
    return experta_recommend_trip(season, budget, start, end)


get_city_coords = experta_get_city_coords
get_attractions = experta_get_attractions
get_all_cities = experta_get_all_cities
city_exists = experta_city_exists
