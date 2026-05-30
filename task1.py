from collections import deque, defaultdict

def add_edge(graph, capacity, u, v, cap):
    graph[u].append(v)
    graph[v].append(u)
    capacity[(u, v)] += cap
    capacity[(v, u)] += 0

def edmonds_karp(graph, capacity, source, sink):
    total_flow = 0
    augmenting_paths = []

    while True:
        parent = {source: None}
        queue = deque([source])

        while queue and sink not in parent:
            u = queue.popleft()
            for v in graph[u]:
                if v not in parent and capacity[(u, v)] > 0:
                    parent[v] = u
                    queue.append(v)

        if sink not in parent:
            break

        path = []
        path_flow = float("inf")
        v = sink

        while v != source:
            u = parent[v]
            path.append((u, v))
            path_flow = min(path_flow, capacity[(u, v)])
            v = u

        path.reverse()

        for u, v in path:
            capacity[(u, v)] -= path_flow
            capacity[(v, u)] += path_flow

        total_flow += path_flow
        augmenting_paths.append((path, path_flow))

    return total_flow, augmenting_paths

graph = defaultdict(list)
capacity = defaultdict(int)

source = "S"
sink = "T"

terminals = ["Термінал 1", "Термінал 2"]
warehouses = ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]
stores = [f"Магазин {i}" for i in range(1, 15)]

add_edge(graph, capacity, source, "Термінал 1", 60)
add_edge(graph, capacity, source, "Термінал 2", 55)

add_edge(graph, capacity, "Термінал 1", "Склад 1", 25)
add_edge(graph, capacity, "Термінал 1", "Склад 2", 20)
add_edge(graph, capacity, "Термінал 1", "Склад 3", 15)

add_edge(graph, capacity, "Термінал 2", "Склад 3", 15)
add_edge(graph, capacity, "Термінал 2", "Склад 4", 30)
add_edge(graph, capacity, "Термінал 2", "Склад 2", 10)

store_edges = [
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

for u, v, cap in store_edges:
    add_edge(graph, capacity, u, v, cap)
    add_edge(graph, capacity, v, sink, cap)

original_capacity = dict(capacity)

max_flow, augmenting_paths = edmonds_karp(graph, capacity, source, sink)

edge_flows = {}
for (u, v), cap in original_capacity.items():
    if cap > 0:
        edge_flows[(u, v)] = cap - capacity[(u, v)]

warehouse_inflows = {w: {t: 0 for t in terminals} for w in warehouses}
for t in terminals:
    for w in warehouses:
        warehouse_inflows[w][t] = edge_flows.get((t, w), 0)

warehouse_store_flows = {w: [] for w in warehouses}
for w, s, _ in store_edges:
    flow = edge_flows.get((w, s), 0)
    warehouse_store_flows[w].append((s, flow))

terminal_store_flows = defaultdict(int)

for w in warehouses:
    remaining = dict(warehouse_inflows[w])
    for store, amount in warehouse_store_flows[w]:
        left = amount
        for terminal in terminals:
            take = min(left, remaining[terminal])
            if take > 0:
                terminal_store_flows[(terminal, store)] += take
                remaining[terminal] -= take
                left -= take
            if left == 0:
                break

print("Максимальний потік:", max_flow)
print()

print("Покрокові шляхи збільшення потоку:")
for i, (path, flow) in enumerate(augmenting_paths, 1):
    path_str = " -> ".join([u for u, v in path] + [path[-1][1]])
    print(f"{i}. {path_str} | Потік: {flow}")

print()
print("Фактичні потоки по ребрах:")
for (u, v), flow in edge_flows.items():
    if u != source and v != sink and flow > 0:
        print(f"{u} -> {v}: {flow}")

print()
print("Таблиця потоків між терміналами та магазинами:")
print(f"{'Термінал':<15} {'Магазин':<12} {'Фактичний потік':<18}")
for terminal in terminals:
    for store in stores:
        flow = terminal_store_flows.get((terminal, store), 0)
        print(f"{terminal:<15} {store:<12} {flow:<18}")

print()
print("Сумарний потік по терміналах:")
for terminal in terminals:
    total = sum(terminal_store_flows.get((terminal, store), 0) for store in stores)
    print(f"{terminal}: {total}")
