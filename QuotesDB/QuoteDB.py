import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from datetime import datetime
from copy import deepcopy

default_settings = {
	"index": 1,
	"quotes": {}
}

class QuoteDB
	"""Quote Database. Store and recall your favourite quotes!"""

		def __init__(self, bot):
		self.bot = bot
		self.quote_db_location = "data/quotedb/quotedb.json"
		self.quote_db = dataIO.load_json(self.quote_db_location)

		def list_quotes(self) -> List[str]:
			lquotes = [(int(i), j)
				for (i, j) in self.quote_db["quotes"].items()]

			lquotes.sort(key=lambda x: x[0])
			return ["{}. {}".format(k, l) for (k, l) in lquotes]


		@commands.command(pass_context=True, no_pm=True)
		async def addquote(self, ctx, username: str, quote: str)
			"""Adds a new quote"""

			quote_index = self.settings["index"]
			self.quote_db["quotes"][str(quote_index)] = username + ": " + quote
			self.quote_db["index"] += 1
			dataIO.save_json(self.quote_db_location, self.quote_db)

			await self.bot.say("Quote number {} has been added!".format(quote_index))



def check_folders():
	if not os.path.exists("data/quotedb"):
		print("Creating data/quotedb folder...")
		os.makedirs("data/quotedb")


def check_files():

	f = "data/quotedb/quotes_settings.json"
	if not dataIO.is_valid_json(f):
		print("Creating default quotes settings...")
		dataIO.save_json(f, {})

	f = "data/quotedb/quotedb.json"
	if not dataIO.is_valid_json(f):
		print("Creating empty quotedb.json...")
		dataIO.save_json(f, {})


def setup(bot):
	global logger
	check_folders()
	check_files()
	logger = logging.getLogger("red.casino")
	if logger.level == 0:
		# Prevents the logger from being loaded again in case of module reload
		logger.setLevel(logging.INFO)
		handler = logging.FileHandler(
			filename='data/quotedb/quotes.log', encoding='utf-8', mode='a')
		handler.setFormatter(logging.Formatter(
			'%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
		logger.addHandler(handler)
	bot.add_cog(QuoteDB(bot))
