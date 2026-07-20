from backend.app.clients.graphhopper import GraphHopperClient
from backend.app.engines.cost_engine import calculate_trip_cost
from backend.app.models.trip import (
    AddressTripEstimateRequest,
    AddressTripEstimateResponse,
    Coordinate,
    GeocodedLocation,
    MultiStopTripRequest,
    MultiStopTripResponse,
    TripCostRequest,
    TripEstimateRequest,
    TripEstimateResponse,
)
from backend.app.services.geocoding import geocode_location


METERS_PER_MILE = 1609.344
MILLISECONDS_PER_MINUTE = 60_000


async def estimate_trip(
    request: TripEstimateRequest,
    graphhopper_client: GraphHopperClient,
) -> TripEstimateResponse:
    route = await graphhopper_client.get_route(
        points=[
            (
                request.start.latitude,
                request.start.longitude,
            ),
            (
                request.destination.latitude,
                request.destination.longitude,
            ),
        ]
    )
    one_way_miles = route["distance"] / METERS_PER_MILE
    one_way_minutes = route["time"] / MILLISECONDS_PER_MINUTE

    cost = calculate_trip_cost(
        TripCostRequest(
            one_way_miles=one_way_miles,
            round_trip=request.round_trip,
            vehicle=request.vehicle,
        )
    )

    trip_multiplier = 2 if request.round_trip else 1

    return TripEstimateResponse(
        one_way_miles=round(one_way_miles, 1),
        total_miles=cost.total_miles,
        one_way_minutes=round(one_way_minutes, 1),
        total_minutes=round(one_way_minutes * trip_multiplier, 1),
        fuel_gallons=cost.fuel_gallons,
        fuel_cost=cost.fuel_cost,
    )
async def estimate_trip_from_addresses(
    request: AddressTripEstimateRequest,
    graphhopper_client: GraphHopperClient,
) -> AddressTripEstimateResponse:
    start = await geocode_location(
        query=request.start.query,
        graphhopper_client=graphhopper_client,
    )

    destination = await geocode_location(
        query=request.destination.query,
        graphhopper_client=graphhopper_client,
    )

    coordinate_request = TripEstimateRequest(
        start=Coordinate(
            latitude=start.latitude,
            longitude=start.longitude,
        ),
        destination=Coordinate(
            latitude=destination.latitude,
            longitude=destination.longitude,
        ),
        round_trip=request.round_trip,
        vehicle=request.vehicle,
    )

    estimate = await estimate_trip(
        request=coordinate_request,
        graphhopper_client=graphhopper_client,
    )

    return AddressTripEstimateResponse(
        start=start,
        destination=destination,
        one_way_miles=estimate.one_way_miles,
        total_miles=estimate.total_miles,
        one_way_minutes=estimate.one_way_minutes,
        total_minutes=estimate.total_minutes,
        fuel_gallons=estimate.fuel_gallons,
        fuel_cost=estimate.fuel_cost,
    )

async def estimate_multi_stop_trip(
    request: MultiStopTripRequest,
    graphhopper_client: GraphHopperClient,
) -> MultiStopTripResponse:
    start = await geocode_location(
        query=request.start.query,
        graphhopper_client=graphhopper_client,
    )

    destination = await geocode_location(
        query=request.destination.query,
        graphhopper_client=graphhopper_client,
    )

    stops: list[GeocodedLocation] = []

    for stop_input in request.stops:
        stop = await geocode_location(
            query=stop_input.query,
            graphhopper_client=graphhopper_client,
        )
        stops.append(stop)

    direct_points = [
        (start.latitude, start.longitude),
        (destination.latitude, destination.longitude),
    ]

    route_points = [
        (start.latitude, start.longitude),
        *[
            (stop.latitude, stop.longitude)
            for stop in stops
        ],
        (destination.latitude, destination.longitude),
    ]

    direct_route = await graphhopper_client.get_route(
        points=direct_points
    )

    selected_route = await graphhopper_client.get_route(
        points=route_points
    )

    direct_one_way_miles = (
        direct_route["distance"] / METERS_PER_MILE
    )
    direct_one_way_minutes = (
        direct_route["time"] / MILLISECONDS_PER_MINUTE
    )

    route_one_way_miles = (
        selected_route["distance"] / METERS_PER_MILE
    )
    route_one_way_minutes = (
        selected_route["time"] / MILLISECONDS_PER_MINUTE
    )

    direct_cost = calculate_trip_cost(
        TripCostRequest(
            one_way_miles=direct_one_way_miles,
            round_trip=request.round_trip,
            vehicle=request.vehicle,
        )
    )

    route_cost = calculate_trip_cost(
        TripCostRequest(
            one_way_miles=route_one_way_miles,
            round_trip=request.round_trip,
            vehicle=request.vehicle,
        )
    )

    multiplier = 2 if request.round_trip else 1

    direct_total_minutes = (
        direct_one_way_minutes * multiplier
    )
    route_total_minutes = (
        route_one_way_minutes * multiplier
    )

    added_miles = (
        route_cost.total_miles - direct_cost.total_miles
    )
    added_minutes = (
        route_total_minutes - direct_total_minutes
    )
    added_fuel_gallons = (
        route_cost.fuel_gallons
        - direct_cost.fuel_gallons
    )
    added_fuel_cost = (
        route_cost.fuel_cost
        - direct_cost.fuel_cost
    )

    return MultiStopTripResponse(
        start=start,
        stops=stops,
        destination=destination,

        direct_one_way_miles=round(
            direct_one_way_miles,
            1,
        ),
        direct_total_miles=direct_cost.total_miles,
        direct_one_way_minutes=round(
            direct_one_way_minutes,
            1,
        ),
        direct_total_minutes=round(
            direct_total_minutes,
            1,
        ),
        direct_fuel_cost=direct_cost.fuel_cost,

        route_one_way_miles=round(
            route_one_way_miles,
            1,
        ),
        route_total_miles=route_cost.total_miles,
        route_one_way_minutes=round(
            route_one_way_minutes,
            1,
        ),
        route_total_minutes=round(
            route_total_minutes,
            1,
        ),
        route_fuel_gallons=route_cost.fuel_gallons,
        route_fuel_cost=route_cost.fuel_cost,

        added_miles=round(added_miles, 1),
        added_minutes=round(added_minutes, 1),
        added_fuel_gallons=round(
            added_fuel_gallons,
            2,
        ),
        added_fuel_cost=round(
            added_fuel_cost,
            2,
        ),
    )