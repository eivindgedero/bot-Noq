import discord
import random
import re
import config

client = discord.Client(intents=discord.Intents.all())

links_to_copy = ["puu", "imgur", "gyazo", "streamable"]
clue_phrasings = ["your clues", "ur clues", "do clues"]
pg_12 = ["you're 12", "you 12", "12 year", "im 12", "i'm 12", "your 12", "12 btw", "pg12",
         "is 12", "I'm 12", "Im 12", "ur 12", "pg 12", "pg-12", "r 12", "he's 12", "He's 12", "12 y"]


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message_delete(message):
    if message.author.id == 234623956869447680:
        number = random.randint(1, 3)
        if number == 2:
            await message.channel.send(file=discord.File("danny3.png"))
    if message.guild.id == 725845122901737524:
        if message.channel.id == 902972612601323691:
            return
        elif message.channel.id == 1017593223226609664:
            return
        elif message.author.id == 946786439172087838:
            return
        else:
            channel = client.get_channel(1017593223226609664)
            await channel.send(f"**{message.channel.name}**")
            await channel.send(f"**deleted**       {message.author.name}: *{message.content}*", allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, users=False))


@client.event
async def on_message_edit(before, after):
    if before.guild.id == 725845122901737524:
        if before.content != after.content:
            if before.channel.id == 902972612601323691:
                return
            elif before.channel.id == 1017593223226609664:
                return
            else:
                channel = client.get_channel(1017593223226609664)
                await channel.send(f"**{before.channel.name}**")
                await channel.send(f"**original**       {before.author.name}: *{before.content}*", allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, users=False))
                await channel.send(f"**after edit**    {before.author.name}: *{after.content}*", allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, users=False))


@client.event
async def on_member_join(member):
    channel = client.get_channel(1017593223226609664)
    await channel.send(f"{member.name} has joined the server.")


@client.event
async def on_member_remove(member):
    channel = client.get_channel(1017593223226609664)
    await channel.send(f"{member.name} has left the server.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if ((message.channel.id == 744692129812447343) and message.attachments) or ((message.channel.id == 744692129812447343) and any(link in msg for link in links_to_copy)):
        await message.add_reaction("<a:stitch_cheer:806648037908807739>")
        await message.add_reaction("<a:panda_w00t:842286461990600714>")

    # if bool(re.search(r'[Aa]bba', msg))== True and bool(re.search(r'[Kk][Ii][Ll]', msg)) == True:
    #   await message.channel.send(file=discord.File("bot.png"))

    if any(link in msg for link in links_to_copy):
        with open("file_with_links.txt", "a") as links:
            bildelinker = re.findall(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)
            for bildelink in bildelinker:
                links.write(bildelink)
                links.write("\n")

    dutch = re.findall("[Dd]utch", msg)
    if any(d in msg for d in dutch):
        number = random.randint(1, 5)
        if number == 4:
            await message.channel.send(file=discord.File("abba_dutch.png"))
    # if any(clue in msg for clue in clue_phrasings):
    #   await message.channel.send("<:pepe_clue:939686143081996369>")

    # if any(kid in msg for kid in pg_12):
    #   await message.channel.send("<a:pg12:951603378625077329>")


    # if message.content.startswith('$dannylate'):
    #   await message.channel.send("<@234623956869447680> quit playing your stupid F1 game..")

    # if message.content.startswith("$abbalate"):
    #   await message.channel.send("<@185793621524611081> wake up, it's time to game!")

    # Melvin
    # if message.author.id == 275134985869197312:
    #   number = random.randint(1,9)
    #   if number == 3:
    #     await message.channel.send("<:mulvin:879195318057578516>")

    # Abba
    if message.author.id == 185793621524611081:
        number = random.randint(1, 10)
        # if number == 2:
        #   await message.channel.send("<:abba_approved:753774504873820251> <:abba_soup:753775919587393546>")
        wah = re.findall('[Ww][Aa]+[Hh]+', msg)
        if any(waah in msg for waah in wah):
            await message.channel.send(wah[-1] + " " + wah[-1])
            await message.add_reaction("<:abba_wah:892937828500144169>")
        emotes = re.findall(r'[Ww][Aa][Tt].*', msg)
        for e in emotes:
            if number == 3:
                await message.channel.send("<:what:966402492504092692>")

    # Andria
    # if message.author.id == 207554978133442561:
    #   number = random.randint(1,30)
    #   if number == 5:
    #     await message.channel.send("<:Orlando_Panda:947349761021837363> <:andria_spoon:949735041049718804>")
    #   emotes = re.findall(r':.*cat.*:', msg)
    #   for e in emotes:
    #     await message.channel.send("<:coco_zbfa:844717311574802433>")
    #   number = random.randint(1,100)
    #   if number == 69:
    #     await message.add_reaction("<:meow_lub:809896200290959431>")

    # Danny
    # if message.author.id == 234623956869447680:
    #   number = random.randint(1,40)
    #   if number == 2:
    #     await message.add_reaction("<:danny:803790234265452575>")
    #   elif number == 4:
    #     await message.channel.send("<a:pepe_nerd:913165676070445157>")
    #   elif number == 5:
    #     await message.add_reaction("<a:danny_mald:957097485782880276>")

    # Soul
    # if message.author.id == 223280159967543296:
    #   emotes = re.findall(r'.*[Ss][Uu][Ss].*', msg)
    #   for e in emotes:
    #     await message.send("<:snakie2:830485528821760040>")
    #   number = random.randint(1,30)
    #   if number == 4:
    #     await message.send("<:snakie:812761513868918844>")
    #   elif number == 6:
    #     await message.send("<:snakie3:830485522702008351>")

    # Hex
    # if message.author.id == 159623799459938304:
    #   emotes = re.findall(r':[Ss]orn.+:', msg)
    #   for e in emotes:
    #     await message.channel.send("<:ThaisOut:951628888457482340>")

    # Ryan
    # if message.author.id == 131586629541429248:
    #   if bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+' , msg)) == True:
    #     number = random.randint(1,4)
    #     if number == 2:
    #       await message.channel.send("<:ryan:803786019630481408>")

    # Dan
    # if message.author.id == 168793407249055744:
    #   if bool(re.search("amazing day", msg)) == True:
    #     await message.reply("You too! <:cat_heart:753781525342060545>")

    # if bool(re.search(r'.olak', msg)) == True:
    #   number = random.randint(1,5)
    #   if number == 4:
    #     await message.reply("https://puu.sh/IFPuo/d644ffe5bb.png%7C%7C")

    # Noq
    # if message.author.id == 157211170233647104:
        # await message.reply("<:snakie2:830485528821760040>")
        # await message.reply("https://puu.sh/IFPuo/d644ffe5bb.png%7C%7C")


client.run(config.secret)
