from pydantic import BaseModel, Field


class VehicleInput(BaseModel):
    mpg: float = Field(gt=0)
    fuel_price_per_gallon: float = Field(ge=0)


class TripCostRequest(BaseModel):
    one_way_miles: float = Field(ge=0)
    round_trip: bool = True
    vehicle: VehicleInput


class TripCostResponse(BaseModel):
    one_way_miles: float
    total_miles: float
    fuel_gallons: float
    fuel_cost: float

from pydantic import BaseModel, Field


class Coordinate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class TripEstimateRequest(BaseModel):
    start: Coordinate
    destination: Coordinate
    round_trip: bool = True
    vehicle: VehicleInput


class TripEstimateResponse(BaseModel):
    one_way_miles: float
    total_miles: float
    one_way_minutes: float
    total_minutes: float
    fuel_gallons: float
    fuel_cost: float

class LocationInput(BaseModel):
    query: str = Field(min_length=2)


class AddressTripEstimateRequest(BaseModel):
    start: LocationInput
    destination: LocationInput
    round_trip: bool = True
    vehicle: VehicleInput


class GeocodedLocation(BaseModel):
    name: str
    latitude: float
    longitude: float


class AddressTripEstimateResponse(BaseModel):
    start: GeocodedLocation
    destination: GeocodedLocation
    one_way_miles: float
    total_miles: float
    one_way_minutes: float
    total_minutes: float
    fuel_gallons: float
    fuel_cost: float

class MultiStopTripRequest(BaseModel):
    start: LocationInput
    destination: LocationInput
    stops: list[LocationInput] = Field(default_factory=list)
    round_trip: bool = True
    vehicle: VehicleInput


class MultiStopTripResponse(BaseModel):
    start: GeocodedLocation
    stops: list[GeocodedLocation]
    destination: GeocodedLocation

    direct_one_way_miles: float
    direct_total_miles: float
    direct_one_way_minutes: float
    direct_total_minutes: float
    direct_fuel_cost: float

    route_one_way_miles: float
    route_total_miles: float
    route_one_way_minutes: float
    route_total_minutes: float
    route_fuel_gallons: float
    route_fuel_cost: float

    added_miles: float
    added_minutes: float
    added_fuel_gallons: float
    added_fuel_cost: float