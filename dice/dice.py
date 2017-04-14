import discord
from discord.ext import commands
import random

class Dice:
	"""A dice roller, for all your dice rolling needs."""

	def __init__(self, bot):
		self.bot = bot
		self.roll_arr = []			# Array of rolls
		self.discord_arr =[]			# Array of discord emoji rolls
		self.discord_dict ={'0':':zero:',	# Dictionary of discord emoji
				   '1':':one:',
				   '2':':two:',
				   '3':':three:',
				   '4':':four:',
				   '5':':five:',
				   '6':':six:',
				   '7':':seven:',
				   '8':':eight:',
				   '9':':nine:',
				  'sod':':small_orange_diamond:'}

	def roll_dice(self, dice, sides):

		result_arr = []
		for i in range(0, dice):
			result_arr.append(random.randint(1, sides))
		
		result_arr.sort()
		return result_arr

	def discord_dice(self):
		
		result_arr=[]
		for roll in self.roll_arr:
			derp = ''
			for d in str(roll):
				derp += (self.discord_dict[d])
			result_arr.append(derp)

		return result_arr

	@commands.command(pass_context = True)
	async def droll(self, ctx, dice=4, sides=20):
		""" Rolls #dx. Default roll is 4d20. Use [p]droll # x """

		def is_number(s):
			try:
				int(s)
				return True
			except ValueError:
				return False
		
		if is_number(dice) and is_number(sides):

			# Limit dice so we don't overwhelm Discord 
			if dice <= 50:
			
				# Get our dice rolls
				self.roll_arr = self.roll_dice(int(dice), int(sides))
				# Convert our dice rolls to discord number emoji
				self.discord_arr = self.discord_dice() 

				# Text output for rolls
				message = self.discord_dict['sod'] + ' '
				for roll in self.discord_arr:
					message += (str(roll) + ' ' + self.discord_dict['sod'] + ' ')
				
				await self.bot.say("You rolled: \n" + message + " \n Your sum: " + self.roll_arr.sum())
			else:
				await self.bot.say("Too many dice. You can roll up to 50 dice at a time.")

		else:
			await self.bot.say("That's not proper dice format! Use [p]droll # x (ie: [p]droll 2 4)")


def setup(bot):
	bot.add_cog(Dice(bot))
