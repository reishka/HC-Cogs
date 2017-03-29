import discord
from discord.ext import commands
from __main__ import send_cmd_help
from decimal import Decimal


class Converter:

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def convert(ctx):
        if ctx.invoked_subcommand is None:
            '''await send_cmd_help(ctx)'''
            await bot.say('Invalid convert parameter')
    
    @convert.command(pass_context=True)
    async def freedom(ctx):
        await self.bot.say(ctx + " in Commie units is " + str(float(ctx)*1.8+32) + " freedom units.")
        
    @convert.command(name="commie", pass_context=True)
    async def _convert_commie(self,ctx):
        await self.bot.say(ctx +" in Freedom Units is " + str(float(ctx)-32*.5556) + " commies.")

def setup(bot):
    bot.add_cog(Converter(bot))
