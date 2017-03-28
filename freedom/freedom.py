import discord
from discord.ext import commands

class Freedom2:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def freedom2(self,ctx):
    
        #Your code will go here
        await self.bot.say("I can do stuff!")

def setup(bot):
    bot.add_cog(Freedom2(bot))
