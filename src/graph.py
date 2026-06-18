import json


class Graph:
    def __init__(self, filepath: str):
        # load data dari locations.json
        with open(filepath, "r") as f:
            data = json.load(f)

        self.node_count = 1 + len(data["customers"])
        self.adj_matrix = data["distance_matrix"]
        self.hub = data["hub"]
        self.customers = data["customers"]

        # map berat paket dari pelanggan
        self.packages = {c["id"]: c["package_weight_kg"] for c in data["customers"]}
        self.params = data["params"]

    def distance(self, i: int, j: int) -> float:
        return self.adj_matrix[i][j]

    def get_package_weight(self, loc_id: int) -> float:
        if loc_id == 0:
            return 0.0
        return self.packages.get(loc_id, 0.0)

    def total_customers(self) -> int:
        return self.node_count - 1
