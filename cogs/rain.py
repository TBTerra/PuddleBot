import discord
from discord.ext.commands import group
from discord.ext.commands import bot
from discord.ext import commands
import asyncio
import requests
import cfg
import json

class Rain:
	def __init__(self, bot):
		self.bot = bot
		try:
			with open('rain.json') as f:
				self.lookup = json.load(f)
		except:
			self.lookup = {'DA':{},'CF':{},'SJ':{}}
	
	@group(pass_context=True)
	async def rain(self, ctx):
		"""A group of commands to lookup updates from the rain comic."""
		if ctx.invoked_subcommand is None:
			return await ctx.send('Missing Argument: use `cf (number)` `sf (number)` `da (code)` or `latest`\nAlternatively use {comand prefix}help rain for a more indepth help',delete_after=10)
			
	@rain.command()
	async def cf(self, ctx, *, page):
		"""
		Look up a specified update on comic fury
		Usage:
			{command_prefix}rain cf 1000
			will look for the 1000th update on the comic fury site
		This will only work for pages in the bots page list
		you can use the latest command to check if the list is up to date
		"""
		if page in self.lookup['CF']:
			output = 'Comic Fury: http://rain.thecomicseries.com/comics/{}'.format(page)
			if self.lookup['CF'][page][2] != '':
				output += '\nSmackJeeves: http://rainlgbt.smackjeeves.com/comics/{}'.format(self.lookup['CF'][page][2])
			if self.lookup['CF'][page][3] != '':
				output += '\nDeviant art: https://www.deviantart.com/jocelynsamara/art/{}'.format(self.lookup['CF'][page][3])
			em = discord.Embed(title=self.lookup['CF'][page][0], description=output, colour=cfg.colors['green'])
			return await ctx.send(embed=em)
		else:
			em = discord.Embed(title="Error", description="Unable to find an update with that number", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)
			
	@rain.command()
	async def sj(self, ctx, *, page):
		"""
		Look up a specified update on SmackJeeves
		Usage:
			{command_prefix}rain sj 1000
			will look for the 1000th update on the SmackJeeves site
		This will only work for pages in the bots page list
		you can use the latest command to check if the list is up to date
		"""
		if page in self.lookup['SJ']:
			output = ''
			if self.lookup['SJ'][page][1] != '':
				output += 'Comic Fury: http://rain.thecomicseries.com/comics/{}\n'.format(self.lookup['SJ'][page][1])
			output += 'SmackJeeves: http://rainlgbt.smackjeeves.com/comics/{}'.format(self.lookup['SJ'][page][2])
			if self.lookup['SJ'][page][3] != '':
				output += '\nDeviant art: https://www.deviantart.com/jocelynsamara/art/{}'.format(self.lookup['SJ'][page][3])
			em = discord.Embed(title=self.lookup['SJ'][page][0], description=output, colour=cfg.colors['green'])
			return await ctx.send(embed=em)
		else:
			em = discord.Embed(title="Error", description="Unable to find an update with that number", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)

	@rain.command()
	async def da(self, ctx, *, page):
		"""
		Look up a specified page on Deviant art (page, chapter or numbered rain delay)
		Usage:
			{command_prefix}rain da 1000
			will look for page 1000 based on deviant art's numbering
			{command_prefix}rain da C15
			will look for the title pages for chapter 15
			{command_prefix}rain da RD12
			will look for the 12th of the numbered rain delays
		This will only work for pages in the bots page list
		you can use the latest command to check if the list is up to date
		"""
		if page in self.lookup['DA']:
			output = ''
			if self.lookup['DA'][page][1] != '':
				output += 'Comic Fury: http://rain.thecomicseries.com/comics/{}\n'.format(self.lookup['DA'][page][1])
			if self.lookup['DA'][page][1] != '':
				output += 'SmackJeeves: http://rainlgbt.smackjeeves.com/comics/{}\n'.format(self.lookup['DA'][page][2])
			output += 'Deviant art: https://www.deviantart.com/jocelynsamara/art/{}'.format(self.lookup['DA'][page][3])
			em = discord.Embed(title=self.lookup['DA'][page][0], description=output, colour=cfg.colors['green'])
			return await ctx.send(embed=em)
		else:
			em = discord.Embed(title="Error", description="Unable to find an update with that page code", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)

	@rain.command(aliases=["last","new"])
	async def latest(self, ctx):
		"""Get the latest page of the comic, and check the page list is up to data"""
		r = requests.get('http://rain.thecomicseries.com/comics/')
		if(r.status_code != 200):
			return await ctx.send('Could not find the most recent comic')
		html = r.content
		start = html.find(b'class="heading">Comic ')
		stop = html.find(b' ',start+23)
		curUpdate = int(html[start+22:stop].decode("utf-8"))
		output = 'Comic Fury: http://rain.thecomicseries.com/comics/\nSmackJeeves: http://rainlgbt.smackjeeves.com/comics/\n'
		if curUpdate == len(self.lookup['CF']):
			if self.lookup['CF'][str(curUpdate)][3] != '':
				output += 'Deviant art: https://www.deviantart.com/jocelynsamara/art/' + self.lookup['CF'][str(curUpdate)][3] + '\n'
			output += '\nPage list is up to date'
			output = 'Title: {}\n'.format(self.lookup['CF'][str(curUpdate)][0]) + output
		else:
			output += '\nPage list is out of date by {} updates'.format(curUpdate-len(self.lookup['CF']))
		em = discord.Embed(title="Latest Page", description=output, colour=cfg.colors['green'])
		return await ctx.send(embed=em)

	@rain.command()
	@commands.is_owner()
	async def update(self, ctx):
		"""Reload the page list without needing to restart the bot (bot owner only)"""
		try:
			with open('rain.json') as f:
				self.lookup = json.load(f)
				return await ctx.send('Updated sucsessfuly.')
		except:
			self.lookup = {'DA':{},'CF':{},'SJ':{}}
			return await ctx.send('Failed to update.')

def setup(bot):
	bot.add_cog(Rain(bot))