import discord
import os
import logging
import random
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from datetime import datetime
from copy import deepcopy
from typing import List

# Third Party Libraries
try:
	from fuzzywuzzy import fuzz
	from fuzzywuzzy import process
	fuzzyAvailable = True
except ImportError:
	fuzzzyAvailable = False

default_settings = {
	"index": 1,
	"quotes": {}
}

class QuotesDB:
	"""Quote Database. Store and recall your favourite quotes!"""

	def __init__(self, bot):
		self.bot = bot
		self.quote_db_location = "data/quotedb/quotedb.json"
		self.quote_db = dataIO.load_json(self.quote_db_location)

	def is_number(self, n):
		try:
			int(n)
			return True
		except ValueError:
			return False

	@commands.command(pass_context=True, no_pm=True)
	async def addquote(self, ctx, user: discord.User, *quote: str):
		"""Adds a new quote. You can @mention the user when creating your quote, or simply spell their name."""

		# First, let's make sure the user is an actual user. You can use 
		# @mentions or just spell the user's name - we work on IDs
		server = ctx.message.server
		if server.get_member(user.id):
			quote_index = self.quote_db["index"]
			self.quote_db["quotes"][str(quote_index)] = "<@"+user.id + ">: " + " ".join(quote)
			self.quote_db["index"] += 1
			dataIO.save_json(self.quote_db_location, self.quote_db)
			message = "Quote number {} has been added!".format(quote_index)
		else:
			message = "No user with that username"

		await self.bot.say(message)

	@commands.command(pass_context=True, no_pm=True)
	async def quote (self, ctx, search=None):
		"""Display a quote. Search parameters are optional. You can specify a quote by number, or search for a random quote based on a search term. To see all quotes by a user or for a search term, use the allquotes command instead.

		Default quote behaviour is to display a random quote"""

		if search is None:
			quote_index = random.randint(1, self.quote_db["index"]-1)
			try:
				message = self.quote_db["quotes"][str(quote_index)]
			except KeyError:
				message = "Something is borked. Tell ★< O^-Ç=#1796."

		elif self.is_number(search):
			try:
				message = self.quote_db["quotes"][str(search)]
			except KeyError:
				message = "There is no quote with that number. Try again."
		else:

			fuzzy_matches = process.extractBests(search, self.quote_db["quotes"], score_cutoff=60)

			if len(fuzzy_matches) is 0:
				message = "Sorry, no matches!"
			elif len(fuzzy_matches) > 1:
				message = fuzzy_matches[random.randint(0, len(fuzzy_matches)-1)][0]
			else:
				message = fuzzy_matches[0][0]

		await self.bot.say(message)

def check_folders():
	if not os.path.exists("data/quotedb"):
		print("Creating data/quotedb folder...")
		os.makedirs("data/quotedb")

def check_files():

	f = "data/quotedb/quotedb.json"
	if not dataIO.is_valid_json(f):

		settings = {"index": 1, "quotes": {} }
		print("Creating empty quotedb.json...")
		dataIO.save_json(f, settings)

def setup(bot):
	global logger

	if not fuzzyAvailable:
		raise RuntimeError("You need to run `pip3 install fuzzywuzzy[speedup]`")

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
	bot.add_cog(QuotesDB(bot))
