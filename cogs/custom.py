import discord
from discord.ext.commands import group
from discord.ext.commands import RoleConverter
from discord.ext import commands
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
			self.cc = [{},{}]
			print('no custom command list, making blank one')
	
	def user_has_power(ctx):
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
		if message.author.bot:
			return
		msg = message.content.lower()
		if msg.startswith(self.bot.command_prefix):
			msg = msg[len(self.bot.command_prefix):]
			if msg in self.cc[1]:
				if "{}" in self.cc[1][msg]:
					return await message.channel.send(self.cc[1][msg].format(message.author.display_name))
				else:
					return await message.channel.send(self.cc[1][msg])
		else:
			if msg in self.cc[0]:
				if "{}" in self.cc[0][msg]:
					return await message.channel.send(self.cc[0][msg].format(message.author.display_name))
				else:
					return await message.channel.send(self.cc[0][msg])
		return
	
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			if ctx.message.content[len(self.bot.command_prefix):] in self.cc[1]:
				return
			else:
				print('{} does not exist as a command'.format(ctx.message.content[len(self.bot.command_prefix):]))
				return
		raise error
	
	@group(pass_context=True, aliases=["cc"])
	async def custom(self, ctx):
		"""A group of commands to manage custom commands for your server."""
		if ctx.invoked_subcommand is None:
			return await ctx.send('Missing Argument')
	
	@custom.command()
	@commands.check(user_has_power)
	async def add(self, ctx, command, *, output):
		"""
		add a custom command (needs privilege)
		Usage:
			{command_prefix}custom add test This as a test command.
			will add the command 'test' with the reply of 'This as a test command.'
			adding a 0 to the end of the command will mean it does not require a prefix
		"""
		command = command.lower()
		prefix = 1
		if output[-1:] == '0':
			prefix = 0
			output = output[:-1]
		
		if ctx.message.mention_everyone:
			em = discord.Embed(title="Error", description="Custom Commands cannot mention everyone.", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)
		elif len(output) > 1800:
			em = discord.Embed(title="Error", description="The output is too long", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)
		elif command in self.bot.commands and prefix==1:
			em = discord.Embed(title="Error", description="This is already the name of a built in command.", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)
		elif command in self.cc[0] or command in self.cc[1]:
			em = discord.Embed(title="Error", description="Custom Command already exists. Use edit to change it, not add.", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)
		##add the command to the custom list, then save the custom list
		self.cc[prefix][command] = output
		with open('cc.json','w') as f:
			json.dump(self.cc,f)
		em = discord.Embed(title="Done", description='{} has been added as a command'.format(command), colour=cfg.colors['green'])
		return await ctx.send(embed=em)
	
	@custom.command()
	@commands.check(user_has_power)
	async def edit(self, ctx, command, *, output):
		"""
		edit a custom command (needs privilege)
		Usage:
			{command_prefix}custom edit test This as a test command.
			will edit the command 'test' and change its reply to 'This as a test command.'
		"""
		if ctx.message.mention_everyone:
			em = discord.Embed(title="Error", description="Custom Commands cannot mention everyone.", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)
		elif len(output) > 1800:
			em = discord.Embed(title="Error", description="The output is too long", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)
		elif command in self.bot.commands:
			em = discord.Embed(title="Error", description="This is already the name of a built in command.", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)
		elif command not in self.cc[0] and command not in self.cc[1]:
			em = discord.Embed(title="Error", description="Custom Command does not exist. Use add not edit.", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)
		##add the command to the custom list, then save the custom list
		if command in self.cc[0]:
			self.cc[0][command] = output
		if command in self.cc[1]:
			self.cc[1][command] = output
		with open('cc.json','w') as f:
			json.dump(self.cc,f)
		em = discord.Embed(title="Done", description='{} has been updated'.format(command), colour=cfg.colors['green'])
		return await ctx.send(embed=em)
	
	@custom.command()
	@commands.check(user_has_power)
	async def remove(self, ctx, command):
		"""
		delete a custom command (needs privilege)
		Usage:
			{command_prefix}custom remove test
			will remove the command 'test'
		"""
		if command not in self.cc[0] and command not in self.cc[1]:
			em = discord.Embed(title="Error", description="Custom Command does not exist.\nHow am I supposed to remove it", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)
		##remove the command from the custom list, then save the custom list
		if command in self.cc[0]:
			del self.cc[0][command]
		if command in self.cc[1]:
			del self.cc[1][command]
		with open('cc.json','w') as f:
			json.dump(self.cc,f)
		em = discord.Embed(title="Done", description='{} has been removed'.format(command), colour=cfg.colors['green'])
		return await ctx.send(embed=em)
	
	@custom.command()
	async def list(self, ctx):
		list = 'Comands with prefix:\n'
		for key in self.cc[1].keys():
			list += '{}\n'.format(key)
		list += 'Comands without prefix:\n'
		for key in self.cc[0].keys():
			list += '{}\n'.format(key)
		list=list[:-1]
		em = discord.Embed(title="Custom Command list", description=list, colour=cfg.colors['blue'])
		return await ctx.send(embed=em)
	
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
	async def say(self, ctx, *, convert):
		await ctx.send(convert)
		return await ctx.message.delete()

def setup(bot):
	bot.add_cog(Custom(bot))