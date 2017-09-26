import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands

import game, player, text	# Our modules

# ================================ HELPER FUNCTIONS ================================
def convert_id(author):
    """ Returns numerical part of Discord username for id purposes. """
    return str(author).split("#")[1]

def okint(n):
    """ Returns if <str> n can be converted to an int. """
    allowed = "0123456789"
    for ch in n:
        if not(ch in allowed):
            return False
    return True

# ================================ BOT SETUP ================================

Client = discord.Client()
bot_prefix= "]"
client = commands.Bot(command_prefix=bot_prefix)

token = text.t#input("Enter token: ")

print ("Set up complete.")

# ================================ MAIN PROGRAM ================================

# Stores channel.name keys with Game() object pairs
games = {}

@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith(bot_prefix):
        content = message.content.split()
        parts = len(content)
        author = convert_id(str(message.author))
        start = content[0][1:]
        
        # Shows details and syntax for a command
        if start == "help":
            if parts == 1:
                t = "__AVAILIBLE COMMANDS__\n"
                for command in sorted(text.command_info):
                    t += "*{0}* : {1}\n\n".format(command, text.command_info[command][1])
                yield from client.send_message(message.channel, t)
            elif parts == 2:
                if content[1] in text.command_info:
                    command = content[1]
                    t = "__{0} COMMAND INFO__\nUse: {1}\nSyntax: {2}\n".format(command.upper(), text.command_info[command][1], text.command_info[command][0])
                    yield from client.send_message(message.channel, t)
                else:  
                    yield from client.send_message(message.channel, ":thinking: That command doesn't exist. To see a list of commands, type ']help'.")
            else:  
                yield from client.send_message(message.channel, ":sweat_smile: The syntax is {}. Type ']help' for more info.".format(text.command_info["help"][0]))

        # Starts a new game session in text channel
        if start == "start":
            if parts == 2:
                # Game already exists
                if (message.channel.name in games):
                   yield from client.send_message(
                       message.channel, ":sad: A game already exists in this channel..."
                       )
                else:
                    # Content must be integer between 4 and 8 (inclusive)
                    if okint(content[1]) and 4 <= int(content[1]) and int(content[1]) <= 8:
                        games[message.channel.name] = game.Game(int(content[1]))
                        current_game = games[message.channel.name]
                        current_game.player_join(author, message.author)
                        yield from client.send_message(
                            message.channel, ":dang: {0} started a Classic game for {1} people!".format(
                                message.author,content[1])
                            )
                    else:
                        yield from client.send_message(
                            message.channel, ":sad: Sorry, the number of players must be an integer from 4 to 8..."
                            )
            else:
                yield from client.send_message(
                    message.channel, ":sweat_smile: The syntax is {}. Type ']help' for more info.".format(text.command_info["start"][0])
                    )

        # Joins a game queue
        if start == "join":
            if parts == 1:
                # Check if game exists
                if (message.channel.name in games):
                    current_game = games[message.channel.name]
                    if current_game.state == "Queue":
                        if author in current_game.players:
                            yield from client.send_message(
                                message.channel, ":dang: You're already in the queue..."
                            )                     
                        else:
                            current_game.player_join(author, message.author)
                            yield from client.send_message(
                                message.channel, ":smile: {0} has joined! ({1}/{2})".format(
                                message.author, len(current_game.players), current_game.capacity)
                            )
                            if current_game.state == "Active":
                                yield from client.send_message(
                                message.channel, "The game has started!"
                            )
                    else:
                         yield from client.send_message(
                           message.channel, ":deng: The game is no longer accepting players..."
                           )                     
                else:
                    yield from client.send_message(
                       message.channel, ":sad: No game exists in this channel... wanna try and start one?"
                       )
            else:
            	yield from client.send_message(
                    message.channel, ":sweat_smile: The syntax is {}. Type ']help' for more info.".format(text.command_info["join"][0])
                    )  

        # Leaves a game queue
        if start == "leave":
            if parts == 1:
                # Check if game exists
                if (message.channel.name in games):
                    current_game = games[message.channel.name]
                    if current_game.state == "Queue":
                        if author in current_game.players:
                            current_game.player_leave(author)
                            yield from client.send_message(
                                message.channel, ":deng: {0} has left... ({1}/{2})".format(
                                message.author, len(current_game.players), current_game.capacity)
                                )                    
                        else:
                            yield from client.send_message(
                                message.channel, ":thinking: You're not in the queue..."
                            ) 
                    else:
                         yield from client.send_message(
                           message.channel, ":deng: The game is in progress..."
                        )                     
                else:
                    yield from client.send_message(
                       message.channel, ":sad: No game exists in this channel... wanna try and start one?"
                    )
            else:
            	yield from client.send_message(
                    message.channel, ":sweat_smile: The syntax is {}. Type ']help' for more info.".format(text.command_info["leave"][0])
                    )
            
        #Displays players in queue or game
        if start == "players":
            if parts == 1:
                # Check if game exists
                if (message.channel.name in games):
                    current_game = games[message.channel.name]
                    yield from client.send_message(message.channel, current_game.list_players())                                          
                else:
                    yield from client.send_message(
                       message.channel, ":sad: No game exists in this channel... wanna try and start one?"
                       )
            else:
            	yield from client.send_message(
                    message.channel, ":sweat_smile: The syntax is {}. Type ']help' for more info.".format(text.command_info["players"][0])
                    )

client.run(token)






