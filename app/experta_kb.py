"""
New modular Experta-based knowledge module (v2).

This module uses the improved modular structure with separated concerns:
- app.kb.entities: Domain models (City, Connection, Enums)
- app.kb.data: Factual knowledge base
- app.kb.rules: Expert system inference rules
- app.kb.algorithms: Graph algorithms for pathfinding

This is the new recommended way to use the travel planner KB.
"""
from typing import List, Dict, Any, Optional
from app.kb.entities import Season, BudgetLevel
from app.kb.data import CITIES_BY_NAME, get_city, get_all_cities as get_all_city_objects
from app.kb.algorithms import build_distance_graph, dijkstra_shortest_path
from app.kb.rules import create_engine_with_preferences, EXPERTA_AVAILABLE


def recommend_trip(
    season: str, 
    budget: str, 
    start: str = 'colombo', 
    end: str = None,
    interests: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Get travel route recommendations using expert system reasoning.
    
    Args:
        season: Travel season (winter/summer/all_year)
        budget: Budget level (budget/moderate/high/variable)
        start: Starting city name
        end: Ending city name (if None, recommends multiple destinations)
        interests: Optional list of interests (beach, culture, history, nature, hiking)
    
    Returns:
        List of route recommendations with:
        - route: List of city names from start to end
        - distance: Total distance in km
        - recommended_score: Higher for expert-system recommended cities
        - reason: Why this route was recommended (if available)
    """
    # Build distance graph for pathfinding
    graph = build_distance_graph()
    
    # Get expert system recommendations
    recommended_cities = set()
    highly_recommended = set()
    avoided_cities = set()
    
    if EXPERTA_AVAILABLE:
        engine = create_engine_with_preferences(season, budget, interests or [])
        recommendations = engine.get_recommendations()
        recommended_cities = recommendations.get('recommended', set())
        highly_recommended = recommendations.get('highly_recommended', set())
        avoided_cities = recommendations.get('avoided', set())
    else:
        # Fallback: simple filtering if Experta not available
        for city in get_all_city_objects():
            season_match = (season == 'all_year' or 
                          city.best_season.value == season or 
                          city.best_season == Season.ALL_YEAR)
            budget_match = (budget == 'variable' or 
                          city.budget_level.value == budget or 
                          city.budget_level == BudgetLevel.VARIABLE)
            
            if season_match and budget_match:
                recommended_cities.add(city.name)
    
    # Determine candidate destinations
    if end:
        # Specific destination requested
        candidates = [end] if end in CITIES_BY_NAME else []
    else:
        # Recommend from expert system suggestions
        candidates = list(recommended_cities - avoided_cities)
    
    # Calculate routes to each candidate
    results: List[Dict[str, Any]] = []
    start_city = start or 'colombo'
    
    for destination in candidates:
        if destination == start_city:
            # Same start and end
            results.append({
                'route': [start_city],
                'distance': 0,
                'recommended_score': 2 if destination in highly_recommended else 1,
                'reason': 'same_location'
            })
        else:
            # Find shortest path
            path, distance = dijkstra_shortest_path(graph, start_city, destination)
            
            if path:
                score = 0
                reason = 'route_available'
                
                if destination in highly_recommended:
                    score = 3
                    reason = 'highly_recommended_destination'
                elif destination in recommended_cities:
                    score = 2
                    reason = 'recommended_destination'
                elif destination in avoided_cities:
                    score = -1
                    reason = 'not_ideal_season'
                else:
                    score = 1
                
                results.append({
                    'route': path,
                    'distance': distance,
                    'recommended_score': score,
                    'reason': reason
                })
    
    # Sort by recommendation score (descending), then distance (ascending)
    results.sort(key=lambda r: (-r.get('recommended_score', 0), r.get('distance', 0)))
    
    return results


def get_city_coords(cities: List[str]) -> Dict[str, Dict[str, float]]:
    """
    Get coordinates for a list of cities.
    
    Args:
        cities: List of city names
    
    Returns:
        Dict mapping city names to {lat, lon} dicts
    """
    coords = {}
    for city_name in cities:
        city = get_city(city_name)
        if city:
            coords[city_name] = {
                'lat': city.latitude,
                'lon': city.longitude
            }
    return coords


def get_attractions(cities: List[str]) -> Dict[str, List[str]]:
    """
    Get attractions for a list of cities.
    
    Args:
        cities: List of city names
    
    Returns:
        Dict mapping city names to lists of attraction names
    """
    attractions = {}
    for city_name in cities:
        city = get_city(city_name)
        if city:
            attractions[city_name] = city.attractions
        else:
            attractions[city_name] = []
    return attractions


def get_all_cities() -> List[str]:
    """
    Get list of all available city names, sorted alphabetically.
    
    Returns:
        Sorted list of city names
    """
    return sorted(CITIES_BY_NAME.keys())


def city_exists(city_name: str) -> bool:
    """
    Check if a city exists in the knowledge base.
    
    Args:
        city_name: Name of the city to check
    
    Returns:
        True if city exists, False otherwise
    """
    return city_name in CITIES_BY_NAME


def get_city_info(city_name: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a city.
    
    Args:
        city_name: Name of the city
    
    Returns:
        Dict with city details, or None if city doesn't exist
    """
    city = get_city(city_name)
    if not city:
        return None
    
    return {
        'name': city.name,
        'type': city.city_type.value,
        'region': city.region.value,
        'climate': city.climate.value,
        'best_season': city.best_season.value,
        'budget_level': city.budget_level.value,
        'coordinates': {'lat': city.latitude, 'lon': city.longitude},
        'attractions': city.attractions
    }
