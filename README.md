![pokemon](https://user-images.githubusercontent.com/77111035/148031517-120da067-3d9b-412a-b3a5-6341ee62a560.gif)
# Pokemon Game Ex4
this is the fourth assignment in the OOP course, ariel univerisy. In this assignment we should have to crate a pokemon game wich consists of some of Agants (Pokabolls)
that shuld capture as much as possible Pokemons in limited time. each Pokemon has a value, so the agant will prefer to cath the most worth pokemon at any time.
In addition each agant has a speed - As much as he will eat more pokemon his speed will be increased.

# This assignment was written by
 [Taliya Shitreet](https://github.com/taliyashitreet "Profile") and  [Renana Rimon](https://github.com/renanarimon "Profile")
 # Our game look like:
 ![image](https://user-images.githubusercontent.com/77111035/148042934-cfc27add-ac10-4940-b0cb-f5538182ee53.png)

 
# pakeges: 
![image](https://user-images.githubusercontent.com/77111035/148047663-434ce3f6-d5c2-42a5-a4dc-9e87362d4deb.png)

**client:**
doesnt written by us, this class activate the server 
**student_code:**
the main class contains the GUI, represent the graph, pokemons and agants.
- Main Functions: <br />
- pickPok2Agent() : this function represents the algorithm of the game and assigns each Agent the best Pokemon according to the following criteria:<br />
  1. The shortest path (in terms of weight) <br />
  2. Pokemon value <br />
  ---> We search the maximum value of:  (Pokemon value) - (weight of path) <br />
  The function is Bijection: each Agent has one Pokemon adapted at each iteration and vice versa. <br />
  this algotithm create to each agant a list of node he need to pass in order,the last two nodes are the srs and dest of the pokemon's edge. <br />

**agant:** 
contains : id, speed, value, src, dest, pos
**pokimon:** 
contains : pos, value, type (If he is on the edge descending or ascending) 
**Game:** 
contains : the all info of the game (load as Json file), has the graph (Digraph)
***Main function :*** 
- shortestPath(): <br />
this unction find the shortest path between to nodes on the graph by the Dijkstra's algorithm [Dijkstra](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) 
- load_agents() , load_pokemon() :  <br />
  create a agant and pokemon from Json format <br />
- findEdge() :<br />
  this tunction finds the src and dest of a given pokemon's edge. calculate distants two point and checking if : (dest pos) =< (pokemin pos) =< (src pos) <br />
We took the samo implement of : [OOP_Ex3](https://github.com/taliyashitreet/OOP_Ex3)
# How To Run
- in the terminal: java -jar Ex4_Server_v0.0.jar 0 (instead of 0 put any level you want to run)
- run the "student_code" at the project
