import math
import functools
import random

from graph.GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    """This abstract class represents a directed weighted graph."""

    nodes = {}
    edgesAmount = 0
    children = {}
    parents = {}
    MC = 0

    def __init__(self):
        self.nodes = {}
        self.edgesAmount = 0
        self.children = {}
        self.parents = {}
        self.MC = 0

    """
   @return: The number of vertices in this graph
    """

    def v_size(self) -> int:
        return len(self.nodes)

    """
    @return: The number of edges in this graph
    """

    def e_size(self) -> int:
        return self.edgesAmount

    """return a dictionary of all the nodes in the Graph, 
        each node is represented using a pair (node_id, Node)
    """

    def get_all_v(self) -> dict:
        return self.nodes

    """return a dictionary of all the nodes connected to (into) node_id ,
    each node is represented using a pair (other_node_id, weight)
     """

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.parents[id1]

    """return a dictionary of all the nodes connected from node_id , 
    each node is represented using a pair (other_node_id, weight)
    """

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.children[id1]

    """
    Returns the current version of this graph,
    on every change in the graph state - the MC should be increased
    @return: The current version of this graph.
    """

    def get_mc(self) -> int:
        return self.MC

    """
    Adds an edge to the graph.
    @param id1: The start node of the edge
    @param id2: The end node of the edge
    @param weight: The weight of the edge
    @return: True if the edge was added successfully, False o.w.
    Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
    """

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if self.nodes.get(id1) is not None and self.nodes.get(id2) is not None:
            if self.children[id1].get(id2) is not None:
                return False
            self.children[id1].update({id2: weight})
            self.parents[id2].update({id1: weight})
            self.MC += 1
            self.edgesAmount += 1
            return True
        else:
            return False

    """
    Adds a node to the graph.
    @param node_id: The node ID
    @param pos: The position of the node
    @return: True if the node was added successfully, False o.w.
    Note: if the node id already exists the node will not be added
    """

    def add_node(self, node_id: int, pos: tuple = None, val: float = 0.0) -> bool:
        if node_id not in self.nodes:
            if pos is None:
                x = random.uniform(35.19, 35.22)
                y = random.uniform(32.05, 32.22)
                pos = (x, y, 0.0)
            newOne = Node(node_id, pos, val)
            self.nodes[node_id] = newOne
            self.children[node_id] = {}
            self.parents[node_id] = {}
            self.MC += 1
            return True
        else:
            return False

    """
    Removes a node from the graph.
    @param node_id: The node ID
    @return: True if the node was removed successfully, False o.w.
    Note: if the node id does not exists the function will do nothing
    """

    def remove_node(self, node_id: int) -> bool:
        if node_id in self.nodes:
            for n in list(self.children[node_id]):
                self.remove_edge(n, node_id)
                self.remove_edge(node_id, n)
            del self.nodes[node_id]
            return True
        else:
            return False

    """
    Removes an edge from the graph.
    @param node_id1: The start node of the edge
    @param node_id2: The end node of the edge
    @return: True if the edge was removed successfully, False o.w.
    Note: If such an edge does not exists the function will do nothing
    """

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        try:
            p = self.children[node_id1][node_id2]
        except:
            p = None
        if node_id1 and node_id2 in self.nodes \
                and p is not None:
            del self.parents[node_id2][node_id1]
            del self.children[node_id1][node_id2]
            self.MC += 1
            self.edgesAmount -= 1
            return True
        else:
            return False

    def __repr__(self):
        st = ""
        st += "Graph: |v|="
        st += str(self.v_size())
        st += " , |E|="
        st += str(self.e_size())
        st += "\n{"

        for n in self.nodes.values():
            st += str(n.id)
            st += ": |edges out| "
            st += str(len(self.all_out_edges_of_node(n.id)))

            st += "|edges in| "
            st += str(len(self.all_in_edges_of_node(n.id)))
            st += ", "

        st += "}"

        return st


class Node:
    """ This abstract class represents a Node in the graph"""

    def __init__(self, id1: int, pos: tuple = None, val: float = 0.0):
        self.pos = pos
        self.id = id1
        self.father = None
        self.weight = math.inf
        self.visited = 0
        self.value = val

    """ compare between 2 nodes by weight
    """

    def __lt__(self, other):
        return self.weight < getattr(other, 'weight', other)

    def __eq__(self, other):
        return self.weight == getattr(other, 'weight', other)

    def __repr__(self):
        st = str(self.id)
        return st

    def pos_to_string(self):
        string = "{},{},{}".format(self.pos[0], self.pos[1], self.pos[2])
        return string
