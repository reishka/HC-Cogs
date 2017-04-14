import discord
from discord.ext import commands
import random

class Dice:
	"""A dice roller, for all your dice rolling needs."""

	def __init__(self, bot):
		self.bot = bot
		self.roll_vals = []

	def roll_dice(self, dice, sides, result):

		for i in range(0, dice):
			roll = random.randint(1, sides)
			
			result.append(roll)
			self.roll_arr = result

	@commands.command(pass_context = True)
	async def droll(self, ctx, dice=4, sides=20):
		""" Rolls #dx. Default roll is 4d20. """

		def is_number(s):
			try:
				int(s)
				return True
			except ValueError:
				return False
		
		if is_number(dice) and is_number(sides):
			
			self.roll_arr = []
			self.roll_dice(int(dice), int(sides), [])

			# Text output for now
			message = "**[" + "]** **[".join(str(roll) for roll in self.roll_arr) + "]**"
			await self.bot.say("You rolled: \n" + message)

		else:
			await self.bot.say("That's not proper dice format! Use [p]roll #dx (ie: 2d4)")


def setup(bot):
	bot.add_cog(Dice(bot))
