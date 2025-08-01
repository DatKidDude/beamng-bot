import traceback
import discord
from discord.ext import commands
from bot import EconomyBot
from datetime import datetime, timezone

class MustBeRegistered(commands.CheckFailure): pass

class Economy(commands.Cog):
    def __init__(self, bot: EconomyBot) -> None:
        self.bot = bot
        self.bank = self.bot.db.bank
    
    async def cog_check(self, ctx: commands.Context) -> bool:
        """Run a boolean check on every command inside the class. If True is 
        returned the command is ran
        
        Returns:
            bool: If True the command is ran else raises Exception
        
        Raises:
            MustBeRegistered (commands.CheckFailure): Runs if user is not stored in the database
        """
        # Allow the !join command to bypass registration check
        if ctx.command and ctx.command.qualified_name == "join": 
            return True

        user_id = str(ctx.author.id)
        is_registered = await self.bank.check_user_exists(discord_id=user_id)
        if not is_registered:
            raise MustBeRegistered(f"{ctx.author.mention} type !join to be able to run commands")
        return True
    
    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        """Called whenever an error is dispatched inside the Economy Cog"""
        if isinstance(error, commands.CommandInvokeError):
            print(error.original)

        if isinstance(error, MustBeRegistered):
            await ctx.send(str(error))
        else:
            error_data = "".join(traceback.format_exception(type(error), error, error.__traceback__))
            print(error_data)
    
    @commands.command()
    async def join(self, ctx) -> None:
        """Adds user to the database
        
        Args:
            ctx (commands.Context): Invocation context meta data
        
        Raises:
            Exception: catches any exception 
        """
        user = ctx.author
        user_id = str(user.id)
        account = {
            "discord_id": user_id,
            "username": user.name,
            "currency": 1000,
            "daily_cd": None,
            "weekly_cd": None
        }

        if await self.bank.check_user_exists(user_id):
            await ctx.send(f"{user.mention} has already joined")
            return

        try:
            await self.bank.add_account(discord_member=account)
        except Exception as e:
            print(f"An error occurred: {e}")
            return 
        else:
            await ctx.send(f"{user.mention} has joined the community")

    @commands.command()
    async def work(self, ctx) -> None:
        """Daily command for a user to earn currency"""
        user = ctx.author
        user_id = str(ctx.author.id)

        account = await self.bank.get_account(discord_id=user_id)
        print(account)

async def setup(bot):
    await bot.add_cog(Economy(bot))