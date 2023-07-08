def audio_picker(member):
    if member.id == 157211170233647104:
        return "tiddies.mp3"
    


# @client.command(
#     name='vuvuzela',
#     description='Plays an awful vuvuzela in the voice channel',
#     pass_context=True,
# )
# async def vuvuzela(context):
#     # grab the user who sent the command
#     user = context.message.author
#     voice_channel = member.voice.voice_channel
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