import discord
import random
import math
import config
import os
import json
from discord import app_commands
from discord.ext import commands
from divide_teams import divide_teams


config_file = "guild_config.json"
if os.path.exists(config_file):
    with open(config_file, "r") as f:
        guild_config = json.load(f)
else:
    guild_config = {}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Helper function to save config
def save_config():
    with open(config_file, "w") as f:
        json.dump(guild_config, f, indent = 2)

# Slash commands
@bot.tree.command(name="setlogchannel", description="Set the log channel for this server (Admin only)")
@app_commands.describe(channel="The text channel to log messages in")
@app_commands.default_permissions(administrator=True)
async def set_log_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    guild_config[str(interaction.guild.id)] = {"log_channel_id": channel.id}
    save_config()
    await interaction.response.send_message(
        f"Log channel set to {channel.mention}.", ephemeral=True
    )

@bot.tree.command(name="removelogchannel", description="Remove the log channel configuration (Admin only)")
@app_commands.default_permissions(administrator=True)
async def remove_log_channel(interaction: discord.Interaction):
    guild_id = str(interaction.guild.id)
    if guild_id in guild_config:
        del guild_config[guild_id]
        save_config()
        await interaction.response.send_message("Log channel configuration removed.", ephemeral=True)
    else:
        await interaction.response.send_message("No log channel is currently set.", ephemeral=True)

@set_log_channel.error
@remove_log_channel.error
async def admin_error_handler(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)
    else:
        raise error


# Divide teams
@bot.tree.command(name="teamsize", description="Divide your current voice chat into teams of given size.")
@app_commands.describe(
    teamsize="Number of players per team",
    game="Optional game name or label for the match"
)
async def teamsize(interaction: discord.Interaction, teamsize: int, game: str = ""):
    member = interaction.user

    # Check if user is in a voice channel
    if not member.voice or not member.voice.channel:
        await interaction.response.send_message(
            "You must be in a voice channel to create teams.",
            ephemeral=True
        )
        return

    channel = member.voice.channel
    members = [m for m in channel.members if not m.bot]
    players = [m.display_name for m in members]

    if not players:
        await interaction.response.send_message("No valid players found in the voice channel.", ephemeral=True)
        return

    # Divide teams
    random.shuffle(players)
    num_teams = math.ceil(len(players) / teamsize)
    new_teams = divide_teams(players, teamsize)

    # Create and send embed
    title = game if game else f"Teams in {channel.name}"
    embed = discord.Embed(title=title, color=discord.Color.blurple())

    separator = ", "
    for i in range(num_teams):
        embed.add_field(
            name=f"Team {i + 1}",
            value=separator.join(new_teams[i]),
            inline=True
        )

    await interaction.response.send_message(embed=embed)

@bot.command(brief="Abbas volvo message", 
             description="Shows a picture of Abbas mood whenever he finds out he needs new parts for his Volvo."
             )    
async def volvo(ctx):
    await ctx.send(file=discord.File('images/abba_volvo.png'))
    
@bot.command(brief="Abba is dead.", description="Shows what soul will do to Abba when he breaks his word.")
async def abba_dead(ctx):
    await ctx.send(file=discord.File('images/bot.png'))

# On delete functionality
@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    guild_id = str(message.guild.id)
    config = guild_config.get(guild_id)
    if not config:
        return
    log_channel = bot.get_channel(config["log_channel_id"])
    if log_channel:
        embed = discord.Embed(
            title="Message Deleted",
            description=f"**Author:** {message.author.mention}\n"
                        f"**Channel:** {message.channel.mention}\n"
                        f"**Content:**\n{message.content}\n",
            color=discord.Color.red()
        )
        if message.attachments:
            attachments_info = "\n".join([attachment.url for attachment in message.attachments])
            embed.add_field(name="Attachments", value=attachments_info, inline=False)
        await log_channel.send(embed=embed)
    else:
        print(f"Log channel with ID {config["log_channel_id"]} not found.")

# On edit functionality
@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    
    guild_id = str(before.guild.id)
    config = guild_config.get(guild_id)
    if not config:
        return
    
    log_channel = bot.get_channel(config["log_channel_id"])
    if not log_channel:
        print(f"Log channel with ID {config["log_channel_id"]} not found")
        return
    
    content_changed = before.content != after.content
    attachments_changed = before.attachments != after.attachments
    
    if not (content_changed or attachments_changed):
        return
    
    embed = discord.Embed(
        title="Message Edited",
        description=f"**Author:** {before.author.mention}\n"
        f"**Channel:** {before.channel.mention}\n",
        color=discord.Color.orange()
    )

    if content_changed:
        embed.add_field(name="Before Edit", value=f"{before.content}", inline=False)
        embed.add_field(name="After Edit", value=f"{after.content}", inline=False)

    await log_channel.send(embed=embed)

@bot.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    config = guild_config.get(guild_id)
    if not config:
        return
    log_channel = bot.get_channel(config["log_channel_id"])
    if not log_channel:
        print(f"Log channel with ID {config['log_channel_id']} not found")
        return

    embed = discord.Embed(
        description=f"{member.mention} has joined the server!",
        color=discord.Color.dark_purple()
    )
    await log_channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    guild_id = str(member.guild.id)
    config = guild_config.get(guild_id)
    if not config:
        return
    log_channel = bot.get_channel(config["log_channel_id"])
    if not log_channel:
        print(f"Log channel with ID {config['log_channel_id']} not found")
        return

    embed = discord.Embed(
        description=f"{member.mention} has left the server.",
        color=discord.Color.dark_purple()
    )
    await log_channel.send(embed=embed)

# Starting bot
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}.")

bot.run(config.secret)


