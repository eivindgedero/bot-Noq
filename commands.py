import discord
import random
import math
import config
from discord.ext import commands
# from wind_converter import wind_converter
from divide_teams import divide_teams
# from discord import FFmpegPCMAudio
# from discord import FFmpegOpusAudio
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
    await message.send(file=discord.File('abba_volvo.png'))


@bot.command(brief="List of all picture links posted in discord", 
             description="This command posts a file with all the video and picture links posted in this discord, so they can be easily accessed and 'revived'."
             )
async def storage(message):
    await message.send(file=discord.File('file_with_links.txt'))

bot.run(config.secret)

# @bot.command(pass_context=True)
# async def play(message):
    
#     voice_channel = message.author.voice.channel
#     await voice_channel.connect()
#     message.author.voice.channel.play(discord.FFmpegPCMAudio(executable="C:\FFmpeg", source="tiddies.mp3"))


#Need weather API config code

# base_url = "https://api.openweathermap.org/data/2.5/weather?"

# @bot.command(brief="Check the current weather", 
#              description="Check the current weather in a city of your choice. !weather <city>",
#              )
# async def weather(ctx, *, city: str = commands.parameter(description=" ")):
#     if ctx.channel.id != 784215570173657118:
#         await ctx.channel.send("Please use <#784215570173657118>.")
#     elif city != None:
#         unit = "units=metric"
#         complete_url = f"{base_url}appid={config.weather_api}&q={city}&{unit}"
#         response = requests.get(complete_url)
#         result = response.json()

#         channel = ctx.message.channel
#         if result["cod"] != "404":
#             city = result["name"]
#             weather_description = result["weather"][0]["description"]
#             temperature = result["main"]["temp"]
#             minimum_temperature = result["main"]["temp_min"]
#             maximum_temperature = result["main"]["temp_max"]
#             pressure = result["main"]["pressure"]
#             humidity = result["main"]["humidity"]
#             wind_speed = result["wind"]["speed"]
#             wind_direction = result["wind"]["deg"]
#             print(wind_direction)
#             embed=discord.Embed(title=f"{city}", color=0x14aaeb)
#             embed.add_field(name="Temperature", value=f"{temperature}°C", inline = True)
#             embed.add_field(name="max", value=f"{maximum_temperature}°C", inline = True)
#             embed.add_field(name="min", value=f"{minimum_temperature}°C", inline = True)
#             embed.add_field(name="Description", value=f"{weather_description}", inline = False)
#             embed.add_field(name="Wind condition", value=f"{wind_speed}m/s {wind_converter(wind_direction)}", inline = False)
#             embed.add_field(name="Pressure", value=f"{pressure}hPa", inline = True)
#             embed.add_field(name="humidity", value=f"{humidity}%", inline = True)          
#             await channel.send(embed=embed)
#         else:
#             await channel.send("City not found.")
# @client.command(
#     name='vuvuzela',
#     description='Plays an awful vuvuzela in the voice channel',
#     pass_context=True,
# )
# async def vuvuzela(context):
#     # grab the user who sent the command
#     user = context.message.author
#     voice_channel = user.voice.voice_channel
#     channel = None
#     if voice_channel != None:
#         channel = voice_channel.name
#         await client.say('User is in channel: ' + channel)
#         vc = await client.join_voice_channel(voice_channel)
#         player = vc.create_ffmpeg_player('vuvuzela.mp3', after=lambda: print('done'))
#         player.start()
#         while not player.is_done():
#             await asyncio.sleep(1)
#         player.stop()
#         await vc.disconnect()
#     else:
#         await client.say('User is not in a channel.')