from graph.DiGraph import DiGraph


class algo:
    def __init__(self, g: DiGraph = DiGraph()):
        self.graph = g
        self.copyGraph = g

    def copy(self):
        g = DiGraph()
        for n in self.graph.nodes.values():
            g.add_node(n.id, n.pos)
        for n in self.graph.nodes.values():
            for k in self.graph.all_out_edges_of_node(n.id):
                w = self.graph.children[n.id][k]
                g.add_edge(n.id, k, w)

        return g


