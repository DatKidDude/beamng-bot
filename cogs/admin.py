import discord
from discord.ext import commands


class Admin(commands.Cog):
    """Admin only commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        """Hot reload all extensions except this one"""
        reloaded = []
        for ext in list(self.bot.extensions.keys()):
            if ext == "cogs.admin":
                continue
            try:
                await self.bot.reload_extension(ext)
                reloaded.append(ext)
            except Exception as e:
                print(f"Failed to reload `{ext}`: {e}")
        print(f"Reloaded: {', '.join(reloaded)}")
    
    @commands.command()
    @commands.is_owner()
    async def remove(self, ctx):
        """Removes all comments from channel"""
        await ctx.channel.purge(limit=1000)



async def setup(bot):
    await bot.add_cog(Admin(bot))