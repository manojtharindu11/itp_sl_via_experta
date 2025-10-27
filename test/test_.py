"""Unit tests updated to use the Experta-based KB directly.

These tests no longer require SWI-Prolog and instead call the Python
implementation in `app.experta_kb`.
"""
import sys
import os
# Add parent directory to path so we can import from app/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.experta_kb import recommend_trip, get_all_cities, get_city_coords, get_attractions, city_exists


# ============= Season-based Tests =============

def test_recommend_winter_beach():
    """Winter season should recommend south/west coast beaches like Mirissa, Galle"""
    res = recommend_trip('winter', 'moderate', 'colombo', 'mirissa')
    assert len(res) > 0, "Should return at least one route"
    assert any(r for r in res if r.get('route') and r['route'][-1] == 'mirissa')


def test_recommend_summer_east_coast():
    """Summer season should work for east coast destinations"""
    res = recommend_trip('summer', 'budget', 'colombo', 'arugam_bay')
    assert len(res) > 0, "Should return routes to Arugam Bay in summer"
    assert any(r for r in res if 'arugam_bay' in r.get('route', []))


def test_recommend_all_year():
    """All year should return cultural/hill country destinations"""
    res = recommend_trip('all_year', 'moderate', 'colombo', 'kandy')
    assert len(res) > 0, "Should return routes for all-year destinations"
    assert any(r for r in res if 'kandy' in r.get('route', []))


# ============= Budget-based Tests =============

def test_budget_low():
    """Budget category should recommend affordable destinations like Ella"""
    res = recommend_trip('summer', 'budget', 'colombo', 'ella')
    assert len(res) > 0, "Should return budget-friendly routes"
    assert any(r for r in res if 'ella' in r.get('route', []))


def test_budget_high():
    """High budget should work for luxury destinations like Nuwara Eliya"""
    res = recommend_trip('all_year', 'high', 'colombo', 'nuwara_eliya')
    assert len(res) > 0, "Should return routes to high-end destinations"
    assert any(r for r in res if 'nuwara_eliya' in r.get('route', []))


def test_budget_variable():
    """Variable budget should match any destination"""
    res = recommend_trip('all_year', 'variable', 'colombo', 'kandy')
    assert len(res) > 0, "Variable budget should work with any city"


# ============= Route Planning Tests =============

def test_route_colombo_ella():
    """Test standard hill country route"""
    res = recommend_trip('all_year', 'budget', 'colombo', 'ella')
    assert any(r for r in res if 'colombo' in r.get('route', []) and 'ella' in r.get('route', []))
    # Route should include intermediate cities
    route = res[0]['route']
    assert len(route) >= 2, "Route should have at least start and end"


def test_route_distance_calculation():
    """Test that distances are calculated correctly"""
    res = recommend_trip('winter', 'moderate', 'colombo', 'galle')
    assert len(res) > 0
    assert res[0].get('distance') is not None, "Distance should be calculated"
    assert res[0]['distance'] > 0, "Distance should be positive"


def test_same_start_end():
    """Test route when start and end are the same city"""
    res = recommend_trip('all_year', 'moderate', 'colombo', 'colombo')
    assert len(res) > 0
    route = res[0]['route']
    assert route == ['colombo'], "Same start/end should return single-city route"
    assert res[0]['distance'] == 0, "Distance should be zero"


def test_unreachable_destination():
    """Test with cities that might not have direct connections based on budget/season"""
    # This should still work as long as cities exist
    res = recommend_trip('winter', 'budget', 'colombo', 'jaffna')
    # Jaffna is not a winter destination, so result might be empty
    # This tests the filtering logic
    assert isinstance(res, list), "Should return a list even if empty"


# ============= Helper Function Tests =============

def test_get_all_cities():
    """Test retrieving all cities"""
    cities = get_all_cities()
    assert len(cities) > 0, "Should return multiple cities"
    assert 'colombo' in cities, "Should include Colombo"
    assert 'ella' in cities, "Should include Ella"
    assert isinstance(cities, list), "Should return a list"


def test_city_exists():
    """Test city existence check"""
    assert city_exists('colombo') == True, "Colombo should exist"
    assert city_exists('kandy') == True, "Kandy should exist"
    assert city_exists('fake_city') == False, "Fake city should not exist"
    assert city_exists('COLOMBO') == False, "City names are case-sensitive"


def test_get_city_coords():
    """Test retrieving coordinates for cities"""
    coords = get_city_coords(['colombo', 'kandy', 'ella'])
    assert len(coords) == 3, "Should return coords for all 3 cities"
    assert 'colombo' in coords, "Should include Colombo coords"
    assert coords['colombo']['lat'] > 0, "Latitude should be positive for Sri Lanka"
    assert coords['colombo']['lon'] > 0, "Longitude should be positive for Sri Lanka"


def test_get_city_coords_invalid():
    """Test coords with invalid city"""
    coords = get_city_coords(['colombo', 'invalid_city'])
    assert 'colombo' in coords, "Should return valid city coords"
    assert 'invalid_city' not in coords, "Should skip invalid cities"


def test_get_attractions():
    """Test retrieving attractions"""
    attractions = get_attractions(['kandy', 'ella', 'galle'])
    assert 'kandy' in attractions, "Should include Kandy attractions"
    assert len(attractions['kandy']) > 0, "Kandy should have attractions"
    assert 'temple_of_tooth' in attractions['kandy'], "Kandy should have Temple of Tooth"
    assert 'ella' in attractions, "Should include Ella"


def test_get_attractions_empty():
    """Test attractions for cities without notable attractions"""
    attractions = get_attractions(['colombo'])
    # Colombo might not have attractions in our KB
    assert 'colombo' in attractions, "Should still return key even if empty"


# ============= Edge Cases & Error Handling =============

def test_invalid_season():
    """Test with invalid season parameter"""
    # Should still work, just won't match any season-specific cities
    res = recommend_trip('invalid_season', 'moderate', 'colombo', 'kandy')
    assert isinstance(res, list), "Should return list even with invalid season"


def test_invalid_budget():
    """Test with invalid budget parameter"""
    res = recommend_trip('all_year', 'invalid_budget', 'colombo', 'kandy')
    assert isinstance(res, list), "Should return list even with invalid budget"


def test_empty_route():
    """Test when no route is possible due to strict filters"""
    # Winter + east coast city that's summer-only
    res = recommend_trip('winter', 'high', 'colombo', 'trincomalee')
    # Trincomalee is summer destination, so might not match
    assert isinstance(res, list), "Should return list (possibly empty)"


def test_multiple_route_options():
    """Test that system can return multiple route options if available"""
    res = recommend_trip('all_year', 'moderate', 'colombo', 'sigiriya')
    assert len(res) > 0, "Should return at least one route"
    # Check all results have required fields
    for r in res:
        assert 'route' in r, "Each result should have a route"
        assert 'distance' in r, "Each result should have a distance"


# ============= Integration Tests =============

def test_full_winter_beach_scenario():
    """Complete scenario: Winter beach trip from Colombo to south coast"""
    res = recommend_trip('winter', 'moderate', 'colombo', 'mirissa')
    assert len(res) > 0, "Should find routes"
    
    route = res[0]['route']
    assert route[0] == 'colombo', "Should start at Colombo"
    assert route[-1] == 'mirissa', "Should end at Mirissa"
    assert res[0]['distance'] > 0, "Should calculate distance"
    
    # Get attractions for the route
    attractions = get_attractions(route)
    assert len(attractions) > 0, "Route cities should have attractions"


def test_full_hill_country_scenario():
    """Complete scenario: Hill country tour"""
    res = recommend_trip('all_year', 'budget', 'colombo', 'ella')
    assert len(res) > 0, "Should find routes"
    
    route = res[0]['route']
    # Verify coordinates exist for all cities
    coords = get_city_coords(route)
    assert len(coords) == len(route), "All cities should have coordinates"
    
    # Check distance is reasonable (not zero, not impossibly large)
    assert 0 < res[0]['distance'] < 1000, "Distance should be reasonable for Sri Lanka"


def test_cultural_triangle_tour():
    """Complete scenario: Cultural triangle exploration"""
    res = recommend_trip('all_year', 'moderate', 'colombo', 'anuradhapura')
    assert len(res) > 0, "Should find routes to ancient cities"
    
    attractions = get_attractions(['anuradhapura', 'sigiriya', 'polonnaruwa'])
    assert 'ancient_ruins' in attractions['anuradhapura'], "Should have cultural attractions"

