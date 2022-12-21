import discord
from discord.ext.pages import Paginator, Page

from config import DISCORD_TOKEN
from qbit import get_torrents, TorrentStatus



class MyView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vanilla",
                description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!"
            )
        ]
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")

def get_client():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    return client


client = get_client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    if message.author == client.user:
        return

    await send_download_status(message)    

@client.event
async def send_download_status(message, num_downloads=10):
    # await message.channel.send('Hello!')
    # await message.channel.send("Choose a flavor!", view=MyView())
    torrents = get_torrents()
    embeds = []

    import sys

    print(sys.executable)
    
    for torrent in torrents[:min(num_downloads, len(torrents))]:
        embed = create_torrent_embed(torrent)
        embeds.append(embed)

    await message.channel.send(embeds=embeds)


def create_torrent_embed(torrent):
    user = client.user

    embed = discord.Embed(
        title=torrent.name,
        fields=[
            discord.EmbedField(
                name=torrent.get_status_str(),
                # ▏▏▎▎▍▍▌▌▌▋▋▊▊▊▉
                value=f"▰▰▰▰▰▰▰▰▰▰▱▱▱ 100%\ncompleted on {torrent.completed_on}",
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