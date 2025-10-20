import discord
from discord.ext import commands
import os
import asyncio
import config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, name: str):
    try:
        await bot.reload_extension(f"cogs.{name}")
        await ctx.send(f"Reloaded `{name}` cog.")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        
@bot.command(hidden=True)
@commands.is_owner()
async def stop(ctx, name: str):
    try:
        await bot.unload_extension(f"cogs.{name}")
        await ctx.send(f"Stopped `{name}` cog.")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        
@bot.command(hidden=True)
@commands.is_owner()
async def start(ctx, name: str):
    try:
        await bot.load_extension(f"cogs.{name}")
        await ctx.send(f"Started `{name}` cog.")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")
    print(f"Synced {len(bot.tree.get_commands())} slash commands.")
    print(f"Loaded Cogs: {', '.join(bot.cogs.keys())}")

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(config.secret)

if __name__ == "__main__":
    asyncio.run(main())
    