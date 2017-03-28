import discord
from discord.ext import commands

import decimal import Decimal

class Converter:
    """My custom cog that does stuff!"""
    
    def _to_fahrenheit(self, num):
        return str((num*1.8+32))
    
    def _to_celcius(self, num):
        return str((num - 32)*.5556)
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def convertf(self, num:Decimal):

        #Your code will go here
        await self.bot.say(_to_fahrenheit)

def setup(bot):
    bot.add_cog(Converter(bot))
