import json
import os.path
from os import path

from Players.Agent import Agent
from Players.Pokimon import Pokemon
from client_python.client import Client

from graph.GraphAlgo import GraphAlgo


class Game:
    # algoGraph = GraphAlgo()

    def __init__(self, json_str: str):
        # client = Client()
        l = json.loads(json_str)['GameServer']

        print(l)

        self.numOfPokemons = l['pokemons']
        self.is_logged_in = l['is_logged_in']
        self.moves = l['moves']
        self.grade = l['grade']
        self.game_level = l['game_level']
        self.max_user_level = l['max_user_level']
        self.id = l['id']
        self.graph_json = l['graph']
        self.numOfAgent = l['agents']
        print(self.graph_json)
        self.algoGraph = GraphAlgo()

        path1 = "../" + json_str
        print(path1)
        self.algoGraph.load_from_json("../" + self.graph_json)
        self.pokemons = []
        self.agents = []


    def load_pokemon(self, file_name):

        l = json.loads(file_name)
        print(type(l))
        ListPokemons = l['Pokemons']

        for p in ListPokemons:
            pok = p['Pokemon']
            tmp = pok['pos'].split(",")
            x = float(tmp[0])
            y = float(tmp[1])
            pos = (x, y, 0.0)
            pokemon = Pokemon(pok['value'], pok['type'], pos)
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
            agent = Agent(ag['id'], ag['value'], ag['src'], ag['dest'], ag['speed'], pos)
            self.agents.append(agent)

