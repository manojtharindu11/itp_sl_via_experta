from __future__ import annotations

import pydeck as pdk

from .config import AppConfig


def get_base_map_and_style(cfg: AppConfig):
    """Return (base_layer_or_None, map_style_or_None).

    If Mapbox is configured, returns (None, mapbox_style) and sets the API key.
    Otherwise, returns (TileLayer, None) for OSM.
    """
    if cfg.use_mapbox and cfg.mapbox_token:
        try:
            pdk.settings.mapbox_api_key = cfg.mapbox_token  # type: ignore[attr-defined]
        except Exception:
            pass
        return None, (cfg.mapbox_style or "mapbox://styles/mapbox/streets-v11")

    base_map = pdk.Layer(
        "TileLayer",
        data=cfg.osm_tile_url,
        min_zoom=0,
        max_zoom=19,
        tile_size=256,
    )
    return base_map, None
