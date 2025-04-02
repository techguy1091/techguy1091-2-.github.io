import random

# Project dungeon-game 0.5
# Mise à jour 09/03
# Groupe 10: CASSARD-BRO Marcel/ HONORE Gabriel/ NAEGELEN Hugo
# Nouvelle version semi-fonctionnelle, 09/03/2025

# Instructions
def show_instructions():
    print("""
    Welcome to the Dungeon Escape!
    Commands: go [direction], take [item], inventory, exit
    Find the key and escape through the door!
    """)

# Define the map
dungeon_map = {
    'entrance': {'north': 'hallway', 'item': None},
    'hallway': {'south': 'entrance', 'east': 'armory', 'west': 'library', 'north': 'trap', 'item': 'torch'},
    'armory': {'west': 'hallway', 'item': 'sword'},
    'trap': {'message': 'You fell into a trap and died!'},
    'library': {'east': 'hallway', 'north': 'secret room', 'item': 'book', 'monster': True},
    'secret room': {'south': 'library', 'item': 'key', 'monster': True},
    'exit': {'locked': True}
}

# Define player
player = {'location': 'entrance', 'inventory': []}

def move(direction):
    global game_running  # To track if the game should continue

    if direction in dungeon_map[player['location']]:
        new_location = dungeon_map[player['location']][direction]

        if new_location == 'trap':
            print("You fell into a trap and died!")
            game_running = False  # End game
            return

        player['location'] = new_location
        print(f"You moved {direction} to the {new_location}.")

        # Check if there's a monster
        if dungeon_map[new_location].get('monster', False):
            monster_encounter()

        # Display available directions and items
        available_directions = [dir for dir in dungeon_map[new_location] if dir not in ['item', 'locked', 'message', 'monster']]
        item = dungeon_map[new_location].get('item', None)

        print(f"Available directions: {available_directions}" if available_directions else "No available directions.")
        print(f"There is a {item} here." if item else "There's nothing to take here.")

    else:
        print("You can't go that way!")

def take_item():
    item = dungeon_map[player['location']].get('item')
    if item:
        player['inventory'].append(item)
        print(f"You picked up {item}.")
        dungeon_map[player['location']]['item'] = None  # Remove item from room
    else:
        print("There's nothing to take here.")

def check_exit():
    if player['location'] == 'exit':
        if 'key' in player['inventory']:
            print("Congratulations! You unlocked the door and escaped!")
            global game_running
            game_running = False  # End game
        else:
            print("The door is locked! Find the key first.")

def monster_encounter():
    global game_running

    print("A monster is here!")
    command = input("Do you want to 'fight', 'hide', or 'run'? ").lower()

    if command == 'hide':
        if random.choice([True, False]):  # 50/50 chance
            print("The monster found you!")
            command = input("Do you want to 'fight' or 'run'? ").lower()
        else:
            print("You successfully hid from the monster.")
            return

    if command == 'fight':
        if 'sword' in player['inventory']:
            print("You attack and kill the monster!")
            dungeon_map[player['location']]['monster'] = False  # Monster is gone
        else:
            print("You have no weapon! The monster kills you.")
            game_running = False  # End game

    elif command == 'run':
        print("You tried to run but the monster caught you and you died.")
        game_running = False  # End game

# Start game
show_instructions()
game_running = True

while game_running:
    command = input("\nWhat do you want to do? ").lower().split()

    if not command:
        print("Invalid command.")
        continue

    action = command[0]

    if action == 'go' and len(command) > 1:
        move(command[1])
    elif action == 'take':
        take_item()
    elif action == 'inventory':
        print("You have:", ', '.join(player['inventory']) if player['inventory'] else "nothing.")
    elif action == 'exit':
        check_exit()
    else:
        print("Unknown command!")

print("Game over.")  # Display when the game ends
