import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
notes = {}

@bot.command()
async def add(ctx, *, note: str):
    if ctx.message.author.id not in notes:
        notes[ctx.message.author.id] = []
    notes[ctx.message.author.id].append(note)
    await ctx.send('Note added!')

@bot.command()
async def view(ctx):
    if ctx.message.author.id in notes and len(notes[ctx.message.author.id]) > 0:
        await ctx.send('\n'.join(notes[ctx.message.author.id]))
    else:
        await ctx.send('You have no notes.')

@bot.command()
async def delete(ctx, number: int):
    if ctx.message.author.id in notes and len(notes[ctx.message.author.id]) >= number:
        deleted_note = notes[ctx.message.author.id].pop(number - 1)
        await ctx.send(f'Deleted note: {deleted_note}')
    else:
        await ctx.send('Could not find note to delete. Make sure you have entered the correct note number.')


bot.run(os.environ["DISCORD_TOKEN"])
