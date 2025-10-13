import json
import os
import datetime
from discord.ext import commands, tasks

class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.local_tz = datetime.datetime.now().astimezone().tzinfo
        self.birthdays = self.load_birthdays()
        self.check_birthdays.start()

    def cog_unload(self):
        self.check_birthdays.cancel()

    def load_birthdays(self):
        if os.path.exists("birthdays.json"):
            with open("birthdays.json", "r") as file:
                return json.load(file)
        return {}

    @tasks.loop(time=datetime.time(hour=6, minute=0, tzinfo=datetime.datetime.now().astimezone().tzinfo)) # time=datetime.time(hour=6, minute=0, tzinfo=datetime.datetime.now().astimezone().tzinfo)
    async def check_birthdays(self):
        today = datetime.datetime.now().strftime("%m-%d")
        channel = self.bot.get_channel(725845123572957207)  # Test birthday channel 921934495832211460 main channel 725845123572957207

        for user_id, info in self.birthdays.items():
            if info.get("birthday") == today:
                emote = info.get("emote", "")
                message = f"Happy Birthday <@{user_id}>!"
                if emote:
                    message += f" {emote}"
                await channel.send(message)

    @check_birthdays.before_loop
    async def before_check_birthdays(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Birthdays(bot))
