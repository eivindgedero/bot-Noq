import discord
import random
import re
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_guild = 725845122901737524 # test disc 921934495832211456 main disc 725845122901737524
        self.image_links = ("puu", "imgur", "gyazo", "streamable")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild and message.guild.id != self.allowed_guild:
            return  # ignore all other guilds

        if message.author.bot:
            return

        msg = message.content

        # Achievement channel reactions
        if message.channel.id == 744692129812447343 and (message.attachments or any(link in msg for link in self.image_links)):
            await message.add_reaction("<a:stitch_cheer:806648037908807739>")
            await message.add_reaction("<a:panda_w00t:842286461990600714>")

        # "Dutch" easter egg
        if re.search(r"\bdutch\b", msg, re.IGNORECASE):
            if random.randint(1, 5) == 4:
                await message.channel.send(file=discord.File("images/abba_dutch.png"))

        # "Wah" meme
        if message.author.id == 185793621524611081: # Abba 157211170233647104 Eivind 185793621524611081
            if re.search(r"[Ww][Aa]+[Hh]+", msg):
                await message.channel.send(msg + " " + msg)

            if re.search(r"[Ww][Aa][Tt]", msg) and random.randint(1, 10) == 3:
                await message.channel.send("<:what:966402492504092692>")

async def setup(bot):
    await bot.add_cog(Fun(bot))
