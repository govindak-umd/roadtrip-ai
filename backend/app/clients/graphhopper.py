from typing import Any

import httpx


class GraphHopperClient:
    ROUTE_URL = "https://graphhopper.com/api/1/route"
    GEOCODE_URL = "https://graphhopper.com/api/1/geocode"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def get_route(
            self,
            points: list[tuple[float, float]],
    ) -> dict[str, Any]:
        if len(points) < 2:
            raise ValueError("A route requires at least two points.")

        params: list[tuple[str, str]] = []

        for latitude, longitude in points:
            params.append(
                ("point", f"{latitude},{longitude}")
            )

        params.extend(
            [
                ("profile", "car"),
                ("locale", "en"),
                ("calc_points", "true"),
                ("points_encoded", "false"),
                ("instructions", "false"),
                ("key", self.api_key),
            ]
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                self.ROUTE_URL,
                params=params,
            )
            response.raise_for_status()
            data = response.json()

        paths = data.get("paths", [])

        if not paths:
            message = data.get(
                "message",
                "GraphHopper could not find a route.",
            )
            raise ValueError(message)

        return paths[0]

    async def geocode(
        self,
        query: str,
    ) -> dict[str, Any]:
        params = {
            "q": query,
            "locale": "en",
            "limit": 1,
            "key": self.api_key,
        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                self.GEOCODE_URL,
                params=params,
            )
            response.raise_for_status()
            data = response.json()

        hits = data.get("hits", [])

        if not hits:
            raise ValueError(
                f'No location was found for "{query}".'
            )

        return hits[0]