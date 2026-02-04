import discord
from discord.ext import commands
import aiohttp
from collections import defaultdict, deque

OLLAMA_MODEL = "deepseek-coder:6.7b"
OLLAMA_URL = "http://localhost:11434/api/generate"

class Ollama(commands.Cog):
    """DM chat via local Ollama model, with per-user memory until reset."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.history = defaultdict(lambda: deque(maxlen=50))
        self.session: aiohttp.ClientSession | None = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        if self.session and not self.session.closed:
            await self.session.close()

    @commands.command()
    async def reset(self, ctx):
        self.history.pop(ctx.author.id, None)
        await ctx.reply("Chat history cleared.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.guild is not None:
            return
        
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return

        if not message.content.strip():
            return

        if self.session is None:
            self.session = aiohttp.ClientSession()

        user_id = message.author.id
        self.history[user_id].append(("user", message.content))

        # Build prompt from conversation history
        prompt_parts = []
        for role, content in self.history[user_id]:
            if role == "user":
                prompt_parts.append(f"User:\n{content}")
            else:
                prompt_parts.append(f"Assistant:\n{content}")

        prompt_parts.append("Assistant:")
        prompt = "\n\n".join(prompt_parts)

        async with message.channel.typing():
            try:
                payload = {
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                }

                async with self.session.post(
                    OLLAMA_URL,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=180),
                ) as resp:
                    resp.raise_for_status()
                    data = await resp.json()

                reply = data.get("response", "").strip() or "(No response)"

            except Exception as e:
                reply = f"Error contacting AI: {e}"

        self.history[user_id].append(("assistant", reply))
        await message.channel.send(reply)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ollama(bot))
