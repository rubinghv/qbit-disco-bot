import discord
from discord.ext.pages import Paginator, Page
from discord.ext import tasks
from datetime import datetime

from util import get_progress_bar
from config import DISCORD_TOKEN, DISCORD_CHANNEL_ID, BOT_UPDATE_INTERVAL_SECONDS
from qbit import get_torrents, TorrentStatus

def get_client():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    return client


client = get_client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(DISCORD_CHANNEL_ID)

    # if there is no message to edit, create one
    if len(await channel.history(limit=1).flatten()) == 0:
        await channel.send("Getting ready...")

    update_downloads.start()


@tasks.loop(seconds=BOT_UPDATE_INTERVAL_SECONDS)
async def update_downloads():
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    message = (await channel.history(limit=1).flatten())[0]
    await edit_download_status(message)


@client.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    if message.author == client.user:
        return


@client.event
async def edit_download_status(message, num_downloads=10):
    torrents = get_torrents()
    embeds = []
    
    for torrent in torrents[:min(num_downloads, len(torrents))]:
        embed = create_torrent_embed(torrent)
        embeds.append(embed)

    await message.edit(f'Last updated at: {datetime.now()}', embeds=embeds)


def create_torrent_embed(torrent):
    user = client.user
    status_str =f"""{get_progress_bar(torrent.progress)} {torrent.get_progress_str()}%
{torrent.get_full_status_str()}"""

    embed = discord.Embed(
        title=torrent.name,
        fields=[
            discord.EmbedField(
                name=torrent.get_status_str(),
                value=status_str,
                inline=False,
            ),  

        ],
        timestamp=torrent.added_on,
        # footer= text="This user is not in this server.")

        # set color to match status of download
        #embed.colour = 
        description=f'💾 {torrent.get_size_str()}',
        color = torrent.get_status_color()
    )

    embed.set_footer(text="Added on")

    # embed.set_author(name=user.name)
    # embed.set_thumbnail(url=user.display_avatar.url)
    return embed

client.run(DISCORD_TOKEN)