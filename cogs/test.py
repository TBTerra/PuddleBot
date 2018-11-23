import discord
from discord.ext import commands
import cfg

class Test:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def say(self, ctx, *, text):
		return await ctx.send('{}: {}'.format(ctx.author.display_name,text))
	
	@commands.command()
	async def yes(self, ctx):
		em = discord.Embed(title="Indeed", description='I agree', colour=cfg.colors['green'])
		return await ctx.send(embed=em)
	
	@commands.command()
	async def no(self, ctx):
		em = discord.Embed(title="No way", description='I disagree', colour=cfg.colors['red'])
		return await ctx.send(embed=em)

def setup(bot):
	bot.add_cog(Test(bot))