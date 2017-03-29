import discord
from discord.ext import commands
from __main__ import send_cmd_help
from decimal import Decimal


class Converter:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, no_pm=True)
    def convert(self, ctx):
        """Cookie settings group command"""

        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
    
    @convert.command(name="freedom", pass_context=True, manage_server=False)
    def freedom(self, message):
        msg = str(float(message[0])*1.8+32)
        await self.bot.say(msg)
        
    @convert.command()
    async def toCommie(self,ctx):
    
        #Your code will go here
        await self.bot.say(ctx +" in Freedom Units is " + str(float(ctx)-32*.5556) + " commies.")

def setup(bot):
    bot.add_cog(Converter(bot))
