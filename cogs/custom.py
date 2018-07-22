import discord
from discord.ext.commands import group
from discord.ext.commands import bot
from discord.ext.commands import RoleConverter
import cfg
import json

class Custom:
	def __init__(self, bot):
		self.bot = bot
		#load custom command list
		try:
			with open('cc.json') as f:
				self.cc = json.load(f)
		except:
			self.cc = {}
	
	def user_has_power(self,ctx):
		if ctx.message.author.id == cfg.bot['owner']: return True
		#get the role with the right ID
		for role in ctx.guild.roles:
			if role.id == cfg.bot['power-role']:
				if ctx.message.author.top_role >= role:
					return True
		return False
	
	async def on_message(self,message):
		if message.author == self.bot.user:
			return
		msg = message.content.lower()
		if msg.startswith(self.bot.command_prefix):
			if msg.split(self.bot.command_prefix)[1] in self.cc:
				return await message.channel.send(self.cc[msg.split(self.bot.command_prefix)[1]])
		return
	
	@group(pass_context=True, aliases=["cc"])
	async def custom(self, ctx):
		"""A group of commands to manage custom commands for your server."""
		if ctx.invoked_subcommand is None:
			return await ctx.send('Missing Argument')
	
	@custom.command()
	async def add(self, ctx, command, *, output):
		"""
		add a custom command (needs privilege)
		Usage:
			{command_prefix}custom add test This as a test command.
			will add the command 'test' with the reply of 'This as a test command.'
		"""
		if not self.user_has_power(ctx):
			return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nYou don\'t have permission!'.format(ctx.author.name))
		if ctx.message.mentions or ctx.message.mention_everyone or ctx.message.role_mentions:
			em = discord.Embed(title="Error", description="Custom Commands cannot mention people/roles/everyone.", colour=cfg.colors['red'])
			return await ctx.send(embed=em)
		elif len(output) > 1800:
			em = discord.Embed(title="Error", description="The output is too long", colour=cfg.colors['red'])
			return await ctx.send(embed=em)
		elif command in self.bot.commands:
			em = discord.Embed(title="Error", description="This is already the name of a built in command.", colour=cfg.colors['red'])
			return await ctx.send(embed=em)
		elif command in self.cc:
			em = discord.Embed(title="Error", description="Custom Command already exists. Use edit to change it, not add.", colour=cfg.colors['red'])
			return await ctx.send(embed=em)
		##add the command to the custom list, then save the custom list
		self.cc[command] = output
		with open('cc.json','w') as f:
			json.dump(self.cc,f)
		em = discord.Embed(title="Done", description='{} has been added as a command'.format(command), colour=cfg.colors['green'])
		return await ctx.send(embed=em)
	
	@custom.command()
	async def edit(self, ctx, command, *, output):
		"""
		edit a custom command (needs privilege)
		Usage:
			{command_prefix}custom edit test This as a test command.
			will edit the command 'test' and change its reply to 'This as a test command.'
		"""
		if not self.user_has_power(ctx):
			return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nYou don\'t have permission!'.format(ctx.author.name))
		if ctx.message.mentions or ctx.message.mention_everyone or ctx.message.role_mentions:
			em = discord.Embed(title="Error", description="Custom Commands cannot mention people/roles/everyone.", colour=cfg.colors['red'])
			return await ctx.send(embed=em)
		elif len(output) > 1800:
			em = discord.Embed(title="Error", description="The output is too long", colour=cfg.colors['red'])
			return await ctx.send(embed=em)
		elif command in self.bot.commands:
			em = discord.Embed(title="Error", description="This is already the name of a built in command.", colour=cfg.colors['red'])
			return await ctx.send(embed=em)
		elif command not in self.cc:
			em = discord.Embed(title="Error", description="Custom Command does not exist. Use add not edit.", colour=cfg.colors['red'])
			return await ctx.send(embed=em)
		##add the command to the custom list, then save the custom list
		self.cc[command] = output
		with open('cc.json','w') as f:
			json.dump(self.cc,f)
		em = discord.Embed(title="Done", description='{} has been updated'.format(command), colour=cfg.colors['green'])
		return await ctx.send(embed=em)
	
	@custom.command()
	async def remove(self, ctx, command):
		"""
		delete a custom command (needs privilege)
		Usage:
			{command_prefix}custom remove test
			will remove the command 'test'
		"""
		if not self.user_has_power(ctx):
			return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nYou don\'t have permission!'.format(ctx.author.name))
		if command not in self.cc:
			em = discord.Embed(title="Error", description="Custom Command does not exist.\nHow am I supposed to remove it", colour=cfg.colors['red'])
			return await ctx.send(embed=em)
		##remove the command from the custom list, then save the custom list
		del self.cc[command]
		with open('cc.json','w') as f:
			json.dump(self.cc,f)
		em = discord.Embed(title="Done", description='{} has been removed'.format(command), colour=cfg.colors['green'])
		return await ctx.send(embed=em)
	
	@bot.command()
	async def setpower(self, ctx, *, role: discord.Role = None):
		""""set privilege level (bot owner only)"""
		if ctx.message.author.id != cfg.bot['owner']:
			return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nYou arnt the bot owner!'.format(ctx.author.name))
		if role is None:
			return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nYou haven\'t specified a role!'.format(ctx.author.name))
		if role not in ctx.message.guild.roles:
			return await ctx.send('I\'m sorry {}. I\'m afraid I can\'t do that :confused:\nThat role dosnt exist!'.format(ctx.author.name))
		cfg.bot['power-role'] = role.id
		cfg.savecfg()

def setup(bot):
	bot.add_cog(Custom(bot))