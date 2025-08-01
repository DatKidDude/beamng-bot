import traceback
import discord
from random import choice
from pymongo.errors import PyMongoError
from discord.ext import commands
from bot import EconomyBot
from datetime import datetime, timezone, timedelta

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
    
    ########################## COG COMMANDS ##########################

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
        except PyMongoError as e:
            print(f"An error occurred: {e}")
            return 
        else:
            await ctx.send(f"{user.mention} has joined the community")

    @commands.command()
    async def work(self, ctx) -> None:
        """Daily command for a user to earn currency"""
        jobs = {
        "cleaned porta potties": 100,
        "commentatated for derby": 600,
        "won a derby": 1000,
        "sold merchandise": 300,
        "worked pit crew": 500,
        "watered the track": 100,
        "worked the food stand": 200,
        "worked the entrance": 600,
        "worked security detail": 400,
        "cleaned the cars": 700
        }
        user = ctx.author
        user_id = str(ctx.author.id)
        cd_field = "daily_cd" # daily cooldown field name

        account = await self.bank.get_account(discord_id=user_id)
        current_time_utc = datetime.now(tz=timezone.utc)
        cooldown_time_utc = account[cd_field]

        if cooldown_time_utc is None or current_time_utc >= cooldown_time_utc:
            job, pay = choice(list(jobs.items()))
            try:
                tomorrow_utc = current_time_utc + timedelta(hours=24)
                balance = await self.bank.update_balance(discord_id=user_id, amount=pay, cooldown_field=cd_field, cooldown_time=tomorrow_utc)
            except PyMongoError as e:
                print(f"An error occured: {e}")
            else:
                await ctx.send(f"{user.mention} {job} and made ${pay}.\nCurrent balance: ${balance}")
        else:
            cooldown = cooldown_time_utc - current_time_utc # returns a timedelta object
            hour = cooldown.seconds // 3600   
            minutes = (cooldown.seconds // 60) % 60
            await ctx.send(f"{user.mention} must wait {hour}:{minutes:02} before working again")


async def setup(bot):
    await bot.add_cog(Economy(bot))