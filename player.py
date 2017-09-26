import text

class Player:
    def __init__(self, num, username, game):
        self.id = num        		# Discord id number
        self.username = username	# Discord username
        self.game = game
        
        self.hp = 0         # Health and max cards
        self.cards = []
        self.special = 0    # Special counter (depends on character)

        # Position on map
        self.x = None
        self.y = None
        
        self.role = ""          # Role of player (sheriff, outlaw, etc.)
        self.character = ""     # Character of player (Hare, Fox, etc.)
        
    def display_status(self):
        """ Shows player name, character, and status. """
        # Show character symbol
        r = text.characters[self.character][0] + " "
        r += self.username + " the "
        
        # Show role if sheriff or if you're dead
        if text.roles[self.role] == "Sheriff" or self.hp == 0:
            r += text.roles[self.role]
        else:
            r += "Stranger"
            
        # Show health, or death symbol
        if self.hp > 0:
            r += " ({}:hearts:)".format(self.hp)
        else:
            r += " (:skull_and_crossbones:)"
            
        return r
      
    def setup(self, character, role):
        """ Gives player character and role. """
        self.character = character
        self.role = role

        if self.role == 0:
            self.hp = 5
        else:
            self.hp = 4

    def move(self, x, y):
        """ Moves player to location x, y. """
        self.x = x
        self.y = y
