import discord
from discord.ext import commands
import random
from .utils.dataIO import fileIO
from .utils.dataIO import dataIO
from __main__ import send_cmd_help

# Third Party Libraries
try:
	from PIL import Image
	pillowAvailable = True
except ImportError:
	pillowAvailable = False

SETTINGS_PATH = 'data/dice/settings.json'	# Where our settings live
DICE_PATH = 'data/dice/d'			# Prefix for Where our dice live


class Dice:
	"""A dice roller, for all your dice rolling needs."""

	def __init__(self, bot):
		self.bot = bot
		self.roll_arr = []				# Array of rolls
		self.image_rolls = []				# Array of image rolls
		self.de = {'0' : ':zero:',			# Discord Emoji
				'1' : ':one:',
				'2' : ':two:',
				'3' : ':three:',
				'4' : ':four:',
				'5' : ':five:',
				'6' : ':six:',
				'7' : ':seven:',
				'8' : ':eight:',
				'9' : ':nine:',
				'sod' : ':small_orange_diamond:',
				'sbd' : ':small_blue_diamond:'}
		
		self.settings = dataIO.load_json(SETTINGS_PATH)

	def roll_dice(self, dice, sides):

		result_arr = []
		for i in range(0, dice):
			result_arr.append(random.randint(1, sides))


		if str.casefold(self.settings["SORT"]) == "on":
			result_arr.sort()

		return result_arr

	def dice_rolls(self, num_array, sides):

		result_arr=[]
		for roll in num_array:
			derp=''
			derp += DICE_PATH + str(sides) +"/"+str(roll)+".jpg"
			result_arr.append(derp)

		return result_arr
	
	def image_grid(self, image_arr, dice):
		
		# Our grid will be determined by user settings, 100x100 px each cell.
		# Height will be determined by number of dice

		d_width = int(self.settings["DICE_WIDTH"])
		
		width = d_width
		if dice < d_width:
			width = dice
		width = int(width*100) # Turn number of dice into px for canvas
		
		height = 1 # Default height
		if dice > d_width:
			height = int(dice/d_width)
			if dice%d_width !=0:
				height +=1
		height *=100
		
		# New blank image 
		canvas = Image.new('RGB',(int(width), int(height)))
		
		image_index=0
		
		for y in range(0, int(height), 100):
			for x in range(0, int(width), 100):
				if image_index < len(image_arr):
					im = Image.open(str(image_arr[image_index]))
					canvas.paste(im, (x, y))
					image_index+=1
		
		canvas.save('data/dice/temp.jpg', 'JPEG')

	def dice_sum(self, roll_arr):
		
		sum = 0
		for num in roll_arr:
			sum += num

		derp = self.de['sbd'] + ' ' 
		for n in str(sum):
			derp += str(self.de[str(n)])

		derp += ' ' + self.de['sbd']

		
		return derp

	def hit_miss(self, roll_arr):

		hit = 0
		miss = 0

		for num in roll_arr:
			if num < self.settings["HIT_THRESHOLD"]:
				miss += 1
			else:
				hit += 1

		m = self.de['sod'] + "Miss : " + str(miss) + " " +  self.de['sod'] + " Hit: " + str(hit) + " " + self.de['sod']

		return m

	def is_number(self, s):
		try:
			int(s)
			return True
		except ValueError:
			return False

	def is_onoff(self, s):
		if str.casefold(s) != "on" and str.casefold(s) != "off":
			return False
		else:
			return True

	@commands.command(pass_context = True)
	async def dice(self, ctx, dice=4, sides=20):
		""" A dice roller that rolls dice. Default roll is 4d20.

		See [p]dice_set command for more options. """

		if self.is_number(dice) and self.is_number(sides):

			# Get our dice rolls
			self.roll_arr = self.roll_dice(int(dice), int(sides))

			# Get our dice images
			self.image_rolls = self.dice_rolls(self.roll_arr, int(sides))

			# Stick all our dice images into one image
			self.image_grid(self.image_rolls, int(dice))
			
			await self.bot.send_file(ctx.message.channel, 'data/dice/temp.jpg')

			# If 'sum' setting is turned on, print the sum
			if str.casefold(self.settings["SUM"]) == "on":
				message = str(self.dice_sum(self.roll_arr))
				await self.bot.say("Your Sum: " + message)

			# If hit/miss tallying setting is turned on, tabulate hit/miss
			if str.casefold(self.settings["HIT"]) == "on":
				message = str(self.hit_miss(self.roll_arr))
				await self.bot.say ("Hit/Miss Threshold: " + str(self.settings["HIT_THRESHOLD"]) + " "  + message)

		else:
			await self.bot.say("That's not proper dice format! Use [p]droll # x (ie: [p]droll 2 4)")


	@commands.group(name="dice_set", pass_context=True)
	async def dice_set(self, ctx):
		"""Configure settings used by droll."""
		if ctx.invoked_subcommand is None:
			await send_cmd_help(ctx)

	@dice_set.command(name="dice", pass_context=True)
	async def dice(self, ctx, d: int):
		"""Set the amount of dice displayed on one line. Between 1 and 20."""
		if self.is_number(d):
			if d < 1 or d > 20:
				await self.bot.say("You can only set a value between 1 and 20")
			else:
				self.settings["DICE_WIDTH"] = d
				dataIO.save_json(SETTINGS_PATH, self.settings)
				await self.bot.say("Current dice width set to: " + 
					str(self.settings["DICE_WIDTH"]))
		else: await self.bot.say("Not a valid amount.")

	@dice_set.command(name="sum", pass_context=True)
	async def sum(self, ctx, s: str):
		"""Turn summing the dice on or off"""
		if not self.is_onoff(s):
			await self.bot.say ("The only options are 'on' or 'off'. " +
						"Currently, sums are: " + str(self.settings["SUM"]))
		else:
			self.settings["SUM"] = s
			dataIO.save_json(SETTINGS_PATH, self.settings)
			await self.bot.say("Sums are now " + str(self.settings["SUM"]))

	@dice_set.command(name="hit_threshold", pass_context=True)
	async def hit_threshold(self, ctx, h: int):
		"""Set the threshold for pass/fail hit tally. Number specified is INCLUDED in pass
		ie: specifying 8 will specify pass for rolls of 8 and above.  """

		if not self.is_number(h):
			await self.bot.say("Not a valid amount.")
		else:
			self.settings["HIT_THRESHOLD"] = h
			dataIO.save_json(SETTINGS_PATH, self.settings)
			await self.bot.say("Threshold is now: " + str(self.settings["HIT_THRESHOLD"]))

	@dice_set.command(name="hit", pass_context=True)
	async def hit(self, ctx, s: str):
		"""Turn hit/miss tally on or off"""
		if not self.is_onoff(s):
			await self.bot.say("The only options are 'on' or 'off'. " +
						"Currently, hit/miss tallying is " + str(self.settings["HIT"]))
		else:
			self.settings["HIT"] = s
			dataIO.save_json(SETTINGS_PATH, self.settings)
			await self.bot.say("Hit/Miss tallying is now: " + str(self.settings["HIT"]))

	@dice_set.command(name="sort", pass_context=True)
	async def sort(self, ctx, s: str):
		"""Turn dice sorting on or off"""

		if not self.is_onoff(s):
			await self.bot.say("The only options are 'on' or 'off'. " + 
						"Currently, sorting is: " + str(self.settings["SORT"]))
		else:
			self.settings["SORT"] = s
			dataIO.save_json(SETTINGS_PATH, self.settings)
			await self.bot.say("Sorting is now: " + str(self.settings["SORT"]))

def file_check():
	
	default_settings = {"DICE_WIDTH": 7,
				"SUM": "off",
				"HIT_THRESHOLD": 0,
				"HIT": "off",
				"SORT": "off"}

	if not dataIO.is_valid_json(SETTINGS_PATH):
		print("Creating default settings file...")
		dataIO.save_json(SETTINGS_PATH, default_settings)

def setup(bot):

	if not pillowAvailable:
		raise RuntimeError("You need to run 'pip3 install Pillow'")
	else:
		file_check()
		bot.add_cog(Dice(bot))
