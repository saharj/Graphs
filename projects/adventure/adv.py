from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "/Users/sahar/Documents/lambda-excercise/Graphs/projects/adventure/maps/test_cross.txt"
# map_file = "/Users/sahar/Documents/lambda-excercise/Graphs/projects/adventure/maps/test_loop.txt"
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

# create an empty dict to keep track of visited rooms (Maybe set works too?)
# add the first room id to the dic with the value of True
# define the recursive fn that receives prev room.id and the prev direction
# in the room
# if room id exist in the dict, return
# else, add the current room id to the dic with the val of True
# create a map for all vailable directions
# if prev direction is available, update the value of the opposite direction with the prev room id
# call the fn for any other directions whitout the value
# if in the current room there is no direction without value,
# return an obj with the current room data + returned data, and current room id
# {data: {2: {"n": 1}, 3:{...}}, roomId: 2}
# return the value of data
visited_rooms = set()
opposites = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
}


def visit(player, prev_room_id=None, prev_direction=""):
    room = player.current_room
    next_room_data = {}
    room_map = {}

    if room.id not in visited_rooms:
        visited_rooms.add(room.id)
        available_dir = room.get_exits()
        room_map = {room.id: {}}
        for direction in available_dir:
            if prev_room_id is not None and direction == opposites[prev_direction]:
                room_map[room.id][direction] = prev_room_id
            else:
                room_map[room.id][direction] = None

        # if a door in the room is not met
        if None in room_map[room.id].values():
            for door in room_map[room.id]:

                if room_map[room.id][door] is None:
                    temp_player = player
                    temp_player.travel(door)
                    traversal_path.append(door)
                    next_room = visit(temp_player, room.id, door)
                    if next_room is not None:
                        room_map[room.id][door] = next_room["id"]
                        next_room_data = {
                            **next_room["data"], **next_room_data}
        else:
            player.travel(opposites[prev_direction])
            traversal_path.append(opposites[prev_direction])
    else:
        print("Room visited")
        print(room.id)
        print(room_map)
        print(next_room_data)
        return
    next_room_data = {**room_map, **next_room_data}

    return {"id": room.id, "data": next_room_data}


visit(player)
# print(ss["data"])


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
# print("moves")
# print(len(traversal_path))

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
