"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace

from Players.Game import Game
from Players.Pokimon import Pokemon
from graph.GraphAlgo import GraphAlgo
from graph.DiGraph import DiGraph, Node
from client import Client
import data
import json
from pygame import gfxdraw
import pygame
from pygame import *

# init pygame


WIDTH, HEIGHT = 1080, 720
gray = Color(64, 64, 64)
blue = Color(6, 187, 193)
yellow = Color(255, 255, 102)
black = (0, 0, 0)
white = (255, 255, 255)
# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

algoGraph = GraphAlgo()
algoGraph.load_from_json(client.get_graph())
game = Game(client.get_info())
graph = game.algoGraph.graph

pokemon_json = client.get_pokemons()
pokemons_obj = game.load_pokemon(pokemon_json)
pokemonList = game.pokemons

agentList = game.agents

FONT = pygame.font.SysFont('Arial', 20, bold=True)

min_x = float(min(list(graph.nodes.values()), key=lambda node: node.pos[0]).pos[0])
min_y = float(min(list(graph.nodes.values()), key=lambda node: node.pos[1]).pos[1])
max_x = float(max(list(graph.nodes.values()), key=lambda node: node.pos[0]).pos[0])
max_y = float(max(list(graph.nodes.values()), key=lambda node: node.pos[1]).pos[1])


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def gui_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


r = 15

client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""


def drawNode(n1: Node):
    # n = graph.nodes.get(n1)
    x = gui_scale(float(n1.pos[0]), x=True)
    y = gui_scale(float(n1.pos[1]), y=True)
    gfxdraw.filled_circle(screen, int(x), int(y),
                          r, blue)
    gfxdraw.aacircle(screen, int(x), int(y),
                     r, Color(255, 255, 102))
    font = pygame.font.SysFont('chalkduster.ttf', 20)
    # img = font.render('hello', True, BLUE)
    id_srf = font.render(str(n.id), True, yellow)
    rect = id_srf.get_rect(topright=(x, y))
    screen.blit(id_srf, rect)


def drawOneEdge(src: Node, dest: Node, color: Color):
    src_x = gui_scale(src.pos[0], x=True)
    src_y = gui_scale(src.pos[1], y=True)
    dest_x = gui_scale(dest.pos[0], x=True)
    dest_y = gui_scale(dest.pos[1], y=True)
    pygame.draw.line(screen, color, (src_x, src_y), (dest_x, dest_y))


while client.is_running() == 'true':
    game.load_pokemon(client.get_pokemons())
    # pokemonList = game.pokemons
    for p in game.pokemons:
        x, y, _ = p.pos
        x = gui_scale(float(x), x=True)
        y = gui_scale(float(y), y=True)
        p.pos = (x, y, 0.0)

    game.load_agents(client.get_agents())
    for a in game.agents:
        x, y, _ = a.pos
        x = gui_scale(float(x), x=True)
        y = gui_scale(float(y), y=True)
        a.pos = (x, y, 0.0)
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(gray)

    # draw nodes
    for n in graph.nodes.values():
        drawNode(n)
        for e in graph.all_out_edges_of_node(n.id):
            dest = graph.nodes.get(e)
            drawOneEdge(n, dest, Color(21, 239, 246))

    # draw agents
    for agent in agentList:
        pygame.draw.circle(screen, color=Color(122, 61, 23), center=(agent.pos[0], agent.pos[1]), radius=10)

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemonList:
        pygame.draw.circle(screen,color= Color(0, 255, 255),center=(p.pos[0], p.pos[1]), radius=10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    # choose next edge
    min_sp
    for agent in game.agents:
        for pok in game.pokemons:
            sp = algoGraph.shortest_path(agent.id, pok.id)



        if agent.dest == -1:
            next_node = (agent.src - 1) % len(graph.nodes)
            print("src: ", agent.src, "len: ", len(graph.nodes), "next: ", next_node)
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    client.move()
# game over:
