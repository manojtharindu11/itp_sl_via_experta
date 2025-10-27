"""Unit tests updated to use the Experta-based KB directly.

These tests no longer require SWI-Prolog and instead call the Python
implementation in `app.experta_kb`.
"""
from app.experta_kb import recommend_trip, get_all_cities


def test_recommend_mirissa_winter():
    # Recommend trips for winter with moderate budget and explicit end mirissa
    res = recommend_trip('winter', 'moderate', 'colombo', 'mirissa')
    assert any(r for r in res if r.get('route') and r['route'][-1] == 'mirissa')


def test_route_colombo_ella():
    res = recommend_trip('all_year', 'budget', 'colombo', 'ella')
    assert any(r for r in res if 'colombo' in r.get('route', []) and 'ella' in r.get('route', []))
