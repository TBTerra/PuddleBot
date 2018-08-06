import discord
from discord.ext.commands import group
from discord.ext.commands import bot
from discord.ext import commands
import requests
import cfg
import json


class Guess:
	def __init__(self, bot):
		self.bot = bot
		#load gamestate
		try:
			with open('guess-state.json') as f:
				self.state = json.load(f)
			with open('guess-data/pages.json') as f:
				self.pages = json.load(f)
		except:
			print('no game state, making blank one')
			self.state = {'curImg':0,'lastTime':0,'posX':-1, 'posY':-1, 'hintLV':0}

	def newPage(ctx):
		##choose a new page
		##choose cropping
		##generate crop
		##update/save gamestate
		##output new hint
		return await ctx.send('Not yet implimented',delete_after=10)
		
	def correct(ctx):
		##generate image with hint area highlighted
		##output that
		await ctx.send('Not yet implimented',delete_after=10)
		##make a new hint
		return newPage(ctx)
		
	
	@group(pass_context=True)
	async def guess(self, ctx):
		"""A group of commands for the Comic Guess Game. use {prefix}help guess for more details"""
		if ctx.invoked_subcommand is None:
			return await ctx.send('No sub-command recognised. use {prefix}help guess to see avalable sub-commands',delete_after=10)

	@guess.command()
	async def hint(self, ctx):
		"""Gives a larger hint for the current page (only works after 5 mins)"""
		##check if its been 5 mins
		##make a bigger hint of the current page
		return await ctx.send('Not yet implimented',delete_after=10)

	@guess.command()
	async def skip(self, ctx):
		"""Skip to the next random page (only works after 1 hour)"""
		##check if its been 1 hour
		##make a new page
		return await ctx.send('Not yet implimented',delete_after=10)

	@guess.command(aliases=["cur"])
	async def current(self, ctx):
		"""Gives the current hint for the current page"""
		return await ctx.send('Not yet implimented',delete_after=10)

	@guess.command()
	async def da(self, ctx, *, page):
		"""Make a guess at the current page using a DA page number"""
		return await ctx.send('Not yet implimented',delete_after=10)

	@guess.command()
	async def cf(self, ctx, *, page):
		"""Make a guess at the current page using a CF page number"""
		return await ctx.send('Not yet implimented',delete_after=10)

	@guess.command()
	async def sj(self, ctx, *, page):
		"""Make a guess at the current page using a SJ page number"""
		return await ctx.send('Not yet implimented',delete_after=10)

def setup(bot):
	bot.add_cog(Guess(bot))