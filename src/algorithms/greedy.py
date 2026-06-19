from algorithms.base import Solver


class GreedySolver(Solver):
    def solve(self, graph, start_idx: int = 0) -> dict:
        n = graph.node_count
        visited = [False] * n
        path = [start_idx]
        visited[start_idx] = True
        current = start_idx
        total_distance = 0.0
        
        #Iterasi kunjungi semua node
        for _ in range(n - 1):
            nearest = -1
            min_dist = float('inf')
            
            for next_node in range(n):
                if visited[next_node]:
                    continue
                
                dist = graph.distance(current, next_node)
                if dist < min_dist:
                    min_dist = dist
                    nearest = next_node
            
            if nearest == -1:
                break
            
            path.append(nearest)
            visited[nearest] = True
            total_distance += min_dist
            current = nearest
        
        #Kembali ke start
        return_dist = graph.distance(current, start_idx)
        total_distance += return_dist
        path.append(start_idx)
        
        return {
            "path": path,
            "distance_km": round(total_distance, 2),
            "time_ms": 0.0,
        }