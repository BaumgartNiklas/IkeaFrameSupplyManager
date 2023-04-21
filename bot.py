import asyncio
import os
import sys
import json
import aiosqlite
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
import helper
import cogs

# load config
if not os.path.isfile(helper.get_real_path("config.json")):
    sys.exit("No 'config.json' was found!")
else:
    with open(helper.get_real_path("config.json")) as file:
        config = json.load(file)

# create intents
intents = discord.Intents(
    guild_messages=True,
    guild_reactions=True,
    message_content=True
)

# create bot instance
bot = Bot(command_prefix=commands.when_mentioned_or(config["prefix"]),
          intents=intents,
          help_command=cogs.general.CustomHelp())


async def init_db() -> None:
    """Creates database connection and loads sql schema"""
    async with aiosqlite.connect(helper.get_real_path(config["database_path"])) as db:
        with open(helper.get_real_path(config["database_schema_path"])) as sql_schema:
            await db.executescript(sql_schema.read())
        await db.commit()


async def load_cogs() -> None:
    """Loads the commands of the bot"""
    await bot.load_extension("cogs.general")
    await bot.load_extension("cogs.deco_management")


@bot.event
async def on_ready() -> None:
    """Callback function, executed when bot is ready"""
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Decorations Inventory"))


@bot.event
async def on_command_error(context: Context, error) -> None:
    if isinstance(error, cogs.DecorationNotFound):
        embed = discord.Embed(description="No corresponding request was found")
        await context.reply(embed=embed)

    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description=f"Insufficient Permissions. You need to be at least one of {', '.join(error.missing_permissions)}.")
        await context.reply(embed=embed)

    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description=f"I am missing Permissions to perform this action: {', '.join(error.missing_permissions)}")
        await context.reply(embed=embed)

    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description=str(error).capitalize())
        await context.reply(embed=embed)

    else:
        raise error

bot.config = config
asyncio.run(init_db())
asyncio.run(load_cogs())
bot.run(config["token"])
