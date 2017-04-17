import discord
from discord.ext import commands
import random

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
		self.DICE_PATH = 'data/dice/d'
		self.roll_arr = []			# Array of rolls
		self.discord_arr =[]			# Array of discord emoji rolls
		self.image_rolls = []			# Array of image rolls
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
				  'sod':':small_orange_diamond:',
				  'sbd':':small_blue_diamond:'}

	def roll_dice(self, dice, sides):

		result_arr = []
		for i in range(0, dice):
			result_arr.append(random.randint(1, sides))
		
		# result_arr.sort()
		return result_arr

	def discord_emoji(self, num_array):
		
		result_arr=[]
		for roll in num_array:
			derp = ''
			for d in str(roll):
				derp += (self.discord_dict[d])
			result_arr.append(derp)

		return result_arr

	def dice_rolls(self, num_array, sides):

		result_arr=[]
		for roll in num_array:
			derp=''
			for d in str(roll):
				derp += self.DICE_PATH + str(sides) +"/"+str(d)+".jpg"
			result_arr.append(derp)

		return result_arr
	
	def image_grid(self, image_arr, dice):
		
		# Our grid will always be 5 across, 100x100 px each cell.
		# Height will be determined by number of dice 
		
		width = 500 # Default width
		if dice<5:
			width = dice*100
		
		height = 1 # Default height
		if dice > 5:
			height = dice/5
			if dice%5 !=0:
				height +=1
		height *=100
		
		# New blank image 
		canvas = Image.new('RGB',(int(width), int(height)))
		
		image_index=0
		
		for y in range(0, int(height), 50):
			for x in range(0, int(width), 100):
				if image_index < len(image_arr):
					im = Image.open(str(image_arr[image_index]))
					im.thumbnail((100,100))
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

			# Limit dice so we don't overwhelm Discord 
			if dice <= 50:
			
				# Get our dice rolls
				self.roll_arr = self.roll_dice(int(dice), int(sides))

				# Get our dice images
				self.image_rolls = self.dice_rolls(self.roll_arr, int(sides))

				# Convert our dice rolls to discord number emoji
				# self.discord_arr = self.discord_emoji(self.roll_arr) 
				
				# discord_total = self.discord_emoji(list(str(sum(self.roll_arr))))

				# Text output for rolls
				# message = "You rolled: \n" + self.discord_dict['sod'] + ' '
				# for roll in self.discord_arr:
				#	message += (str(roll) + ' ' + self.discord_dict['sod'] + ' ')
				# message += "\n Your sum: \n" + ' ' + self.discord_dict['sbd'] + ' '
				
				# for num in discord_total:
				# 	message += (str(num))   
				# message += self.discord_dict['sbd'] + ' '
								
				# message = "Your rolls: \n"
				# for roll in self.image_rolls:
				#	message += str(roll) + ' '
				
				#for dimage in self.image_rolls:
				#	await self.bot.send_file(ctx.message.channel, str(dimage))
				
				self.image_grid(self.image_rolls, int(dice))
				await self.bot.send_file(ctx.message.channel, 'data/dice/temp.jpg')

				# await self.bot.say( message )
			else:
				await self.bot.say("Too many dice. You can roll up to 50 dice at a time.")

		else:
			await self.bot.say("That's not proper dice format! Use [p]droll # x (ie: [p]droll 2 4)")


def setup(bot):
	if not pillowAvailable:
		raise RuntimeError("You need to run 'pip3 install Pillow'")
	else:
		bot.add_cog(Dice(bot))
