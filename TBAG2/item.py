class Item():
# Different objects player might find/interact with in the game.
    def __init__(self, item_name, item_category, item_description):
    # Initialises values but when an instance is created, attributes are empty until explicitly set.
        self._name = item_name # Stores the name of the item.
        self._category = item_category # Stores the category of the item.
        self._description = item_description # Stores a description of the item.

    def get_name(self):
        return self._name
    

    def get_category(self):
        return self._category


    def get_description(self):
        return self._description
    
    # String representation
    def __str__(self):
        return f"{self._name} ({self._category}): {self._description}"

    def __repr__(self):
        return f"Item(name={self._name}, category={self._category}, description={self._description})"
    
    
    def get_item_details(self):
        print(self._name)
        print("-------------------------")
        print(self._description)