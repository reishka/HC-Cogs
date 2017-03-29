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
        """Convert commies to freedoms"""
        await self.bot.say(str(ctx) + " in commies is " + str(float(ctx)*1.8+32) + " freedoms.")

    @convert.command(name="freedoms", pass_context=False)
    async def freedoms(self, ctx):
        """Convert freedoms to commies"""
        await self.bot.say(str(ctx) +" in freedoms is " + str(float(ctx)-32*.5556) + " commies.")

    @convert.command(name='c', pass_context=False)
    async def c(self, ctx):
        """Convert celsius to fahrenheit"""
        await self.bot.say(str(ctx) + " in celcius units is " + str(float(ctx)*1.8+32) + " fahrenheit.")

    @convert.command(name="f", pass_context=False)
    async def f(self, ctx):
        """Convert fahrenheit to celsius"""
        await self.bot.say(str(ctx) +" in fahrenheit is " + str(float(ctx)-32*.5556) + " celsius.")    
             
    @convert.command(name="cm-in", pass_context=False)
    async def cmim(self, ctx):
        """Convert centimeters to inches"""
        await self.bot.say(str(ctx) + " centieters is " + str(float(ctx)/2.54) + " inches.")
        
    @convert.command(name="cm-ft", pass_context=False)
    async def cmft(self, ctx):
        """Convert centimeters to feet"""
        await self.bot.say(str(ctx) + " centimeters is " + str(float(ctx)*0.032808) + " feet.")
    
def setup(bot):
    bot.add_cog(Converter(bot))
