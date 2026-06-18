# Contracts

## Person 1 — Dataset

Edit `data/locations.json`. Jangan ubah struktur atau key, hanya isi nilainya.

### Lokasi
- **1 hub** + **12 pelanggan** real (nama, latitude, longitude)
- Ambil koordinat dari Google Maps

### Matriks Jarak
- Array 2D 13×13, baris = kolom = index node
- Index `0` = hub, index `1-12` = pelanggan sesuai urutan di `customers[]`
- Isi dalam satuan **kilometer (km)**
- Bisa pakai: OSRM API, Google Maps Distance Matrix, atau Haversine formula

### Berat Paket
- Tiap pelanggan punya `package_weight_kg` — bebas tentukan sendiri (1-10 kg)

### Params
- Hanya ganti `fuel_price_per_liter` sesuai skenario
- Jangan ubah `consumption_full_load`, `consumption_empty`, `compute_cost_per_ms`

---

## Person 2 — Greedy Algorithm

File: `src/algorithms/greedy.py`

### Input
```python
graph: Graph   # dari graph.py — method yang tersedia:
               #   graph.distance(i, j) -> float
               #   graph.get_package_weight(id) -> float
               #   graph.total_customers() -> int
               #   graph.node_count -> int

start_idx: int = 0  # index node awal (0 = hub)
```

### Output (return dict)
```python
{
    "path": [0, 3, 1, 2, 0],  # list[int] — urutan node dari start sampai kembali
    "distance_km": 45.2,        # float — total jarak rute
    "time_ms": 0.0,             # float — isi 0, nanti diukur otomatis
}
```

### Method signature
```python
class GreedySolver:
    def solve(self, graph, start_idx: int = 0) -> dict:
        ...
```

---

## Person 3 — Exact Algorithm

File: `src/algorithms/exact.py`

### Input
```python
graph: Graph   # method sama dengan Person 2
start_idx: int = 0
```

### Output (return dict)
```python
{
    "path": [0, 3, 1, 2, 0],  # list[int] — rute optimal
    "distance_km": 45.2,        # float — total jarak rute
    "time_ms": 0.0,             # float — isi 0
}
```

### Method signature
```python
class ExactSolver:
    def solve(self, graph, start_idx: int = 0) -> dict:
        ...
```

Bebas pilih strategi: DFS brute force, backtracking, Branch & Bound, atau Held-Karp DP. Yang penting **menjamin rute terpendek absolut**.

---

## Integrasi

Setelah semua selesai:

1. Masing-masing bikin branch sendiri:
   - Person 2: `feat/greedy`
   - Person 3: `feat/exact`
   - Person 1: `feat/dataset`
2. Coding di branch masing-masing, lalu push
3. Bikin **Pull Request** ke branch `main`
4. Person 4 (Integration Lead) yang review dan merge
5. Person 4 test `python src/main.py --all` di main setelah semua merged
