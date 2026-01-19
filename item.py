class Item:
    """
    Représente un item manipulable par le joueur.
    Attributes:
        name (str): Le nom de l'item.
        description (str): La description de l'item.
        weight (float): Le poids de l'item en kilogrammes.
    """

    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"