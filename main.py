import discord
from discord.ext import commands
import os
import music
from keep_alive import keep_alive


cogs = [music]

client = commands.Bot(command_prefix='!', intents = discord.Intents.all())

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  for i in range(len(cogs)):
    await cogs[i].setup(client)

@client.event
async def on_command(ctx):
  if ctx.command is None:
    ctx.channel.send('This is not an existing command!')

@client.command()
async def stupid(ctx, *, arg):
  await ctx.channel.send("I'm stupid")

keep_alive()
client.run(os.getenv('Token'))