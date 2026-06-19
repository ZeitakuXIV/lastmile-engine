from algorithms.base import Solver


class ExactSolver(Solver):
    def solve(self, graph, start_idx: int = 0) -> dict:
        
        n = graph.node_count
        
        if n <= 1:
            return {"path": [start_idx], "distance_km": 0.0, "time_ms": 0.0}
        
        #Node pelanggan
        customers = [i for i in range(n) if i != start_idx]
        m = len(customers)
        
        #Map: index pelanggan (0..m-1) -> node id sebenarnya
        #Map: node id -> index pelanggan (0..m-1)
        node_to_idx = {customers[i]: i for i in range(m)}
        INF = float('inf')
        
        #Inisialisasi DP
        #dp[mask][last_idx] = (min_distance, prev_idx untuk reconstruct)
        dp = {}
        
        #Base case: dari start_idx ke setiap pelanggan pertama
        for i in range(m):
            node_i = customers[i]
            dist = graph.distance(start_idx, node_i)
            mask = 1 << i
            dp[(mask, i)] = (dist, -1) 
        
        #Build DP untuk subset yang lebih besar
        for mask_size in range(2, m + 1):
            for mask in range(1 << m):
                if bin(mask).count('1') != mask_size:
                    continue
                
                for last in range(m):
                    if not (mask & (1 << last)):
                        continue
                    
                    prev_mask = mask ^ (1 << last)
                    min_dist = INF
                    best_prev = -1
                    
                    for prev in range(m):
                        if not (prev_mask & (1 << prev)):
                            continue
                        
                        prev_dist, _ = dp.get((prev_mask, prev), (INF, -1))
                        if prev_dist == INF:
                            continue
                        
                        node_prev = customers[prev]
                        node_last = customers[last]
                        edge_dist = graph.distance(node_prev, node_last)
                        total = prev_dist + edge_dist
                        
                        if total < min_dist:
                            min_dist = total
                            best_prev = prev
                    
                    if min_dist < INF:
                        dp[(mask, last)] = (min_dist, best_prev)
        
        #kembali ke start_idx dari semua pelanggan
        full_mask = (1 << m) - 1
        min_total = INF
        best_last = -1
        
        for last in range(m):
            if not (full_mask & (1 << last)):
                continue
            
            dist_to_hub, _ = dp.get((full_mask, last), (INF, -1))
            if dist_to_hub == INF:
                continue
            
            node_last = customers[last]
            return_dist = graph.distance(node_last, start_idx)
            total = dist_to_hub + return_dist
            
            if total < min_total:
                min_total = total
                best_last = last
        
        path = [start_idx]
        mask = full_mask
        last = best_last
        
        #Backtrack untuk dapat urutan pelanggan
        order = []
        while last != -1:
            order.append(customers[last])
            _, prev = dp[(mask, last)]
            mask ^= (1 << last)
            last = prev
        
        order.reverse()
        path.extend(order)
        path.append(start_idx)
        
        return {
            "path": path,
            "distance_km": round(min_total, 2),
            "time_ms": 0.0,
        }