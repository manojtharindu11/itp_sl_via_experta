"""
Lightweight Experta-based knowledge module for the travel planner.

This module mirrors the facts in `kb/*.pl` and provides a small wrapper using
Experta to mark recommended cities by season and budget. It also exposes
helper functions used by `app/query.py`: `recommend_trip`, `get_city_coords`,
`get_attractions`, `get_all_cities`, and `city_exists`.

The route-finding uses a simple Dijkstra implementation on the distances
graph defined below. Experta is used to demonstrate rule firing for
recommendations; the path computation is performed in Python for simplicity
and determinism.
"""
from typing import List, Dict, Any, Tuple
try:
    from experta import KnowledgeEngine, Fact, Rule, MATCH
    EXPERTA_AVAILABLE = True
except Exception:
    EXPERTA_AVAILABLE = False

# --- Data (translated from kb/*.pl) ---
# city(Name) -> (type, region, climate)
CITIES: Dict[str, Tuple[str, str, str]] = {
    'colombo': ('urban', 'west', 'tropical'),
    'galle': ('beach', 'south', 'tropical'),
    'mirissa': ('beach', 'south', 'tropical'),
    'hambantota': ('beach', 'south', 'tropical'),
    'kandy': ('cultural', 'central', 'mild'),
    'nuwara_eliya': ('hill_country', 'central', 'cool'),
    'ella': ('hill_country', 'uva', 'mild'),
    'anuradhapura': ('historical', 'north_central', 'dry'),
    'sigiriya': ('historical', 'north_central', 'dry'),
    'yala': ('national_park', 'southeast', 'tropical'),
    'horton_plains': ('national_park', 'central', 'cool'),
    'jaffna': ('urban', 'north', 'dry'),
    'trincomalee': ('beach', 'east', 'tropical'),
    'arugam_bay': ('beach', 'east', 'tropical'),
    'polonnaruwa': ('historical', 'north_central', 'dry'),
    'dambulla': ('historical', 'central', 'dry'),
    'bentota': ('beach', 'west', 'tropical'),
    'negombo': ('beach', 'west', 'tropical'),
    'matara': ('urban', 'south', 'tropical'),
    'badulla': ('hill_country', 'uva', 'mild'),
}

ATTRACTIONS: Dict[str, List[str]] = {
    'kandy': ['temple_of_tooth'],
    'nuwara_eliya': ['tea_plantations'],
    'mirissa': ['whale_watching'],
    'ella': ['nine_arches_bridge'],
    'galle': ['galle_fort'],
    'anuradhapura': ['ancient_ruins'],
    'sigiriya': ['sigiriya_rock'],
    'yala': ['wildlife_safari'],
    'horton_plains': ['worlds_end'],
    'jaffna': ['nallur_kandaswamy_temple'],
    'trincomalee': ['pigeon_island'],
    'arugam_bay': ['surfing'],
    'polonnaruwa': ['gal_vihara'],
    'dambulla': ['golden_temple'],
    'bentota': ['water_sports'],
    'negombo': ['fish_market'],
    'matara': ['star_fort'],
    'badulla': ['demodara_loop'],
}

DISTANCES: List[Tuple[str, str, int]] = [
    ('colombo', 'kandy', 115), ('kandy', 'nuwara_eliya', 77), ('nuwara_eliya', 'ella', 60),
    ('colombo', 'mirissa', 155), ('colombo', 'galle', 119), ('galle', 'mirissa', 36),
    ('ella', 'yala', 130), ('colombo', 'anuradhapura', 205), ('anuradhapura', 'sigiriya', 22),
    ('kandy', 'sigiriya', 90), ('kandy', 'horton_plains', 60), ('mirissa', 'matara', 12),
    ('matara', 'hambantota', 80), ('hambantota', 'yala', 60), ('colombo', 'negombo', 34),
    ('negombo', 'kandy', 100), ('kandy', 'dambulla', 72), ('dambulla', 'sigiriya', 17),
    ('sigiriya', 'polonnaruwa', 60), ('polonnaruwa', 'trincomalee', 107), ('kandy', 'badulla', 137),
    ('badulla', 'ella', 28), ('trincomalee', 'anuradhapura', 110), ('anuradhapura', 'jaffna', 200),
    ('arugam_bay', 'yala', 160), ('arugam_bay', 'ella', 165), ('bentota', 'galle', 56),
    ('bentota', 'colombo', 65),
]

COORDS: Dict[str, Dict[str, float]] = {
    'colombo': {'lat': 6.9271, 'lon': 79.8612}, 'galle': {'lat': 6.0535, 'lon': 80.2210},
    'mirissa': {'lat': 5.9485, 'lon': 80.4719}, 'hambantota': {'lat': 6.1246, 'lon': 81.1210},
    'kandy': {'lat': 7.2906, 'lon': 80.6337}, 'nuwara_eliya': {'lat': 6.9497, 'lon': 80.7891},
    'ella': {'lat': 6.8755, 'lon': 81.0460}, 'anuradhapura': {'lat': 8.3114, 'lon': 80.4037},
    'sigiriya': {'lat': 7.9570, 'lon': 80.7603}, 'yala': {'lat': 6.3667, 'lon': 81.5167},
    'horton_plains': {'lat': 6.8020, 'lon': 80.7998}, 'jaffna': {'lat': 9.6615, 'lon': 80.0255},
    'trincomalee': {'lat': 8.5874, 'lon': 81.2152}, 'arugam_bay': {'lat': 6.8390, 'lon': 81.8386},
    'polonnaruwa': {'lat': 7.9396, 'lon': 81.0003}, 'dambulla': {'lat': 7.8568, 'lon': 80.6490},
    'bentota': {'lat': 6.4210, 'lon': 80.0011}, 'negombo': {'lat': 7.2083, 'lon': 79.8358},
    'matara': {'lat': 5.9549, 'lon': 80.5550}, 'badulla': {'lat': 6.9897, 'lon': 81.0550},
}

BUDGETS: Dict[str, str] = {
    'mirissa': 'moderate', 'nuwara_eliya': 'high', 'kandy': 'moderate', 'ella': 'budget',
    'colombo': 'variable', 'galle': 'moderate', 'negombo': 'budget', 'bentota': 'moderate',
    'anuradhapura': 'budget', 'sigiriya': 'moderate', 'polonnaruwa': 'budget', 'dambulla': 'budget',
    'trincomalee': 'moderate', 'jaffna': 'moderate', 'arugam_bay': 'budget', 'matara': 'budget',
    'badulla': 'budget',
}

BEST_SEASON: Dict[str, str] = {
    'mirissa': 'winter', 'ella': 'summer', 'kandy': 'all_year', 'nuwara_eliya': 'all_year',
    'galle': 'winter', 'yala': 'winter', 'arugam_bay': 'summer', 'trincomalee': 'summer',
    'jaffna': 'summer', 'negombo': 'all_year', 'bentota': 'winter', 'anuradhapura': 'all_year',
    'sigiriya': 'all_year', 'polonnaruwa': 'all_year', 'dambulla': 'all_year', 'horton_plains': 'all_year',
    'matara': 'winter', 'badulla': 'summer',
}


def _build_graph() -> Dict[str, Dict[str, int]]:
    g: Dict[str, Dict[str, int]] = {}
    for a, b, d in DISTANCES:
        g.setdefault(a, {})[b] = d
        g.setdefault(b, {})[a] = d
    return g


def _dijkstra(graph: Dict[str, Dict[str, int]], source: str, target: str) -> Tuple[List[str], int]:
    # Standard Dijkstra for shortest path by distance
    import heapq

    if source == target:
        return [source], 0

    queue = [(0, source, [source])]
    seen = {source: 0}
    while queue:
        dist, node, path = heapq.heappop(queue)
        if node == target:
            return path, dist
        for neigh, w in graph.get(node, {}).items():
            nd = dist + w
            if neigh not in seen or nd < seen[neigh]:
                seen[neigh] = nd
                heapq.heappush(queue, (nd, neigh, path + [neigh]))
    return [], 0


if EXPERTA_AVAILABLE:
    class TravelEngine(KnowledgeEngine):
        @Rule(Fact(city=MATCH.city, budget=MATCH.budget, best_season=MATCH.season))
        def mark_recommended(self, city, budget, season):
            # When a city fact matches, assert a recommended fact for it.
            self.declare(Fact(recommended=city))


def recommend_trip(season: str, budget: str, start: str = 'colombo', end: str = None) -> List[Dict[str, Any]]:
    """Return route recommendations as list of dicts {'route': [...], 'distance': int}.

    This uses Experta to mark recommended cities (when available) but computes
    the actual route using a deterministic Dijkstra implementation on the
    DISTANCES graph.
    """
    candidates = []
    # Simple budget match: variable matches everything
    for city in CITIES.keys():
        city_budget = BUDGETS.get(city, 'variable')
        season_ok = (season == 'all_year') or (BEST_SEASON.get(city) == season)
        budget_ok = (budget == 'variable') or (city_budget == budget)
        if season_ok and budget_ok:
            candidates.append(city)

    # If experta is available, run engine to get 'recommended' facts (demonstration)
    recommended_by_experta = set()
    if EXPERTA_AVAILABLE:
        engine = TravelEngine()
        # Declare compound facts with fields city, budget, best_season
        for c in CITIES.keys():
            engine.declare(Fact(city=c, budget=BUDGETS.get(c), best_season=BEST_SEASON.get(c)))
        engine.run()
        for f in engine.facts.values():
            if isinstance(f, Fact) and f.get('recommended'):
                recommended_by_experta.add(f.get('recommended'))

    # Build graph and compute routes
    graph = _build_graph()
    start_city = start or 'colombo'
    results: List[Dict[str, Any]] = []
    for dest in candidates:
        end_city = end or dest
        path, dist = _dijkstra(graph, start_city, end_city)
        if path:
            score_boost = 1 if dest in recommended_by_experta else 0
            results.append({'route': path, 'distance': dist, 'recommended_score': score_boost})

    # Sort by distance, then experta score (recommended first)
    results.sort(key=lambda r: (r['distance'] - r.get('recommended_score', 0)))
    return results


def get_city_coords(cities: List[str]) -> Dict[str, Dict[str, float]]:
    return {c: COORDS[c] for c in cities if c in COORDS}


def get_attractions(cities: List[str]) -> Dict[str, List[str]]:
    return {c: ATTRACTIONS.get(c, []) for c in cities}


def get_all_cities() -> List[str]:
    return sorted(list(CITIES.keys()))


def city_exists(city: str) -> bool:
    return city in CITIES
