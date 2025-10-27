"""Graph algorithms for route planning.

This module contains pathfinding and graph manipulation algorithms
separated from the domain logic.
"""
from typing import Dict, List, Tuple, Optional
import heapq
from app.kb.data import CONNECTIONS_DATA, get_city


def build_distance_graph() -> Dict[str, Dict[str, int]]:
    """
    Build an adjacency list representation of the city network.
    
    Returns:
        Dict mapping city names to their neighbors with distances.
        Graph is bidirectional (undirected).
    """
    graph: Dict[str, Dict[str, int]] = {}
    
    for connection in CONNECTIONS_DATA:
        # Add edge in both directions
        graph.setdefault(connection.city_a, {})[connection.city_b] = connection.distance_km
        graph.setdefault(connection.city_b, {})[connection.city_a] = connection.distance_km
    
    return graph


def dijkstra_shortest_path(
    graph: Dict[str, Dict[str, int]], 
    source: str, 
    target: str
) -> Tuple[List[str], int]:
    """
    Find the shortest path between two cities using Dijkstra's algorithm.
    
    Args:
        graph: Adjacency list of city connections with distances
        source: Starting city name
        target: Destination city name
    
    Returns:
        Tuple of (path as list of city names, total distance in km)
        Returns ([], 0) if no path exists
    """
    if source == target:
        return [source], 0
    
    if source not in graph or target not in graph:
        return [], 0
    
    # Priority queue: (distance, current_city, path_so_far)
    queue = [(0, source, [source])]
    # Track shortest distance to each city
    distances = {source: 0}
    
    while queue:
        current_dist, current_city, path = heapq.heappop(queue)
        
        # Found the target
        if current_city == target:
            return path, current_dist
        
        # Skip if we've already found a shorter path to this city
        if current_dist > distances.get(current_city, float('inf')):
            continue
        
        # Explore neighbors
        for neighbor, edge_weight in graph.get(current_city, {}).items():
            new_distance = current_dist + edge_weight
            
            # Only process if this is a shorter path
            if neighbor not in distances or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                new_path = path + [neighbor]
                heapq.heappush(queue, (new_distance, neighbor, new_path))
    
    # No path found
    return [], 0


def find_all_paths(
    graph: Dict[str, Dict[str, int]],
    source: str,
    target: str,
    max_paths: int = 5
) -> List[Tuple[List[str], int]]:
    """
    Find multiple paths between cities (not just the shortest).
    Uses DFS with pruning to find reasonable alternatives.
    
    Args:
        graph: Adjacency list of city connections
        source: Starting city
        target: Destination city
        max_paths: Maximum number of paths to return
    
    Returns:
        List of (path, distance) tuples, sorted by distance
    """
    paths = []
    
    def dfs(current: str, visited: set, path: List[str], distance: int):
        if len(paths) >= max_paths:
            return
        
        if current == target:
            paths.append((path.copy(), distance))
            return
        
        if current not in graph:
            return
        
        for neighbor, edge_dist in graph[current].items():
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, visited, path, distance + edge_dist)
                path.pop()
                visited.remove(neighbor)
    
    dfs(source, {source}, [source], 0)
    
    # Sort by distance and return
    paths.sort(key=lambda x: x[1])
    return paths


def get_cities_within_distance(
    graph: Dict[str, Dict[str, int]],
    source: str,
    max_distance: int
) -> Dict[str, int]:
    """
    Find all cities within a certain distance from a source city.
    
    Args:
        graph: Adjacency list of city connections
        source: Starting city
        max_distance: Maximum distance in km
    
    Returns:
        Dict mapping reachable city names to their distances
    """
    if source not in graph:
        return {}
    
    distances = {source: 0}
    queue = [(0, source)]
    
    while queue:
        current_dist, current_city = heapq.heappop(queue)
        
        if current_dist > max_distance:
            continue
        
        if current_dist > distances.get(current_city, float('inf')):
            continue
        
        for neighbor, edge_weight in graph.get(current_city, {}).items():
            new_distance = current_dist + edge_weight
            
            if new_distance <= max_distance:
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(queue, (new_distance, neighbor))
    
    return distances
