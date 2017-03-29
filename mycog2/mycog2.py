import discord
from discord.ext import commands
try:
    from bs4 import BeautifulSoup
    soupAvailable = True
except ModuleNotFound:
    soupAvailable = False
import aiohttp


class Mycog2:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gihcom(self):
        """Command takes no argument, says line."""

        #Your code will go here
        await self.bot.say("I can do stuff!")
        
    @commands.command()
    async def punch(self, user : discord.Member):
        """Command takes argument, adds it to string to say."""
    
        #Your code will go here
        await self.bot.say("ONE PUNCH! And " + user.mention + " is out! ლ(ಠ益ಠლ)")

    @commands.command()
    async def getItem(self):
        """Command takes argument, adds it to string to say."""
        
        url = 'https://api.xivdb.com/item/17433'
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), 'html.parser')
        import pdb; pdb.set_trace()
        try:
            online = 'blabla'


def setup(bot):
    if soupAvailable:
        bot.add_cog(Mycog2(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")
