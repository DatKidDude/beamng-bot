import discord
from typing import Any
import os, sys
from discord.ext import commands
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv

try:
    load_dotenv(find_dotenv(raise_error_if_not_found=True))
except OSError as e:
    print("Could not find .env file. Shutting down bot...")


@dataclass(frozen=True)
class Auth:
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    DB_NAME: str = os.getenv("DB_NAME", "BeamDB")
    COMMAND_PREFIX: str = "!"


class EconomyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=Auth.COMMAND_PREFIX, 
                         intents=discord.Intents.all())

    async def on_ready(self):
        print("Discord bot connected")
    
    def run(self, *args, **kwargs):
        try:
            super().run(token=Auth.DISCORD_TOKEN, *args, **kwargs)
        except (discord.LoginFailure, KeyboardInterrupt) as e:
            print(f"Error occured: {e}\nExiting...")
            sys.exit()
    

bot = EconomyBot()
bot.run()


