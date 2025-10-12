import discord
import random
import re
import config

client = discord.Client(intents=discord.Intents.all())

image_links = ["puu", "imgur", "gyazo", "streamable"]

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content

    if message.channel.id == 744692129812447343 and (message.attachments or any(link in msg for link in image_links)):
        await message.add_reaction("<a:stitch_cheer:806648037908807739>")
        await message.add_reaction("<a:panda_w00t:842286461990600714>")

    dutch = re.findall("[Dd]utch", msg)
    if any(d in msg for d in dutch):
        number = random.randint(1, 5)
        if number == 4:
            await message.channel.send(file=discord.File("images/abba_dutch.png"))

    if message.author.id == 185793621524611081:
        number = random.randint(1, 10)
        wah = re.findall('[Ww][Aa]+[Hh]+', msg)
        if any(waah in msg for waah in wah):
            await message.channel.send(wah[-1] + " " + wah[-1])
        emotes = re.findall(r'[Ww][Aa][Tt].*', msg)
        for e in emotes:
            if number == 3:
                await message.channel.send("<:what:966402492504092692>")

client.run(config.secret)
