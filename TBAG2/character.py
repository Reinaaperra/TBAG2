class Character():

    def __init__(self, char_name, char_description, inventory = None):
    #Initialises values but when an instance is created, attributes are empty until explicitly set.
        self.name = char_name
        self.description = char_description
        self.conversation = None
        self.inventory = inventory if inventory is not None else [] 

    def describe(self):
    # Prints the characters and description when encountered.
        print(f"{self.name} is here!")
        print( self.description)

    def set_conversation(self, conversation):
    # Lets the character have dialogue. 
        self.conversation = conversation

    def talk(self):
    # Triggers the character dialogue.
        if self.conversation is not None:
            print(f"{self.name} : {self.conversation}")
        else:
            print(f"{self.name} doesn't want to talk to you.")

    # Place holder in parent class.
    def fight(self, weapon):
    # Non-Enemy Characters don't engage in combat
        print(f"{self.name} doesn't want to fight with you")
        return True
        # Returns true to imply the fight has been "won"
        # to avoid disrupting game flow.


class Enemy(Character):
    # Inherits the Character parent class but represents Enemy interactions.
    def __init__(self, char_name, char_description, inventory=None):
        super().__init__(char_name, char_description)
        self.weakness = None  # Weapon that can defeat the enemy in combat.
        self.bribed = False  # Boolean indicates if enemy has been successfully bribed.
        self.desired_item = None  # Item enemy will let you bribe them with.
        self.inventory = inventory if inventory is not None else []  # Enemy's inventory as a list.
        self.sleeping = False  # Boolean indicating if enemy is sleeping.
        self.key = None  # Key that can be given to the player.

    def add_key(self, key):
        self.key = key  # Assign a key to the enemy

    # Setting and retrieving the enemy's weakness (used in combat).
    def set_weakness(self, weapon_weakness):
        self.weakness = weapon_weakness.lower()

    def get_weakness(self):
        return self.weakness

    # The enemy's sleep status (used to put the enemy to sleep or check whether they are asleep).
    def set_sleep(self, sleep_status):
        self.sleeping = sleep_status

    def get_sleep_status(self):
        return self.sleeping

    # Setting and retrieving the item that the enemy desires (for bribes).
    def set_desired_item(self, bribe_item):
        self.desired_item = bribe_item.lower()

    def get_desired_item(self):
        return self.desired_item

    def add_to_inventory(self, item):
        self.inventory.append(item)


    def fight(self, chosen_weapon):
        while True:

            if self.sleeping:
                print(f"Shhhh! {self.name} is sleeping, you can sneakily defeat them!")
                return True
            
            if chosen_weapon == self.weakness:
                print(f"You fended {self.name} off with the {chosen_weapon}.")
                return True, self.inventory, self.key
            else:
                print(f"{self.name} laughs at your attempt to attack with the {chosen_weapon}!")
                return False, [], None  # The player loses and cannot continue fighting


    def bribe(self, bribe_item):
        # Allows the player to bribe the enemy using a specific item.
        if bribe_item.lower() == self.desired_item:
            # If the item matches, bribe is successful, and the enemy will let the player pass.
            print(f"{self.name} accepts {bribe_item} and lets you pass!")
            self.bribed = True
            return True, self.inventory, self.key  # Return loot and key
        else:
            # Otherwise, the bribe fails.
            print(f"{self.name} doesn't care for {bribe_item}.")
            return False, [], None  # Return empty on failed bribe


    def sleep(self, player_inventory):
        if 'Sleep Potion' in player_inventory:
            if not self.sleeping:
                print(f"Shhh! You have put {self.name} to sleep using the potion.")
                self.sleeping = True
            else:
                print(f"{self.name} is already asleep, shhhhh!")
        else:
            print("OOPS.. You don't have the Sleep Potion to make them sleep!")

        
class Player:
    def __init__(self, player_name, chosen_weapons):
        self.player_name = player_name  # Store the player's name.
        self.chosen_weapons = chosen_weapons  # Store the chosen weapons.
        self.inventory = self.inventory = {
        "weapons": chosen_weapons,
        "key": [],
        "tool": [],
        "loot": [],
        "bribes": []
    }

    def has_key(self, room_name):
        return any(key.get_name() == room_name for key in self.inventory if key.get_category() == "Key")
    
    def add_to_inventory(self, item):
        # Adds an item to the player's inventory.
        self.inventory.append(item)
        print(f"{item.get_name()} has been added to your inventory.")

    def check_inventory(self):
        # Displays the items in the player's inventory.
        if self.inventory:
            print("Your inventory contains:")
            for item in self.inventory:
                print(f"- {item.get_name()}")
        else:
            print("Your inventory is empty.")

    def display_weapons(self):
        # Displays the player's chosen weapons.
        print("Your chosen weapons:")
        for index, weapon in enumerate(self.chosen_weapons, 1):
            print(f"{index}. {weapon}")

    def use_weapon(self, weapon_index):
        # Allows the player to select and use a weapon from their chosen weapons.
        if 0 <= weapon_index < len(self.chosen_weapons):
            weapon = self.chosen_weapons[weapon_index]
            print(f"You are using {weapon}.")
            return weapon
        else:
            print("Invalid weapon choice.")
            return None