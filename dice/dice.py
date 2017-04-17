import discord
from discord.ext import commands
import random
from .utils.dataIO import fileIO

# Third Party Libraries
try: 
	from PIL import Image
	pillowAvailable = True
except ImportError:
	pillowAvailable = False

class Dice:
	"""A dice roller, for all your dice rolling needs."""

	def __init__(self, bot):
		self.bot = bot
		self.DICE_PATH = 'data/dice/d'			# Where our dice live
		self.SETTINGS_PATH = 'data/dice/settings.json'	# Where our settings live
		self.roll_arr = []				# Array of rolls
		self.image_rolls = []				# Array of image rolls
		
		self.settings = fileIO(self.SETTINGS_PATH, "load")
		
		self.default_settings = {"DICE_WIDTH": 7,
				    	"SUM": "Y"}
		
	def roll_dice(self, dice, sides):

		result_arr = []
		for i in range(0, dice):
			result_arr.append(random.randint(1, sides))
		
		# result_arr.sort()
		return result_arr

	def dice_rolls(self, num_array, sides):

		result_arr=[]
		for roll in num_array:
			derp=''
			derp += self.DICE_PATH + str(sides) +"/"+str(roll)+".jpg"
			result_arr.append(derp)

		return result_arr
	
	def image_grid(self, image_arr, dice):
		
		# Our grid will be determined by user settings, 100x100 px each cell.
		# Height will be determined by number of dice 
		
		width = int(self.settings["DICE_WIDTH"]) # Default width
		if dice<5:
			width = dice*100
		
		height = 1 # Default height
		if dice > 5:
			height = int(dice/5)
			if dice%5 !=0:
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

			# Get our dice rolls
			self.roll_arr = self.roll_dice(int(dice), int(sides))

			# Get our dice images
			self.image_rolls = self.dice_rolls(self.roll_arr, int(sides))

			# Stick all our dice images into one image 				
			self.image_grid(self.image_rolls, int(dice))
			
			await self.bot.send_file(ctx.message.channel, 'data/dice/temp.jpg')

		else:
			await self.bot.say("That's not proper dice format! Use [p]droll # x (ie: [p]droll 2 4)")


def file_check():
    	
	if not dataIO.is_valid_json(self.SETTINGS_PATH):
		print("Creating default settings file...")
		dataIO.save_json(self.SETTINGS_PATH, self.default_settings)

def setup(bot):
	if not pillowAvailable:
		raise RuntimeError("You need to run 'pip3 install Pillow'")
	else:
		bot.add_cog(Dice(bot))
