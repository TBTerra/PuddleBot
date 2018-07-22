import json

with open('config.json') as f:
	config = json.load(f)

bot = config['bot']
cogs = config['cogs']
colors = config['colors']

def savecfg():
	config['bot'] = bot
	config['cogs'] = cogs
	config['colors'] = colors
	with open('config.json','w') as f:
		json.dump(config,f, indent=4, separators=(',', ': '))