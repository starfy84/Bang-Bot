# Only the Classic Gamemode for now

import random
import player

characters = ["Hawk","Rat","Wolf","Bat","Hare","Fox","Scorpion","Bull","Stallion"]
roles = ["Sheriff","Vice","Outlaw","Renegade"]

#Cards: 1-10 are ACTION cards, 11-15 are WEAPONS, 16-20 are SPECIAL 
cards = ["Bang","Mancato","Indians","Gatling","Duel","Panic","Cat Balou","Beer","Saloon","Emporio",
         "Volcanic","Schofield","Remington","Rev. Carabine","Winchester",
         "Dynamite","Barrel","Prison","Mustang","Scope"]

# Small deck example
small_deck = [
    "Bang","Bang","Bang","Bang","Bang",
    "Bang","Bang","Bang","Mancato","Mancato",
    "Mancato","Mancato","Cat Balou","Cat Balou","Event",
    "Event","Beer","Beer","Beer","Beer"
]

# Map Presets for player capacity
map_presets = {
    4 : {"Players":[[3,0],[0,2],[6,2],[3,4]],"Size":[7,5]},
    5 : {"Players":[[3,0],[0,2],[6,2],[1,5],[5,5]],"Size":[7,6]},
    6 : {"Players":[[3,0],[0,1],[6,1],[0,4],[6,4],[3,5]],"Size":[7,6]},
    7 : {"Players":[[3,0],[0,2],[6,2],[0,4],[6,4],[2,6],[4,6]],"Size":[7,7]},
    8 : {"Players":[[2,0],[4,0],[0,2],[6,2],[0,4],[6,4],[2,6],[4,6]],"Size":[7,7]},
}

rolePresets = { # Availible roles for player capacity
    4 : [0,1,2,2],
    5 : [0,1,2,2,3],
    6 : [0,1,1,2,2,3],
    7 : [0,1,1,2,2,2,3],
    8 : [0,1,1,2,2,2,3,3]
}

class Game:
    def __init__(self, capacity):
        # Player capacity
        self.capacity = capacity

        # Choose random set of characters
        self.characters = list(characters)
        random.shuffle(self.characters)
        self.characters = self.characters[:capacity]

        # Set preset roles
        self.roles = list(rolePresets[capacity])
        random.shuffle(self.roles)
        self.players = {}
        self.state = "Queue"

        # Create deck sized to players.
        self.deckSize = len(small_deck) * capacity
        self.deck = small_deck * capacity
        self.cardsDealt = 0

    def __str__(self):
        r = "Game Info ({0}):\n".format(self.state)
        r += "Capacity: {0}\nCharacters: {1}\n".format(self.capacity,self.characters)
        r += "Roles: {0}\nPlayers: {1}\n".format(self.roles,self.players)
        return r

    def print_map(self):
        for y in range(len(self.map)):
            print(self.map[y])

    def setup(self):
        """ Assign roles, characters, stats to all players and generate map. """
        # Empty map
        self.map = [[9 for x in range(map_presets[self.capacity]["Size"][0])] for y in range(map_presets[self.capacity]["Size"][1])]
        
        n = 0
        for p in self.players:
            self.players[p].setup(self.characters[n],self.roles[n])

            # Move player to starting location
            self.players[p].move(map_presets[self.capacity]["Players"][n][0],map_presets[self.capacity]["Players"][n][1])
            self.map[map_presets[self.capacity]["Players"][n][1]][map_presets[self.capacity]["Players"][n][0]] = n

            n += 1
  	
    def list_players(self):
        """ Return a formatted string of the players."""
        output = ""
        if self.state == "Queue":
            output += "__Current Queue__\n"
            n = 1
            for x in self.players:
                #Formats to 1. PlayerName
                output += ("{0}. {1}\n").format(n,self.players[x].username)
                n += 1
        else:
            output += "__Players__\n"
            n = 1
            for x in self.players:
                #Formats to 1. emoji PlayerName the Role (HP)
                output += "{0}. {1}\n".format(n,self.players[x].display_status())
                n += 1

        return output
        
    def player_join(self, num, username):
        """ Add player to queue, check for full queue. """
        self.players[num] = player.Player(num, username, self)
        if len(self.players) == self.capacity:
            self.state = "Active"
            self.setup()

    def player_leave(self, num):
        """ Player leaves queue. """
        self.players.pop(num, None)

    def deal_card(self, playerNum):
        """ Deals card to a player. """
        # Deal card to player
        self.players[playerNum].cards.append(self.deck.pop(0))
        self.cardsDealt += 1

        # Shuffle deck when all cards have been played
        if self.cardsDealt == self.deckSize:
            random.shuffle(self.deck)
            self.cardsDealt = 0
