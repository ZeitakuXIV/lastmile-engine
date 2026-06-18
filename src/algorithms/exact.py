from algorithms.base import Solver


class ExactSolver(Solver):
    def solve(self, graph, start_idx: int = 0) -> dict:
        return {"path": [0], "distance_km": 0.0, "time_ms": 0.0}
