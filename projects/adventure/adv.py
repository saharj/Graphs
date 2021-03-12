from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "/Users/sahar/Documents/lambda-excercise/Graphs/projects/adventure/maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "/Users/sahar/Documents/lambda-excercise/Graphs/projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# print('****')
# print(player.current_room.id)
# print(player.current_room.get_exits())
# print(player.current_room.get_room_in_direction('n'))
# player.travel('n', True)
# print(player.current_room.get_room_in_direction('n'))
# print(player.travel(direction))
# print('****')

traversal_graph = {}
prev_room_ids = []
prev_dirs = []
opposites = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
}

while True:
    current = player.current_room

    if len(prev_room_ids) > 0:
        if traversal_graph[prev_room_ids[-1]][prev_dirs[-1]] is None:
            traversal_graph[prev_room_ids[-1]][prev_dirs[-1]] = current.id
        else:
            player.travel(opposites[prev_dirs[-1]], False)
            prev_dirs.pop()
            prev_room_ids.pop()
            continue
    # if current room is not in graph add it and it's directions
    if current.id not in traversal_graph:
        available_dir = current.get_exits()
        obj = {}
        for direction in available_dir:
            if len(prev_dirs) > 0 and direction == opposites[prev_dirs[-1]]:
                obj[direction] = prev_room_ids[-1]
            else:
                obj[direction] = None
        traversal_graph[current.id] = obj
    # For exists of the current room
    is_end = True
    for ex in traversal_graph[current.id]:
        # if exit is not met, travel to that direction
        if traversal_graph[current.id][ex] is None:
            prev_room_ids.append(current.id)
            prev_dirs.append(ex)
            player.travel(ex, False)
            is_end = False
            break
    # if node doesn't have next room, travel back
    if is_end:
        # we have visited all rooms and are back at the start
        if len(prev_dirs) == 0:
            break
        player.travel(opposites[prev_dirs[-1]], False)
print("VVVVVV")
print(traversal_graph)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
