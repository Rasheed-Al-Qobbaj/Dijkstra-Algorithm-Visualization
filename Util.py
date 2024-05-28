import math


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        self.elements.append((priority, item))
        self.elements.sort(reverse=True)

    def get(self):
        return self.elements.pop()[1]


def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def read_graph_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    vertex_count, edge_count = map(int, lines[0].split())
    vertices = {}
    edges = []

    for i in range(1, vertex_count + 1):
        parts = lines[i].split()
        city = parts[0]
        x, y = float(parts[1]), float(parts[2])
        vertices[city] = (x, y)

    for i in range(vertex_count + 1, vertex_count + 1 + edge_count):
        city1, city2 = lines[i].split()
        edges.append((city1, city2))

    return vertices, edges


def build_graph(vertices, edges):
    graph = {city: [] for city in vertices}
    for city1, city2 in edges:
        x1, y1 = vertices[city1]
        x2, y2 = vertices[city2]
        distance = euclidean_distance(x1, y1, x2, y2)
        graph[city1].append((city2, distance))
        graph[city2].append((city1, distance))
    return graph


def dijkstra(graph, start):
    dist = {vertex: float('infinity') for vertex in graph}
    prev = {vertex: None for vertex in graph}
    dist[start] = 0

    pq = PriorityQueue()
    pq.put(start, 0)

    while not pq.is_empty():
        current = pq.get()

        for neighbor, weight in graph[current]:
            alt = dist[current] + weight
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = current
                pq.put(neighbor, alt)

    return dist, prev


def shortest_path(prev, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = prev[current]
    path.append(start)
    path.reverse()
    return path


def main(filename, start_city, end_city):
    vertices, edges = read_graph_from_file(filename)
    graph = build_graph(vertices, edges)
    dist, prev = dijkstra(graph, start_city)
    path = shortest_path(prev, start_city, end_city)
    return path, dist[end_city]


if __name__ == "__main__":
    filename = "map.txt"
    start_city = "Country1"
    end_city = "Country5"
    path, cost = main(filename, start_city, end_city)
    print(f"Shortest path from {start_city} to {end_city}: {' -> '.join(path)}")
    print(f"Total cost: {cost}")
