import httpx
from fastapi import FastAPI, HTTPException

from backend.app.clients.graphhopper import GraphHopperClient
from backend.app.config import get_settings
from backend.app.engines.cost_engine import calculate_trip_cost
from backend.app.models.trip import (
    AddressTripEstimateRequest,
    AddressTripEstimateResponse,
    TripCostRequest,
    TripCostResponse,
    TripEstimateRequest,
    TripEstimateResponse,
    MultiStopTripRequest,
    MultiStopTripResponse,
)
from backend.app.services.routing import (
    estimate_multi_stop_trip,
    estimate_trip,
    estimate_trip_from_addresses,
)

app = FastAPI(
    title="RoadTrip AI",
    version="0.2.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/trip/cost", response_model=TripCostResponse)
def estimate_trip_cost(
    request: TripCostRequest,
) -> TripCostResponse:
    return calculate_trip_cost(request)


@app.post("/trip/estimate", response_model=TripEstimateResponse)
async def estimate_trip_route(
    request: TripEstimateRequest,
) -> TripEstimateResponse:
    settings = get_settings()

    graphhopper_client = GraphHopperClient(
        api_key=settings.graphhopper_api_key
    )

    try:
        return await estimate_trip(
            request=request,
            graphhopper_client=graphhopper_client,
        )

    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code

        if status_code == 401:
            detail = "GraphHopper rejected the API key."
        elif status_code == 429:
            detail = "GraphHopper usage limit has been reached."
        else:
            detail = f"GraphHopper returned HTTP {status_code}."

        raise HTTPException(
            status_code=502,
            detail=detail,
        ) from exc

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to GraphHopper.",
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

@app.post(
    "/trip/estimate-by-address",
    response_model=AddressTripEstimateResponse,
)
async def estimate_trip_by_address(
    request: AddressTripEstimateRequest,
) -> AddressTripEstimateResponse:
    settings = get_settings()

    graphhopper_client = GraphHopperClient(
        api_key=settings.graphhopper_api_key
    )

    try:
        return await estimate_trip_from_addresses(
            request=request,
            graphhopper_client=graphhopper_client,
        )

    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code

        if status_code == 401:
            detail = "GraphHopper rejected the API key."
        elif status_code == 429:
            detail = "GraphHopper usage limit has been reached."
        else:
            detail = f"GraphHopper returned HTTP {status_code}."

        raise HTTPException(
            status_code=502,
            detail=detail,
        ) from exc

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to GraphHopper.",
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

@app.post(
    "/trip/estimate-with-stops",
    response_model=MultiStopTripResponse,
)
async def estimate_trip_with_stops(
    request: MultiStopTripRequest,
) -> MultiStopTripResponse:
    settings = get_settings()

    graphhopper_client = GraphHopperClient(
        api_key=settings.graphhopper_api_key
    )

    try:
        return await estimate_multi_stop_trip(
            request=request,
            graphhopper_client=graphhopper_client,
        )

    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code

        if status_code == 401:
            detail = "GraphHopper rejected the API key."
        elif status_code == 429:
            detail = "GraphHopper usage limit has been reached."
        else:
            detail = f"GraphHopper returned HTTP {status_code}."

        raise HTTPException(
            status_code=502,
            detail=detail,
        ) from exc

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to GraphHopper.",
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc