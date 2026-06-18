from abc import ABC, abstractmethod
from typing import Any


class Solver(ABC):
    @abstractmethod
    def solve(self, graph: Any, start_idx: int = 0) -> Any:
        """
        Cari rute optimal

        Input:
            graph: representasi graf dari problem
            start_idx: indeks node awal (default: 0)

        Output:
            dict dengan key:
                'path': list indeks node yang membentuk rute optimal
                'distance_km': total jarak dalam kilometer dari rute optimal
                'time_ms': total waktu dalam milidetik dari rute optimal
        """
