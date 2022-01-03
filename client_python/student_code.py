"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import sys
from types import SimpleNamespace

import pygame_gui

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
bg = pygame.image.load("../images/backgruond.jpg")
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=HWSURFACE|DOUBLEBUF|RESIZABLE)
fake_screen = screen.copy()
background = pygame.Surface((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
# background.blit(bg, (0,0), special_flags=RESIZABLE)
# background.fill(bg)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

algoGraph = GraphAlgo()
algoGraph.load_from_json(client.get_graph())
game = Game(client.get_info())
graph = game.algoGraph.graph
# copyGraph = algoGraph.copy()

# pokemon_json = client.get_pokemons()
# pokemons_obj = game.load_pokemon(pokemon_json)
#
# pokemonList = game.pokemons
# agentList = game.agents

FONT = pygame.font.SysFont('Arial', 20, bold=True)

manager = pygame_gui.UIManager((WIDTH, HEIGHT))
btnStop = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen.get_width()-100, 0), (115, 40)),
                                       text='STOP GAME',
                                       manager=manager)

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


r = 5
for i in range(game.numOfAgent):
    st = "{id:"
    st += str(i)
    st += "}"
    client.add_agent(st)
# client.add_agent("{\"id\":0}")
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
    x = gui_scale(float(n1.pos[0]), x=True)
    y = gui_scale(float(n1.pos[1]), y=True)
    gfxdraw.filled_circle(screen, int(x), int(y),
                          r, black)
    gfxdraw.aacircle(screen, int(x), int(y),
                     r, Color(255, 255, 102))
    font = pygame.font.SysFont('chalkduster.ttf', 20)
    # img = font.render('hello', True, BLUE)
    id_srf = font.render(str(n.id), True, black)
    rect = id_srf.get_rect(topright=(x, y))
    screen.blit(id_srf, rect)


def drawOneEdge(src: Node, dest: Node, color: Color):
    src_x = gui_scale(src.pos[0], x=True)
    src_y = gui_scale(src.pos[1], y=True)
    dest_x = gui_scale(dest.pos[0], x=True)
    dest_y = gui_scale(dest.pos[1], y=True)
    pygame.draw.line(screen, color, (src_x, src_y), (dest_x, dest_y))


while client.is_running() == 'true':
    time_delta = clock.tick(60) / 1000.0
    # if game.numOfPokemons > len(game.pokemons):
    game.load_pokemon(client.get_pokemons())
    for p in game.pokemons:
        x, y, _ = p.pos
        x = gui_scale(float(x), x=True)
        y = gui_scale(float(y), y=True)
        p.posScale = (x, y, 0.0)

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
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == btnStop:
                    pygame.quit()
                    exit(0)

        manager.process_events(event)
    manager.update(time_delta)
    fake_screen.fill('black')
    fake_screen.blit(bg, (0,0))
    screen.blit(pygame.transform.scale(fake_screen, screen.get_rect().size), (0, 0))
    manager.draw_ui(screen)
    rect = pygame.draw.rect(screen, gray, [0, 0,150,100], 0)



    # draw nodes
    for n in graph.nodes.values():
        drawNode(n)
        for e in graph.all_out_edges_of_node(n.id):
            dest = graph.nodes.get(e)
            drawOneEdge(n, dest, black)

    # draw agents
    for agent in game.agents:
        image = agent.image
        rect = image.get_rect()
        rect.center = (agent.pos[0], agent.pos[1])
        screen.blit(image, rect)

    for p in game.pokemons:
        # print(p.pos)
        if p.type > 0:
            image = p.image_U
        else:
            image = p.image_D
        rect = image.get_rect()
        rect.center = (p.posScale[0], p.posScale[1])
        screen.blit(image, rect)
    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    for agent in game.agents:
        # print("****",agent.src , agent.lastDest)
        if agent.src == agent.lastDest or len(agent.orderList) == 0:
            # print("inside")
            v = -sys.maxsize
            bestPok = Pokemon(0.0, 0, (0.0, 0.0, 0.0), 0)
            for pok in game.pokemons:
                if not pok.took:
                    src1, dest1 = game.findEdge(graph, pok.pos, pok.type)
                    agent.lastDest = dest1.id
                    print("src1, dest1:", src1, dest1)
                    # print([agent.src, src1.id, dest1.id])
                    if agent.src == src1.id:
                        w, lst = game.shortest_path(src1.id, dest1.id)
                        # l = [src1.id, dest1.id]
                    elif agent.src == dest1.id:
                        lst = [src1.id, dest1.id]
                        bestPok = pok
                        agent.orderList = lst
                        # print("lst elif:",lst)
                        break
                    else:
                        w, lst = game.threeShortestPath(agent.src, src1.id, dest1.id)
                        # l = [agent.src, src1.id, dest1.id]

                    # print("l: ",l)

                    # lst, w = game.TSP(l)
                    # print("tsp: ", lst)
                    lst.pop(0)
                    # print("after pop: ", lst)
                    if (pok.value - w) > v:
                        v = pok.value - w
                        bestPok = pok
                        agent.orderList = lst
                # else:
            # game.pokemons.remove(bestPok)
            bestPok.took = True

    for agent in game.agents:
        if agent.dest == -1:
            # if len(agent.orderList)>0:
            print(agent.orderList)
            nextNode = agent.orderList.pop(0)

            # print('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(nextNode) + '}')
            client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(nextNode) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())
        client.move()

# game over:
