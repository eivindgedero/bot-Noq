import discord
import random
import math
import json
import os
import whatismyip
from discord import app_commands
from discord.ext import commands

config_file = "guild_config.json"

if os.path.exists(config_file):
    with open(config_file, "r") as f:
        guild_config = json.load(f)
else:
    guild_config = {}

def save_config():
    with open(config_file, "w") as f:
        json.dump(guild_config, f, indent=2)

def divide_teams(players, size):
    return [players[i:i + size] for i in range(0, len(players), size)]

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_guild = 725845122901737524

    # Slash commands

    @app_commands.command(name="setlogchannel", description="Set the log channel for this server (Admin only)")
    @app_commands.describe(channel="The text channel to log messages in")
    @app_commands.default_permissions(administrator=True)
    async def set_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_config[str(interaction.guild.id)] = {"log_channel_id": channel.id}
        save_config()
        await interaction.response.send_message(f"Log channel set to {channel.mention}.", ephemeral=True)

    @app_commands.command(name="removelogchannel", description="Remove the log channel configuration (Admin only)")
    @app_commands.default_permissions(administrator=True)
    async def remove_log_channel(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        if guild_id in guild_config:
            del guild_config[guild_id]
            save_config()
            await interaction.response.send_message("Log channel configuration removed.", ephemeral=True)
        else:
            await interaction.response.send_message("No log channel is currently set.", ephemeral=True)

    @set_log_channel.error
    @remove_log_channel.error
    async def admin_error_handler(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)
        else:
            raise error

    @app_commands.command(name="teamsize", description="Divide your current voice chat into teams of given size.")
    @app_commands.describe(teamsize="Number of players per team", game="Optional game name or label for the match")
    async def teamsize(self, interaction: discord.Interaction, teamsize: int, game: str = ""):
        member = interaction.user

        if not member.voice or not member.voice.channel:
            await interaction.response.send_message("You must be in a voice channel to create teams.", ephemeral=True)
            return

        channel = member.voice.channel
        members = [m for m in channel.members if not m.bot]
        players = [m.display_name for m in members]

        if not players:
            await interaction.response.send_message("No valid players found in the voice channel.", ephemeral=True)
            return

        random.shuffle(players)
        new_teams = divide_teams(players, teamsize)

        title = game if game else f"Teams in {channel.name}"
        embed = discord.Embed(title=title, color=discord.Color.blurple())

        for i, team in enumerate(new_teams, start=1):
            embed.add_field(name=f"Team {i}", value=", ".join(team), inline=True)

        await interaction.response.send_message(embed=embed)

    # Prefix commands

    @commands.command(brief="Abbas volvo message")
    async def volvo(self, ctx):
        await ctx.send(file=discord.File('images/abba_volvo.png'))

    @commands.command(brief="Abba is dead.")
    async def abbadead(self, ctx):
        await ctx.send(file=discord.File('images/bot.png'))

    @commands.command(hidden=True, brief="Minecraft servers")
    async def servers(self, ctx):
        if ctx.guild and ctx.guild.id != self.allowed_guild:
            return  # ignore all other guilds

        ip = whatismyip.whatismyipv4()
        embed = discord.Embed(
            title="Minecraft servers",
            color=discord.Color.purple(),
            description=f"**Meow server:** {ip}\n**New town:** {ip}:420"
        )

        await ctx.send(embed=embed)

    # Add commands to add, delete, modifiy and list minecraft locations

    # Event listeners

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        guild_id = str(message.guild.id)
        config = guild_config.get(guild_id)
        if not config:
            return
        log_channel = self.bot.get_channel(config["log_channel_id"])
        if not log_channel:
            print(f"Log channel with ID {config['log_channel_id']} not found.")
            return

        embed = discord.Embed(
            title="Message Deleted",
            description=f"**Author:** {message.author.mention}\n"
                        f"**Channel:** {message.channel.mention}\n"
                        f"**Content:**\n{message.content}\n",
            color=discord.Color.red()
        )
        if message.attachments:
            attachments_info = "\n".join([a.url for a in message.attachments])
            embed.add_field(name="Attachments", value=attachments_info, inline=False)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        guild_id = str(before.guild.id)
        config = guild_config.get(guild_id)
        if not config:
            return

        log_channel = self.bot.get_channel(config["log_channel_id"])
        if not log_channel:
            print(f"Log channel with ID {config['log_channel_id']} not found.")
            return

        if before.content == after.content and before.attachments == after.attachments:
            return

        embed = discord.Embed(
            title="Message Edited",
            description=f"**Author:** {before.author.mention}\n"
                        f"**Channel:** {before.channel.mention}\n",
            color=discord.Color.orange()
        )
        if before.content != after.content:
            embed.add_field(name="Before Edit", value=before.content or "(empty)", inline=False)
            embed.add_field(name="After Edit", value=after.content or "(empty)", inline=False)

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        config = guild_config.get(guild_id)
        if not config:
            return
        log_channel = self.bot.get_channel(config["log_channel_id"])
        if log_channel:
            embed = discord.Embed(description=f"{member.mention} has joined the server!", color=discord.Color.dark_purple())
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = str(member.guild.id)
        config = guild_config.get(guild_id)
        if not config:
            return
        log_channel = self.bot.get_channel(config["log_channel_id"])
        if log_channel:
            embed = discord.Embed(description=f"{member.mention} has left the server.", color=discord.Color.dark_purple())
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))
