import discord
from discord.ext import commands
from decimal import Decimal

class Converter:
    
    def to_fahrenheit(self, num:Decimal):
        return str((num*1.8+32))
    
    def to_celcius(self, num:Decimal):
        return str((num - 32)*.5556)
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def convertf(self, num:Decimal):

        #Your code will go here
        self.bot.say(to_fahrenheit)

def setup(bot):
    bot.add_cog(Converter(bot))
