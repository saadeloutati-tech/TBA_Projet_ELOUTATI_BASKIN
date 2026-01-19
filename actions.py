# Description: The actions module.


# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.

import character


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"


class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).


        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.


        Returns:
            bool: True if the command was executed successfully, False otherwise.


        Examples:
       
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False


        """
       
        player = game.player
        l = len(list_of_words)


        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False


        direction_input = list_of_words[1]


        # --- normalisation ---
        DIRECTIONS = {
            "N": "N", "NORD": "N", "Nord": "N", "nord": "N", "n": "N",
            "S": "S", "SUD": "S", "Sud": "S", "sud": "S", "s": "S",
            "E": "E", "EST": "E", "Est": "E", "est": "E", "e": "E",
            "O": "O", "OUEST": "O", "Ouest": "O", "ouest": "O", "o": "O",
            "U": "U", "UP": "U", "Up": "U", "up": "U", "u": "U",
            "D": "D", "DOWN": "D", "Down": "D", "down": "D", "d": "D",
        }


        # --- direction invalide ---
        if direction_input not in DIRECTIONS:
            print(f"\nDirection '{direction_input}' non reconnue.\n")
            # 👉 on réaffiche la salle actuelle
            print(player.current_room.get_long_description())
            return False


        direction = DIRECTIONS[direction_input]


        success = player.move(direction)
        # Check room visit objectives
        player.quest_manager.check_room_objectives(player.current_room.name)
        if success:
            print(player.get_history())
        return success

    def back(game, list_of_words, number_of_parameters):
        """Revenir à la pièce précédente dans l'historique du joueur.
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the command was executed successfully, False otherwise.
        Examples:
            >>> from game import Game
            >>> game = Game()
            >>> game.setup()
            >>> go(game, ["go", "N"], 1)
            True
            >>> back(game, ["back"], 0)
            True
            >>> back(game, ["back", "N"], 0)
            False
        """

        player = game.player
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        if not player.history:
            print("\nVous ne pouvez pas revenir en arrière.\n")
            print(player.current_room.get_long_description())
            return False

        previous_room = player.history.pop()
        player.current_room = previous_room

        print(player.current_room.get_long_description())
        print(player.get_history())

        return True

    def look(game, list_of_words, number_of_parameters):
        """Regarder la pièce courante.
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the command was executed successfully, False otherwise.
        Examples:
            >>> from game import Game
            >>> game = Game()
            >>> game.setup()
            >>> look(game, ["look"], 0)
            True
        """
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        print(game.player.current_room.look())
        return True

    def talk(game, list_of_words, number_of_parameters):
        """Faire parler un personnage qui peut avoir un nom composé dans la pièce courante.
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the command was executed successfully, False otherwise.
        Examples:
            >>> from game import Game
            >>> game = Game()
            >>> game.setup()
            >>> talk(game, ["talk", "Ralen"], 1)
            True
            >>> talk(game, ["talk"], 1)
            False
        """
        if len(list_of_words) < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        name = " ".join(list_of_words[1:])

        print(game.player.talk(name))
        
        game.player.quest_manager.check_action_objectives("parler", name)

        return True

    def take(game, list_of_words, number_of_parameters):
        """Prendre un item qui peut avoir un nom composé dans la pièce courante.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
            Returns: bool: True if the command was executed successfully, False otherwise.
            Examples:
            >>> from game import Game
            >>> game = Game()
            >>> game.setup()
            >>> take(game, ["take", "Ancient", "Sword"], 1)
            True
            >>> take(game, ["take"], 1)
            False
        """
        if len(list_of_words) < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # 🔥 reconstruction du nom complet de l’item
        item_name = " ".join(list_of_words[1:])

        print(game.player.take(item_name))
        game.player.quest_manager.check_action_objectives("prendre", item_name)
        return True

    def drop(game, list_of_words, number_of_parameters):
        """Déposer un item qui peut avoir un nom composé depuis l’inventaire du joueur.
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the command was executed successfully, False otherwise.
        Examples:
            >>> from game import Game
            >>> game = Game()
            >>> game.setup()
            >>> drop(game, ["drop", "Ancient", "Sword"], 1)
            True
            >>> drop(game, ["drop"], 1)
            False
        """
        if len(list_of_words) < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # reconstruction du nom complet de l'item
        item_name = " ".join(list_of_words[1:])

        print(game.player.drop(item_name))
        return True

    def check(game, list_of_words, number_of_parameters):
        """
        Vérifie l'état d'un objet dans la pièce courante.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
            >>> from game import Game
            >>> game = Game()
            >>> game.setup()
            >>> check(game, ["check"], 0)
            True
        """
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        print(game.player.check())
        return True

    def history(game, list_of_words, number_of_parameters):
        """Affiche l'historique des actions du joueur.
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the command was executed successfully, False otherwise.
        Examples:
            >>> from game import Game
            >>> game = Game()
            >>> game.setup()
            >>> history(game, ["history"], 0)
            True
        """
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False


        print(game.player.get_history())
        return True

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.


        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.


        Returns:
            bool: True if the command was executed successfully, False otherwise.


        Examples:


        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False


        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
       
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
       
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.


        Returns:
            bool: True if the command was executed successfully, False otherwise.


        Examples:


        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False


        """


        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
       
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
        
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True

    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True

    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False

    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True