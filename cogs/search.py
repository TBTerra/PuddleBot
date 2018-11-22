import requests
import json
import random
import discord
import xml.etree.ElementTree as ET
import urllib
from discord.ext import commands
import cfg

class Search:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def img(self, ctx, *, search):
		"""
		Gets an image based on search
		Uses Google, returns first result
		Usage:
			{command_prefix}img cute dogs
		"""
		saniSearch = search.replace(' ','+')
		r = requests.get('https://www.googleapis.com/customsearch/v1?q={}&cx=010484447505514448994%3Ahdizm3skfck&num=1&safe=active&searchType=image&key={}'.format(saniSearch,cfg.bot['img-api']))
		data = json.loads(r.text)
		url = data['items'][0]['link']
		print(url)
		em = discord.Embed(title="Image search for: {}".format(saniSearch), description='{}\n{}'.format(ctx.author.nick if ctx.author.nick!=None else ctx.author.name,url), colour=cfg.colors['green'])
		em.set_image(url=url)
		return await ctx.send(embed=em)
	
	@commands.command()
	async def yt(self, ctx, *, search):
		"""
		Gets a youtube video based on search
		Usage:
			{command_prefix}yt cute dogs
		"""
		r = requests.get('https://www.googleapis.com/youtube/v3/search/?part=snippet&key={}&q={}'.format(cfg.bot['yt-api'],search))
		data = json.loads(r.text)
		for item in data['items']:
			if item['id']['kind'] == 'youtube#video':
				return await ctx.send('https://www.youtube.com/watch?v={}'.format(item['id']['videoId']))
		return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nSomething went wrong'.format(ctx.author.display_name),delete_after=5)
	
	@commands.command()
	async def wa(self, ctx, *, search):
		"""
		Runs a query trough WolframAlpha
		Usage:
			{command_prefix}wa 110kph in imperial
		"""
		r = requests.get('http://api.wolframalpha.com/v2/query?{}'.format(urllib.parse.urlencode({'appid': cfg.bot['wa-api'], 'input': search})))
		root = ET.fromstring(r.text)
		primaryPod = None
		for pod in root.iter('pod'):
			try:
				if pod.attrib['primary'] == 'true':
					primaryPod = pod
					break
			except:
				pass
		if primaryPod:
			plaintext = []
			for ptEl in primaryPod.iter('plaintext'):
				plaintext.append(ptEl.text)
			return await ctx.send('**Result:**\n'+'\n\n'.join(plaintext))
		return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nSomething went wrong'.format(ctx.author.nick if ctx.author.nick!=None else ctx.author.name),delete_after=5)

def setup(bot):
	bot.add_cog(Search(bot))