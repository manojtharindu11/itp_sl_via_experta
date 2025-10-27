from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # It's fine if dotenv isn't installed or .env doesn't exist
    pass


@dataclass(frozen=True)
class AppConfig:
    osm_tile_url: str = "https://c.tile.openstreetmap.org/{z}/{x}/{y}.png"
    use_mapbox: bool = False
    mapbox_token: Optional[str] = None
    mapbox_style: Optional[str] = None


def str_to_bool(val: Optional[str], default: bool = False) -> bool:
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}


def get_config() -> AppConfig:
    return AppConfig(
        osm_tile_url=os.getenv("OSM_TILE_URL", AppConfig.osm_tile_url),
        use_mapbox=str_to_bool(os.getenv("USE_MAPBOX"), False),
        mapbox_token=os.getenv("MAPBOX_TOKEN"),
        mapbox_style=os.getenv("MAPBOX_STYLE") or "mapbox://styles/mapbox/streets-v11",
    )
