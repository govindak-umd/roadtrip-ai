from backend.app.models.trip import TripCostRequest, TripCostResponse


def calculate_trip_cost(request: TripCostRequest) -> TripCostResponse:
    distance_multiplier = 2 if request.round_trip else 1

    total_miles = request.one_way_miles * distance_multiplier
    fuel_gallons = total_miles / request.vehicle.mpg
    fuel_cost = fuel_gallons * request.vehicle.fuel_price_per_gallon

    return TripCostResponse(
        one_way_miles=round(request.one_way_miles, 1),
        total_miles=round(total_miles, 1),
        fuel_gallons=round(fuel_gallons, 2),
        fuel_cost=round(fuel_cost, 2),
    )