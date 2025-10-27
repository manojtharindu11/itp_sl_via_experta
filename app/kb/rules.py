"""Expert system rules for travel recommendations using Experta.

This module contains the inference engine and rule definitions for
the intelligent travel planning system.
"""
from typing import List, Set
try:
    from experta import KnowledgeEngine, Fact, Rule, MATCH, OR, AND, NOT, AS
    EXPERTA_AVAILABLE = True
except ImportError:
    EXPERTA_AVAILABLE = False

from app.kb.entities import Season, BudgetLevel, Region
from app.kb.data import get_city, get_all_cities


if EXPERTA_AVAILABLE:
    
    class TravelRecommendationEngine(KnowledgeEngine):
        """
        Expert system for travel recommendations.
        
        The engine uses forward chaining to infer recommended destinations
        based on traveler preferences and domain knowledge.
        """
        
        def __init__(self):
            super().__init__()
            self.recommended_cities: Set[str] = set()
            self.avoided_cities: Set[str] = set()
            self.preferred_cities: Set[str] = set()
        
        # =========== Season-based Recommendation Rules ===========
        
        @Rule(
            Fact(preference='season', value=MATCH.season),
            Fact(city=MATCH.city, best_season=MATCH.city_season)
        )
        def recommend_exact_season_match(self, season, city, city_season):
            """Recommend cities with exact season match."""
            if season == city_season:
                self.declare(Fact(recommended=city, reason='perfect_season_match'))
                self.recommended_cities.add(city)
        
        @Rule(
            Fact(preference='season', value=Season.ALL_YEAR.value),
            Fact(city=MATCH.city)
        )
        def recommend_all_year_for_any_season(self, city):
            """All-year cities work for any season preference."""
            city_obj = get_city(city)
            if city_obj and city_obj.best_season == Season.ALL_YEAR:
                self.declare(Fact(recommended=city, reason='all_year_destination'))
                self.recommended_cities.add(city)
        
        @Rule(
            Fact(preference='season', value='winter'),
            Fact(city=MATCH.city, region=Region.EAST.value)
        )
        def avoid_east_coast_in_winter(self, city):
            """Avoid east coast during winter (NE monsoon)."""
            self.declare(Fact(avoided=city, reason='northeast_monsoon'))
            self.avoided_cities.add(city)
        
        @Rule(
            Fact(preference='season', value='summer'),
            Fact(city=MATCH.city, region=OR(Region.WEST.value, Region.SOUTH.value))
        )
        def avoid_west_south_in_summer(self, city):
            """Avoid west/south coast during summer (SW monsoon)."""
            city_obj = get_city(city)
            if city_obj and city_obj.best_season != Season.ALL_YEAR:
                self.declare(Fact(avoided=city, reason='southwest_monsoon'))
                self.avoided_cities.add(city)
        
        # =========== Budget-based Recommendation Rules ===========
        
        @Rule(
            Fact(preference='budget', value=MATCH.budget),
            Fact(city=MATCH.city, budget_level=MATCH.city_budget)
        )
        def recommend_budget_match(self, budget, city, city_budget):
            """Recommend cities matching budget preference."""
            if budget == city_budget or city_budget == BudgetLevel.VARIABLE.value:
                self.declare(Fact(budget_appropriate=city))
        
        @Rule(
            Fact(preference='budget', value=BudgetLevel.VARIABLE.value),
            Fact(city=MATCH.city)
        )
        def all_budgets_for_variable(self, city):
            """Variable budget accepts all destinations."""
            self.declare(Fact(budget_appropriate=city))
        
        @Rule(
            Fact(preference='budget', value=BudgetLevel.BUDGET.value),
            Fact(city=MATCH.city, budget_level=BudgetLevel.HIGH.value)
        )
        def avoid_expensive_for_budget(self, city):
            """Budget travelers should avoid high-cost destinations."""
            if city not in self.recommended_cities:
                self.declare(Fact(budget_mismatch=city))
        
        # =========== Preference-based Rules ===========
        
        @Rule(
            Fact(preference='interests', value=MATCH.interest),
            Fact(city=MATCH.city, city_type=MATCH.city_type)
        )
        def recommend_by_interest(self, interest, city, city_type):
            """Recommend cities matching traveler interests."""
            interest_map = {
                'beach': 'beach',
                'culture': 'cultural',
                'history': 'historical',
                'nature': 'national_park',
                'hiking': 'hill_country',
            }
            if interest_map.get(interest) == city_type:
                self.declare(Fact(interest_match=city))
                self.preferred_cities.add(city)
        
        # =========== Combined Recommendation Rules ===========
        
        @Rule(
            Fact(recommended=MATCH.city),
            Fact(budget_appropriate=MATCH.city),
            NOT(Fact(avoided=MATCH.city))
        )
        def final_recommendation(self, city):
            """City passes all filters - final recommendation."""
            self.declare(Fact(final_recommended=city))
        
        @Rule(
            Fact(recommended=MATCH.city),
            Fact(budget_appropriate=MATCH.city),
            Fact(interest_match=MATCH.city),
            NOT(Fact(avoided=MATCH.city))
        )
        def preferred_recommendation(self, city):
            """City matches all criteria including interests - highly recommended."""
            self.declare(Fact(highly_recommended=city))
        
        def get_recommendations(self) -> dict:
            """Get categorized recommendations."""
            final = set()
            highly = set()
            
            for fact in self.facts.values():
                if isinstance(fact, Fact):
                    if fact.get('final_recommended'):
                        final.add(fact['final_recommended'])
                    if fact.get('highly_recommended'):
                        highly.add(fact['highly_recommended'])
            
            return {
                'recommended': self.recommended_cities - self.avoided_cities,
                'highly_recommended': highly,
                'avoided': self.avoided_cities,
                'all_final': final
            }


def create_engine_with_preferences(season: str, budget: str, interests: List[str] = None) -> 'TravelRecommendationEngine':
    """
    Create and initialize an expert system engine with user preferences.
    
    Args:
        season: Preferred travel season (winter/summer/all_year)
        budget: Budget level (budget/moderate/high/variable)
        interests: List of interests (beach, culture, history, nature, hiking)
    
    Returns:
        Initialized and run TravelRecommendationEngine
    """
    if not EXPERTA_AVAILABLE:
        return None
    
    engine = TravelRecommendationEngine()
    engine.reset()
    
    # Declare user preferences
    engine.declare(Fact(preference='season', value=season))
    engine.declare(Fact(preference='budget', value=budget))
    
    if interests:
        for interest in interests:
            engine.declare(Fact(preference='interests', value=interest))
    
    # Declare all city facts
    for city in get_all_cities():
        engine.declare(Fact(
            city=city.name,
            best_season=city.best_season.value,
            budget_level=city.budget_level.value,
            city_type=city.city_type.value,
            region=city.region.value
        ))
    
    # Run inference
    engine.run()
    
    return engine
