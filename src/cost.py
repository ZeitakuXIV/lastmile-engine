import time


def get_consumption_rate(
    current_weight: float,
    total_weight: float,
    full_rate: float,
    empty_rate: float,
) -> float:
    if total_weight <= 0:
        return empty_rate
    ratio = current_weight / total_weight
    return full_rate - (full_rate - empty_rate) * (1 - ratio)


def calculate_segment_liters(
    graph,
    from_node: int,
    to_node: int,
    current_weight: float,
    total_weight: float,
    params: dict,
) -> float:
    dist = graph.distance(from_node, to_node)
    rate = get_consumption_rate(
        current_weight, total_weight,
        params["consumption_full_load"], params["consumption_empty"],
    )
    return dist * rate


def calculate_total_liters(graph, route: list[int], params: dict) -> float:
    total_weight = sum(graph.get_package_weight(n) for n in route if n != 0)
    current_weight = total_weight
    total_liters = 0.0

    for i in range(len(route) - 1):
        liters = calculate_segment_liters(
            graph, route[i], route[i + 1], current_weight, total_weight, params,
        )
        total_liters += liters
        if route[i + 1] != 0:
            current_weight -= graph.get_package_weight(route[i + 1])

    return total_liters


def calculate_fuel_cost(total_liters: float, fuel_price: float) -> float:
    return total_liters * fuel_price


def calculate_compute_cost(time_ms: float, cost_per_ms: float) -> float:
    return time_ms * cost_per_ms


def calculate_tco(fuel_cost: float, compute_cost: float) -> float:
    return fuel_cost + compute_cost


class Timer:
    def __init__(self):
        self._start = 0.0
        self._elapsed = 0.0

    def start(self):
        self._start = time.perf_counter()

    def stop(self) -> float:
        self._elapsed = (time.perf_counter() - self._start) * 1000
        return self._elapsed

    @property
    def elapsed_ms(self) -> float:
        return self._elapsed

    @staticmethod
    def measure(func, *args, **kwargs) -> tuple:
        t = Timer()
        t.start()
        result = func(*args, **kwargs)
        t.stop()
        return result, t.elapsed_ms
