import discord
import pudb
import requests
import os
from .utils.dataIO import dataIO
from discord.ext import commands
from __main__ import send_cmd_help

UPDATES_PATH = 'data/converter/updates.json'
RATES_PATH = 'data/converter/rates_' 
RATES_SUFF = '.json'

class Converter:

	def __init__(self, bot):
		self.bot = bot
		self.input_message = "That's not a number!"     # Error message for garbage input
		self.last_update = dataIO.load_json(UPDATES_PATH)
		self.valid_currencies = "AUD, BGN, BRL, CAD, CHF, CNY, CZK, DKK, GBP, HKD, HRK, HUF, IDR, ILS, INR, JPY, KRW, MXN, MYR, NOK, NZD, PHP, PLN, RON, RUB, SEK, SGD, THB, TRY, ZAR, EUR"

	def is_number(self, s):
		try:
			float(s)
			return True
		except ValueError: 
			return False
	def get_rates(self, currency_from):
		payload = {'base':currency_from}
		return requests.get('http://api.fixer.io/latest', payload)
		
	def get_exchange_rate(self, amount:float, currency_from:str, currency_to:str):
		
		rates_file_path = RATES_PATH + currency_from + RATES_SUFF
		
		if self.last_update[currency_from] is not None:
			update_delta = datetime.now() - self.last_update[currency_from]
			
			if update_delta.hours > 24: 
				rates = get_rates(currency_from)
				dataIO.save_json(rates_file_path, rates)
				self.last_update[currency_from] = datetime.now()
				dataIO.save_json(UPDATES_PATH, self.last_update)
			else:
				rates = dataIO.load_json(rates_file_path)
				
		else:
			rates = get_rates(currency_from)
			dataIO.save_json(rates_file_path, rates)
			self.last_update[currency_from] = datetime.now()
			dataIO.save_json(UPDATES_PATH, self.last_update)
				
		return rates

	@commands.group(name="convert", pass_context=True)
	async def convert(self, ctx):
		"""Convert a multitude of things"""
		if ctx.invoked_subcommand is None:
			await send_cmd_help(ctx)

	@convert.command(name='commies', pass_context=True)
	async def commies(self, ctx, commies: float):
		"""Convert commies to freedoms"""

		if self.is_number(commies): 
			f = commies*1.8+32
			await self.bot.say("{0} commies :arrow_right: {1} freedoms.".format(str(commies), str(f)))
		else:
			await self.bot.say(self.input_message)

	@convert.command(name="freedoms", pass_context=True)
	async def freedoms(self, ctx, freedoms: float):
		"""Convert freedoms to commies"""

		if self.is_number(freedoms):
			c = (freedoms-32)*.5556
			await self.bot.say("{0} freedoms :arrow_right: {1} commies.".format(str(freedoms), str(c)))
		else:
			await self.bot.say(self.input_message)

	@convert.command(name='c-f', pass_context=True)
	async def c(self, ctx, celsius: float):
		"""Convert celsius to fahrenheit"""

		if self.is_number(celsius): 
			f = celsius*1.8+32
			await self.bot.say("{0} celsius :arrow_right: {1} fahrenheit.".format(str(celsius), str(f)))
		else:
			await self.bot.say(self.input_message)

	@convert.command(name="f-c", pass_context=True)
	async def f(self, ctx, fahrenheit: float):
		"""Convert fahrenheit to celsius"""

		if self.is_number(fahrenheit):
			c = (fahrenheit-32)*.5556
			await self.bot.say("{0} fahrenheit :arrow_right: {1} celsius.".format(str(fahrenheit), str(c)))
		else:
			await self.bot.say(self.input_message)

	@convert.command(name="cm-in", pass_context=True)
	async def cmim(self, ctx, cm: float):
		"""Convert centimeters to inches"""

		if self.is_number(cm):
			i = cm/2.54
			await self.bot.say("{0} centimeters :arrow_right: {1} inches.".format(str(cm), str(i)))
		else:
			await self.bot.say(self.input_message)
		
	@convert.command(name="cm-ft", pass_context=True)
	async def cmft(self, ctx, cm: float):
		"""Convert centimeters to feet"""

		if self.is_number(cm):
			ft = cm*0.032808
			await self.bot.say("{0} centimeters :arrow_right: {1} feet.".format(str(cm), str(ft)))
		else:
			await self.bot.say(self.input_message)
		
	@convert.command(name="ft-m", pass_context=True)
	async def ftm(self, ctx, ft: float):
		"""Convert feet to meters"""

		if self.is_number(ft):
			m = ft/3.2808
			await self.bot.say("{0} feet :arrow_right: {1} meters.".format(str(ft), str(m)))
		else:
			await self.bot.say(self.input_message)

	@convert.command(name="m-ft", pass_context=True)
	async def mft(self, ctx, meters: float):
		"""Convert meters to feet"""

		if self.is_number(meters):
			ft = meters/0.3048
			await self.bot.say("{0} meters :arrow_right: {1} feet.".format(str(meters), str(ft)))
		else:
			await self.bot.say(self.input_message)

	@convert.command(name="m-y", pass_context=True)
	async def my(self, ctx, meters: float):
		"""Convert meters to yards"""

		if self.is_number(meters):
			y = meters*1.0936
			await self.bot.say("{0} meters :arrow_right: {1} yards.".format(str(meters), str(y)))
		else:
			await self.bot.say(self.input_message)
		
	@convert.command(name="in-cm", pass_context=True)
	async def incm(self, ctx, inches: float):
		"""Convert inches to centimeters"""

		if self.is_number(inches):
			cm = inches*2.54
			await self.bot.say("{0} inches :arrow_right: {1} centimeters.".format(str(inches), str(cm)))
		else:
			await self.bot.say(self.input_message)
		
	@convert.command(name="lb-kg", pass_context=True)
	async def lbkg(self, ctx, lb: float):
		"""Convert pounds to kilograms"""

		if self.is_number(lb):
			kg = lb/0.45359237
			await self.bot.say("{0} pounds :arrow_right: {1} kilograms.".format(str(lb), str(kg)))
		else:
			await self.bot.say(self.input_message)

	@convert.command(name="kg-lb", pass_context=True)
	async def lbkg(self, ctx, kg: float):
		"""Convert kilograms to pounds"""

		if self.is_number(kg):
			lb = kg*2.2043
			await self.bot.say("{0} kilograms :arrow_right: {1} pounds.".format(str(kg), str(lb)))
		else:
			await self.bot.say(self.input_message)
			
			
	@convert.command(name="currency", pass_context=True)
	async def currency(self, ctx, amount: float, currency_from="usd", currency_to="cad"):
		"""Convert from one currency to another. Defaults USD to CAD. Use [p]currencies to get a list of accepted convertable currencies."""
		
		rate = self.get_exchange_rate(amount, currency_from, currency_to)
		await self.bot.say(str(rate))
		
		
	@convert.command(name="currencies", pass_context=True)
	async def currencies(self, ctx):
		"""List of convertable currencies using [p]convert currency command."""

		await self.bot.say(self.valid_currencies)		

def check_folders(): 
	if not os.path.exists("data/converter/"):
		print("Creating data/converter folder...")
		os.makedirs("data/converter")
	
def check_files(): 
	if not dataIO.is_valid_json(UPDATES_PATH):
		print("Creating default updates file...")
		default_updates = {"AUD":None,
				"BGN":None, 
				"BRL":None,
				"CAD":None,
				"CHF":None,
				"CNY":None,
				"CZK":None,
				"DKK":None,
				"GBP":None,
				"HKD":None,
				"HRK":None,
				"HUF":None,
				"IDR":None,
				"ILS":None,
				"INR":None,
				"JPY":None,
				"KRW":None,
				"MXN":None,
				"MYR":None,
				"NOK":None,
				"NZD":None,
				"PHP":None,
				"PLN":None,
				"RON":None,
				"RUB":None,
				"SEK":None,
				"SGD":None,
				"THB":None,
				"TRY":None,
				"ZAR":None,
				"USD":None,
				"EUR":None}
		dataIO.save_json(UPDATES_PATH, default_updates)	
	
	
def setup(bot):
	check_folders()
	check_files()
	bot.add_cog(Converter(bot))
