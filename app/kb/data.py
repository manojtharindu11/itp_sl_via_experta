"""Travel planning knowledge base data.

This module contains the factual data about Sri Lankan destinations,
structured using domain entities for better maintainability.
"""
from app.kb.entities import City, Connection, CityType, Region, Climate, Season, BudgetLevel


# Sri Lankan Cities Knowledge Base
CITIES_DATA = [
    City('colombo', CityType.URBAN, Region.WEST, Climate.TROPICAL, Season.ALL_YEAR, 
         BudgetLevel.VARIABLE, 6.9271, 79.8612, []),
    
    City('galle', CityType.BEACH, Region.SOUTH, Climate.TROPICAL, Season.WINTER,
         BudgetLevel.MODERATE, 6.0535, 80.2210, ['galle_fort']),
    
    City('mirissa', CityType.BEACH, Region.SOUTH, Climate.TROPICAL, Season.WINTER,
         BudgetLevel.MODERATE, 5.9485, 80.4719, ['whale_watching']),
    
    City('hambantota', CityType.BEACH, Region.SOUTH, Climate.TROPICAL, Season.WINTER,
         BudgetLevel.BUDGET, 6.1246, 81.1210, []),
    
    City('kandy', CityType.CULTURAL, Region.CENTRAL, Climate.MILD, Season.ALL_YEAR,
         BudgetLevel.MODERATE, 7.2906, 80.6337, ['temple_of_tooth']),
    
    City('nuwara_eliya', CityType.HILL_COUNTRY, Region.CENTRAL, Climate.COOL, Season.ALL_YEAR,
         BudgetLevel.HIGH, 6.9497, 80.7891, ['tea_plantations']),
    
    City('ella', CityType.HILL_COUNTRY, Region.UVA, Climate.MILD, Season.SUMMER,
         BudgetLevel.BUDGET, 6.8755, 81.0460, ['nine_arches_bridge']),
    
    City('anuradhapura', CityType.HISTORICAL, Region.NORTH_CENTRAL, Climate.DRY, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 8.3114, 80.4037, ['ancient_ruins']),
    
    City('sigiriya', CityType.HISTORICAL, Region.NORTH_CENTRAL, Climate.DRY, Season.ALL_YEAR,
         BudgetLevel.MODERATE, 7.9570, 80.7603, ['sigiriya_rock']),
    
    City('yala', CityType.NATIONAL_PARK, Region.SOUTHEAST, Climate.TROPICAL, Season.WINTER,
         BudgetLevel.MODERATE, 6.3667, 81.5167, ['wildlife_safari']),
    
    City('horton_plains', CityType.NATIONAL_PARK, Region.CENTRAL, Climate.COOL, Season.ALL_YEAR,
         BudgetLevel.MODERATE, 6.8020, 80.7998, ['worlds_end']),
    
    City('jaffna', CityType.URBAN, Region.NORTH, Climate.DRY, Season.SUMMER,
         BudgetLevel.MODERATE, 9.6615, 80.0255, ['nallur_kandaswamy_temple']),
    
    City('trincomalee', CityType.BEACH, Region.EAST, Climate.TROPICAL, Season.SUMMER,
         BudgetLevel.MODERATE, 8.5874, 81.2152, ['pigeon_island']),
    
    City('arugam_bay', CityType.BEACH, Region.EAST, Climate.TROPICAL, Season.SUMMER,
         BudgetLevel.BUDGET, 6.8390, 81.8386, ['surfing']),
    
    City('polonnaruwa', CityType.HISTORICAL, Region.NORTH_CENTRAL, Climate.DRY, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 7.9396, 81.0003, ['gal_vihara']),
    
    City('dambulla', CityType.HISTORICAL, Region.CENTRAL, Climate.DRY, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 7.8568, 80.6490, ['golden_temple']),
    
    City('bentota', CityType.BEACH, Region.WEST, Climate.TROPICAL, Season.WINTER,
         BudgetLevel.MODERATE, 6.4210, 80.0011, ['water_sports']),
    
    City('negombo', CityType.BEACH, Region.WEST, Climate.TROPICAL, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 7.2083, 79.8358, ['fish_market']),
    
    City('matara', CityType.URBAN, Region.SOUTH, Climate.TROPICAL, Season.WINTER,
         BudgetLevel.BUDGET, 5.9549, 80.5550, ['star_fort']),
    
    City('badulla', CityType.HILL_COUNTRY, Region.UVA, Climate.MILD, Season.SUMMER,
         BudgetLevel.BUDGET, 6.9897, 81.0550, ['demodara_loop']),
    
    # Additional major cities
    City('kurunegala', CityType.URBAN, Region.NORTH_WESTERN, Climate.TROPICAL, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 7.4863, 80.3623, ['ridi_viharaya']),
    
    City('ratnapura', CityType.URBAN, Region.SABARAGAMUWA, Climate.TROPICAL, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 6.6828, 80.3992, ['gem_mining', 'sinharaja_forest']),
    
    City('batticaloa', CityType.URBAN, Region.EAST, Climate.TROPICAL, Season.SUMMER,
         BudgetLevel.BUDGET, 7.7310, 81.6925, ['batticaloa_lagoon']),
    
    City('kalmunai', CityType.URBAN, Region.EAST, Climate.TROPICAL, Season.SUMMER,
         BudgetLevel.BUDGET, 7.4088, 81.8200, []),
    
    City('vavuniya', CityType.URBAN, Region.NORTH, Climate.DRY, Season.SUMMER,
         BudgetLevel.BUDGET, 8.7514, 80.4971, []),
    
    City('mannar', CityType.URBAN, Region.NORTH, Climate.DRY, Season.SUMMER,
         BudgetLevel.BUDGET, 8.9810, 79.9042, ['adams_bridge']),
    
    City('puttalam', CityType.URBAN, Region.NORTH_WESTERN, Climate.TROPICAL, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 8.0362, 79.8283, ['kalpitiya']),
    
    City('chilaw', CityType.URBAN, Region.NORTH_WESTERN, Climate.TROPICAL, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 7.5758, 79.7953, ['munneswaram_temple']),
    
    City('matale', CityType.URBAN, Region.CENTRAL, Climate.MILD, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 7.4675, 80.6234, ['aluvihare_temple', 'spice_gardens']),
    
    City('ampara', CityType.URBAN, Region.EAST, Climate.TROPICAL, Season.SUMMER,
         BudgetLevel.BUDGET, 7.2978, 81.6722, []),
    
    City('monaragala', CityType.URBAN, Region.UVA, Climate.DRY, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 6.8723, 81.3507, []),
    
    City('kegalle', CityType.URBAN, Region.SABARAGAMUWA, Climate.MILD, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 7.2523, 80.3436, ['pinnawala_elephant_orphanage']),
    
    City('kalutara', CityType.BEACH, Region.WEST, Climate.TROPICAL, Season.WINTER,
         BudgetLevel.MODERATE, 6.5854, 79.9607, ['kalutara_temple']),
    
    City('hikkaduwa', CityType.BEACH, Region.SOUTH, Climate.TROPICAL, Season.WINTER,
         BudgetLevel.MODERATE, 6.1409, 80.1001, ['coral_reefs', 'turtle_hatchery']),
    
    City('unawatuna', CityType.BEACH, Region.SOUTH, Climate.TROPICAL, Season.WINTER,
         BudgetLevel.MODERATE, 6.0108, 80.2490, ['beach']),
    
    City('nilaveli', CityType.BEACH, Region.EAST, Climate.TROPICAL, Season.SUMMER,
         BudgetLevel.MODERATE, 8.6977, 81.1884, ['pigeon_island_beach']),
    
    City('passikudah', CityType.BEACH, Region.EAST, Climate.TROPICAL, Season.SUMMER,
         BudgetLevel.MODERATE, 7.9362, 81.5579, ['beach']),
    
    City('haputale', CityType.HILL_COUNTRY, Region.UVA, Climate.COOL, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 6.7679, 80.9564, ['liptons_seat']),
    
    City('bandarawela', CityType.HILL_COUNTRY, Region.UVA, Climate.MILD, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 6.8323, 80.9856, []),
    
    City('gampaha', CityType.URBAN, Region.WEST, Climate.TROPICAL, Season.ALL_YEAR,
         BudgetLevel.BUDGET, 7.0905, 79.9996, []),
    
    City('kilinochchi', CityType.URBAN, Region.NORTH, Climate.DRY, Season.SUMMER,
         BudgetLevel.BUDGET, 9.3965, 80.3999, []),
    
    City('mullativu', CityType.URBAN, Region.NORTH, Climate.DRY, Season.SUMMER,
         BudgetLevel.BUDGET, 9.2671, 80.8142, []),
]


# Road network connections (bidirectional)
CONNECTIONS_DATA = [
    # Main west coast corridor
    Connection('colombo', 'negombo', 34),
    Connection('colombo', 'galle', 119),
    Connection('colombo', 'bentota', 65),
    Connection('bentota', 'galle', 56),
    Connection('galle', 'mirissa', 36),
    Connection('mirissa', 'matara', 12),
    Connection('matara', 'hambantota', 80),
    
    # Central highlands
    Connection('colombo', 'kandy', 115),
    Connection('negombo', 'kandy', 100),
    Connection('kandy', 'nuwara_eliya', 77),
    Connection('nuwara_eliya', 'ella', 60),
    Connection('kandy', 'badulla', 137),
    Connection('badulla', 'ella', 28),
    Connection('kandy', 'horton_plains', 60),
    
    # Cultural triangle
    Connection('colombo', 'anuradhapura', 205),
    Connection('kandy', 'dambulla', 72),
    Connection('dambulla', 'sigiriya', 17),
    Connection('kandy', 'sigiriya', 90),
    Connection('anuradhapura', 'sigiriya', 22),
    Connection('sigiriya', 'polonnaruwa', 60),
    
    # East coast
    Connection('polonnaruwa', 'trincomalee', 107),
    Connection('trincomalee', 'anuradhapura', 110),
    
    # North
    Connection('anuradhapura', 'jaffna', 200),
    
    # Southeast
    Connection('ella', 'yala', 130),
    Connection('hambantota', 'yala', 60),
    Connection('arugam_bay', 'yala', 160),
    Connection('arugam_bay', 'ella', 165),
    
    # Additional west coast connections
    Connection('colombo', 'kalutara', 43),
    Connection('kalutara', 'bentota', 22),
    Connection('galle', 'hikkaduwa', 18),
    Connection('hikkaduwa', 'bentota', 38),
    Connection('galle', 'unawatuna', 6),
    Connection('negombo', 'gampaha', 18),
    Connection('gampaha', 'colombo', 30),
    
    # North-western connections
    Connection('colombo', 'kurunegala', 94),
    Connection('kurunegala', 'chilaw', 50),
    Connection('chilaw', 'puttalam', 33),
    Connection('puttalam', 'anuradhapura', 90),
    Connection('kurunegala', 'dambulla', 70),
    Connection('kurunegala', 'kandy', 42),
    Connection('negombo', 'chilaw', 60),
    
    # Sabaragamuwa connections
    Connection('colombo', 'ratnapura', 101),
    Connection('ratnapura', 'nuwara_eliya', 110),
    Connection('ratnapura', 'ella', 130),
    Connection('kegalle', 'colombo', 78),
    Connection('kegalle', 'kandy', 37),
    Connection('kegalle', 'kurunegala', 43),
    Connection('kegalle', 'ratnapura', 75),
    
    # Central connections
    Connection('kandy', 'matale', 26),
    Connection('matale', 'dambulla', 43),
    Connection('matale', 'sigiriya', 54),
    
    # Uva province connections
    Connection('ella', 'haputale', 16),
    Connection('haputale', 'bandarawela', 9),
    Connection('bandarawela', 'badulla', 25),
    Connection('badulla', 'monaragala', 60),
    Connection('monaragala', 'yala', 90),
    Connection('monaragala', 'arugam_bay', 98),
    
    # East coast expansion
    Connection('trincomalee', 'nilaveli', 16),
    Connection('trincomalee', 'batticaloa', 108),
    Connection('batticaloa', 'passikudah', 35),
    Connection('batticaloa', 'kalmunai', 38),
    Connection('batticaloa', 'ampara', 33),
    Connection('ampara', 'arugam_bay', 115),
    Connection('kalmunai', 'arugam_bay', 80),
    
    # Northern connections
    Connection('jaffna', 'kilinochchi', 60),
    Connection('kilinochchi', 'vavuniya', 58),
    Connection('vavuniya', 'anuradhapura', 70),
    Connection('jaffna', 'mannar', 132),
    Connection('mannar', 'vavuniya', 86),
    Connection('mannar', 'puttalam', 150),
    Connection('kilinochchi', 'mullativu', 48),
]


# Build lookup dictionaries for fast access
CITIES_BY_NAME = {city.name: city for city in CITIES_DATA}


def get_city(name: str) -> City:
    """Get city by name."""
    return CITIES_BY_NAME.get(name)


def get_all_cities() -> list[City]:
    """Get all cities."""
    return CITIES_DATA


def get_connections_for_city(city_name: str) -> list[Connection]:
    """Get all connections involving a city."""
    return [conn for conn in CONNECTIONS_DATA if conn.connects(city_name)]
