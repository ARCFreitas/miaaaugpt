import discord
from discord.ext import commands
import re
import logging
import os
from dotenv import load_dotenv

intents = discord.Intents.all()

client = commands.Bot(command_prefix='', intents=intents)

# Load environment variables from .env file
load_dotenv()

# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.event
async def on_ready():
    print('Bot is ready!')

@client.event
async def on_message(message):
    if message.author == client.user or "ddinstagram.com" in message.content:
        return

    instagram_url = re.search("(?P<url>https?://(?:www\.)?instagram\.com/.+)", message.content)
    
    if instagram_url:
        processed_message = re.sub(r'instagram.com', 'ddinstagram.com', message.content)
        try:
            new_message = await message.channel.send(f"{processed_message} - Credits to {message.author.mention}")
            await message.delete()
            await new_message.add_reaction('👀')
        except:
            await message.add_reaction('\u274c')
            
    await client.process_commands(message)

bot_token = os.environ.get('DISCORD_TOKEN')

if bot_token is None:
    raise ValueError('Token not found in environment variables')
  
client.run(bot_token)
