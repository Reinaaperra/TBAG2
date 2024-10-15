# Class imports
from room import Room
from character import Enemy, Character, Player
from item import Item
from start import Game_start

class Game:
    def __init__(self, starting_room, player_inventory):
        self.current_room = starting_room 
        # Specifies the room game starts in holding a reference to the room allowing other methods 
        # in the class to access and manipulate the current room.
        self.room_descriptions_shown = {}  # Track room descriptions shown.
        # Implemented as previous code repeatedly printed the same descriptions over and over again,
        # this allows the description to only show the first time a player enters the room, improving game play.
        self.player_inventory = player_inventory
        self.myrtle_welcome_shown = False  # Has Myrtle's welcome been shown
        self.magic_ring_used = False  # Track if the Magic Immortality Ring has been used
        

    def game_won(self):
        print("\nYou are now the proud owner of the haunted house!")
        print("You’ve defeated the enemies, collected the keys, and found the House Deed!")
        print("Congratulations! You Win!")
        print("\nGame Over.\n")
        exit()  # End the game

    def enter_room(self, room):
    # Method responsible for managing players transitions into new rooms.
        self.current_room = room
        # Updates instance variable to reference the current room passed as an argument.
        # This is what allows the game to keep track of where the player is as it changes the player's 
        # current location.
        
        # Show room description only once
        if self.current_room not in self.room_descriptions_shown:
        # The conditonal argument line 20 is used for and checks dictionary to track room descriptions 
        # already shown - set on line 14. Necessary for game play outcome desired.
            print(self.current_room.description) 
            # Prints the room description if it hasn't been shown before.
            self.room_descriptions_shown[self.current_room] = True
            # Printed description is then added to dictionary to prevent repetition.

        
        if self.current_room.get_character() is not None:
            self.current_room.interact_with_character()
        
        self.handle_player_actions()


    def inventory_display(self):
        print("**Inventory**")
        for category, items in self.player_inventory.items():
            if items:
                print(f"- {category.title()}:")
                for item in items:
                    if isinstance(item, Item):
                        print(f" - {item.get_name()}")
                    else:
                        print(f" - {item}")


    def add_item_to_inventory(self, item):
        category = item.get_category()
        if category in self.player_inventory:
            self.player_inventory[category].append(item)
        else:
            print(f"Warning: Category '{category}' not found in player inventory!")

    def handle_player_actions(self):
        inhabitant = self.current_room.get_character()

        while True:
            # Interaction display for player commands
            print("\nType the following commands, so you can:")
            print("- Check your Inventory = Inventory")
            print("- Search the room for items = Search")
            print("- Talk to the character = Talk")
            print("- Use a sleep potion = Sleep")
            print("- Offer a bribe to the character if you have items = Bribe")
            print("- Fight the character = Fight")
            print("- Move = North/South/East/West/Up/Down")

            command = input("> ").strip().lower()

            if command == "inventory":
                self.inventory_display()

            elif command in ["north", "south", "east", "west", "up", "down"]:
                next_room = self.current_room.move(command, self.player_inventory)

                if next_room:
                    # Check if a key is required and if the player has it
                    if next_room.get_key_required() and not next_room.can_enter(self.player_inventory):
                        print(f"You need the {next_room.get_key_required().get_name()} to enter this room.")
                    else:
                        self.enter_room(next_room)
                else:
                    print("You can't go that way!")

            elif command == "search":
                print("Searching for items...")
                self.current_room.search_room()

                if self.current_room.items:

                    for item in self.current_room.items:
                        print(f"Found {item.get_name()} ({item.get_category()}) - {item.get_description()}")

                        if item.get_name == "House Deed":
                            self.game_won()  # End the game

                        else:
                            self.add_item_to_inventory(item)
                            print(f"{item.get_name()} has been added to your inventory")

                    self.current_room.items.clear()
                else:
                    print("No items found in this room!")

            elif command == "talk" and inhabitant is not None:
                inhabitant.talk()

            elif command == "fight" and inhabitant is not None:
                print("Which weapon will you use?")
                for index, chosen_weapon in enumerate(self.player_inventory["weapons"]):
                    print(f"{index + 1}. {chosen_weapon}")

                try:
                    weapon_choice = int(input("> ")) - 1
                    selected_weapon = self.player_inventory["weapons"][weapon_choice]

                    if inhabitant.fight(selected_weapon):
                        acquired_items = inhabitant.inventory
                        for item in acquired_items:
                            self.add_item_to_inventory(item)
                        item_names = ', '.join(item.get_name() for item in acquired_items)
                        print(f"You have defeated {inhabitant.name} and acquired: {item_names}!")
                        self.inventory_display()
                        self.current_room.set_character(None)  # Remove the character after fight
                    else:
                        # Check if the player has the Magic Immortality Ring
                        if "Magic Immortality Ring" in self.player_inventory["loot"] and not self.magic_ring_used:
                            print("The Magic Immortality Ring protects you! You survive this encounter.")
                            self.magic_ring_used = True  # Mark the ring as used
                            # Optional: You can give the player a chance to escape or choose a different action here.
                        else:
                            print(f"{inhabitant.name} has defeated you. Game over.")
                            return  # End the game loop if the player loses

                except (IndexError, ValueError):
                    print("Invalid weapon choice format, try again entering Weapon number!")


            elif command == "sleep" and inhabitant is not None:
                if any(item.name.lower() == "sleep potion" for item in self.player_inventory["tool"]):
                    inhabitant.set_sleep(True)  # Put the enemy to sleep
                    print(f"Shhh! You have put {inhabitant.name} to sleep using the potion, you don't have to fight them now!")

                    acquired_items = inhabitant.inventory
                    for item in acquired_items:
                        self.add_item_to_inventory(item)
                    print(f"You have acquired: {', '.join(item.get_name() for item in acquired_items)}!")

                    self.player_inventory["tool"] = [
                        item for item in self.player_inventory["tool"] if item.name.lower() != "sleep potion"
                    ]
                    self.current_room.set_character(None)
                else:
                    print("You don't have a sleep potion!")

            elif command == "bribe" and inhabitant is not None:
                print("Available bribe items:")
                bribe_items = self.player_inventory['bribes']
                if bribe_items:
                    for item in bribe_items:
                        print(f"- {item.name} ({item.category}): {item.description}")
                else:
                    print("You have no items to bribe with.")
                    continue

                bribe_choice = input("Which item will you use to bribe? ").strip().lower()
                for item in bribe_items:
                    if item.name.lower() == bribe_choice:
                        if inhabitant.accept_bribe(item):
                            print(f"You bribed {inhabitant.name} with {item.name}!")
                            self.player_inventory['bribes'].remove(item)
                            break
                else:
                    print(f"{inhabitant.name} does not want that item.")
            else:
                print("Invalid command. Please try again.")


def main():
    # Setup player name before Moaning Myrtle's message
    game_start = Game_start(None, None, None)
    player_name = game_start.setup_player()

    # Setup Moaning Myrtle's conversation after obtaining player_name
    moaning_myrtle = Character("Moaning Myrtle the Friendly Ghost", "A friendly ghost that offers you advice.")
    moaning_myrtle.set_conversation(
        f"Hello {player_name}! Welcome to the haunted house! "
        "I guess I'll help you; you need to defeat enemies to collect keys and find the house deed. "
        "If you manage to find the deed you'll become the new homeowner and my cute housemate, hehehe. "
        "Or.... if you die, you'll be stuck with me forever, hehehe."
    )

    # Display Moaning Myrtle's message
    print(f"{moaning_myrtle.name} appears...")
    print(moaning_myrtle.conversation)

    # Get chosen weapons and starting location
    chosen_weapons = Game_start.choose_weapons()

    starting_location = Game_start.choose_starting_room()
    game_start = Game_start(player_name, chosen_weapons, starting_location)

    global player_inventory
    player_inventory = {
        "weapons": chosen_weapons,
        "key": [],
        "tool": [],
        "loot": [],
        "bribes": []
    }

    # Room instances created

    entrance = Room("Entrance", "A dark entryway full of cobwebs, dust, with a flickering light.")
    kitchen = Room("Kitchen", "A dank and dirty room buzzing with flies.")
    ballroom = Room("Ballroom", "A vast room with a shiny wooden floor.")
    dining_hall = Room("Dining Hall", "A large room with ornate golden decorations.")
    primary_bedroom = Room("Primary Bedroom", "A bedroom decorated like it's stuck in Victorian times, with a pungent stench.")
    bathroom = Room("Bathroom", "A large bathroom with a leaking sink, clogged toilet, and carpet on the floor.")
    attic = Room("Attic", "Cramped attic, with floorboards missing and a bat flying around.")
    basement = Room("Basement", "Massive space with another flickering light, broken oil lamp, and a stale mattress in the corner.")

    current_room = entrance  
    if starting_location == "Kitchen":
        current_room = kitchen
    elif starting_location == "Ballroom":
        current_room = ballroom
    elif starting_location == "Dining Hall":
        current_room = dining_hall
    elif starting_location == "Primary Bedroom":
        current_room = primary_bedroom
    elif starting_location == "Bathroom":
        current_room = bathroom
    elif starting_location == "Attic":
        current_room = attic
    elif starting_location == "Basement":
        current_room = basement

    # Set keys required for each room
    kitchen_key = Item(item_name="Key to Kitchen", item_category="key", item_description="Unlocks the Kitchen")
    bathroom_key = Item(item_name="Key to Bathroom", item_category="key", item_description="Unlocks the Bathroom door")
    ballroom_key = Item(item_name="Key to Ballroom", item_category="key", item_description="Unlocks the Ballroom")
    dining_hall_key = Item(item_name="Key to Dining Hall", item_category="key", item_description="Unlocks the Dining Hall")
    bedroom_key = Item(item_name="Key to Primary Bedroom", item_category="key", item_description="Unlocks the Primary Bedroom")
    attic_key = Item(item_name="Key to Attic", item_category="key", item_description="Unlocks the Attic")
    basement_key = Item(item_name="Key to Basement", item_category="key", item_description="Unlocks the Basement")

    # Set keys required for each room
    kitchen.set_key_required(kitchen_key)
    ballroom.set_key_required(ballroom_key)
    dining_hall.set_key_required(dining_hall_key)
    primary_bedroom.set_key_required(bedroom_key)
    bathroom.set_key_required(bathroom_key)
    attic.set_key_required(attic_key)
    basement.set_key_required(basement_key)

    # Link rooms together
    kitchen.link_room(ballroom, "south")
    kitchen.link_room(dining_hall, "east")
    dining_hall.link_room(kitchen, "west")
    dining_hall.link_room(primary_bedroom, "south")
    primary_bedroom.link_room(dining_hall, "north")
    primary_bedroom.link_room(ballroom, "west")
    primary_bedroom.link_room(attic, "up")
    ballroom.link_room(kitchen, "north")
    ballroom.link_room(dining_hall, "east")
    ballroom.link_room(basement, "down")
    bathroom.link_room(dining_hall, "west")
    bathroom.link_room(kitchen, "south")
    attic.link_room(primary_bedroom, "down")
    basement.link_room(ballroom, "up")



    # Items in the game
    sleep_potion = Item("Sleep Potion", "tool", "Special Potion that puts Enemies to sleep!")
    wooden_stake = Item("Wooden Stake", "weapons", "Aim for the heart ;)")
    flamethrower = Item("Flamethrower", "weapons", "Long range, don't get bitten ;)")
    magic_immortality_ring = Item("Magic Immortality Ring", "loot", "Only Protects you if you die once :( ... You're welcome!)")
    pig_brain = Item("Pig Brain", "bribes", "Big Juicy Pig Brain!")
    blood_vial = Item("Blood Vial", "bribes", "Deep Red Healthy Blood.")
    witch_brew = Item("Witch's Brew", "bribes", "A mysterious potion that promises to enhance one's magical powers. A certain someone can't resist the temptation!")
    crossbow = Item("Crossbow", "weapons", "Perfect for something flying about ;)")
    silver_dagger = Item("Silver Dagger", "weapons", "Made by a Mad Scientist ;)")
    magic_wand = Item("Magic Wand", "weapons", "Hope you studied your spells ;)")
    house_deed = Item("House Deed", "tool", "Home Ownership Document!")

    # Adding items to rooms
    kitchen.add_item(sleep_potion)
    kitchen.add_item(crossbow)  
    ballroom.add_item(wooden_stake) 
    dining_hall.add_item(flamethrower) 
    dining_hall.add_item(witch_brew)
    primary_bedroom.add_item(magic_wand)  
    attic.add_item(silver_dagger)  
    bathroom.add_item(pig_brain)  
    basement.add_item(blood_vial)  
    basement.add_item(house_deed)


    # Creation of enemies
    limbless_larry = Enemy("Limbless Larry", "A smelly zombie", inventory=[bedroom_key])
    roaslie = Enemy("Rosalie", "An unhinged fledgling!", inventory=[ballroom_key])
    casper = Enemy("Casper the Ghost", "Not the friendly type, but a hungry spirit", inventory=[dining_hall_key])
    belatrix = Enemy("Belatrix", "A deranged witch with a cackle", inventory=[attic_key])
    frankenstein = Enemy("Frankenstein", "A terrifying creature", inventory=[basement_key])
    gary = Enemy("Gary the Goblin", "A 6ft hideous, nosepicking cretin", inventory=[bathroom_key])
    dave = Enemy("Dreadful Dave","A terrifying spectre with a haunting wail and a penchant for mischief.",inventory=[kitchen_key] )
    
    # Assigning enemies to rooms
    entrance.set_character(moaning_myrtle)
    kitchen.set_character(roaslie)
    ballroom.set_character(casper)
    dining_hall.set_character(limbless_larry)
    primary_bedroom.set_character(belatrix)
    basement.set_character(frankenstein)
    attic.set_character(gary)
    bathroom.set_character(dave)

    # Set weaknesses
    limbless_larry.set_weakness("Flamethrower")
    roaslie.set_weakness("Wooden Stake")
    casper.set_weakness("Crossbow")
    belatrix.set_weakness("Magic Wand")
    frankenstein.set_weakness("Silver Dagger")
    gary.set_weakness("Iron Darts")
    dave.set_weakness("Ghostly Net")

    # Adding Loot
    roaslie.add_to_inventory(magic_immortality_ring)

    # Conversations
    roaslie.set_conversation("Welcome! I hope you brought a snack! I get a little... cranky when I'm hungry. And I'm always hungry!")
    limbless_larry.set_conversation("Grrr... What do you want, living person? I'm just trying to enjoy my rotten flesh... er, I mean, my undead existence!")
    casper.set_conversation("Boo! Did I scare you? No? Well, I'm not just here to frighten you; I'm here to haunt your dreams!")
    belatrix.set_conversation("Ah, a visitor! Come closer so I can see the fear in your eyes! Or maybe I’ll turn you into a toad!")
    frankenstein.set_conversation("You dare approach me? I am the result of a madman's experiments! Do you wish to join me in misery?")
    gary.set_conversation("Oi! You got something to say? Or are you just here to admire my... delightful hygiene?")
    dave.set_conversation("I’ll haunt your nightmares if you dare to cross me!")
    
    game = Game(current_room, player_inventory) # Initialises instance of game class using current room flow.
    game.enter_room(current_room) # Calls enter room method on game instance using specific room entering logic.

if __name__ == "__main__":
    main()
