import discord

from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    if message.author == client.user:
        return

    # if message.content.startswith('$hello'):
    await message.channel.send('Hello!')
        
client.run(DISCORD_TOKEN)