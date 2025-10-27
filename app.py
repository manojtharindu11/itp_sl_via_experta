import os
import sys
import streamlit as st
import pandas as pd
import pydeck as pdk
import subprocess

# Ensure app folder is on sys.path for clean imports
_app_dir = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, _app_dir)

from utils.config import get_config
from utils.map_layers import get_base_map_and_style
from query import recommend_trip_py, get_city_coords, get_attractions, get_all_cities, city_exists

st.set_page_config(page_title="ITP-SL: Sri Lanka Travel Expert", page_icon="🇱🇰", layout="wide")
CFG = get_config()

st.title("Intelligent Travel Planner — Sri Lanka")
st.caption("Experta-powered recommendations with interactive maps")

with st.sidebar:
    st.header("Trip preferences")
    season = st.selectbox("Season", ["winter", "summer", "all_year"], index=0)
    budget = st.selectbox("Budget", ["budget", "moderate", "high", "variable"], index=1)
    # Fetch cities from the Experta-backed knowledge module for safer selection
    cities = get_all_cities() or ["colombo", "kandy", "ella"]
    start = st.selectbox("Start city", cities, index=cities.index("colombo") if "colombo" in cities else 0)
    end = st.selectbox("End city", cities, index=cities.index("ella") if "ella" in cities else 0)
    show_attractions = st.checkbox("Show attractions on map", value=True)
    go = st.button("Find Route")

st.markdown("---")

if go:
    with st.spinner("Building your route..."):
        try:
            # Validate cities just in case
            if not city_exists(start) or not city_exists(end):
                st.error("Unknown start or end city. Please pick from the list.")
                st.stop()
            recs = recommend_trip_py(season, budget, start, end)
        except Exception as e:
            st.error('Reasoning error. Ensure the knowledge module is available and inputs are valid.')
            st.code(str(e))
            recs = []

    if not recs:
        st.error("No recommendations found. Try adjusting season/budget/cities.")
    else:
        rec = recs[0]
        route = rec.get('route', [])
        distance = rec.get('distance', None)

        st.subheader("Suggested route")
        cols = st.columns([3,1])
        with cols[0]:
            st.write(" → ".join(route))
        with cols[1]:
            if distance is not None:
                st.metric("Total distance", f"{distance} km")

        coords = get_city_coords(route)
        if show_attractions:
            city_atts = get_attractions(route)
        else:
            city_atts = {c: [] for c in route}

        points = []
        lines = []
        for i, city in enumerate(route):
            c = coords.get(city)
            if not c:
                continue
            points.append({
                "name": city,
                "lat": c['lat'],
                "lon": c['lon'],
                "attractions": ", ".join(city_atts.get(city, [])) or "—"
            })
            if i < len(route)-1:
                ncity = route[i+1]
                nc = coords.get(ncity)
                if nc:
                    lines.append({
                        "from_lat": c['lat'], "from_lon": c['lon'],
                        "to_lat": nc['lat'], "to_lon": nc['lon']
                    })

        # Prepare data frames (can be empty)
        df_points = pd.DataFrame(points) if points else pd.DataFrame(columns=["name","lat","lon","attractions"]) 
        df_lines = pd.DataFrame(lines) if lines else pd.DataFrame(columns=["from_lat","from_lon","to_lat","to_lon"]) 

        # Fallback to a Sri Lanka-centered view if we don't have points
        if not df_points.empty:
            center_lat, center_lon = df_points['lat'].mean(), df_points['lon'].mean()
            zoom = 7
        else:
            center_lat, center_lon = 7.8731, 80.7718  # Sri Lanka centroid
            zoom = 6.5

        st.subheader("Map view")
        # Base map: OSM by default, Mapbox if configured via .env
        base_map, map_style = get_base_map_and_style(CFG)

        city_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_points,
            get_position='[lon, lat]',
            get_radius=4000,
            get_color='[0, 136, 204, 200]',
            pickable=True,
        )

        line_layer = pdk.Layer(
            "LineLayer",
            data=df_lines,
            get_source_position='[from_lon, from_lat]',
            get_target_position='[to_lon, to_lat]',
            get_color='[220, 20, 60, 220]',  # crimson
            get_width=4,
            pickable=False,
        )

        deck = pdk.Deck(
            map_style=map_style,  # None uses OSM TileLayer; Mapbox style if token configured
            initial_view_state=pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=zoom, pitch=30),
            layers=[l for l in [base_map, line_layer, city_layer] if l is not None],
            tooltip={"text": "{name}\n{attractions}"}
        )
        st.pydeck_chart(deck)

        with st.expander("Why these suggestions?"):
            st.markdown(
                f"- Season fit: prioritizes destinations with best season = `{season}`\n"
                f"- Budget fit: tries destinations with budget = `{budget}`\n"
                f"- Route: built from known inter-city distances\n"
                f"- Data source: Experta-based knowledge module in `app/experta_kb.py` (Prolog KB archived)"
            )
else:
    st.info("Set your preferences in the sidebar and click 'Find Route'")
