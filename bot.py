import discord
from discord.ext import commands
import json
import cfg

bot = commands.Bot(
	command_prefix=cfg.bot['prefix'],
	description=cfg.bot['description'],
	owner_id=cfg.bot['owner'],
	activity=discord.Game(name=cfg.bot['game'], type=0),
	case_insensitive=True
)

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print("Has nitro: " + str(bot.user.premium))
	print("prefix: {}".format(cfg.bot['prefix']))
	print('------')

@bot.event
async def on_message(message):
	if len(message.content) <= 1:#embeds or single char
		return
	if message.content[len(cfg.bot['prefix'])] == cfg.bot['prefix'][0]:
		return
	return await bot.process_commands(message)

if __name__ == "__main__":
	for cog in cfg.cogs:
		cogName = 'cogs.{}'.format(cog)
		print('loading: {}'.format(cogName))
		bot.load_extension(cogName)
	bot.run(cfg.bot['token'], bot=True, reconnect=True)