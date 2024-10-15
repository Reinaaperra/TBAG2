from character import Enemy, Character
from room import Room

class Game_start():
    def __init__(self, player_name, chosen_weapons, starting_location):
        self.player_name = player_name
        self.chosen_weapons = chosen_weapons
        self.starting_location = starting_location

    @staticmethod # Helper function
    # Decorator that defines method that belongs to the class, but does not need access to any instance of the class,
    # doesn't take self or cls as first parameter and can be called directly on the class itself rather than on an instance of the class.
    def setup_player():
    # Player name set up
        player_name = input("Enter your players name: ")
        return player_name

    @staticmethod
    def choose_weapons():
    # Weapon selection
        available_weapons = ["Wooden Stake", "Flamethrower", "Silver Dagger", "Magic Wand", "Poison Gas", "Crossbow"]
        print("Choose 2 weapons, and choose wisely: ")
        for index, weapon in enumerate(available_weapons, 1):
    # enumerate takes the list and returns pairs of each item's index and value.
            print(f"{index}: {weapon}")
    
        chosen_weapons = [] # Empty list to store players chosen weapons.
    
        for _ in range(2): # Allows the player to only choose 2 weapons.
            choice = int(input("Enter the number of your weapon choice: ")) - 1
            chosen_weapons.append(available_weapons[choice])

        return chosen_weapons


    @staticmethod
    def choose_starting_room():
        print("Where would you like to start? (Note: Entrance is not an option)")
        starting_location = ["Kitchen", "Ballroom", "Dining Hall", "Primary Bedroom", "Bathroom", "Attic", "Basement"]

        for index, room in enumerate(starting_location, 1):
            print(f"{index}: {room}")
        
        while True:
            try:
                choice = int(input("Choose a room number: ")) - 1
                if 0 <= choice < len(starting_location):
                    return starting_location[choice]
                else:
                    print("Invalid choice. Please choose a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
