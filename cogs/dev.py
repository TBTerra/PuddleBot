import discord
import cfg
from discord.ext import commands

class Dev:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.is_owner()
	async def setpower(self, ctx, *, role: discord.Role = None):
		""""set privilege level (bot owner only)"""
		if role is None:
			return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nYou haven\'t specified a role!'.format(ctx.author.nick if ctx.author.nick!=None else ctx.author.name),delete_after=5)
		if role not in ctx.message.guild.roles:
			return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nThat role dosnt exist!'.format(ctx.author.nick if ctx.author.nick!=None else ctx.author.name),delete_after=5)
		cfg.bot['power-role'] = role.id
		cfg.savecfg()
	
	@commands.command()
	@commands.is_owner()
	async def role(self, ctx, *, role: discord.Role = None):
		"""grab the ID of the role specified (bot owner only)"""
		if role is None:
			return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nYou haven\'t specified a role!'.format(ctx.author.nick if ctx.author.nick!=None else ctx.author.name),delete_after=5)
		if role not in ctx.message.guild.roles:
			return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nThat role dosnt exist!'.format(ctx.author.nick if ctx.author.nick!=None else ctx.author.name),delete_after=5)
		await ctx.send('That Role has the ID: {} and has {} members'.format(role.id, len(role.members)),delete_after=15)
		return await ctx.message.delete()

	@commands.command()
	@commands.is_owner()
	async def say(self, ctx, *, convert):
		await ctx.send(convert)
		return await ctx.message.delete()

def setup(bot):
	bot.add_cog(Dev(bot))