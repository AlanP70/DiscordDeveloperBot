import discord
import requests
import json
import os
import logging

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = '!', intents=intents)

member_role = "Member"

@bot.event
async def on_ready ():
        print(f'Logged on as {bot.user}!')
    
@bot.event
async def on_member_join(member):
        await member.send(f"Welcome to the server {member.name}!")

@bot.event
async def on_message(message):
        if message.author == bot.user:
            return
    
        if message.content.startswith('hello'):
            await message.channel.send(f'Hey {message.author.mention}!')

        await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

@bot.command()
async def assign_role(ctx):
    role = discord.utils.get(ctx.guild.roles, name=member_role)
    if role: 
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {role.name}!")
    else:
        await ctx.send("Role not found.")

@bot.command()
async def remove_role(ctx):
    role = discord.utils.get(ctx.guild.roles, name=member_role)
    if role: 
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} is now removed from {role.name}!")
    else:
        await ctx.send("Role not found.")

@bot.command()
async def dm(ctx, *, message):
    await ctx.author.send(message)

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(member_role)
async def member(ctx):
    await ctx.send(f"Welcome to the members")

@member.error
async def member_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You dont have permission to access this command.")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

    