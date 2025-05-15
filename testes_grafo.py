import unittest
from MyGraph2 import MyGraph

class TestMyGraphWeighted(unittest.TestCase):

    def setUp(self):
        # Grafo ponderado de exemplo
        # A -> B (2), A -> C (5), B -> C (1), C -> D (4)
        self.graph = MyGraph({
            'A': [('B', 2), ('C', 5)],
            'B': [('C', 1)],
            'C': [('D', 4)],
            'D': []
        })

    def test_get_nodes_and_edges(self):
        # Verifica nós e arestas com peso
        self.assertCountEqual(self.graph.get_nodes(), ['A','B','C','D'])  # ordem irrelevante :contentReference[oaicite:3]{index=3}
        expected_edges = [
            ('A','B',2), ('A','C',5),
            ('B','C',1),
            ('C','D',4)
        ]
        self.assertCountEqual(self.graph.get_edges(), expected_edges)

    def test_size(self):
        # 4 nós e 4 arestas
        self.assertEqual(self.graph.size(), (4,4))

    def test_add_vertex_and_edge(self):
        # Adiciona novo vértice e aresta ponderada
        self.graph.add_vertex('E')
        self.assertIn('E', self.graph.graph)
        self.graph.add_edge('E','A',3)
        self.assertIn(('A',3), self.graph.graph['E'])

    def test_successors_predecessors_adjacents(self):
        # Sucessores de A: B e C
        self.assertCountEqual(self.graph.get_successors('A'), ['B','C'])
        # Predecessores de C: A e B
        self.assertCountEqual(self.graph.get_predecessors('C'), ['A','B'])
        # Adjacentes de C: união de predecessores e sucessores
        self.assertCountEqual(self.graph.get_adjacents('C'), ['A','B','D'])

    def test_degrees(self):
        # Grau de saída, entrada e total
        self.assertEqual(self.graph.out_degree('A'), 2)
        self.assertEqual(self.graph.in_degree('C'), 2)
        self.assertEqual(self.graph.degree('C'), 3)

    def test_dijkstra_distance(self):
        # Distância mínima de A até D: A->B->C->D = 2+1+4 = 7
        self.assertEqual(self.graph.dijkstra_distance('A','D'), 7)
        # Distância de um nó para ele mesmo é zero
        self.assertEqual(self.graph.dijkstra_distance('B','B'), 0)
        # Sem caminho: retorna None
        self.assertIsNone(self.graph.dijkstra_distance('D','A'))

    def test_shortest_path(self):
        # Caminho mais curto de A até D
        self.assertEqual(self.graph.shortest_path('A','D'),
                         ['A','B','C','D'])
        # De D para A não há caminho
        self.assertIsNone(self.graph.shortest_path('D','A'))

    def test_cycle_detection(self):
        # Grafo sem ciclos inicialmente
        self.assertFalse(self.graph.has_cycle())
        # Insere ciclo simples: D -> A
        self.graph.add_edge('D','A',1)
        self.assertTrue(self.graph.node_has_cycle('A'))
        self.assertTrue(self.graph.has_cycle())

if __name__ == '__main__':
    unittest.main()
