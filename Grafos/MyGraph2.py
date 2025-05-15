import heapq

class MyGraph:
    def __init__(self, g=None):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g if g is not None else {}

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph:
            print(v, " -> ", self.graph[v])

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())

    def get_edges(self):
        ''' Returns edges in the graph as a list of tuples (origin, destination, weight) '''
        edges = []
        for v in self.graph:
            for dest, weight in self.graph[v]:
                edges.append((v, dest, weight))
        return edges

    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())

    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph:
            self.graph[v] = []

    def add_edge(self, o, d, w):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph '''
        if o not in self.graph:
            self.add_vertex(o)
        if d not in self.graph:
            self.add_vertex(d)
        if (d, w) not in self.graph[o]:
            self.graph[o].append((d, w))

    def get_successors(self, v):
        return [dest for dest, _ in self.graph.get(v, [])]

    def get_predecessors(self, v):
        res = []
        for k in self.graph:
            for dest, _ in self.graph[k]:
                if dest == v:
                    res.append(k)
        return res

    def get_adjacents(self, v):
        suc = set(self.get_successors(v))
        pred = set(self.get_predecessors(v))
        return list(suc | pred)

    def out_degree(self, v):
        return len(self.graph.get(v, []))

    def in_degree(self, v):
        return len(self.get_predecessors(v))

    def degree(self, v):
        return len(self.get_adjacents(v))

    def dijkstra_distance(self, s, d):
        if s == d:
            return 0
        dist = {v: float('inf') for v in self.graph}
        dist[s] = 0
        visited = set()
        heap = [(0, s)]

        while heap:
            cur_dist, node = heapq.heappop(heap)
            if node in visited:
                continue
            visited.add(node)
            if node == d:
                return cur_dist
            for neighbor, weight in self.graph[node]:
                if neighbor not in visited:
                    new_dist = cur_dist + weight
                    if new_dist < dist[neighbor]:
                        dist[neighbor] = new_dist
                        heapq.heappush(heap, (new_dist, neighbor))
        return None

    def shortest_path(self, s, d):
        if s == d:
            return [s]
        dist = {v: float('inf') for v in self.graph}
        prev = {v: None for v in self.graph}
        dist[s] = 0
        visited = set()
        heap = [(0, s)]

        while heap:
            cur_dist, node = heapq.heappop(heap)
            if node in visited:
                continue
            visited.add(node)
            if node == d:
                break
            for neighbor, weight in self.graph[node]:
                if neighbor not in visited:
                    new_dist = cur_dist + weight
                    if new_dist < dist[neighbor]:
                        dist[neighbor] = new_dist
                        prev[neighbor] = node
                        heapq.heappush(heap, (new_dist, neighbor))

        if dist[d] == float('inf'):
            return None
        path = []
        current = d
        while current is not None:
            path.insert(0, current)
            current = prev[current]
        return path

    def node_has_cycle(self, v):
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            for neighbor, _ in self.graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        return dfs(v)

    def has_cycle(self):
        visited = set()
        for node in self.graph:
            if node not in visited:
                if self.node_has_cycle(node):
                    return True
        return False
