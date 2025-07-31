import discord
import sys
from discord.ext import commands
from modules import Database
from config import Auth
from pathlib import Path

class EconomyBot(commands.Bot):
    """The entry point for the Discord bot."""
    def __init__(self, auth: Auth, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.auth = auth
        self.db = Database(db_name=self.auth.DB_NAME)
        self.ext_dir = Path("cogs")
    
    async def _load_extension(self):
        """Loads all Cogs from the cogs directory"""
        print("Loading extensions...")
        for file in self.ext_dir.rglob("*.py"):
            if file.stem.startswith("_"):
                continue
            try:
                await self.load_extension(".".join(file.with_suffix("").parts))
                print(f"Loaded {file}")
            except commands.ExtensionError as e:
                print(f"Failed to load {file}: {e}")
        
    async def setup_hook(self) -> None:
        await self._load_extension()

    async def on_ready(self):
        print("Discord bot connected")
    
    def run(self, *args, **kwargs):
        try:
            super().run(token=self.auth.DISCORD_TOKEN, *args, **kwargs)
        except (discord.LoginFailure, KeyboardInterrupt) as e:
            print(f"Error occured: {e}\nExiting...")
            sys.exit()


