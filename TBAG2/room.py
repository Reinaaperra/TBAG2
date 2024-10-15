from character import Enemy, Character, Player
from item import Item

class Room:
    # The behaviour and attributes of a room in the game.
    def __init__(self, room_name, description, required_key=None):
        # Initialises values but when an instance is created, attributes are empty until explicitly set.
        self.name = room_name  # Stores the name of the room.
        self.description = description  # Stores the description of the room.
        self.linked_rooms = {}  # Dictionary that links directions to the rooms for navigation.
        self.character = None  # Stores any characters inhabiting each room.
        self.items = []  # List of room items that players can find.
        self.key_required = None  # Key required to enter the room.

    def set_key_required(self, key_item):
        self.key_required = key_item
    
    def get_key_required(self):
        return self.key_required
    
    def can_enter(self, player_inventory):
        # Check if the player has the key in their inventory
        if self.key_required:
            return any(key.get_name() == self.key_required.get_name() for key in player_inventory["key"])
        return True
    
    # Set, retrieve and print room descriptions.
    def set_description(self, room_description):
        self.description = room_description

    def get_description(self):
        return self.description

    def describe(self):
        print(self.description)

    # Set/change and retrieve room names.
    def set_name(self, room_name):
        self.name = room_name

    def get_name(self):
        return self.name

    # Set and retrieve characters in specific rooms.
    def set_character(self, new_character):
        self.character = new_character

    def get_character(self):
        return self.character

    def add_item(self, item):
        self.items.append(item)  # Add an item to a room

    # Links a room to this room in a specific direction, creating connections between rooms.
    def link_room(self, room_to_link, direction):
        self.linked_rooms[direction] = room_to_link

    # Prints the room's name, description, and the rooms that are linked to it in different directions. Useful for players.
    def get_details(self):
        print(self.name)
        print("-------------------------")
        print(self.description)
        for direction in self.linked_rooms:
            room = self.linked_rooms[direction]
            print(f"The {room.get_name()} is {direction}")

    def move(self, direction, player_inventory):
        if direction in self.linked_rooms:
            next_room = self.linked_rooms[direction]
            if next_room.can_enter(player_inventory): 
                return next_room
            else:
                print(f"You need the {next_room.get_key_required()} to enter this room.")
        else:
            print("You can't go that way!")
        return None

     
    def search_room(self):
        if self.items:
            # Checks if the room has any items
            print("You've found:")
            # Categorising the items
            weapons = [item for item in self.items if item.get_category().lower() == "weapons"]
            tools = [item for item in self.items if item.get_category().lower() == "tool"]
            bribes = [item for item in self.items if item.get_category().lower() == "bribe"]
            loot = [item for item in self.items if item.get_category().lower() == "loot"]
            keys = [item for item in self.items if item.get_category().lower() == "key"]

            if weapons:
                print("Weapons: " + ", ".join(item.get_name() for item in weapons))
            if tools:
                print("Tools: " + ", ".join(item.get_name() for item in tools))
            if bribes:
                print("Bribe: " + ", ".join(item.get_name() for item in bribes))
            if loot:
                print("Loot: " + ", ".join(item.get_name() for item in loot))
            if keys:
                print("Keys: " + ", ".join(item.get_name() for item in keys))
        else:
            print("There are no items to be found in this room.")
    
    # Notify the player that they can interact with the characters in the room.
    def interact_with_character(self):
        if self.character:
            print(f"You see {self.character.name} in the room.")
            print(f"You can talk to {self.character.name} for advice or fight them to obtain a key.")
            
            # Automatically prompt the player to fight the character for the key.
            if isinstance(self.character, Enemy) and self.character.get_weakness() is not None:
                print(f"You must defeat {self.character.name} to get the key to proceed to the next room.")
            else:
                print(f"{self.character.name} does not seem to want to fight.")
