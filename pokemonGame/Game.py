import json
import math
import queue
import random
import sys

import numpy as np

from pokemonGame.Agent import Agent
from pokemonGame.Pokimon import Pokemon
from graph.DiGraph import DiGraph


class Game:
    # algoGraph = GraphAlgo()

    def __init__(self, json_str: str):
        self.INFINITY = INFINITY = math.inf
        l = json.loads(json_str)['GameServer']

        self.numOfPokemons = l['pokemons']
        self.is_logged_in = l['is_logged_in']
        self.moves = l['moves']
        self.grade = l['grade']
        self.game_level = l['game_level']
        self.max_user_level = l['max_user_level']
        self.id = l['id']
        self.graph_json = l['graph']
        self.numOfAgent = l['agents']

        self.pokemons = []
        self.agents = []
        self.graph = DiGraph()
        self.load_from_json("../" + self.graph_json)
        self.size = self.graph.v_size()
        self.currDest = 0


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

    def load_pokemon(self, file_name):
        l = json.loads(file_name)
        ListPokemons = l['Pokemons']
        self.pokemons.clear()
        for p in ListPokemons:
            pok = p['Pokemon']
            tmp = pok['pos'].split(",")
            x = float(tmp[0])
            y = float(tmp[1])
            pos = (x, y, 0.0)
            flag1 = True

            for p1 in self.pokemons:
                if all(x == y for x, y in zip(pos, p1.pos)):
                    flag1 = False
                    break
            if flag1:
                pokemon = Pokemon(pok['value'], pok['type'], pos, ++self.size)
                self.pokemons.append(pokemon)

    def load_agents(self, file_name):
        l = json.loads(file_name)
        ListAgents = l['Agents']
        for a in ListAgents:
            ag = a['Agent']
            tmp = ag['pos'].split(",")
            x = float(tmp[0])
            y = float(tmp[1])
            pos = (x, y, 0.0)
            flag = True
            for n in self.agents:
                if n.id == ag['id']:
                    n.value = ag['value']
                    n.src = ag['src']
                    n.dest = ag['dest']
                    n.speed = ag['speed']
                    n.pos = pos
                    flag = False
                    break
            if flag:
                agent = Agent(ag['id'], ag['value'], ag['src'], ag['dest'], ag['speed'], pos)
                self.agents.append(agent)

    def findEdge(self, graph: DiGraph, pokPos: tuple, type_p: int):
        for src in graph.nodes.values():
            for e in graph.all_out_edges_of_node(src.id):
                dest = graph.nodes.get(e)
                s = np.array(src.pos)
                d = np.array(dest.pos)
                p = np.array(pokPos)
                distSrcDest = np.linalg.norm(s - d)
                distSrcPok = np.linalg.norm(s - p)
                distPokDest = np.linalg.norm(d - p)

                if abs(distPokDest + distSrcPok) - sys.float_info.epsilon <= distSrcDest <= abs(
                        distPokDest + distSrcPok) + sys.float_info.epsilon:
                    print('src:' , src, 'dest: ', dest , 'type: ', type_p)
                    if (type_p > 0 and src.id < dest.id) or (src.id > dest.id and type_p < 0):
                        return src, dest
                    else:
                        return dest, src


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

    def findParentPath(self, idCurr: int, weight: float, listAdd: list):
        while self.graph.nodes[idCurr].father is not None:
            listAdd.append(idCurr)
            weight += self.graph.nodes[idCurr].father.weight
            idCurr = self.graph.nodes[idCurr].father.id
        return listAdd, weight

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

    def threeShortestPath(self, id1: int, id2: int, id3: int) -> (float, list):
        w, ans = self.shortest_path(id1, id2)
        w1, ans1 = self.shortest_path(id2, id3)
        ans1.pop(0)
        w += w1
        ans.extend(ans1)
        return w, ans


