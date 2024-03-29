import discord
from discord.ext.commands import group
from discord.ext.commands import RoleConverter
from discord.ext import commands
import random
import cfg
import json

class Custom(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		#load custom command list
		try:
			with open('cc.json') as f:
				self.cc = json.load(f)
		except:
			self.cc = [{},{},{}]
			print('no custom command list, making blank one')
	
	def user_has_power(ctx):
		if ctx.message.author.id == cfg.bot['owner']: return True
		#get the role with the right ID
		for role in ctx.guild.roles:
			if role.id == cfg.bot['power-role']:
				if ctx.message.author.top_role >= role:
					return True
		return False

	def stripPunc(self,text):
		#out = ''
		#for chr in text:
		#	if chr not in {'.',',','?',':',';','\'','\"','!'}:
		#		out = out + chr
		#return out
		a=0
		for chr in reversed(text):
			if chr in {'.',',','?',':',';','\'','\"','!'}:
				a += 1
			else:
				break
		if a>0:
			return text[:-a]
		return text
	def stripFormat(self,text):
		format = ''
		#start from be begining and strip chars that can be formating
		for chr in text:
			if chr in {'_','*','|','~'}:
				format = format + chr
			else:
				break
		a = len(format)
		if a>0:
			return format, self.stripPunc(text[a:-a])
		else:
			return '', self.stripPunc(text)
	def addFormat(self,owner,msg,format):
		if ';;' in msg:
			choices = msg.split(';;')
			response = random.choice(choices)
		else:
			response = msg
		if '{}' in msg:
			response = response.format(owner.display_name)
		return format + response + format[::-1]
	
	@commands.Cog.listener()
	async def on_message(self,message):
		##if message.author.bot:
		if message.author == self.bot.user:
			return
		msg = message.content.lower()
		if msg.startswith(self.bot.command_prefix):
			msg = msg[len(self.bot.command_prefix):]
			print(msg)
			if msg in self.cc[1]:
				return await message.channel.send(self.addFormat(message.author,self.cc[1][msg],''))
			if msg in self.cc[2]:
				if self.cc[2][msg] in self.cc[1]:
					return await message.channel.send(self.addFormat(message.author,self.cc[1][self.cc[2][msg]],''))
				else:
					return await message.channel.send(self.addFormat(message.author,self.cc[2][msg],''))
		else:
			form,msg = self.stripFormat(msg)
			if msg in self.cc[0]:
				return await message.channel.send(self.addFormat(message.author,self.cc[0][msg],form))
		return
	
#	async def on_command_error(self, ctx, error):
#		if isinstance(error, commands.CommandNotFound):
#			cmd = ctx.message.content[len(self.bot.command_prefix):]
#			if cmd in self.cc[1] or cmd in self.cc[2]:
#				return
#			else:
#				print('{} does not exist as a command'.format(ctx.message.content[len(self.bot.command_prefix):]))
#				return
#		raise error
	
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
		if output[-1] == '0':
			prefix = 0
			output = output[:-0].rstrip()
		
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
	async def alias(self, ctx, command, *, output):
		"""
		make an alias for a costom command (needs privilege)
		Usage:
			{command_prefix}custom alias test2 test
			will add the command 'test2' as an alias of the custom command called test.
			if test does not exist, it will add test2 as a hidden command with the response of "test"
			Warning: still in testing, edit and remove may not work on aliased commands
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
		elif command in self.cc[0] or command in self.cc[1]:
			em = discord.Embed(title="Error", description="Custom Command already exists. cant make an alias of the same name.", colour=cfg.colors['red'])
			return await ctx.send(embed=em,delete_after=5)
		##check if its an alias or a hidden command
		self.cc[2][command] = output
		with open('cc.json','w') as f:
			json.dump(self.cc,f)
		em = discord.Embed(title="Done", description='{} has been added.'.format(command), colour=cfg.colors['green'])
		return await ctx.send(embed=em,delete_after=15)
	
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
		list = 'Comands with prefix:\n```'
		for key in self.cc[1].keys():
			list += '{}\n'.format(key)
		list = list[:-1] + '```\nComands without prefix:\n```'
		for key in self.cc[0].keys():
			list += '{}\n'.format(key)
		list = list[:-1] + '```'
		return await ctx.send(list)
	
	@commands.command()
	@commands.check(user_has_power)
	async def clear(self, ctx, num:int=1):
		async for m in ctx.channel.history(limit=(num+1)):
			await m.delete()
		return await ctx.send('cleared {} messages'.format(num))

def setup(bot):
	bot.add_cog(Custom(bot))