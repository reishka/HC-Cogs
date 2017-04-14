import discord
from discord.ext import commands
import random

class Dice:
	"""A dice roller, for all your dice rolling needs."""

	def __init__(self, bot):
		self.bot = bot
		self.roll_arr = []
		self.discord_arr =[]
		self.discord_num={'0':':zero:',
				   '1':':one:',
				   '2':':two:',
				   '3':':three:',
				   '4':':four:',
				   '5':':five:',
				   '6':':six:',
				   '7':':seven:',
				   '8':':eight:',
				   '9':':nine:'}

	def roll_dice(self, dice, sides, result):

		for i in range(0, dice):
			roll = random.randint(1, sides)
			
			result.append(roll)

		self.roll_arr = result
		self.roll_arr.sort()

	def discord_dice(self, result):

		derp = []
		for roll in self.roll_arr:
			derp = []
			for d in str(roll):
				derp.append(self.discord_num[d])
			result.append(derp)

		self.discord_arr = result

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

			# Limit dice so we don't overwhelm Discord 
			if dice <= 100:
			
				self.roll_arr = []
				self.roll_dice(int(dice), int(sides), [])

				self.discord_arr = []
				self.discord_dice([])

				# Text output for now
				message =  + .join(str(roll) for roll in self.discord_arr)
				await self.bot.say("You rolled: \n" + message)
			else:
				await self.bot.say("Too many dice. You can roll up to 100 dice at a time.")

		else:
			await self.bot.say("That's not proper dice format! Use [p]droll # x (ie: [p]droll 2 4)")


def setup(bot):
	bot.add_cog(Dice(bot))
