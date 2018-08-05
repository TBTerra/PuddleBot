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
		except:
			print('no game state, making blank one')
			self.state = {}

	def newPage(ctx):
		return await ctx.send('Not yet implimented',delete_after=10)
		
	def correct(ctx):
		await ctx.send('Not yet implimented',delete_after=10)
		return newPage(ctx)
		
	
	@group(pass_context=True)
	async def guess(self, ctx):
		"""A group of commands for the Comic Guess Game. use {prefix}help guess for more details"""
		if ctx.invoked_subcommand is None:
			return await ctx.send('Not yet implimented',delete_after=10)

	@guess.command()
	async def hint(self, ctx):
		"""Gives a larger hint for the current page (only works after 5 mins)"""
		return await ctx.send('Not yet implimented',delete_after=10)

	@guess.command()
	async def skip(self, ctx):
		"""Skip to the next random page (only works after 1 hour)"""
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