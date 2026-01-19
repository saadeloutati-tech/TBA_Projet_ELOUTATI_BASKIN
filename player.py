# Define the Player class.
from quest import QuestManager


class Player():
    """
    Représente le joueur du jeu.


    Un Player possède un nom et se déplace de pièce en pièce
    en utilisant les sorties disponibles dans la Room courante.


    Attributs
    ----------
    name : str
        Nom du joueur.
    current_room : Room ou None
        Pièce dans laquelle se trouve actuellement le joueur.


    Méthodes
    --------
    move(direction)
        Déplace le joueur dans la direction indiquée si possible.


    Exceptions
    ----------
    KeyError
        Levée si la direction demandée n’existe pas dans les sorties
        de la pièce courante.


    Exemples
    --------
    >>> player = Player("Alice")
    >>> room1 = Room("Hall", "dans un grand hall")
    >>> room2 = Room("Salon", "dans un salon lumineux")
    >>> room1.exits["est"] = room2
    >>> player.current_room = room1
    >>> player.move("est")
    True
    """

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = []
        self.weight = 0  # Current weight of items carried
        self.max_weight = 5  # Maximum weight the player can carry
        self.move_count = 0

        self.quest_manager = QuestManager(self)
        self.rewards = []  # List to store earned rewards
   
    # Define the move method.
    def move(self, direction):
        """Move the player to a different room in the specified direction.
        Args:
            direction (str): the direction to move in.
        Returns:
            bool: True if the move was successful, False otherwise.
        Examples:
            >>> player = Player("Alice")
            >>> room1 = Room("Hall", "dans un grand hall")
            >>> room2 = Room("Salon", "dans un salon lumineux") 
            >>> room1.exits["est"] = room2
            >>> player.current_room = room1
            >>> player.move("est")
            True
            >>> player.current_room == room2
            True
            >>> player.move("ouest")
            False
        """
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]


        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Special check for "Prison centrale" access
        if next_room.name == "Prison centrale":
            if not any(item.name == "Carte d’accès rouillée" for item in self.inventory):
                print("\n🚨 Les scanners détectent une intrusion non autorisée...\n")


        self.history.append(self.current_room)

           
        # Set the current room to the next room.
        self.current_room = next_room
    

        
        print(self.current_room.get_long_description())
        return True

    def get_inventory(self):
        """Get a string representation of the player's inventory.
        Returns:
            str: a string listing the items in the inventory and their total weight.
            Examples:
            >>> player = Player("Alice")
            >>> item1 = Item("Clé", "Une petite clé en métal.", weight=
            0.1)
            >>> item2 = Item("Livre", "Un vieux livre poussiéreux.", weight=
            0.5)
            >>> player.inventory.append(item1)          
            >>> player.inventory.append(item2)
            >>> player.weight = item1.weight + item2.weight
            >>> print(player.get_inventory()) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Vous disposez des items suivants :
                - Clé
                - Livre
            Le poids total des items est de 0.6 kg sur une capacité maximale de
            5 kg.
            <BLANKLINE>
        """
        if not self.inventory:
            return "\nVotre inventaire est vide.\n"

        res = "\nVous disposez des items suivants :\n"
        for item in self.inventory:
            res += f"    - {item}\n"
        res += "Le poids total des items est de " + str(self.weight) + " kg sur une capacité maximale de " + str(self.max_weight) + " kg.\n"
        return res

    def take(self, item_name):
        """take an item from the current room to the player's inventory by name.
        Args:
            item_name (str): the name of the item to take.
            Returns:
            str: a message indicating the result of the take action.
            Examples:
            >>> player = Player("Alice")
            >>> room = Room("Salle", "une salle vide")
            >>> item = Item("Clé", "Une petite clé en métal.")
            >>> room.inventory.append(item)
            >>> player.current_room = room
            >>> print(player.take("Clé")) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Vous avez pris : Clé
            <BLANKLINE>
            >>> print(player.take("Livre")) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Cet item n’est pas présent ici.
            <BLANKLINE>
        """
        room = self.current_room

        for item in room.inventory:
            if item.name.lower() == item_name.lower() and (self.weight + item.weight) <= self.max_weight:
                self.inventory.append(item)
                room.inventory.remove(item)
                self.weight += item.weight
                return f"\nVous avez pris : {item}\n"
            elif item.name.lower() == item_name.lower() and (self.weight + item.weight) > self.max_weight:
                return f"\n🚨 Vous ne pouvez pas prendre {item}. Poids maximum dépassé !\n"
            
        return "\nCet item n’est pas présent ici.\n"

    def drop(self, item_name):
        """drop an item from the player's inventory to the current room by name.
        Args:
            item_name (str): the name of the item to drop.
            Returns:
            str: a message indicating the result of the drop action.
            Examples:
            >>> player = Player("Alice")
            >>> room = Room("Salle", "une salle vide")
            >>> item = Item("Clé", "Une petite clé en métal.")
            >>> player.inventory.append(item)
            >>> player.current_room = room
            >>> print(player.drop("Clé")) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Vous avez déposé : Clé
            <BLANKLINE>
            >>> print(player.drop("Livre")) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Vous ne possédez pas cet item.
            <BLANKLINE>
        """
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                self.inventory.remove(item)
                self.current_room.inventory.append(item)
                self.weight -= item.weight
                return f"\nVous avez déposé : {item}\n"

        return "\nVous ne possédez pas cet item.\n"

    def talk(self, name):
        """talk to a character in the current room by name.
        Args:
            name (str): the name of the character to talk to.
        Returns:
            str: the message from the character or an error message if not found.
        Examples:
            >>> player = Player("Alice")
            >>> room = Room("Salle", "une salle vide")
            >>> character = Character("Bob", "Bonjour, je suis Bob.")
            >>> room.characters.append(character)
            >>> player.current_room = room
            >>> print(player.talk("Bob")) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Bob dit : 'Bonjour, je suis Bob.'
            <BLANKLINE>
            >>> print(player.talk("Charlie")) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Il n'y a personne avec ce nom ici.
            <BLANKLINE>
        """
        for character in self.current_room.characters:
            if character.name.lower() == name.lower():
                return f"\n{character.name} dit : '{character.get_msg()}'\n"

        return "\nIl n'y a personne avec ce nom ici.\n"

    def check(self):
        return self.get_inventory()

    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
        
        Args:
            reward (str): The reward to add.
            
        Examples:
        
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
           # print(f"\n🎁 Vous avez obtenu: {reward}\n")    redondance ??? 

    def show_rewards(self):
        """
        Display all rewards earned by the player.
        
        Examples:
        
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()

    def get_history(self):
        if not self.history:
            return "\nVous n'avez encore visité aucune autre pièce.\n"


        seen = []
        res = "\nVous avez déjà visité les pièces suivantes:\n"


        for room in self.history:
            if room not in seen:
                seen.append(room)
                res += f"    - {room.name}\n"


        return res