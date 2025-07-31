import discord
from discord.ext import commands
from bot import EconomyBot

class MustBeRegistered(commands.CheckFailure): pass

class Economy(commands.Cog):
    def __init__(self, bot: EconomyBot) -> None:
        self.bot = bot
        self.bank = self.bot.db.bank
    
    async def cog_check(self, ctx: commands.Context):
        # Allow the !join command to bypass registration check
        if ctx.command and ctx.command.qualified_name == "join": 
            return True

        user_id = str(ctx.author.id)
        is_registered = await self.bank.check_user_exists(discord_id=user_id)
        if not is_registered:
            raise MustBeRegistered(f"{ctx.author.mention} type !join to be able to run commands")
        return True
    
    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, MustBeRegistered):
            await ctx.send(str(error))
        else:
            print(error)
    
    @commands.command()
    async def join(self, ctx):
        user = ctx.author
        user_id = str(user.id)
        account = {
            "discord_id": user_id,
            "username": user.name,
            "currency": 1000
        }
        try:
            await self.bank.add_account(discord_member=account)
        except Exception as e:
            print(f"An error occurred: {e}")
            return 
        else:
            await ctx.send(f"{user.mention} has joined the community")

async def setup(bot):
    await bot.add_cog(Economy(bot))