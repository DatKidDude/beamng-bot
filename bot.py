import discord
import sys
from discord.ext import commands
from modules import Database
from config import Auth

class EconomyBot(commands.Bot):
    """The entry point for the Discord bot."""
    def __init__(self, auth: Auth, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.auth = auth
        self.db = Database(db_name=self.auth.DB_NAME)
    
    async def setup_hook(self) -> None:
        await self.load_extension("cogs.economy")

    async def on_ready(self):
        print("Discord bot connected")
    
    def run(self, *args, **kwargs):
        try:
            super().run(token=self.auth.DISCORD_TOKEN, *args, **kwargs)
        except (discord.LoginFailure, KeyboardInterrupt) as e:
            print(f"Error occured: {e}\nExiting...")
            sys.exit()


