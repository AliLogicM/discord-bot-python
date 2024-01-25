import re
import discord
import datetime
import wikipedia as wiki
import wikipediaapi
import requests
from discord.ext import commands
from config import TOKEN, DEEPL
from urllib import parse, request
from deepl import Translator


wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='MyDiscordBot/1.0 (love_jiyupe53@gmail.com)')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', description='This is a helper bot', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def sum(ctx, numberOne: int, numberTwo: int):
    await ctx.send(numberOne + numberTwo)

@bot.command()
async def info(ctx):
    guild = await bot.fetch_guild(ctx.guild.id)
    owner = await bot.fetch_user(guild.owner_id)

    embed = discord.Embed(title=f"{ctx.guild.name}", description="Haro everynyan", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{owner}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon}")
    await ctx.send(embed=embed)

@bot.command()
async def wikipedia(ctx, *, search):
    page_py = wiki_wiki.page(search)
    if page_py.exists():
        summary_sentences = page_py.summary.split('. ')
        summary = '. '.join(summary_sentences[:5]) + '.' if len(summary_sentences) > 0 else ''
        image = wiki.page(search).images[0]
        embed = discord.Embed(title=search, description=summary, color=discord.Color.blue())
        embed.set_image(url=image)
        await ctx.send(embed=embed)
    else:
        await ctx.send('No results found.')

@bot.command()
async def translate(ctx, target_language: str, *, text: str):
    translator = Translator(DEEPL)
    result = translator.translate_text(text, target_lang=target_language.upper())
    await ctx.send(result)

#Events
@bot.event
async def on_ready():
    print('My bot is ready')

bot.run(TOKEN)