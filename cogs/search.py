import requests
import json
import random
import discord
from discord.ext.commands import bot
import cfg

class Search:
	def __init__(self, bot):
		self.bot = bot
	
	@bot.command()
	async def img(self, ctx, *, search):
		"""
		Gets an image based on search
		Uses duckduckgo, returns a random image from the first page of results
		Usage:
			{command_prefix}img cute dogs
		"""
		r = requests.post('https://duckduckgo.com/', data={'q': search})
		html = r.content
		start = html.find(b'vqd=\'')
		stop = html.find(b'\'',start+7)
		vqd = html[start+5:stop]
		print(vqd)
		params = (('l', 'wt-wt'),('o', 'json'),('q', search),('vqd', vqd),('f', ',,,'),('p', '1'))
		headers = {
			'accept-encoding': 'gzip, deflate, br',
			'x-requested-with': 'XMLHttpRequest',
			'accept-language': 'en,en-US;q=0.9,de;q=0.8',
			'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
			'accept': 'application/json, text/javascript, */*; q=0.01',
			'referer': 'https://duckduckgo.com/',
			'authority': 'duckduckgo.com',
			'scheme': 'https'
		}
		requestUrl = 'https://duckduckgo.com/i.js'
		r = requests.get(requestUrl, headers=headers, params=params)
		data = json.loads(r.text)
		url = (random.choice(data['results']))['image']
		print(url)
		em = discord.Embed(title="Image search for: {}".format(search), description='{}\n{}'.format(ctx.author.nick if ctx.author.nick!=None else ctx.author.name,url), colour=cfg.colors['green'])
		em.set_image(url=url)
		em.set_thumbnail(url='https://duckduckgo.com/assets/logo_header.v107.min.png')
		return await ctx.send(embed=em)
	
	@bot.command()
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
		return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nSomething went wrong'.format(ctx.author.nick if ctx.author.nick!=None else ctx.author.name))

def setup(bot):
	bot.add_cog(Search(bot))