import discord
from discord.ext.commands import bot

class Fun:
	def __init__(self, bot):
		self.bot = bot
	
	@bot.command()
	async def hug(self, ctx, *, member: discord.Member = None):
		"""
		Hugs the mentioned user :3
		Usage:
			{command_prefix}hug @PuddleBot#4998
			{command_prefix}hug
			to hug self
		"""
		if not member:
			return await ctx.send(":blush: *{} hugs {}*".format(self.bot.user.name, ctx.author.nick if ctx.author.nick!=None else ctx.author.name))
		return await ctx.send(":blush: *{} hugs {}*".format(self.bot.user.name, member.nick if member.nick!=None else member.name))

	@bot.command(aliases=["headpat", "pet"])
	async def pat(self, ctx, *, member: discord.Member = None):
		"""
		Gives headpats to the mentioned user :3
		Usage:
			{command_prefix}pat @PuddleBot#4998
			{command_prefix}pat
			to pat self
		"""
		if not member:
			return await ctx.send("Nyaa! :3 *{} gives headpats to {}*".format(self.bot.user.name, ctx.author.nick if ctx.author.nick!=None else ctx.author.name))
		return await ctx.send("Nyaa! :3 *{} gives headpats to {}*".format(self.bot.user.name, member.nick if member.nick!=None else member.name))
	
	@bot.command(aliases=["cf"])
	async def coinflip(self, ctx):
		"""Flip a coin"""
		return await ctx.send("The coin landed on {}!".format(random.choice(["heads", "tails"])))
	
	@bot.command()
	async def aesthetics(self, ctx, *, convert):
		"""Converts text to be more  a e s t h e t i c s"""
		wide_map = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))  # Create dict with fixed width equivalents for chars
		wide_map[0x20] = 0x3000  # replace space with 'IDEOGRAPHIC SPACE'
		converted = str(convert).translate(wide_map)
		return await ctx.send(converted)


def setup(bot):
	bot.add_cog(Fun(bot))