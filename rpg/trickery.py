import random
import time
import asyncio
import json

import aiohttp
from discord.ext import commands

from .utils import chat_formatting as cf

class RPG:

    """To try things out."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=False, name="rpg")
    async def _rpg(self, ctx: commands.Context):
        """ Doing whatever. """

        msg = await self.bot.say("Let's get started!")  
        

def setup(bot: commands.Bot):
    bot.add_cog(RPG(bot))
