import discord
from discord.ext.commands import group
from discord.ext import commands
import asyncio
import requests
import cfg
import json
import re
import time

makeNull = re.compile('[,.?!"\';:&]|<b>|</b>|<i>|</i>')
nameNull = re.compile('[,.?!"\';:&]|\(.*\)')
makeSpace = {'\n','  ','  '}## th replacing double space with space, twice is to remove multi spaces where there was a situation of [space][punctuation][space]

def stipPunc(t):
	t=t.lower()
	t=makeNull.sub('', t)
	for c in makeSpace:#this is slow
		t=t.replace(c,' ')
	return t
	
def stripName(t):
	t=t.lower()
	t=nameNull.sub('', t)
	t=t.replace('  ',' ')
	return t

class Rain:
	def __init__(self, bot):
		self.bot = bot
		try:
			with open('pages.json') as f:
				self.ref = json.load(f)
		except:
			self.ref = []
		self.makeIndexs()
	
	def makeIndexs(self):
		self.dex = {'DA':{},'CF':{},'SJ':{}}
		for i,page in enumerate(self.ref):
			if 'CF page' in page:
				self.dex['CF'][page['CF page']] = i
			if 'SJ page' in page:
				self.dex['SJ'][page['SJ page']] = i
			if 'DA page' in page:
				for j in page['DA page']:
					self.dex['DA'][j] = i
			if 'chars' in page:
				page['chars'] = set(page['chars'])
	
	def genPage(self,i):
		out = ''
		if 'CF page' in self.ref[i]:
			out += 'Comic Fury: http://rain.thecomicseries.com/comics/{}\n'.format(self.ref[i]['CF page'])
		if 'SJ slug' in self.ref[i]:
			out += 'SmackJeeves: http://rainlgbt.smackjeeves.com/comics/{}'.format(self.ref[i]['SJ slug'])
		if 'DA slug' in self.ref[i]:
			out += '\nDeviant art: https://www.deviantart.com/jocelynsamara/art/{}'.format(self.ref[i]['DA slug'])
		return out
		
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
		page = int(page)
		if page in self.dex['CF']:
			output = self.genPage(self.dex['CF'][page])
			em = discord.Embed(title=self.ref[self.dex['CF'][page]]['Page Title'], description=output, colour=cfg.colors['green'])
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
		page = int(page)
		if page in self.dex['SJ']:
			output = self.genPage(self.dex['SJ'][page])
			em = discord.Embed(title=self.ref[self.dex['SJ'][page]]['Page Title'], description=output, colour=cfg.colors['green'])
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
		if page in self.dex['DA']:
			output = self.genPage(self.dex['DA'][page])
			em = discord.Embed(title=self.ref[self.dex['DA'][page]]['DA Title'], description=output, colour=cfg.colors['green'])
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
		if curUpdate in self.dex['CF']:
			index = self.dex['CF'][curUpdate]
			if 'DA slug' in self.ref[index]:
				output += 'Deviant art: https://www.deviantart.com/jocelynsamara/art/' + self.ref[index]['DA slug'] + '\n'
			output += '\nPage list is up to date'
			output = 'Title: {}\n'.format(self.ref[index]['Page Title']) + output
		else:
			output += '\nPage list is out of date by {} updates'.format(curUpdate-len(self.dex['CF']))
		em = discord.Embed(title="Latest Page", description=output, colour=cfg.colors['green'])
		return await ctx.send(embed=em)

	@rain.command()
	async def search(self, ctx, *, Query):
		startTime = time.perf_counter()
		inQuotes=False
		i=0
		terms = []
		startI=0
		while i<len(Query):
			if Query[i]=='\\':
				i+=2
				continue
			if Query[i]=='"':
				if inQuotes:
					inQuotes=False
				else:
					inQuotes=True
			if Query[i]==' ' and not inQuotes:
				#this is both an end of term and a start(if )
				if startI<i:
					terms.append(Query[startI:i])
				startI=i+1
			i+=1
		if startI<i:
			terms.append(Query[startI:i])
		Cquery = set()
		Tquery = []
		for term in terms:
			if term[0]=='-':
				Cquery.add(stripName(term[1:]))
			else:
				Tquery.append(stipPunc(term))
		print(Cquery,Tquery)
		results = []
		for j, page in enumerate(self.ref):
			if Cquery:#char search first as its fast
				if 'chars' not in page:
					continue
				if not Cquery.issubset(page['chars']):
					continue
			good=True
			if Tquery:#word search
				if 'text' not in page:
					continue
				for phrase in Tquery:
					if phrase not in page['text']:
						good=False
						break
			if good:
				results.append(j)
		output=[]
		if len(results) > 10:
			output.append('Too many pages to list')
		else:
			for result in results:
				output.append(' http://rain.thecomicseries.com/comics/{}'.format(self.ref[result]['CF page']))
		stopTime = time.perf_counter()
		em = discord.Embed(title='found {} results, in {}ms'.format(len(results),int((stopTime-startTime)*1000)), description='\n'.join(output), colour=cfg.colors['green'])
		return await ctx.send(embed=em)

	@rain.command()
	@commands.is_owner()
	async def update(self, ctx):
		"""Reload the page list without needing to restart the bot (bot owner only)"""
		try:
			with open('pages.json') as f:
				self.ref = json.load(f)
				resp = 'Updated sucsessfuly.'
				return await ctx.send()
		except:
			self.ref = []
			resp = 'Failed to update.'
		self.makeIndexs()
		return await ctx.send(resp)

def setup(bot):
	bot.add_cog(Rain(bot))