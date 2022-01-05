from unittest import TestCase
from pokemonGame.Game import Game


class test_Game(TestCase):
    def setUp(self) -> None:
        self.info = """
                    {
                        "GameServer":{
                            "pokemons":1,
                            "is_logged_in":false,
                            "moves":1,
                            "grade":0,
                            "game_level":0,
                            "max_user_level":-1,
                            "id":0,
                            "graph":"data/A0",
                            "agents":1
                        }
                    }
                    """

        self.game = Game(self.info)
        self.graph = self.game.graph
        self.pokemon = """
                         {
                             "Pokemons":[
                                 {
                                     "Pokemon":{
                                         "value":5.0,
                                         "type":-1,
                                         "pos":"35.197656770719604,32.10191878639921,0.0"
                                     }
                                 }
                             ]
                         }

                         """
        self.agant = """
                          {
                              "Agents":[
                                  {
                                      "Agent":
                                      {
                                          "id":0,
                                          "value":0.0,
                                          "src":0,
                                          "dest":1,
                                          "speed":1.0,
                                          "pos":"35.18753053591606,32.10378225882353,0.0"
                                      }
                                  }
                              ]
                          }
                          """
        self.game.load_pokemon(self.pokemon)
        self.game.load_agents(self.agant)
        self.pok = self.game.pokemons.pop(0)

    def test_load_pokemon(self):  # chacks whole of loads
        self.assertEqual(len(self.game.pokemons), 0)
        self.assertEqual(len(self.game.agents), 1)
        self.assertEqual(self.pok.value, 5.0)

    def test_find_edge(self):
        src, dest = self.game.findEdge(self.pok.pos, self.pok.type)
        s = "" + str(src.id) + " " + str(dest.id)
        self.assertEqual("9 8", s)

    def test_shortest_path(self):
        self.assertEqual((1.4575484853801393, [9, 8]), self.game.shortest_path(9, 8))
        self.assertEqual((4.439215347640289, [1, 0, 10, 9]), self.game.shortest_path(1, 9))
        self.assertEqual((1.4620268165085584, [0, 10]), self.game.shortest_path(0, 10))
        self.assertEqual(self.game.shortest_path(0, 11), "node not exist")

    def test_three_shortest_path(self):
        self.assertEqual((5.484805465368355, [10, 0, 1, 2, 3]), (self.game.threeShortestPath(10, 0, 3)))
        self.assertEqual((5.765082354940145, [5, 6, 7, 8, 9]), (self.game.threeShortestPath(5, 8, 9)))
        self.assertEqual((9.010749681933625, [3, 2, 1, 0, 1, 2, 3]), self.game.threeShortestPath(3, 0, 3))
        self.assertEqual("node not exist", (self.game.threeShortestPath(11, 10, 9)))