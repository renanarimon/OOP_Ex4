import json
import math
import random
import queue
import sys
from typing import List
import matplotlib.pyplot as plt

import easygui
import pygame
from pygame import Color, display, gfxdraw
from pygame.constants import RESIZABLE
import pygame_gui
from graph.DiGraph import Node, DiGraph

from graph.GraphAlgoInterface import GraphAlgoInterface
from graph.GraphInterface import GraphInterface

"""This abstract class represents algorithms on directed weighted graph."""


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph = DiGraph()):
        self.graph = g
        self.file = ""

        # flag

    INFINITY = math.inf
    # init algo & graph

    """return: the directed graph on which the algorithm works on."""

    def get_graph(self) -> GraphInterface:
        return self.graph

    """return: deep copy of the graph"""

    def copy(self):
        g = DiGraph()
        for n in self.graph.nodes.values():
            g.add_node(n.id, n.pos)
        for n in self.graph.nodes.values():
            for k in self.graph.all_out_edges_of_node(n.id):
                w = self.graph.children[n.id][k]
                g.add_edge(n.id, k, w)

        return g

    """:return: graph transpose
     help function for isConnected()"""

    def transpose(self):
        g = self.copy()
        tmp = g.children
        g.children = g.parents
        g.parents = tmp
        return g

    """ BFS - search on graph
    https://en.wikipedia.org/wiki/Breadth-first_search
    :param graph
    :param nodeId - root node to start bfs
    :return visited[] - True in the i'th place if visited i node
     """

    def bfs(self, g: DiGraph, nodeId: int) -> list:
        visited = [False] * (g.v_size())
        q = [nodeId]
        visited[nodeId] = True
        while q:
            startNode = q.pop(0)
            for e in g.all_out_edges_of_node(startNode):
                if not visited[e]:
                    q.append(e)
                    visited[e] = True
        return visited

    """1. BFS on graph
       2. BFS on Transpose graph.
       3. if in one of them a V is unvisited --> return False
       :return True iff graph is strongly connected
    """

    def isConnected(self) -> bool:
        start = self.graph.nodes[0].id
        visited = self.bfs(self.graph, start)
        for b in visited:
            if b == 0:
                return False
        visited = self.bfs(self.transpose(), start)
        for b in visited:
            if b == 0:
                return False
        return True

    def dijkstra_algorithm(self, start_node):
        unvisited_nodes = list(self.graph.nodes.values())

        # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
        shortest_path = {}

        # We'll use this dict to save the shortest known path to a node found so far
        previous_nodes = {}

        # We'll use max_value to initialize the "infinity" value of the unvisited nodes
        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node.id] = max_value
        # However, we initialize the starting node's value with 0
        shortest_path[start_node] = 0

        # The algorithm executes until we visit all nodes
        while unvisited_nodes:
            # The code block below finds the node with the lowest score
            current_min_node = None
            for node in unvisited_nodes:  # Iterate over the nodes
                if current_min_node is None:
                    current_min_node = node
                elif shortest_path[node.id] < shortest_path[current_min_node.id]:
                    current_min_node = node

            # The code block below retrieves the current node's neighbors and updates their distances
            neighbors = self.graph.all_out_edges_of_node(current_min_node.id)
            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_node.id] + self.graph.all_out_edges_of_node(current_min_node.id).get(neighbor)
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    # We also update the best path to the current node
                    previous_nodes[neighbor] = current_min_node

            # After visiting its neighbors, we mark the node as "visited"
            unvisited_nodes.remove(current_min_node)

        return previous_nodes, shortest_path

    """ restart nodes: father, weight, visited
        before dijkstra
    """

    def restartNodes(self):
        for n in self.graph.nodes.values():
            n.father = None
            n.weight = self.INFINITY
            n.visited = 0

    """help function for Dijkstra
        if adding the edge make the path shorter --> add edge.
        change the node weight.
        :param src, dest of edge
    """

    def relax(self, src: int, dest: int):
        srcNode = self.graph.nodes[src]
        destNode = self.graph.nodes[dest]
        edgeWeight = self.graph.all_out_edges_of_node(src)[dest]
        if destNode.weight > srcNode.weight + edgeWeight:
            destNode.weight = srcNode.weight + edgeWeight
            destNode.father = srcNode

    """algorithm to find the shortest paths between nodes in a graph,
        update each node's weight - the weight of the shortest path from root to self
        https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """

    def dijkstra(self, src: int, dest: int):
        self.restartNodes()
        root = self.graph.nodes.get(src)
        root.weight = 0
        pq = queue.PriorityQueue()
        pq.put(root)
        while not pq.empty():
            curr = pq.get()
            if curr.visited == 0:  # NOT visited
                if curr.id == dest:
                    return
                curr.visited = 1
                for d in self.graph.all_out_edges_of_node(curr.id):
                    self.relax(curr.id, d)
                    pq.put(self.graph.nodes.get(d))

    """ find the node that has the minimum short path if we start from src with dijkstra algorithm 
        :param node_id: start node
        :param node_lst: cities
        :return ans: dest node id that make the path shortest
        :return path: path from src -> dest
        :return pathWeight: path's weight
    """

    def minShortPath(self, node_id: int, node_lst: List[int]) -> (int, list, float):
        # previous_nodes, shortest_path = self.dijkstra_algorithm(node_id)
        self.dijkstra(node_id, -1)
        minW = sys.maxsize
        ans = 0
        path = []
        for i in node_lst:
            if self.graph.nodes[i].weight < minW:
                minW = self.graph.nodes[i].weight
                ans = i
        last = ans
        pathWeight = self.graph.nodes[last].weight
        path, weight = self.findParentPath(last, pathWeight, path)
        path.append(node_id)
        path.reverse()
        return ans, path, pathWeight

    """
    :return short path of nodes id from src to dest
    :return path weight
    """

    def findParentPath(self, idCurr: int, weight: float, listAdd: list):
        while self.graph.nodes[idCurr].father is not None:
            listAdd.append(idCurr)
            weight += self.graph.nodes[idCurr].father.weight
            idCurr = self.graph.nodes[idCurr].father.id
        return listAdd, weight

    """
    Computes the shortest path between src to dest - as an ordered List of nodes:
    src--> n1-->n2-->...dest
    this function use dijkstra algorithm to find the shortest path
    if no such path --> returns null
    :param id1, id2 
    :return list of nodes path
    """

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        self.dijkstra(id1, id2)
        weightAns = self.graph.nodes[id2].weight
        listAns = []
        curr = id2
        listAns, weight = self.findParentPath(curr, weightAns, listAns)
        if weightAns != math.inf:
            listAns.append(id1)
            listAns.reverse()
        return weightAns, listAns

    """ Computes a list of consecutive nodes which go over all the nodes in cities.
        this is greedy algorithm- first go to the node in index 0 (random)  and in each node-
        prefer go to the closet node (minShortPath function)
    """

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        ans = []
        currNode = node_lst.pop(0)
        ans.append(currNode)
        bestNode = 0
        weight = 0
        while len(node_lst) > 0:
            put = []
            bestNode, put, tmp_wei = self.minShortPath(currNode, node_lst)
            if bestNode != currNode:
                weight += tmp_wei
                put.pop(0)
                ans = ans + put
                node_lst.remove(bestNode)
                currNode = bestNode
            else:
                return None
        return ans, weight

    """help function for center 
    find the node that has the maximum short path if we start from src with dijkstra algorithm 
    :param node_id 
    :return maxW: weight of max path
    """

    def maxShortPath(self, node_id: int) -> int:
        self.dijkstra(node_id, -1)
        maxW = -sys.maxsize
        for n in self.graph.nodes.values():
            if n.weight > maxW:
                maxW = n.weight
        return maxW

    """Finds the NodeData which minimizes the max distance to all the other nodes.
     Iterate all the nodes - for each node, find tha "Maximum short path" it has 
     and find the minimum of all the results
     :return node id, min-maximum distance
    """

    def centerPoint(self) -> (int, float):
        if not self.isConnected():
            return None, self.INFINITY

        minDist = sys.maxsize
        minId = 0
        for n in self.graph.nodes.values():
            maxDist = self.maxShortPath(n.id)
            if maxDist < minDist:
                minDist = maxDist
                minId = n.id
        return minId, minDist

    """ Loads a graph from a json file.
        @param: file_name: The path to the json file
        @return: True if the loading was successful, False o.w."""

    def load_from_json(self, file_name: str) -> bool:
        try:
            self.file = file_name
            self.graph.__init__()
            with open(file_name, 'r') as file:
                l = json.load(file)
                ListNodes = l['Nodes']
                ListEdges = l['Edges']
            for n in ListNodes:
                try:
                    tmp = n['pos'].split(",")
                    x = float(tmp[0])
                    y = float(tmp[1])
                    pos = (x, y, 0.0)
                except Exception:
                    x = random.uniform(35.19, 35.22)
                    y = random.uniform(32.05, 32.22)
                    pos = (x, y, 0.0)

                self.graph.add_node(n['id'], pos)
            for e in ListEdges:
                self.graph.add_edge(e['src'], e['dest'], e['w'])
            return True
        except:
            return False

    """save graph to json file"""

    def save_to_json(self, file_name: str) -> bool:
        if self.graph is None:
            return False
        dict_ans = {"Edges": [], "Nodes": []}
        for n in self.graph.nodes.values():
            node_dict = {"id": n.id}
            if n.pos is not None:
                node_dict["pos"] = n.pos_to_string()
            dict_ans["Nodes"].append(node_dict)
            for e in self.graph.all_out_edges_of_node(n.id):
                edges_dict = {"src": n.id, "w": self.graph.all_out_edges_of_node(n.id)[e], "dest": e}
                dict_ans["Edges"].append(edges_dict)
        try:
            with open(file_name, 'w') as writer:
                writer.write(json.dumps(dict_ans))
                return True
        except:
            return False
        finally:
            writer.close()

    """plot graph with matplotlib"""

    def plot_graph(self) -> None:
        action = ""
        center = 0
        tsp = []
        ShortestPath = []
        graph = self.graph

        R = 10
        WIDTH = 700
        HEIGHT = 500

        # colors
        gray = Color(64, 64, 64)
        blue = Color(6, 187, 193)
        blue1 = Color(21, 239, 246)
        yellow = Color(255, 255, 102)
        white = Color(255, 255, 255)
        pink = Color(255, 153, 104)

        # init pygame
        pygame.init()
        screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        background = pygame.Surface((WIDTH, HEIGHT), flags=RESIZABLE)
        background.fill(gray)
        clock = pygame.time.Clock()
        pygame.font.init()

        FONT = pygame.font.SysFont('Arial', 20)

        manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        btnLoad = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (115, 40)),
                                               text='LOAD',
                                               manager=manager)
        btnCenter = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((115, 0), (115, 40)),
                                                 text='CENTER',
                                                 manager=manager)
        btnTsp = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((230, 0), (115, 40)),
                                              text='TSP',
                                              manager=manager)
        btnShortedPath = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((345, 0), (115, 40)),
                                                      text='SHORTEST PATH',
                                                      manager=manager)
        btnClear = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((460, 0), (115, 40)),
                                                text='CLEAR',
                                                manager=manager)

        def scale(data, min_screen, max_screen, min_data, max_data):
            return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

        min_x = float(min(list(graph.nodes.values()), key=lambda node: node.pos[0]).pos[0])
        min_y = float(min(list(graph.nodes.values()), key=lambda node: node.pos[1]).pos[1])
        max_x = float(max(list(graph.nodes.values()), key=lambda node: node.pos[0]).pos[0])
        max_y = float(max(list(graph.nodes.values()), key=lambda node: node.pos[1]).pos[1])

        def gui_scale(data, x=False, y=False):
            if x:
                return scale(data, 50, screen.get_width() - 50, min_x, max_x)
            if y:
                return scale(data, 50, screen.get_height() - 50, min_y, max_y)

        def draw_arrow(src, dst, d, hi, color):
            dx = float(dst[0]) - float(src[0])
            dy = float(dst[1]) - float(src[1])
            s = float(math.sqrt(dx * dx + dy * dy))
            x1 = float(s - d)
            x2 = float(x1)
            y1 = float(hi)
            y2 = hi * -1
            sin = dy / s
            cos = dx / s
            x_temp = x1 * cos - y1 * sin + float(src[0])
            y1 = x1 * sin + y1 * cos + float(src[1])
            x1 = x_temp
            x_temp = x2 * cos - y2 * sin + float(src[0])
            y2 = x2 * sin + y2 * cos + float(src[1])
            x2 = x_temp
            points = [(dst[0], dst[1]), (int(x1), int(y1)), (int(x2), int(y2))]
            pygame.draw.line(screen, color, src, dst, width=2)
            pygame.draw.polygon(screen, color, points)

        # draw
        def drawNode(n1: Node, color: Color):
            x = gui_scale(float(n1.pos[0]), x=True)
            y = gui_scale(float(n1.pos[1]), y=True)
            gfxdraw.filled_circle(screen, int(x), int(y),
                                  R, color)
            gfxdraw.aacircle(screen, int(x), int(y),
                             R, yellow)
            id_srf = FONT.render(str(n1.id), True, gray)
            rect = id_srf.get_rect(center=(x, y))
            screen.blit(id_srf, rect)

        def drawOneEdge(src: Node, dest: Node, color: Color):
            src_x = gui_scale(src.pos[0], x=True)
            src_y = gui_scale(src.pos[1], y=True)
            dest_x = gui_scale(dest.pos[0], x=True)
            dest_y = gui_scale(dest.pos[1], y=True)
            draw_arrow((src_x, src_y), (dest_x, dest_y), 15, 5, color)

        def drawEdges(n: Node, color: Color):
            for k in self.graph.all_out_edges_of_node(n.id):
                dest = self.graph.nodes.get(k)
                drawOneEdge(n, dest, color)

        def simplePlot():
            x = []
            y = []
            for n in self.graph.nodes.values():
                src_x = n.pos[0]
                src_y = n.pos[1]
                for k in self.graph.all_out_edges_of_node(n.id):
                    dest = self.graph.nodes.get(k)
                    dest_x = dest.pos[0]
                    dest_y = dest.pos[1]
                    plt.annotate("", xy=(src_x, src_y), xytext=(dest_x, dest_y), arrowprops=dict(arrowstyle="->"))

                plt.annotate(n.id, (src_x, src_y))
                x.append(n.pos[0])
                y.append(n.pos[1])

            print(x)
            print(y)
            plt.title(self.file.title())
            plt.scatter(x, y, c='red')
            plt.show()

        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == btnLoad:
                            msg = "Please select a json file: "
                            file = easygui.fileopenbox(msg, '')
                            self.load_from_json(file)
                            action = "clear"
                        if event.ui_element == btnCenter:
                            center = self.centerPoint()[0]
                            action = "center"
                        if event.ui_element == btnTsp:
                            action = "tsp"
                            text = "Enter keys Of Cities: (Example:1 2 3 4)"
                            title = "TSP"
                            output = easygui.enterbox(text, title)
                            listOutput = output.split(" ")
                            listOutput = [int(x) for x in listOutput]
                            tsp = self.TSP(listOutput)[0]

                        if event.ui_element == btnShortedPath:
                            action = "ShortestPath"
                            text = "Enter keys Of src & dest:"
                            title = "Shortest Path"
                            output = easygui.enterbox(text, title)
                            listOutput = output.split(" ")
                            src1 = int(listOutput[0])
                            dest1 = int(listOutput[1])
                            ShortestPath = self.shortest_path(src1, dest1)[1]

                        if event.ui_element == btnClear:
                            action = "clear"

                manager.process_events(event)
            manager.update(time_delta)
            screen.blit(background, (0, 0))
            manager.draw_ui(screen)

            for n in self.graph.nodes.values():
                drawEdges(n, blue1)

            for n in self.graph.nodes.values():
                drawNode(n, blue)

            if action == "clear":
                for n in self.graph.nodes.values():
                    drawEdges(n, blue1)

                for n in self.graph.nodes.values():
                    drawNode(n, blue)

            if action == "center":
                n = self.graph.nodes.get(center)
                drawNode(n, pink)
                pygame.display.flip()

            if action == "tsp":
                for i in range(len(tsp) - 1):
                    src = self.graph.nodes.get(tsp[i])
                    dest = self.graph.nodes.get(tsp[i + 1])
                    drawOneEdge(src, dest, pink)
                pygame.display.flip()

            if action == "ShortestPath":
                for i in range(len(ShortestPath) - 1):
                    src = self.graph.nodes.get(ShortestPath[i])
                    dest = self.graph.nodes.get(ShortestPath[i + 1])
                    drawOneEdge(src, dest, pink)
                pygame.display.flip()

            pygame.display.update()

            clock.tick(60)

if __name__ == '__main__':
    g_algo = GraphAlgo()
    file = '../data/A0'
    g_algo.load_from_json(file)
    # g_algo.plot_graph()
    x = g_algo.TSP([5,0,1])
    print(x)