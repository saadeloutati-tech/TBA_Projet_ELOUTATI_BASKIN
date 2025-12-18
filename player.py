# Define the Player class.

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
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    