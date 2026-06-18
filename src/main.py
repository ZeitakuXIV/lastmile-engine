import argparse

from algorithms.exact import ExactSolver
from algorithms.greedy import GreedySolver
from config import DEFAULT_DATA_PATH, SCENARIOS
from cost import (
    Timer,
    calculate_compute_cost,
    calculate_fuel_cost,
    calculate_tco,
    calculate_total_liters,
)
from graph import Graph


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Last-Mile Engine Simulation")
    parser.add_argument(
        "--scenario",
        choices=["subsidized", "crisis", "all"],
        default="all",
        help="Pilih skenario harga BBM",
    )
    parser.add_argument(
        "--data",
        default=DEFAULT_DATA_PATH,
        help="Path ke file dataset JSON",
    )
    return parser.parse_args()


def build_path_string(graph, path: list[int]) -> str:
    names = []
    for n in path:
        if n == 0:
            names.append(graph.hub["name"])
        else:
            names.append(graph.customers[n - 1]["name"])
    return " -> ".join(names)


def format_currency(value: float) -> str:
    return f"Rp{value:,.2f}"


def print_header(scenario_name: str, fuel_price: float):
    print(f"\n{'=' * 60}")
    print(f"  Skenario: {scenario_name}")
    print(f"  Harga BBM: {format_currency(fuel_price)}/liter")
    print(f"{'=' * 60}")


def print_result(
    name: str,
    path_str: str,
    distance: float,
    time_ms: float,
    fuel_cost: float,
    compute_cost: float,
    tco: float,
):
    print(f"\n  >> {name}")
    print(f"     Rute:     {path_str}")
    print(f"     Jarak:    {distance:.2f} km")
    print(f"     Waktu:    {time_ms:.4f} ms")
    print(f"     BBM:      {format_currency(fuel_cost)}")
    print(f"     Server:   {format_currency(compute_cost)}")
    print(f"     TCO:      {format_currency(tco)}")


def print_recommendation(results: list[dict]):
    winner = min(results, key=lambda x: x["tco"])
    print(
        f"\n  >> Rekomendasi: {winner['name']} (TCO terendah: {format_currency(winner['tco'])})"
    )


def run_scenario(
    graph, scenario_name: str, fuel_price: float, compute_cost_per_ms: float
):
    print_header(scenario_name, fuel_price)

    solvers = [
        ("Greedy NN", GreedySolver()),
        ("Exact", ExactSolver()),
    ]

    results = []
    for name, solver in solvers:
        route_result, elapsed = Timer.measure(solver.solve, graph, 0)
        path_str = build_path_string(graph, route_result["path"])
        distance = route_result["distance_km"]

        total_liters = calculate_total_liters(
            graph,
            route_result["path"],
            {"consumption_full_load": 0.05, "consumption_empty": 0.02},
        )
        fuel_cost = calculate_fuel_cost(total_liters, fuel_price)
        compute_cost = calculate_compute_cost(elapsed, compute_cost_per_ms)
        tco = calculate_tco(fuel_cost, compute_cost)

        print_result(name, path_str, distance, elapsed, fuel_cost, compute_cost, tco)
        results.append({"name": name, "tco": tco})

    print_recommendation(results)


def main():
    args = parse_args()
    graph = Graph(args.data)

    for key, info in SCENARIOS.items():
        if args.scenario == "all" or args.scenario == key:
            run_scenario(
                graph,
                info["name"],
                info["fuel_price"],
                graph.params["compute_cost_per_ms"],
            )


if __name__ == "__main__":
    main()
