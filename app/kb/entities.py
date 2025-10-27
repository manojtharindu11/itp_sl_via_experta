"""Domain entities for the travel planning system.

This module defines the core data structures representing cities and their attributes.
Using dataclasses provides better structure, type safety, and IDE support.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class CityType(Enum):
    """Types of destinations."""
    URBAN = "urban"
    BEACH = "beach"
    CULTURAL = "cultural"
    HILL_COUNTRY = "hill_country"
    HISTORICAL = "historical"
    NATIONAL_PARK = "national_park"


class Region(Enum):
    """Geographic regions of Sri Lanka."""
    WEST = "west"
    SOUTH = "south"
    EAST = "east"
    NORTH = "north"
    CENTRAL = "central"
    NORTH_CENTRAL = "north_central"
    NORTH_WESTERN = "north_western"
    UVA = "uva"
    SABARAGAMUWA = "sabaragamuwa"
    SOUTHEAST = "southeast"


class Climate(Enum):
    """Climate types."""
    TROPICAL = "tropical"
    MILD = "mild"
    COOL = "cool"
    DRY = "dry"


class Season(Enum):
    """Travel seasons based on monsoon patterns."""
    WINTER = "winter"  # Nov-Feb: SW monsoon ends, best for south/west
    SUMMER = "summer"  # May-Aug: NE monsoon ends, best for east/hill country
    ALL_YEAR = "all_year"  # Year-round destinations


class BudgetLevel(Enum):
    """Budget categories for travelers."""
    BUDGET = "budget"
    MODERATE = "moderate"
    HIGH = "high"
    VARIABLE = "variable"


@dataclass
class City:
    """Represents a destination city in Sri Lanka."""
    name: str
    city_type: CityType
    region: Region
    climate: Climate
    best_season: Season
    budget_level: BudgetLevel
    latitude: float
    longitude: float
    attractions: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate city data."""
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Invalid latitude for {self.name}: {self.latitude}")
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Invalid longitude for {self.name}: {self.longitude}")


@dataclass
class Connection:
    """Represents a connection between two cities."""
    city_a: str
    city_b: str
    distance_km: int
    
    def __post_init__(self):
        """Validate connection data."""
        if self.distance_km <= 0:
            raise ValueError(f"Distance must be positive: {self.distance_km}")
    
    def connects(self, city_name: str) -> bool:
        """Check if this connection involves the given city."""
        return city_name in (self.city_a, self.city_b)
    
    def other_end(self, city_name: str) -> Optional[str]:
        """Get the city at the other end of this connection."""
        if city_name == self.city_a:
            return self.city_b
        elif city_name == self.city_b:
            return self.city_a
        return None
