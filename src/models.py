from dataclasses import dataclass
from typing import List


@dataclass
class Location:
    id: int
    name: str
    lat: float
    lng: float


@dataclass
class Package:
    location_id: int
    weight_kg: float


@dataclass
class Route:
    path: List[int]
    distance_km: float
    time_ms: float


@dataclass
class ScenarioParams:
    fuel_price_per_liter: float
    compute_cost_per_ms: float
    consumption_full_load: float
    consumption_empty: float


@dataclass
class ScenarioResult:
    scenario_name: str
    algorithm_name: str
    route: Route
    fuel_cost: float
    compute_cost: float
    tco: float
