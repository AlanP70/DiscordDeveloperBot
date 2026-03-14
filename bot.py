import discord
import requests
import json

from discord.ext import commands
from discord import app_commands

class MyClient(commands.Bot):
    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)

    async def on_ready (self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
    
        if message.content.startswith('hello'):
            await message.channel.send(f'Hey {message.author.mention}!')
    
    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send('You reacted!')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(command_prefix = '!', intents=intents)

GUILD_ID = discord.Object(id=819404306166841384)

@client.tree.command(name="hello", description="Say Hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")

client.run('')

    