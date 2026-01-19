# Description: Game class
# Import modules


from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quest import Quest



class Game:


    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = {}
        self.commands = {}
        self.player = None
   
   # Setup player and starting room
    def setup_player(self):
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = self.rooms["Eridani Prime"]  # Start in the first room
            
    # Setup commands
    def setup_commands(self):
        self.commands["help"] = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["history"] = Command("history"," : afficher l'historique des lieux visités",Actions.history,0)
        self.commands["back"] = Command("back"," : revenir à la pièce précédente", Actions.back,0)
        self.commands["look"] = Command("look", " : observer la pièce", Actions.look, 0)
        self.commands["take"] = Command("take", " <item> : prendre un item", Actions.take, 1)
        self.commands["drop"] = Command("drop", " <item> : déposer un item", Actions.drop, 1)
        self.commands["check"] = Command("check", " : vérifier l’inventaire", Actions.check, 0)
        self.commands["talk"] = Command("talk", " : <nom> parler à un personnage dans la pièce", Actions.talk, 1)
        self.commands["quests"] = Command("quests", " : afficher la liste des quêtes", Actions.quests, 0)
        self.commands["quest"] = Command("quest", " <titre> : afficher les détails d'une quête", Actions.quest, 1)
        self.commands["activate"] = Command("activate" , " <titre> : activer une quête", Actions.activate, 1)
        self.commands["rewards"] = Command("rewards", " afficher vos récompenses", Actions.rewards, 0)

    # Setup rooms
    def setup_rooms(self):
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

        # Create list of rooms
        self.rooms = {
            "Eridani Prime": eridani,
            "Avant-poste minier": avant_poste,
            "Marché labyrinthique": marche,
            "Cité-forteresse": forteresse,
            "Base rebelle de Velyra": base,
            "Quartier civil": quartier,
            "Entrepôts civils": entrepots,
            "Prison centrale": prison
        }

        # Create exits for rooms

        eridani.exits     = {"E": avant_poste, "O": None,         "U": None,        "D": base}
        avant_poste.exits = {"E": marche,      "O": eridani,      "U": None,        "D": None}
        marche.exits      = {"E": forteresse,  "O": avant_poste,  "U": None,        "D": entrepots}
        forteresse.exits  = {"E": None,        "O": marche,       "U": None,        "D": None}

        base.exits        = {"E": quartier,    "O": None,         "U": eridani,     "D": None}
        quartier.exits    = {"E": entrepots,   "O": base,         "U": None,        "D": None}
        entrepots.exits   = {"E": prison,      "O": quartier,     "U": marche,     "D": None}
        prison.exits      = {"E": None,        "O": None,         "U": None,        "D": None}

                
        
        

    # Setup PNJ
    def setup_characters(self):
        ralen = Character(
            "Ralen",
            "Un citoyen au regard vif malgré les cendres sur son visage.",
            self.rooms["Eridani Prime"],
            [
                "Vous n’avez pas l’air d’ici.",
                "Les mines à l’est cachent bien des choses.",
            ]
        )

        malek = Character(
            "Ingénieur Malek",
            "Un technicien nerveux qui tente de réparer une foreuse brisée.",
            self.rooms["Avant-poste minier"],
            [
                "Cette foreuse ne tiendra plus longtemps.",
                "Sans matériel, tout va s’effondrer.",
            ]
        )

        marchand = Character(
            "Marchand",
            "Un homme sec, aux yeux calculateurs, entouré de caisses verrouillées.",
            self.rooms["Marché labyrinthique"],
            [
                "Tout a un prix.",
                "Même la loyauté.",
            ]
        )

        yara = Character(
            "Yara",
            "Une femme encapuchonnée, regard déterminé, symbole rebelle au poignet.",
            self.rooms["Marché labyrinthique"],
            [
                "Ne fais confiance à personne.",
                "La forteresse tombera.",
                "Tu auras besoin d’une carte… mais fais attention."
            ]
        )

        nommera = Character(
            "Nommera",
            "Une jeune femme aux mains couvertes de poussière, le regard creux mais lucide.",
            self.rooms["Entrepôts civils"],
            [
                "Ils ont tout pris.",
                "Il ne nous reste presque rien.",
            ]
        )



        
        self.rooms["Eridani Prime"].characters.append(ralen)
        self.rooms["Avant-poste minier"].characters.append(malek)
        self.rooms["Marché labyrinthique"].characters.append(marchand)
        self.rooms["Marché labyrinthique"].characters.append(yara)
        self.rooms["Entrepôts civils"].characters.append(nommera)
        
    # Setup Items    
    def setup_items(self):    
        battery = Item("Batterie énergétique usée", "Une batterie industrielle à moitié déchargée.", 2)
        shiv = Item("Dague improvisée", "Une lame artisanale forgée à partir de ferraille.", 1)
        keycard = Item("Carte d’accès rouillée", "Une vieille carte magnétique de sécurité.", 1)
        transmitter = Item("Émetteur rebelle crypté", "Un appareil de communication utilisé par la résistance.", 1)

        self.rooms["Avant-poste minier"].inventory.append(battery)
        self.rooms["Marché labyrinthique"].inventory.append(shiv)
        self.rooms["Entrepôts civils"].inventory.append(keycard)
        self.rooms["Base rebelle de Velyra"].inventory.append(transmitter)
        
    # Setup quests 
    def _setup_quests(self):
        """Initialize all quests."""
        item_quest = Quest(
            title="Accès restreint",
            description="Récupérer une carte d’accès dans les entrepôts civils.",
            objectives=["prendre Carte d’accès rouillée"],
            reward="Accès aux zones sécurisées"
            )

        travel_quest = Quest(
            title="Assaut de la prison centrale",
            description="Atteindre la prison centrale et libérer Narek.",
            objectives=["Visiter Prison centrale"],
            reward="Plan de la forteresse"
        )

        talk_quest = Quest(
            title="Alliance rebelle",
            description="Parler au Chef rebelle pour coordonner l’attaque.",
            objectives=["parler avec Yara"],
            reward="Soutien de la résistance"
        )
        
        


        # Add quests to player's quest manager
        self.player.quest_manager.add_quest(item_quest)
        self.player.quest_manager.add_quest(travel_quest)
        self.player.quest_manager.add_quest(talk_quest)



    # Setup the game
    def setup(self):
        # Setup commands
        self.setup_commands()
        # Setup rooms
        self.setup_rooms()
        # Setup Player
        self.setup_player()
        # Setup Characters
        self.setup_characters()
        # Setup items
        self.setup_items()
        # Setup quests
        self._setup_quests()
        


    # Play the game
    def play(self):
        
        self.setup()
        self.print_welcome()
        
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
            
            # Check win/lose conditions
            if self.win():
                print("\n🎉 VOUS AVEZ GAGNÉ LA PARTIE 🎉\n")
                self.finished = True
            elif self.loose():
                print("\n💀 Vous avez été capturé. Fin de partie.\n")
                self.finished = True
            else:
                # Déplacement des PNJ après chaque tour
                self.character_move()
                    
        return None
    
    
    def character_move(self):
        for room in self.rooms.values():
            for character in room.characters:
                character.move()

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
   
    # Check if the player has won
    def win(self):
        for quest in self.player.quest_manager.get_all_quests():
            if not quest.is_completed:
                return False

        print(
            "\n🔓 Les portes de la prison cèdent.\n"
            "Narek est libre.\n"
            "La résistance peut enfin renverser le régime.\n"
        )
        return True

    
    # Check if the player has lost
    def loose(self):
        if self.player.current_room.name == "Prison centrale":
            if not any(item.name == "Carte d’accès rouillée" for item in self.player.inventory):
                print("\n🚨 ALERTE ! Vous êtes intercepté par les tourelles automatiques.")
                print("Vous n'avez pas d'autorisation d'accès.\n")
                return True
        return False




def main():
    # Create a game object and play the game
    Game().play()
   


if __name__ == "__main__":
    main()