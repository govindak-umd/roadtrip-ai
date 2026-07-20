from backend.app.engines.cost_engine import calculate_trip_cost
from backend.app.models.trip import TripCostRequest, VehicleInput


def test_round_trip_cost() -> None:
    request = TripCostRequest(
        one_way_miles=200,
        round_trip=True,
        vehicle=VehicleInput(
            mpg=25,
            fuel_price_per_gallon=4.00,
        ),
    )

    result = calculate_trip_cost(request)

    assert result.total_miles == 400
    assert result.fuel_gallons == 16
    assert result.fuel_cost == 64