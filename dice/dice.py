import discord
import pudb
from discord.ext import commands
from __main__ import send_cmd_help

class Converter:

    def __init__(self, bot):
        self.bot = bot
        self.input_message = "That's not a number!"     # Error message for garbage input

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError: 
            return False

    @commands.group(name="convert", pass_context=True)
	async def convert(self, ctx):
        """Convert a multitude of things"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @convert.command(name='commies', pass_context=True)
    async def commies(self, ctx, c: float):
        """Convert commies to freedoms"""

        if self.is_number(c): 
            f = c*1.8+32
            await self.bot.say("{0} commies -> {1} freedoms.", str(c), str(f))
        else
            await self.bot.say(self.input_message)

    @convert.command(name="freedoms", pass_context=True)
    async def freedoms(self, ctx, f: float):
        """Convert freedoms to commies"""

        if self.is_number(f)
            c = (f-32)*.5556
            await self.bot.say("{0} freedoms -> {1} commies.", str(f), str(c))
        else
            await self.bot.say(self.input_message)

    @convert.command(name='c-f', pass_context=True)
    async def c(self, ctx, c: float):
        """Convert celsius to fahrenheit"""

        if self.is_number(c): 
            f = c*1.8+32
            await self.bot.say("{0} celsius -> {1} fahrenheit.", str(c), str(f))
        else
            await self.bot.say(self.input_message)

    @convert.command(name="f-c", pass_context=True)
    async def f(self, ctx):
        """Convert fahrenheit to celsius"""

        if self.is_number(f)
            c = (f-32)*.5556
            await self.bot.say("{0} fahrenheit -> {1} celsius.", str(f), str(c))
        else
            await self.bot.say(self.input_message)

    @convert.command(name="cm-in", pass_context=True)
    async def cmim(self, ctx, cm: float):
        """Convert centimeters to inches"""

        if self.is_number(cm)
            in = cm/2.54
            await self.bot.say("{0} centimeters -> {1} inches.", str(cm), str(in))
        else
            await self.bot.say(self.input_message)
        
    @convert.command(name="cm-ft", pass_context=True)
    async def cmft(self, ctx, cm: float):
        """Convert centimeters to feet"""

        if self.is_number(cm)
            ft = cm*0.032808
            await self.bot.say("{0} centimeters -> {1} feet.", str(cm), str(ft))
        else
            await self.bot.say(self.input_message)
        
    @convert.command(name="ft-m", pass_context=True)
    async def ftm(self, ctx, ft: float):
        """Convert feet to meters"""

        if self.is_number(ft)
            m = ft/3.2808
            await self.bot.say("{0} feet -> {1} meters.", str(ft), str(m))
        else
            await self.bot.say(self.input_message)

    @convert.command(name="m-ft", pass_context=True)
    async def mft(self, ctx, m: float):
        """Convert meters to feet"""

        if self.is_number(m)
            ft = m/0.3048
            await self.bot.say("{0} meters -> {1} feet.", str(m), str(ft))
        else
            await self.bot.say(self.input_message)

    @convert.command(name="m-y", pass_context=True)
    async def my(self, ctx, m: float):
        """Convert meters to yards"""

        if self.is_number(m)
            y = m*1.0936
            await self.bot.say("{0} meters -> {1} yards.", str(m), str(y))
        else
            await self.bot.say(self.input_message)
        
    @convert.command(name="in-cm", pass_context=True)
    async def incm(self, ctx, in: float):
        """Convert inches to centimeters"""

        if self.is_number(in)
            f = in*2.54
            await self.bot.say("{0} inches -> {1} centimeters.", str(in), str(cm))
        else
            await self.bot.say(self.input_message)
        
    @convert.command(name="lb-kg", pass_context=True)
    async def lbkg(self, ctx, lb: float):
        """Convert pounds to kilograms"""

        if self.is_number(lb)
            kg = lb/0.45359237
            await self.bot.say("{0} pounds -> {1} kilograms.", str(lb), str(kg))
        else
            await self.bot.say(self.input_message)

    @convert.command(name="kg-lb", pass_context=True)
    async def lbkg(self, ctx, kg: float):
        """Convert kilograms to pounds"""

        if self.is_number(kg)
            lb = kg*2.2043
            await self.bot.say("{0} kilograms -> {1} pounds.", str(kg), str(lb))
        else
            await self.bot.say(self.input_message)
    
def setup(bot):
    bot.add_cog(Converter(bot))
