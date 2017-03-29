import discord
import pudb
from discord.ext import commands
from __main__ import send_cmd_help

class Converter:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="convert", pass_context=True)
    async def convert(self, ctx):
        """Convert a multitude of things"""
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

    @convert.command(name='c-f', pass_context=False)
    async def c(self, ctx):
        """Convert celsius to fahrenheit"""
        await self.bot.say(str(ctx) + " in celcius units is " + str(float(ctx)*1.8+32) + " fahrenheit.")

    @convert.command(name="f-c", pass_context=False)
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
        
    @convert.command(name="ft-m", pass_context=False)
    async def ftm(self, ctx):
        """Convert feet to meters"""
        await self.bot.say(str(ctx) + " feet is " + str(float(ctx)/3.2808) + " meters.")
        
    @convert.command(name="m-ft", pass_context=False)
    async def mft(self, ctx):
        """Convert meters to feet"""
        await self.bot.say(str(ctx) + " meters is " + str(float(ctx)/0.3048) + " feet.")
        
    @convert.command(name="m-y", pass_context=False)
    async def my(self, ctx):
        """Convert meters to yards"""
        await self.bot.say(str(ctx) + " meters is " + str(float(ctx)*1.0936) + " yards.")
        
    @convert.command(name="in-cm", pass_context=False)
    async def incm(self, ctx):
        """Convert inchess to centimeters"""
        await self.bot.say(str(ctx) + " inches is " + str(float(ctx)*2.54) + " centimeters.")
        
    @convert.command(name="c-oz", pass_context=False)
    async def coz(self, ctx):
        """Convert cups to fluid ounces"""
        await self.bot.say(str(ctx) + " cups is " + str(float(ctx)*8) + " fluid ounces.")
        
    @convert.command(name="oz-c", pass_context=False)
    async def ozc(self, ctx):
        """Convert fluid ounces to cups"""
        await self.bot.say(str(ctx) + " fluid ounces is " + str(float(ctx)/8) + " cups.")
        
    @convert.command(name="lb-kg", pass_context=False)
    async def lbkg(self, ctx):
        """Convert pounds to kilograms"""
        await self.bot.say(str(ctx) + " pounds is " + str(float(ctx)*0.45359237) + " kilograms.")
        
    
def setup(bot):
    bot.add_cog(Converter(bot))
