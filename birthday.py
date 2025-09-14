import config
import json
from datetime import datetime, timedelta
from discord.ext import commands, tasks
import asyncio
import discord
intents = discord.Intents.all()

with open('birthdays.json', 'r') as file:
    birthdays = json.load(file)

client = discord.Client(intents=discord.Intents.all())


@tasks.loop(hours=24)
async def check_birthdays():
    today = datetime.now().strftime("%m-%d")
    for user_id, info in birthdays.items():
        if info['birthday'] == today:
            channel = client.get_channel(725845123572957207)
            # if info["name"]=="test":
            #     channel = client.get_channel(921934495832211459)
            emote = info.get('emote', '')
            birthday_message = f"Happy Birthday <@{user_id}>!"
            if emote:
                birthday_message += f" {emote}"
            await channel.send(birthday_message)
            
            
@check_birthdays.before_loop
async def before_check_birthdays():
    await client.wait_until_ready()
    now = datetime.now()
    next_time = datetime(now.year, now.month, now.day, 6, 0)
    if next_time < now:
        next_time += timedelta(days=1)
    seconds_until_next_time = (next_time - now).total_seconds()
    await asyncio.sleep(seconds_until_next_time)  # Wait until the next scheduled time


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    check_birthdays.start()

client.run(config.secret)