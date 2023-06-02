import os
import discord
from discord.ext import commands
import datetime
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
notes = {}  # format: {user_id: {category: [note1, note2,...]}}

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Note Keeper Bot Help', description='Use the following commands to manage your notes:', color=discord.Color.blue())
    embed.add_field(name='!add [c=<category>] <note>', value='Add a note to a category. If no category is specified, the note will be added without a category.', inline=False)
    embed.add_field(name='!view', value='View all your notes', inline=False)
    embed.add_field(name='!view_category <category>', value='View notes from a specific category', inline=False)
    embed.add_field(name='!delete <category> <number>', value='Delete a note from a category', inline=False)
    embed.add_field(name='!edit <category> <number> <new_note>', value='Edit a note from a category', inline=False)
    embed.add_field(name='!search <keyword>', value='Search for a keyword in all your notes', inline=False)
    embed.add_field(name='!remind <category> <number> <duration>', value='Set a reminder for a note', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def add(ctx, category_or_note: str = None, *, note: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    note = f"{timestamp}: {note}"
    user_notes = notes.setdefault(ctx.message.author.id, {})
    if category_or_note and category_or_note.startswith("c="):
        category = category_or_note[2:]
        user_notes.setdefault(category, []).append(note)
        await ctx.send('Note added to the category!')
    else:
        category = 'Uncategorized'
        user_notes.setdefault(category, []).append(note)
        await ctx.send('Note added without a category!')

@bot.command()
async def view(ctx):
    user_notes = notes.get(ctx.message.author.id)
    if user_notes:
        embed = discord.Embed(title='Your Notes', color=discord.Color.green())
        for category, notes_list in user_notes.items():
            formatted_notes = '\n'.join([f'Note {i}: {note}' for i, note in enumerate(notes_list, 1)])
            embed.add_field(name=f'Category: {category}', value=formatted_notes, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('You have no notes.')

@bot.command()
async def view_category(ctx, category: str):
    user_notes = notes.get(ctx.message.author.id)
    if user_notes and category in user_notes:
        notes_list = user_notes[category]
        formatted_notes = '\n'.join([f'Note {i}: {note}' for i, note in enumerate(notes_list, 1)])
        embed = discord.Embed(title=f'Notes in Category: {category}', description=formatted_notes, color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        await ctx.send('No notes in this category.')

@bot.command()
async def delete(ctx, category: str, number: int):
    user_notes = notes.get(ctx.message.author.id)
    if user_notes and category in user_notes:
        notes_list = user_notes[category]
        if 1 <= number <= len(notes_list):
            deleted_note = notes_list.pop(number - 1)
            await ctx.send(f'Deleted note: {deleted_note}')
        else:
            await ctx.send('Invalid note number.')
    else:
        await ctx.send('Could not find notes to delete.')

@bot.command()
async def edit(ctx, category: str, number: int, *, new_note: str):
    user_notes = notes.get(ctx.message.author.id)
    if user_notes and category in user_notes:
        notes_list = user_notes[category]
        if 1 <= number <= len(notes_list):
            notes_list[number - 1] = new_note
            await ctx.send('Note updated!')
        else:
            await ctx.send('Invalid note number.')
    else:
        await ctx.send('Could not find notes to edit.')

@bot.command()
async def search(ctx, keyword: str):
    user_notes = notes.get(ctx.message.author.id)
    if user_notes:
        found_notes = []
        for category, notes_list in user_notes.items():
            matches = [f'Note {i}: {note}' for i, note in enumerate(notes_list, 1) if keyword.lower() in note.lower()]
            if matches:
                found_notes.extend(matches)
        if found_notes:
            formatted_notes = '\n'.join(found_notes)
            embed = discord.Embed(title=f'Matching Notes for Keyword: {keyword}', description=formatted_notes, color=discord.Color.orange())
            await ctx.send(embed=embed)
        else:
            await ctx.send('No matching notes found.')
    else:
        await ctx.send('You have no notes.')

@bot.command()
async def remind(ctx, category: str, number: int, duration: str):
    user_notes = notes.get(ctx.message.author.id)
    if user_notes and category in user_notes:
        notes_list = user_notes[category]
        if 1 <= number <= len(notes_list):
            note = notes_list[number - 1]
            reminder_time = get_duration(duration)
            if reminder_time:
                await asyncio.sleep(reminder_time)
                embed = discord.Embed(title='Note Reminder', description=f'Reminder for note in category: {category}', color=discord.Color.gold())
                embed.add_field(name='Note', value=note, inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send('Invalid reminder duration.')
        else:
            await ctx.send('Invalid note number.')
    else:
        await ctx.send('Could not find notes to set a reminder.')

def get_duration(duration):
    units = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400
    }
    try:
        value = int(duration[:-1])
        unit = duration[-1]
        return value * units.get(unit)
    except (ValueError, KeyError):
        return None

bot.run(os.environ["DISCORD_TOKEN"])
