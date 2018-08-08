import discord
from discord.ext.commands import group
from discord.ext.commands import bot
from discord.ext import commands
import json
import random
import time
from PIL import Image, ImageDraw

class Guess:
	def __init__(self, bot):
		self.bot = bot
		#load gamestate
		with open('guess-data/pages.json') as f:
			self.pages = json.load(f)
		try:
			with open('guess-state.json') as f:
				self.state = json.load(f)
		except:
			print('no game state, making blank one')
			self.state = {'curImg':0,'lastTime':0,'posX':-1, 'posY':-1, 'hintLV':0}

	async def newPage(self,ctx):
		##choose a new page
		imgNum = random.randint(0, len(self.pages)-1)
		imgName = 'guess-data/{:04d}.png'.format(int(self.pages[imgNum][0][3:]))
		try:
			original = Image.open(imgName)
		except:
			print('Unable to load image {}'.format(imgName))
			return await ctx.send('Something went wrong, ask Terra to look at the logs',delete_after=10)
		##choose cropping
		X = random.randint(75,original.size[0]-75)
		Y = random.randint(75,original.size[1]-75)
		##generate crop
		original.crop((X-75,Y-75,X+76,Y+76)).save("hint.png")
		##update/save gamestate
		self.state = {'curImg':imgNum,'lastTime':time.time(),'posX':X, 'posY':Y, 'hintLV':0}
		with open('guess-state.json','w') as f:
			json.dump(self.state,f)
		##output new hint
		return await ctx.send('New Hint:', file=discord.File('hint.png'))
		
	async def Correct(self,ctx):
		##generate image with hint area highlighted
		imgName = 'guess-data/{:04d}.png'.format(int(self.pages[self.state['curImg']][0][3:]))
		try:
			original = Image.open(imgName)
			draw = ImageDraw.Draw(original)
			X = self.state['posX']
			Y = self.state['posY']
			draw.rectangle((X-(75+self.state['hintLV']),Y-(75+self.state['hintLV']),X+(76+self.state['hintLV']),Y+(76+self.state['hintLV'])),outline = '#CC0000')
			original.save('overlay.png')
			##output that
			await ctx.send('That is correct',file=discord.File('overlay.png'))
		except:
			await ctx.send('That is correct\nError unable to do overlay image')
		##make a new hint
		return await Guess.newPage(self,ctx)
	
	@group(pass_context=True)
	async def guess(self, ctx):
		"""A group of commands for the Comic Guess Game. use {prefix}help guess for more details"""
		if ctx.invoked_subcommand is None:
			return await ctx.send('No sub-command recognised. use {prefix}help guess to see avalable sub-commands',delete_after=10)

	@guess.command()
	async def hint(self, ctx):
		"""Gives a larger hint for the current page (only works after 5 mins)"""
		##check if its been 5 mins
		if (time.time()-self.state['lastTime']) >= 300:
			self.state['hintLV'] += 25
			self.state['lastTime'] = time.time()
			with open('guess-state.json','w') as f:
				json.dump(self.state,f)
			##make a bigger hint of the current page
			imgName = 'guess-data/{:04d}.png'.format(int(self.pages[self.state['curImg']][0][3:]))
			original = Image.open(imgName)
			##generate crop
			X = self.state['posX']
			Y = self.state['posY']
			original.crop((X-(75+self.state['hintLV']),Y-(75+self.state['hintLV']),X+(76+self.state['hintLV']),Y+(76+self.state['hintLV']))).save("hint.png")
			##output new hint
			return await ctx.send('New Hint:', file=discord.File('hint.png'))
		else:
			return await ctx.send('It hasnt been 5 minutes, can\'t get a hint yet\ntime remaining ({} seconds)'.format(int(300-(time.time()-self.state['lastTime']))))
	@guess.command()
	async def skip(self, ctx):
		"""Skip to the next random page (only works after 1 hour)"""
		##check if its been 1 hour
		if (time.time()-self.state['lastTime']) >= 3600:
			##make a new page
			return await Guess.newPage(self,ctx)
		else:
			return await ctx.send('It hasnt been an hour, can\'t skip yet\ntime remaining ({} seconds)'.format(int(3600-(time.time()-self.state['lastTime']))))

	@guess.command(aliases=["cur"])
	async def current(self, ctx):
		"""Gives the current hint for the current page"""
		return await ctx.send('Current Hint:', file=discord.File('hint.png'))

	@guess.command()
	async def da(self, ctx, *, page):
		"""Make a guess at the current page using a DA page number"""
		try:
			num = int(page)
		except:
			return await ctx.send('Expecting a page number for the guess',delete_after=10)
		gess = 'da {}'.format(num)
		if gess in self.pages[self.state['curImg']]:
			return await Guess.Correct(self,ctx)
		else:
			return await ctx.send('Thats not correct',delete_after=10)

	@guess.command()
	async def cf(self, ctx, *, page):
		"""Make a guess at the current page using a CF page number"""
		try:
			num = int(page)
		except:
			return await ctx.send('Expecting a page number for the guess',delete_after=10)
		gess = 'cf {}'.format(num)
		if gess in self.pages[self.state['curImg']]:
			return await Guess.Correct(self,ctx)
		else:
			return await ctx.send('Thats not correct',delete_after=10)

	@guess.command()
	async def sj(self, ctx, *, page):
		"""Make a guess at the current page using a SJ page number"""
		try:
			num = int(page)
		except:
			return await ctx.send('Expecting a page number for the guess',delete_after=10)
		gess = 'sj {}'.format(num)
		if gess in self.pages[self.state['curImg']]:
			return await Guess.Correct(self,ctx)
		else:
			return await ctx.send('Thats not correct',delete_after=10)

def setup(bot):
	bot.add_cog(Guess(bot))