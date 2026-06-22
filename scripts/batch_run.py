import os
import sys

# Ambil path direktori root project (lastmile-engine)
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Daftarkan folder 'src' ke sys.path agar Python bisa langsung membaca isi di dalamnya
src_dir = os.path.join(root_dir, "src")
sys.path.append(src_dir)

from algorithms.exact import ExactSolver
from algorithms.greedy import GreedySolver
from config import SCENARIOS
from cost import (
    Timer,
    calculate_compute_cost,
    calculate_fuel_cost,
    calculate_tco,
    calculate_total_liters,
)
from graph import Graph


def format_currency(value: float) -> str:
    return f"Rp{value:,.0f}".replace(",", ".")


def main():
    data_dir = "data"

    if not os.path.exists(data_dir):
        print(f"Error: Folder '{data_dir}' tidak ditemukan.")
        return

    json_files = [
        f for f in os.listdir(data_dir) if f.endswith(".json") and f != ".gitkeep"
    ]
    json_files.sort()

    if not json_files:
        print("Tidak ada file dataset JSON di folder data.")
        return

    solvers = {
        "Greedy": GreedySolver(),
        "Exact": ExactSolver(),
    }

    # Menaikkan padding kolom pertama menjadi 30 agar teks panjang tidak merusak baris
    print(f"{'Dataset':<30} | {'Greedy TCO':<12} | {'Exact TCO':<12} | Winner")
    print("-" * 73)

    for file_name in json_files:
        file_path = os.path.join(data_dir, file_name)
        dataset_name = os.path.splitext(file_name)[0]

        try:
            graph = Graph(file_path)
        except Exception as e:
            print(f"{file_name:<30} | Error membaca file JSON.")
            continue

        for scenario_key, scenario_info in SCENARIOS.items():
            fuel_price = scenario_info["fuel_price"]
            compute_cost_per_ms = graph.params["compute_cost_per_ms"]

            tco_results = {}

            for solver_name, solver in solvers.items():
                route_result, elapsed = Timer.measure(solver.solve, graph, 0)

                total_liters = calculate_total_liters(
                    graph,
                    route_result["path"],
                    {
                        "consumption_full_load": graph.params["consumption_full_load"],
                        "consumption_empty": graph.params["consumption_empty"],
                    },
                )

                fuel_cost = calculate_fuel_cost(total_liters, fuel_price)
                compute_cost = calculate_compute_cost(elapsed, compute_cost_per_ms)
                tco = calculate_tco(fuel_cost, compute_cost)

                tco_results[solver_name] = tco

            winner = "Greedy" if tco_results["Greedy"] < tco_results["Exact"] else "Exact"
            display_name = f"{dataset_name} ({scenario_key})"

            # Cetak baris dengan padding 30 agar lurus kebawah
            print(
                f"{display_name:<30} | "
                f"{format_currency(tco_results['Greedy']):<12} | "
                f"{format_currency(tco_results['Exact']):<12} | "
                f"{winner}"
            )


if __name__ == "__main__":
    main()