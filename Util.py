import math


class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}
        self.adjacency_list = {}

    def add_vertex(self, name, x, y):
        """Adds a vertex to the graph."""
        self.vertices[name] = (x, y)
        self.adjacency_list[name] = []

    def add_edge(self, from_vertex, to_vertex):
        """Adds an edge to the graph if both vertices exist."""
        if from_vertex in self.vertices and to_vertex in self.vertices:
            self.edges[(from_vertex, to_vertex)] = self.euclidean_distance(from_vertex, to_vertex)
            self.adjacency_list[from_vertex].append(to_vertex)
            self.adjacency_list[to_vertex].append(from_vertex)

    def euclidean_distance(self, vertex1, vertex2):
        """Calculates the Euclidean distance between two vertices."""
        x1, y1 = self.vertices[vertex1]
        x2, y2 = self.vertices[vertex2]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class MinHeap:
    def __init__(self):
        self.heap = []
        self.vertex_position = {}

    def is_empty(self):
        return len(self.heap) == 0

    def swap(self, i, j):
        """Swaps two elements in the heap and updates their positions."""
        self.vertex_position[self.heap[i][1]] = j
        self.vertex_position[self.heap[j][1]] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def bubble_up(self, index):
        """Maintains the heap property by bubbling up the element at the given index."""
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index][0] < self.heap[parent_index][0]:
            self.swap(index, parent_index)
            self.bubble_up(parent_index)

    def bubble_down(self, index):
        """Maintains the heap property by bubbling down the element at the given index."""
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest = index

        if left_child_index < len(self.heap) and self.heap[left_child_index][0] < self.heap[smallest][0]:
            smallest = left_child_index

        if right_child_index < len(self.heap) and self.heap[right_child_index][0] < self.heap[smallest][0]:
            smallest = right_child_index

        if smallest != index:
            self.swap(index, smallest)
            self.bubble_down(smallest)

    def add_task(self, vertex, priority):
        """Adds a task to the heap or updates the priority if it already exists."""
        if vertex in self.vertex_position:
            self.remove_task(vertex)
        entry = [priority, vertex]
        self.vertex_position[vertex] = len(self.heap)
        self.heap.append(entry)
        self.bubble_up(len(self.heap) - 1)

    def remove_task(self, vertex):
        """Removes a task from the heap."""
        index = self.vertex_position.pop(vertex)
        last_entry = self.heap.pop()
        if index != len(self.heap):
            self.heap[index] = last_entry
            self.vertex_position[last_entry[1]] = index
            self.bubble_up(index)
            self.bubble_down(index)

    def pop_task(self):
        """Pops the task with the smallest priority from the heap."""
        if self.is_empty():
            raise KeyError("pop from an empty priority queue")
        priority, vertex = self.heap[0]
        self.remove_task(vertex)
        return vertex


def dijkstra(graph, start, end):
    """Implements Dijkstra's algorithm to find the shortest path between two vertices."""
    pq = MinHeap()
    pq.add_task(start, 0)
    distances = {vertex: float('infinity') for vertex in graph.vertices}
    previous_vertices = {vertex: None for vertex in graph.vertices}
    distances[start] = 0

    while not pq.is_empty():
        current_vertex = pq.pop_task()

        if current_vertex == end:
            break

        for neighbor in graph.adjacency_list[current_vertex]:
            distance = graph.euclidean_distance(current_vertex, neighbor)
            new_distance = distances[current_vertex] + distance

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_vertices[neighbor] = current_vertex
                pq.add_task(neighbor, new_distance)

    path = []
    current_vertex = end
    while previous_vertices[current_vertex] is not None:
        path.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]
    path.append(start)

    return path[::-1], distances[end]


def read_map(filename):
    """Reads the map from a file and returns a Graph object."""
    graph = Graph()
    with open(filename, 'r') as file:
        # Read the number of vertices and edges
        line = file.readline().strip()
        parts = line.split()
        num_vertices = int(parts[0])
        num_edges = int(parts[1])

        # Read the vertices
        for _ in range(num_vertices):
            line = file.readline().strip()
            parts = line.split()
            name = parts[0]
            x = int(parts[1])
            y = int(parts[2])
            graph.add_vertex(name, x, y)

        # Read the edges
        for _ in range(num_edges):
            line = file.readline().strip()
            parts = line.split()
            from_vertex = parts[0]
            to_vertex = parts[1]
            graph.add_edge(from_vertex, to_vertex)

    return graph



if __name__ == '__main__':
    filename = 'map.txt'
    graph = read_map(filename)
    print(graph.vertices)
    print(graph.edges)
    start = 'Country1'
    end = 'Country6'
    path, distance = dijkstra(graph, start, end)
    print('The shortest path from', start, 'to', end, 'is:', path)
    print('The distance is:', distance)
