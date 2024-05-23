import discord
import random
import math
import config
from discord.ext import commands
from divide_teams import divide_teams
intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents = intents)


@bot.command(brief="Divides into teams of given size", 
             description="Divides everyone in your voice chat into teams of a specified size. !teamsize <players per team> <game>"
             )
async def teamsize(message, teamsize:int = commands.parameter(description=" "), *game):
    players = []
    if message.author.voice and message.author.voice.channel:
        channel = message.author.voice.channel
    else: 
        await message.channel.send("You must be part of the voice chat in order to create teams.")
        return
    members = channel.members
    for member in members:
        players.append(member.display_name)
    numteams = math.ceil(len(players)/teamsize)
    random.shuffle(players)
    new_teams = divide_teams(players, teamsize)
    space = " "
    embed=discord.Embed(title=f"{space.join(game)}", color=0x14aaeb)
    separator = ", "
    for i in range(numteams):
        embed.add_field(name=f"Team {i+1}", value= f"{separator.join(new_teams[i])}", inline = True)
    await message.channel.send(embed=embed)

@bot.command(brief="Abbas volvo message", 
             description="Shows a picture of Abbas mood whenever he finds out he needs new parts for his Volvo."
             )    
async def volvo(message):
    await message.send(file=discord.File('images/abba_volvo.png'))
    
@bot.command(brief="Abba is dead.", description="Shows what soul will do to Abba when he breaks his word.")
async def abba_dead(message):
    await message.send(file=discord.File('images/bot.png'))

@bot.command(brief="List of all picture links posted in discord", 
             description="This command posts a file with all the video and picture links posted in this discord, so they can be easily accessed and 'revived'."
             )
async def storage(message):
    await message.send(file=discord.File('file_with_links.txt'))

bot.run(config.secret)