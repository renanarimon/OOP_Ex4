from unittest import TestCase

from client_python.client import Client
from graph.DiGraph import DiGraph
from pokemonGame.Game import Game
from client_python import *


class TestDiGraph(TestCase):

    def test_v_size(self):
        graph = DiGraph()
        graph.add_node(0, (4., 5, 3, 0))
        graph.add_node(1, (1, 5, 0))
        graph.add_node(2, (2, 7, 0))
        graph.add_node(3, (8, 4, 0))

        self.assertEqual(graph.v_size(), 4)

    def test_e_size(self):
        graph = DiGraph()
        graph.add_node(0, (4., 5, 3, 0))
        graph.add_node(1, (1, 5, 0))
        graph.add_node(2, (2, 7, 0))
        graph.add_node(3, (8, 4, 0))
        graph.add_edge(0, 3, 5)
        graph.add_edge(1, 3, 3)
        graph.add_edge(0, 2, 9)
        graph.add_edge(3, 2, 10)
        self.assertEqual(graph.e_size(), 4)

    def test_add_edge(self):
        graph = DiGraph()
        graph.add_node(0, (4.22, 5, 33, 0))
        graph.add_node(1, (2, 3, 0))
        graph.add_node(2, (5, 6, 0))
        graph.add_edge(0, 1, 5)
        graph.add_edge(1, 2, 3)
        graph.add_edge(0, 2, 9)
        self.assertEqual(graph.e_size(), 3)

    def test_add_node(self):
        graph = DiGraph()
        graph.add_node(0, (4.22, 5, 33, 0))
        graph.add_node(1, (2, 3, 0))
        graph.add_node(2, (5, 6, 0))
        self.assertEqual(graph.v_size(), 3)

    def test_remove_node(self):
        graph = DiGraph()
        graph.add_node(0, (4.22, 5, 33, 0))
        graph.add_node(1, (2, 3, 0))
        graph.add_node(2, (5, 6, 0))

        graph.remove_node(0)

        self.assertEqual(graph.v_size(), 2)

    def test_remove_edge(self):
        graph = DiGraph()
        i = 0
        while i < 4:
            graph.add_node(i)
            i += 1
        graph.add_edge(0, 1, 4.8)
        graph.add_edge(0, 2, 5.0)
        graph.add_edge(1, 3, 4.1)
        graph.add_edge(1, 0, 4.0)
        graph.add_edge(2, 3, 3.8)
        graph.add_edge(3, 2, 5.0)
        graph.add_edge(0, 1, 1.8)
        graph.remove_edge(2, 1)
        self.assertTrue(graph.e_size() == 6)
        graph.remove_edge(2, 3)
        self.assertEqual(graph.all_out_edges_of_node(2).get(3), None)
        self.assertTrue(graph.all_in_edges_of_node(3).get(2) is None)
        self.assertTrue(graph.e_size() == 5)
        graph.remove_edge(1, 2)
        self.assertTrue(graph.e_size() == 5)
