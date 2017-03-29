import random
import time
import asyncio
import json

import aiohttp
from discord.ext import commands

from .utils import chat_formatting as cf

class GeneralTrickery:

    """To try things out."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=False, name="trickery",
                      aliases=["trickeries"])
    async def _trickery(self, ctx: commands.Context):
        """ Doing whatever. """
        the_lounge = self.bot.get_channel("83591694599061504")
        await self.bot.say("Gotta repeat messages here")
        with open("/home/peen/lounge_log.txt",'a') as opened:
            async for message in self.bot.logs_from(the_lounge,100):
                opened.write("{} -!- {} !-! \n".format(message.author,message.content))
            

def setup(bot: commands.Bot):
    bot.add_cog(GeneralTrickery(bot))
