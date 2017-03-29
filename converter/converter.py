import discord
import pudb
from discord.ext import commands
from __main__ import send_cmd_help

class Converter:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="convert", pass_context=True)
    async def convert(self, ctx):

        """Invoke help if there is no command"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @convert.command(name='commies', pass_context=False)
    async def commies(self, ctx):
        await self.bot.say(str(ctx) + " in commies is " + str(float(ctx)*1.8+32) + " freedoms.")

    @convert.command(name="freedoms", pass_context=False)
    async def freedoms(self, ctx):
        await self.bot.say(str(ctx) +" in freedoms is " + str(float(ctx)-32*.5556) + " commies.")

    @convert.command(name='c', pass_context=False)
    async def c(self, ctx):
        await self.bot.say(str(ctx) + " in celcius units is " + str(float(ctx)*1.8+32) + " fahrenheit.")

    @convert.command(name="f", pass_context=False)
    async def f(self, ctx):
        await self.bot.say(str(ctx) +" in fahrenheit is " + str(float(ctx)-32*.5556) + " celsius.")    
    
    @convert.command(name="meters", pass_context=True)
    async def meters(self, ctx):
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            
    @meters.command(name="feet", pass_context=False)
    async def feet(self, ctx):
        await self.bot.say(str(ctx) + " feet is " + str(float(ctx)/3.2808) + " meters.")
    
def setup(bot):
    bot.add_cog(Converter(bot))
