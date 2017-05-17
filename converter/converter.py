import discord
import pudb
import requests
import os
import json
from decimal import *
from datetime import datetime
from .utils.dataIO import dataIO
from discord.ext import commands
from __main__ import send_cmd_help

CURRENCIES_PATH = 'data/converter/currencies.json'
RATES_PATH = 'data/converter/rates_'
RATES_SUFF = '.json'

class Converter:

	def __init__(self, bot):
		self.bot = bot
		self.input_message = "That's not a number!"     # Error message for garbage input
		self.currencies = dataIO.load_json(CURRENCIES_PATH)
		self.valid_currencies = ['AUD','BGN', 'BRL', 'CAD', 'CHF', 'CNY',
					 'CZK', 'DKK', 'GBP', 'HKD', 'HRK', 'HUF',
					 'IDR', 'ILS', 'INR', 'JPY', 'KRW', 'MXN',
					 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON',
					 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'USD',
					 'ZAR', 'EUR']

	def is_number(self, s):
		try:
			Decimal(s)
			return True
		except ValueError:
			return False

	def get_rates(self, currency_from):
		payload = {'base':str.upper(currency_from)}
		rates = requests.get('http://api.fixer.io/latest', payload).json()
		return rates

	def get_exchange_rate(self, amount:Decimal, currency_from:str, currency_to:str):

		rates_file_path = RATES_PATH + currency_from + RATES_SUFF
		currency_f = str.upper(currency_from)

		if self.currencies[currency_f]["last_updt"] is not None:
			update_delta = datetime.now() - datetime.strptime(self.currencies[currency_f]["last_updt"], '%Y-%m-%d %H:%M:%S.%f')

			if update_delta.seconds > 86400:
				rates = self.get_rates(currency_f)
				dataIO.save_json(rates_file_path, rates)
				self.currencies[currency_f]["last_updt"] = str(datetime.now())
				dataIO.save_json(CURRENCIES_PATH, self.currencies)
			else:
				rates = dataIO.load_json(rates_file_path)

		else:
			rates = self.get_rates(currency_f)
			dataIO.save_json(rates_file_path, rates)
			self.currencies[currency_f]["last_updt"] = str(datetime.now())
			dataIO.save_json(CURRENCIES_PATH, self.currencies)

		return rates['rates'][str.upper(currency_to)]

	def formatter(self, amount:Decimal, currency_to:str):

		symbol = self.currencies[str.upper(currency_to)]["symbol"]
		spacer = self.currencies[str.upper(currency_to)]["sep_1"]
		dec_pt = self.currencies[str.upper(currency_to)]["sep_2"]
		minor = self.currencies[str.upper(currency_to)]["minor"]

		quant = Decimal(10) ** -int(minor)
		sign, digits, exp = amount.quantize(quant).as_tuple()
		result = []

		digits = list(digits)
		build, next = result.append, digits.pop

		for i in range(int(minor)):
			build(next() if minor is not '0'  else '0')
		build(dec_pt)
		if not digits:
			build('0')
		i = 0
		while digits:
			build(next())
			i += 1
			if i == 3 and digits:
				i = 0
				build(spacer)
		build(symbol)
		result = [str(item) for item in result]
		return ''.join(reversed(result))

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
	async def currency(self, ctx, amount: Decimal, currency_from="usd", currency_to="cad"):
		"""Convert from one currency to another. Defaults USD to CAD. Use '[p]convert currencies' to get a list of accepted convertable currencies."""

		if (str.upper(currency_from) in self.valid_currencies) and (str.upper(currency_to) in self.valid_currencies):

			rate = self.get_exchange_rate(amount, currency_from, currency_to)
			conversion = Decimal(amount * Decimal(rate))

			await self.bot.say(str(self.formatter(conversion, currency_to)))
		else:
			await self.bot.say("Those might not be currencies.")

	@convert.command(name="currencies", pass_context=True)
	async def currencies(self, ctx):
		"""List of convertable currencies using [p]convert currency command."""

		await self.bot.say(" ".join(self.valid_currencies))

def check_folders():
	if not os.path.exists("data/converter/"):
		print("Creating data/converter folder...")
		os.makedirs("data/converter")

def check_files():

	if not dataIO.is_valid_json(CURRENCIES_PATH):
		print("Creating default currencies file...")
		space = " "
		dot = '.'
		quote = "'"
		comma = ','
		default_countries = {
		"AUD": {'symbol':'$', 	'sep_1':space, 	'sep_2':comma, 	'minor':'2', 'last_updt':None},
		"BGN": {'symbol':'лв', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"BRL": {'symbol':'R$', 	'sep_1':dot, 	'sep_2':comma, 	'minor':'2', 'last_updt':None},
		"CAD": {'symbol':'$', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"CHF": {'symbol':'CHF', 'sep_1':quote, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"CNY": {'symbol':'¥', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"CZK": {'symbol':'Kč', 	'sep_1':dot, 	'sep_2':comma, 	'minor':'2', 'last_updt':None},
		"DKK": {'symbol':'kr', 	'sep_1':dot, 	'sep_2':comma, 	'minor':'2', 'last_updt':None},
		"EUR": {'symbol':'€', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"GBP": {'symbol':'£', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"HKD": {'symbol':'$', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"HRK": {'symbol':'kn', 	'sep_1':dot, 	'sep_2':comma, 	'minor':'2', 'last_updt':None},
		"HUF": {'symbol':'Ft', 	'sep_1':dot, 	'sep_2':comma, 	'minor':'0', 'last_updt':None},
		"IDR": {'symbol':'Rp', 	'sep_1':dot, 	'sep_2':comma, 	'minor':'2', 'last_updt':None},
		"ILS": {'symbol':'₪', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"INR": {'symbol':'₹', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"JPY": {'symbol':'¥', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'0', 'last_updt':None},
		"KRW": {'symbol':'₩', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'0', 'last_updt':None},
		"MXN": {'symbol':'$', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"MYR": {'symbol':'RM', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"NOK": {'symbol':'kr', 	'sep_1':dot, 	'sep_2':comma, 	'minor':'2', 'last_updt':None},
		"NZD": {'symbol':'$', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"PHP": {'symbol':'₱', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"PLN": {'symbol':'zł', 	'sep_1':space, 	'sep_2':comma, 	'minor':'2', 'last_updt':None},
		"RON": {'symbol':'lei',	'sep_1':dot, 	'sep_2':comma, 	'minor':'2', 'last_updt':None},
		"RUB": {'symbol':'₽', 	'sep_1':dot, 	'sep_2':comma, 	'minor':'2', 'last_updt':None},
		"SEK": {'symbol':'kr', 	'sep_1':space, 	'sep_2':comma, 	'minor':'2', 'last_updt':None},
		"SGD": {'symbol':'$', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"THB": {'symbol':'฿', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"TRY": {'symbol':'‎₺', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"USD": {'symbol':'$', 	'sep_1':comma, 	'sep_2':dot, 	'minor':'2', 'last_updt':None},
		"ZAR": {'symbol':'R', 	'sep_1':space, 	'sep_2':dot, 	'minor':'2', 'last_updt':None}}

		dataIO.save_json(CURRENCIES_PATH, default_countries)

def setup(bot):
	check_folders()
	check_files()
	bot.add_cog(Converter(bot))
