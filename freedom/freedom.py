import discord
from discord.ext import commands

class Freedom2:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def freedomUnits(self,ctx):
    
        #Your code will go here
        await self.bot.say(ctx +" in Freedom Units is " + float(ctx)-32*.5556 + " commies.")

def setup(bot):
    bot.add_cog(Freedom2(bot))
