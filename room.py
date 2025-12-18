class Room:
    """
    Représente une pièce du jeu d’aventure.

    Une Room correspond à un lieu dans lequel le joueur peut se trouver.
    Elle possède un nom, une description et un ensemble de sorties menant
    vers d’autres pièces.

    Attributs
    ----------
    name : str
        Nom de la pièce.
    description : str
        Description textuelle de la pièce.
    exits : dict
        Dictionnaire associant une direction (str) à une autre Room ou à None.

    Méthodes
    --------
    get_exit(direction)
        Retourne la pièce associée à la direction donnée.
    get_exit_string()
        Retourne une chaîne décrivant les sorties disponibles.
    get_long_description()
        Retourne une description complète de la pièce incluant les sorties.

    Exemples
    --------
    >>> room = Room("Cuisine", "dans une cuisine sombre")
    >>> room.exits["nord"] = None
    >>> room.get_exit("nord") is None
    True
    >>> "Sorties" in room.get_exit_string()
    True
    """


    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = []



    def look(self):
        res = self.get_long_description()
        res += "\n" + self.get_inventory() + "\n"
        return res



    def get_inventory(self):
        if not self.inventory:
            return "Il n'y a rien ici."

        res = "La pièce contient :\n"
        for item in self.inventory:
            res += f"    - {item}\n"
        return res


    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"
