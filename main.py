import discord
from bot import EconomyBot
from config import Auth

if __name__ == "__main__":
    # start the bot
    auth = Auth()
    intents = discord.Intents.all()
    client = EconomyBot(auth=auth, command_prefix=auth.COMMAND_PREFIX, intents=intents)
    client.run()