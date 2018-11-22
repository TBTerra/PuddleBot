import discord
import random
import re
from discord.ext import commands

class Fun:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def hug(self, ctx, *, text=None):
		"""
		Hugs the mentioned user :3
		Usage:
			{command_prefix}hug @PuddleBot#4998
			{command_prefix}hug
			to hug self
		"""
		if not text:
			return await ctx.send(":blush: *{} hugs {}*".format(self.bot.user.name, ctx.author.nick if ctx.author.nick!=None else ctx.author.name))
		if ctx.message.mentions:
			for member in ctx.message.mentions:
				await ctx.send(":blush: *{} hugs {}*".format(self.bot.user.name, member.nick if member.nick!=None else member.name))
			return
		else:
			return await ctx.send(":blush: *{} hugs {}*".format(self.bot.user.name, text))

	@commands.command(aliases=["headpat", "pet"])
	async def pat(self, ctx, *, text=None):
		"""
		Gives headpats to the mentioned user :3
		Usage:
			{command_prefix}pat @PuddleBot#4998
			{command_prefix}pat
			to pat self
		"""
		if not text:
			return await ctx.send("Nyaa! :3 *{} gives headpats to {}*".format(self.bot.user.name, ctx.author.nick if ctx.author.nick!=None else ctx.author.name))
		if ctx.message.mentions:
			for member in ctx.message.mentions:
				await ctx.send("Nyaa! :3 *{} gives headpats to {}*".format(self.bot.user.name, member.nick if member.nick!=None else member.name))
				return
		else:
			return await ctx.send("Nyaa! :3 *{} gives headpats to {}*".format(self.bot.user.name, text))
			
	
	@commands.command(aliases=["cf"])
	async def coinflip(self, ctx):
		"""Flip a coin"""
		return await ctx.send("The coin landed on {}!".format(random.choice(["heads", "tails"])))
	
	@commands.command(aliases=["aesthetic"])
	async def aesthetics(self, ctx, *, convert):
		"""Converts text to be more  a e s t h e t i c s"""
		wide_map = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))  # Create dict with fixed width equivalents for chars
		wide_map[0x20] = 0x3000  # replace space with 'IDEOGRAPHIC SPACE'
		converted = str(convert).translate(wide_map)
		converted = '{} : {}'.format(ctx.author.nick if ctx.author.nick!=None else ctx.author.name,converted)
		await ctx.send(converted)
		return await ctx.message.delete()

	@commands.command()
	async def roll(self, ctx, *, expression=""):
		"""
		Rolls a die using dice expression format.
		Usage:
			{command_prefix}roll expression
			spaces in expression are ignored
		Example:
			.roll 2d20h1 + 7 # Rolls two D20s takes the highest 1, then adds 7
			.help roll #will give brief overview of dice expression format

		Dice expression format:
			An expression can consist of many sub expressions added together and then a multiplier at the end to indicate how many times the expression should be rolled.
			Sub expressions can be of many types:
				<number> #add this number to the total
				d<sides> #roll a dice with that many sides and add it to the total
				<n>d<sides> #roll n dice. each of those dice have <sides> number of sides, sum all the dice and add to the total
					add r<number> #reroll any rolls below <number>
					add h<number> #only sum the <number> highest rolls rather than all of them
					add l<number> #only sum the <number> lowest rolls rather than all of them
				x<number> #only use at the end. roll the rest of the expression <number> times(max 10)
		Credit: TBTerra#5677
		"""
		max_rolls = 10
		max_verbose = 10
		max_dice = 1000
		response = ''
		roll_verbose = True
		# sanitise input by removing all spaces, converting to lower case
		expression = expression.lower().replace(' ', '')

		# check end of expression for a 'x<number>'
		parts = expression.split('x', 1)
		times = 1
		if len(parts) == 2:  # if theres a x
			try:  # try and work out the number after the x
				times = int(parts[1])
				if times < 1:  # cant roll less than once
					times = 1
				elif times > max_rolls:  # dont want to lag the bot/spam the chat by rolling hundreds of times
					response += "*Warning:* cannot roll an expression more than {0} times. will roll {0} times rather than {1}.\n".format(max_rolls, times)
					times = max_rolls
			except ValueError:  # probably an input syntax error. safest to just roll once.
				times = 1
				response += "*Warning:* was unable to resolve how many times this command was meant to run. defaulted to once.\n"

		# voodoo magic regex (matches A,dB,AdB,AdBrC and AdBh/lD all at once, and splits them up to be processed)

		m = re.findall('(-?)((?:(\d*)d(\d+))|\d+)(r\d+)?([h,l]{1}\d+)?', parts[0])

		if not m:  # either no arguments, or the expression contained nothing that could be seen as a number or roll
			return await ctx.send("Expression missing. If you are unsure of what the format should be, please use `{}help roll`".format(ctx.prefix),delete_after=15)

		dice = []  # this is the list of all dice sets to be rolled
		# each element of the list is a 5 element list, containing
		# [0] the sign of the set
		# [1] how many dice it has
		# [2] how many sides on each dice
		# [3] what numbers to re-roll
		# [4] and how many to select
		for item in m:
			temp = [0]*5
			temp[0] = 1 if item[0] == '' else -1  # if theres a - at the beginning of the sub expression there needs to be a -1 multiplier applied to the sub expression total
			if 'd' in item[1]:  # if its a dice/set of dice rather than a number
				temp[2] = int(item[3])
				if temp[2] == 0:  # safety check for things like 2d0 + 1 (0 sided dice)
					return await ctx.send("cant roll a zero sided dice",delete_after=5)
				if item[2] == '':  # if its just a dY rather than an XdY
					temp[1] = 1
				else:  # its a XdY type unknown if it has r,h,l modifyers, but they dont matter when sorting out the number and sides of dice
					temp[1] = int(item[2])
					if temp[1] > max_dice:  # if there are an unreasonable number of dice, error out. almost no-one needs to roll 9999d20
						return await ctx.send("I can't do that. (Too many dice to roll, max {})".format(max_dice),delete_after=5)
					if temp[1] > max_verbose and roll_verbose:  # if there is a sub expression that involves lots of rolls then turn off verbose mode
						roll_verbose = False
						response += '*Warning:* large number of rolls detected, will not use verbose rolling.\n'
			else:  # numbers are stored as N, 1 sided dice
				temp[1] = int(item[1])
				temp[2] = 1
			temp[3] = 0 if item[4] == '' else int(item[4][1:])  # if it has a reroll value use that. if not, reroll on 0
			if item[5] == '':  # it has no select requirement
				temp[4] = 0
			else:
				if item[5][0] == 'h':  # select highest use positive select argument
					temp[4] = int(item[5][1:])
				else:  # select lowest so use negative select argument
					temp[4] = -int(item[5][1:])
			dice.append(temp)
		# at this point dice contains everything needed to do a roll. if you saved dice then you could roll it again without having to re-parse everything (possible roll saving feature in future?)
		for i in range(times):
			total = 0
			if times > 1:
				response += 'Roll {}: '.format(i+1)
			else:
				response += 'Rolled: '
			for j, die in enumerate(dice):  # for each dice set in the expression
				if j != 0 and roll_verbose:  # dont need the + before the first element
					response += ' + '
				if die[0] == -1 and roll_verbose:  # all the dice sets will return positive numbers so the sign is set entirely by the sign value (element 0)
					response += '-'
				if die[2] == 1:  # its just a number
					if roll_verbose:
						response += '{}'.format(die[1])
					total += die[0] * die[1]
				else:  # its a dice or set of dice
					if roll_verbose:
						response += '('
					temp = []
					for k in range(die[1]):  # for each dice in number of dice
						t = [0, '']
						t[0] = random.randint(1, die[2])  # roll the dice
						t[1] = '{}'.format(t[0])
						if t[0] <= die[3]:  # if its below or equal to the re-roll value, then re-roll it
							t[0] = random.randint(1, die[2])
							t[1] += '__{}__'.format(t[0])  # underline the re-roll so its clear thats the one to pay attention to
						temp.append(t)

					def take_first(ele):
						return ele[0]

					if die[4] > 0:  # if its selecting highest
						temp.sort(key=take_first, reverse=True)  # sort the rolled dice. highest first
						for k, val in enumerate(temp):
							if k >= die[4]:  # if the position in the sorted list is greater than the number of dice wanted, cross it out, and make it not count towards the total
								val[1] = '~~' + val[1] + '~~'
								val[0] = 0
					if die[4] < 0:  # if its selecting lowest
						temp.sort(key=take_first)
						for k, val in enumerate(temp):  # sort the rolled dice. lowest first
							if k >= -die[4]:  # if the position in the sorted list is greater than the number of dice wanted, cross it out, and make it not count towards the total
								val[1] = '~~' + val[1] + '~~'
								val[0] = 0
					for k, val in enumerate(temp):  # loop through all dice rolled and add them to the total. also print them if in verbose mode
						if roll_verbose:
							response += '{},'.format(val[1])
						total += die[0] * val[0]
					if roll_verbose:
						response = response[:-1] + ')'  # clip the trailing ',' and replace it with a ')'
			if roll_verbose:
				response += ' Totaling: {}'.format(total)
			else:
				response += ' Total: {}'.format(total)
			if i < (times-1):
				response += '\n'
		if len(response)>1800:
			return await ctx.send('I\'m not sure what on earth you\'ve done here, but the rolls post is to long to print. <:facepalmy:263144001777958913>')
		return await ctx.send(response)

def setup(bot):
	bot.add_cog(Fun(bot))