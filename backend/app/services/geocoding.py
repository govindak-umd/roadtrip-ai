from typing import Any

from backend.app.clients.graphhopper import GraphHopperClient
from backend.app.models.trip import GeocodedLocation


def build_location_name(hit: dict[str, Any]) -> str:
    parts = [
        hit.get("name"),
        hit.get("city"),
        hit.get("state"),
        hit.get("country"),
    ]

    unique_parts: list[str] = []

    for part in parts:
        if part and part not in unique_parts:
            unique_parts.append(part)

    return ", ".join(unique_parts)


async def geocode_location(
    query: str,
    graphhopper_client: GraphHopperClient,
) -> GeocodedLocation:
    hit = await graphhopper_client.geocode(query)

    point = hit.get("point")

    if not point:
        raise ValueError(
            f'GraphHopper returned no coordinates for "{query}".'
        )

    return GeocodedLocation(
        name=build_location_name(hit),
        latitude=point["lat"],
        longitude=point["lng"],
    )