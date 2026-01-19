import random

class Character:
    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        self._index = 0

    def __str__(self):
        return f"{self.name} : {self.description}"

    def get_msg(self):
        """
        Retourne cycliquement les messages du PNJ en utilisant pop(0).
        On retire le premier message, on l'affiche, puis on le remet à la fin.
        """
        if not self.msgs:
            return f"{self.name} n’a rien à dire."

        msg = self.msgs.pop(0)   # retire le premier
        self.msgs.append(msg)    # le remet à la fin (cycle)
        return msg

    def move(self):
        if random.choice([True, False]) is False:
            return False

        exits = [r for r in self.current_room.exits.values() if r]
        if not exits:
            return False

        new_room = random.choice(exits)
        self.current_room.characters.remove(self)
        new_room.characters.append(self)
        self.current_room = new_room
        return True