# ITP-SL — Intelligent Travel Planning (Sri Lanka)

This project demonstrates an expert-system-backed travel recommender for Sri Lanka using **Experta**.
The original Prolog-based KB has been migrated to a Python implementation (`app/experta_kb.py`).

## How It Works

The intelligent travel planner uses an **Experta-based expert system** to recommend optimal routes through Sri Lanka based on your preferences:

### Season Selection

The system recognizes Sri Lanka's monsoon patterns and recommends destinations based on three seasonal categories:

- **Winter (November - February)**: Best for south and west coast beaches

  - Recommended cities: Mirissa, Galle, Bentota, Matara, Yala National Park
  - Avoid: East coast (affected by northeast monsoon)

- **Summer (May - August)**: Best for east coast and hill country

  - Recommended cities: Trincomalee, Arugam Bay, Jaffna, Ella, Badulla
  - Avoid: West/south coast (southwest monsoon season)

- **All Year**: Destinations that work year-round
  - Recommended cities: Kandy, Nuwara Eliya, Anuradhapura, Sigiriya, Polonnaruwa, Dambulla, Horton Plains

### Budget Categories

The system filters destinations based on your budget preference:

- **Budget**: Affordable destinations for backpackers and budget travelers

  - Examples: Ella, Negombo, Anuradhapura, Polonnaruwa, Dambulla, Arugam Bay, Matara, Badulla
  - Lower accommodation costs, local transport options

- **Moderate**: Mid-range destinations with good value

  - Examples: Kandy, Mirissa, Galle, Bentota, Sigiriya, Trincomalee, Jaffna
  - Mix of comfort and affordability

- **High**: Premium destinations with luxury options

  - Examples: Nuwara Eliya (hill station luxury)
  - Upscale hotels, boutique accommodations

- **Variable**: Destinations that cater to all budget levels
  - Examples: Colombo
  - Options available across all price ranges

### Route Planning

1. **Start & End Cities**: Select your starting point and destination from 20+ Sri Lankan cities
2. **Expert System Reasoning**: The Experta engine:
   - Filters cities by season compatibility (using `best_season` facts)
   - Matches budget preferences (using `budget` facts)
   - Fires rules to assert recommended destinations
3. **Shortest Path Calculation**: Uses Dijkstra's algorithm on the distance graph to find the optimal route
4. **Attractions**: Each city includes notable attractions (temples, natural wonders, wildlife, beaches)

### Example Scenarios

**Scenario 1: Budget Winter Beach Trip**

- Season: Winter
- Budget: Budget
- Start: Colombo → End: Matara
- Result: Route through budget-friendly south coast beaches during the best season

**Scenario 2: Summer Hill Country Adventure**

- Season: Summer
- Budget: Moderate
- Start: Colombo → End: Ella
- Result: Scenic route through Kandy and hill stations, avoiding monsoon-affected areas

**Scenario 3: All-Year Cultural Tour**

- Season: All Year
- Budget: Moderate
- Start: Colombo → End: Anuradhapura
- Result: Cultural triangle route through ancient cities, reliable weather year-round

The system calculates total distance, shows routes on an interactive map, and displays relevant attractions for each city on your itinerary.

Prerequisites

- Python 3.8+
- Streamlit and Experta (installed via requirements.txt)

Files

- `app/experta_kb.py`: Experta-based knowledge module (current KB)
- `app/query.py`: Adapter that exposes helper functions for the UI/tests
- `app.py`: Streamlit UI that uses the Experta KB and shows an interactive map

Quick run

Install dependencies (recommended in a virtual environment):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the Streamlit app:

```powershell
streamlit run app.py
```

Open http://localhost:8501 in your browser. Press Ctrl+C to stop the app.

Run tests (optional):

```powershell
pytest test/test_.py -v
```

## Test Suite

The project includes **23 comprehensive test cases** covering:

### Season-based Tests (3 tests)

- Winter beach destinations (Mirissa, Galle)
- Summer east coast destinations (Arugam Bay)
- All-year destinations (Kandy, cultural sites)

### Budget-based Tests (3 tests)

- Budget-friendly routes (Ella)
- High-end destinations (Nuwara Eliya)
- Variable budget handling (Colombo)

### Route Planning Tests (4 tests)

- Standard route calculations (Colombo → Ella)
- Distance calculations and validation
- Same start/end city handling
- Unreachable destinations with strict filters

### Helper Function Tests (6 tests)

- City listing and existence checks
- Coordinate retrieval and validation
- Attraction data retrieval
- Invalid city handling

### Edge Cases & Error Handling (3 tests)

- Invalid season/budget parameters
- Empty route scenarios
- Multiple route options

### Integration Tests (3 tests)

- Full winter beach trip scenario
- Complete hill country tour
- Cultural triangle exploration

**All tests pass ✅** — Run with `pytest test/test_.py -v` to verify.

Environment variables (.env)

You can configure paths and tokens without hardcoding them. Copy the sample and edit as needed:

```powershell
Copy-Item .env.example .env
# then edit .env in your editor
```

Supported variables:

- `USE_MAPBOX`: `true` to use Mapbox basemap in the UI; otherwise OpenStreetMap tiles are used.
- `MAPBOX_TOKEN`: Your Mapbox access token (required if `USE_MAPBOX=true`).
- `MAPBOX_STYLE`: Mapbox style URI, defaults to `mapbox://styles/mapbox/streets-v11`.
- `OSM_TILE_URL`: Custom OSM tile URL template if you host your own tiles.

Notes

- The canonical knowledge base is `app/experta_kb.py`; extend it by editing the data structures or adding Experta rules.
