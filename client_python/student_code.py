import json
import sys
import time

import pygame_gui

from pokemonGame.Game import Game
from pokemonGame.Pokimon import Pokemon
from graph.DiGraph import DiGraph, Node
from client import Client
from pygame import gfxdraw
import pygame
from pygame import *
import time
from types import SimpleNamespace
"""
run game class using pygame
"""

# init pygame

WIDTH, HEIGHT = 1080, 720
black = Color(0, 0, 0)
r = 5
# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

pygame.init()
bg = pygame.image.load("../images/backgruond.jpg")
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=HWSURFACE | DOUBLEBUF | RESIZABLE)
fake_screen = screen.copy()
background = pygame.Surface((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)

clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

clock10 = pygame.time.Clock()

time_counter = time.time()
move_counter = 0
game = Game(client.get_info())
graph = game.graph

# FONT = pygame.font.SysFont('Arial', 20, bold=True)
fontTimer = pygame.font.SysFont("comicsansms", 60)
fontScore = pygame.font.SysFont("comicsansms", 20)
fontNodeId = pygame.font.SysFont('chalkduster.ttf', 30)
font = pygame.font.SysFont('chalkduster.ttf', 20)


manager = pygame_gui.UIManager((WIDTH, HEIGHT))
btnStop = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen.get_width() - 100, 0), (115, 40)),
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


# add agents

for i in range(game.numOfAgent):
    st = "{id:"
    st += str(i)
    st += "}"
    client.add_agent(st)

# this commnad starts the server - the game is running now
client.start()

"""
gui functions to draw graph:
    1. drawNode
    2. drawOneEdge
"""


def drawNode(n1: Node):
    x = gui_scale(float(n1.pos[0]), x=True)
    y = gui_scale(float(n1.pos[1]), y=True)
    gfxdraw.filled_circle(screen, int(x), int(y),
                          r, black)
    gfxdraw.aacircle(screen, int(x), int(y),
                     r, Color(255, 255, 102))
    id_srf = fontNodeId.render(str(n.id), True, black)
    rect = id_srf.get_rect(topright=(x - 10, y - 10))
    screen.blit(id_srf, rect)


def drawOneEdge(src: Node, dest: Node, color: Color):
    src_x = gui_scale(src.pos[0], x=True)
    src_y = gui_scale(src.pos[1], y=True)
    dest_x = gui_scale(dest.pos[0], x=True)
    dest_y = gui_scale(dest.pos[1], y=True)
    pygame.draw.line(screen, color, (src_x, src_y), (dest_x, dest_y))


def pickPok2Agent():
    """
    The function assigns each Agent the best Pokemon according to the following criteria:
        1. The shortest path (in terms of weight)
        2. Pokemon value

    The function is Bijection: each Agent has one Pokemon adapted at each iteration and vice versa.
    ** update agent.orderList with new path **
    """
    for agent in game.agents:
        if agent.src == agent.lastDest or len(agent.orderList) == 0:
            v = -sys.maxsize
            bestPok = Pokemon(0.0, 0, (0.0, 0.0, 0.0), 0)
            for pok in game.pokemons:
                if not pok.took:
                    src1, dest1 = game.findEdge(pok.pos, pok.type)
                    agent.lastDest = dest1.id
                    if agent.src == src1.id:
                        w, lst = game.shortest_path(src1.id, dest1.id)
                    elif agent.src == dest1.id:
                        lst = [src1.id, dest1.id]
                        bestPok = pok
                        agent.orderList = lst
                        break
                    else:
                        w, lst = game.threeShortestPath(agent.src, src1.id, dest1.id)

                    lst.pop(0)
                    if (pok.value - w) > v:
                        v = pok.value - w
                        bestPok = pok
                        agent.orderList = lst

            bestPok.took = True


"""
while game is running:
    1. load & scale pokemons
    2. load & scale agents
    3. handle events
    4. draw: graph, agents, pokemons
    5. pickPok2Agent()
"""

while client.is_running() == 'true':
    # time.sleep(0.1)
    inf = json.loads(client.get_info(), object_hook = lambda d: SimpleNamespace(**d)).GameServer
    time_delta = clock.tick(60) / 1000.0

    # load & scale pokemons
    game.load_pokemon(client.get_pokemons())
    for p in game.pokemons:
        x, y, _ = p.pos
        x = gui_scale(float(x), x=True)
        y = gui_scale(float(y), y=True)
        p.posScale = (x, y, 0.0)

    # load & scale agents
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
    fake_screen.blit(bg, (0, 0))
    screen.blit(pygame.transform.scale(fake_screen, screen.get_rect().size), (0, 0))
    manager.draw_ui(screen)
    timerStr = "time to end: "
    try:
        timerStr += client.time_to_end()
    except:
        timerStr += "0"
    timer = fontScore.render(timerStr, True, black)
    screen.blit(timer, (0, 0))

    # st = "score: "
    # st += str(game.grade)
    # sc = fontScore.render(st, True, black)
    # screen.blit(sc, (200,0))

    # draw graph
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
        agentId = font.render(str(agent.id), True, black)
        # rect = id_srf.get_rect(topright=(x - 10, y - 10))
        screen.blit(image, rect)
        screen.blit(agentId, rect)

    # draw pokemons
    for p in game.pokemons:
        if p.type > 0:
            image = p.image_U
        else:
            image = p.image_D
        rect = image.get_rect()
        rect.center = (p.posScale[0], p.posScale[1])
        pokVal = font.render(str(p.value), True, black)
        screen.blit(image, rect)
        screen.blit(pokVal, rect)
    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    pickPok2Agent()

    # move each agent to the next node on the path to pokemon according to his current orderList
    flag = True
    for agent in game.agents:
        if agent.dest == -1:
            flag = False
            nextNode = agent.orderList.pop(0)
            print("next: ", nextNode)
            print("agent: ", agent.id)
            client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(nextNode) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    if inf.moves/(time.time() - time_counter) < 10 and flag:
        client.move()

# game over
