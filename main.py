import os
import discord
from discord.ext import commands
import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
notes = {}  # format: {user_id: {category: [note1, note2,...]}}

@bot.command()
async def help(ctx):
    await ctx.send('''
    **!add <category> <note>** - Add a note to a category
    **!view** - View all your notes
    **!view_category <category>** - View notes from a specific category
    **!delete <category> <number>** - Delete a note from a category
    **!edit <category> <number> <new_note>** - Edit a note from a category
    **!search <keyword>** - Search for a keyword in all your notes
    '''
    )

@bot.command()
async def add(ctx, category: str, *, note: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    note = f"{timestamp}: {note}"
    if ctx.message.author.id not in notes:
        notes[ctx.message.author.id] = {}
    if category not in notes[ctx.message.author.id]:
        notes[ctx.message.author.id][category] = []
    notes[ctx.message.author.id][category].append(note)
    await ctx.send('Note added to the category!')

@bot.command()
async def view(ctx):
    if ctx.message.author.id in notes and len(notes[ctx.message.author.id]) > 0:
        for category, notes_list in notes[ctx.message.author.id].items():
            await ctx.send(f'{category}:\n' + '\n'.join(notes_list))
    else:
        await ctx.send('You have no notes.')

@bot.command()
async def view_category(ctx, category: str):
    if ctx.message.author.id in notes and category in notes[ctx.message.author.id]:
        await ctx.send('\n'.join(notes[ctx.message.author.id][category]))
    else:
        await ctx.send('No notes in this category.')

@bot.command()
async def delete(ctx, category: str, number: int):
    if ctx.message.author.id in notes and category in notes[ctx.message.author.id] and len(notes[ctx.message.author.id][category]) >= number:
        deleted_note = notes[ctx.message.author.id][category].pop(number - 1)
        await ctx.send(f'Deleted note: {deleted_note}')
    else:
        await ctx.send('Could not find note to delete. Make sure you have entered the correct note number.')

@bot.command()
async def edit(ctx, category: str, number: int, *, new_note: str):
    if ctx.message.author.id in notes and category in notes[ctx.message.author.id] and len(notes[ctx.message.author.id][category]) >= number:
        notes[ctx.message.author.id][category][number - 1] = new_note
        await ctx.send('Note updated!')
    else:
        await ctx.send('Could not find note to edit. Make sure you have entered the correct note number.')

@bot.command()
async def search(ctx, keyword: str):
    if ctx.message.author.id in notes and len(notes[ctx.message.author.id]) > 0:
        found = False
        for category, notes_list in notes[ctx.message.author.id].items():
            matches = [note for note in notes_list if keyword.lower() in note.lower()]
            if matches:
                found = True
                await ctx.send(f'{category}:\n' + '\n'.join(matches))
        if not found:
            await ctx.send('No matching notes found.')
    else:
        await ctx.send('You have no notes.')
    
bot.run(os.environ["DISCORD_TOKEN"])
               
