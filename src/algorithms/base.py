from abc import ABC, abstractmethod


class Solver(ABC):
    @abstractmethod
    def solve(self, graph, start_idx: int = 0) -> dict:
        """Cari rute optimal dari start_idx kembali ke start_idx.

        Input:
            graph       -> objek Graph (graph.py)
            start_idx   -> int, index node awal (default: 0 = hub)

        Output:
            dict {
                "path": list[int],       # urutan node yang dikunjungi
                "distance_km": float,    # total jarak rute (km)
                "time_ms": float         # diisi 0, diukur otomatis
            }
        """
