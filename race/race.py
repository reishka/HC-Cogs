import random
import time
import asyncio
import json

import aiohttp
from discord.ext import commands

from .utils import chat_formatting as cf

class Race:

    """To try things out."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=False, name="race",
                      aliases=["races"])
    async def _race(self, ctx: commands.Context):
        """Doing whatever."""

        base_text1 = "# - O \n"
        base_text2 = "# - X"
        await self.bot.say("Let's get this race on!")
        msg = await self.bot.say(base_text1+base_text2)  
        i = 0
        length_1 = 0
        length_2 = 0
        while i < 40: 
            await asyncio.sleep(1)
            length_1 += random.randint(1,5)
            length_2 += random.randint(1,5)
            text1 = base_text1.replace('-','-'*length_1)
            text2 = base_text2.replace('-','-'*length_2)
            await self.bot.edit_message(msg, text1+text2)
            if len(text1) > 40:
                await self.bot.say("Player 1 is victorious!")
                return
            if len(text2) > 40:
                await self.bot.say("Player 2 is victorious!")
                return
            i += 1

def setup(bot: commands.Bot):
    bot.add_cog(Race(bot))
