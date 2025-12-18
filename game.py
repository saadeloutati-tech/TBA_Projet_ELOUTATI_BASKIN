# Description: Game class


# Import modules


from room import Room
from player import Player
from command import Command
from actions import Actions


class Game:


    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
   
    # Setup the game
    def setup(self):


        # Setup commands


        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        history = Command("history"," : afficher l'historique des lieux visités",Actions.history,0)
        self.commands["history"] = history
        back = Command("back"," : revenir à la pièce précédente", Actions.back,0)
        self.commands["back"] = back


       
        # Setup rooms
        eridani = Room(
            "Eridani Prime",
            "un district pauvre où des fumées noires s’élèvent au-dessus des toits. "
            "Des affiches de propagande couvrent les murs. "
            "Les habitants avancent avec un mélange de peur et de résignation."
        )


        avant_poste = Room(
            "Avant-poste minier",
            "un enchevêtrement d’échafaudages branlants, de gardes épuisés et de mineurs au regard vide. "
            "L’air est lourd de poussière et d’électricité."
        )


        marche = Room(
            "Marché labyrinthique",
            "un dédale d’allées étroites, d’échoppes sombres et de murmures étouffés. "
            "Les hommes de main de Vorn rôdent à chaque coin d’ombre."
        )


        forteresse = Room(
            "Cité-forteresse",
            "des tours massives balayées par des projecteurs écarlates. "
            "Des soldats patrouillent sans relâche : c’est ici que le capitaine Vorn impose son règne."
        )




        base = Room(
            "Base rebelle de Velyra",
            "un bunker dissimulé sous les ruines d’un ancien quartier industriel. "
            "Des écrans grésillent, affichant les patrouilles de drones du gouverneur Karn."
        )


        quartier = Room(
            "Quartier civil",
            "des immeubles serrés sous des néons blafards. "
            "Les habitants marchent tête baissée sous l’œil constant des caméras."
        )


        entrepots = Room(
            "Entrepôts civils",
            "de vastes hangars contenant les réserves d’énergie et de nourriture. "
            "Des gardes mécaniques veillent sans relâche."
        )


        prison = Room(
            "Prison centrale",
            "une forteresse de métal noir hérissée de tourelles automatiques. "
            "C’est ici que sont enfermés Narek et les chefs rebelles."
        )


 




        # Create exits for rooms
        eridani.exits = {"E": avant_poste, "O": None, "U": None, "D": base}
        avant_poste.exits = {"E": marche, "O": eridani, "U": None, "D": None}
        marche.exits = {"E": forteresse, "O": avant_poste, "U": None, "D": entrepots}
        forteresse.exits = {"E": None, "O": marche, "U": None, "D": prison}
        base.exits = {"E": quartier, "O": None, "U": eridani, "D": None}
        quartier.exits = {"E": entrepots, "O": base, "U": None, "D": None}
        entrepots.exits = {"E": prison, "O": quartier, "U": marche, "D": None}
        prison.exits = {"E": None, "O": entrepots, "U": forteresse, "D": None}




        # Setup player and starting room


        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = eridani


    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None


    # Process the command entered by the player
    def process_command(self, command_string) -> None:


        # Ignorer les commandes vides
        if command_string.strip() == "":
            return


        # Split the command string into a list of words
        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]


        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)


    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
   


def main():
    # Create a game object and play the game
    Game().play()
   


if __name__ == "__main__":
    main()


