import discord
from discord.ext import commands
from __main__ import send_cmd_help
from decimal import Decimal


class Converter:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, no_pm=True)
    async def convert(self, ctx, *):
        """Cookie settings group command"""

        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
    
    @convert.command(name="freedom", pass_context=True, manage_server=False)
    async def freedom(self, *message):
        msg = str(float(message[0])*1.8+32)
        await self.bot.say(msg)
        
    @convert.command(name="commie", pass_context=True, manage_server=False)
    async def commie(self, ctx, amount:str):
        msg = str((float(amount)-32)*.5556)
        await self.bot.say(msg)

def setup(bot):
    bot.add_cog(Converter(bot))
