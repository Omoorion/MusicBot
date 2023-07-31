import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import ffmpeg
import ffprobe
from replit import db
import urllib.request
import re

class music(commands.Cog):
  def __init__(self, client):
    self.client = client

    if 'loop' not in db.keys():
      db['loop'] = False

  # async def duration():
  #   global is_playing
  #   is_playing = true
  #   await asyncio.sleep(duration)
  #   is_playing = false

  @commands.command()
  async def j(self,ctx):
    if ctx.author.voice is None:
      await ctx.send("You're not in a voice channel!")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)

  @commands.command()
  async def dis(self,ctx):
    await ctx.voice_client.disconnect()
  
  @commands.command()
  async def p(self, ctx, *args):
    url = " ".join(args[:])
    
    if "https://www.youtube.com/watch?v=" not in url:
      url = re.sub("[$@&',]","",url)
      url = url.replace(" ", "+")
      if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel!")
      else:
        voice_channel = ctx.author.voice.channel

      if ctx.voice_client is None:
        await voice_channel.connect()

      if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
      FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
      YDL_OPTIONS = {'format': "bestaudio"}
      vc = ctx.voice_client
      html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url)
      video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
      if not video_ids:
        ctx.send("No results were found!")
        #else:
      # songlist = ""
      # for video in video_ids:
      #   if video_ids.index(video) < 5:
      #     songlist+=str((video_ids.index(video) + 1)) + ". www.youtube.com/watch?v=" + video_ids[video_ids.index(video)] + "\n"
      #   else:
      #     break
      # await ctx.send("Choose by number:\n"+songlist)
      # #num = await songtoplay(self, ctx, url)
      # # Sends the questions one after another
      # msg = await ctx.wait_for('message')
      # while msg.author != ctx.author: #In order to prevent inturuption
      #   msg = await ctx.wait_for('message')
      videourl = "https://www.youtube.com/watch?v=" + video_ids[0]
      with YoutubeDL(YDL_OPTIONS) as ydl:
        print("Trying to show video by name")
        info = ydl.extract_info(videourl, download = False)
        url2=""
        for i in range(len(info['formats'])):
          url2 = info['formats'][i]['url']
          if("videoplayback" in url2):
            break;
        #url2 = info['formats'][0]['url']
        #result = f'{url2}'
        #print("url2: " + result)
        #print("Playing M.mp3")
        source = await discord.FFmpegOpusAudio.from_probe(url2, method='fallback')
        # if not duration.is_playing:
        #   await ctx.send('finished playing')
        vc.play(source)
          #if videourl:
            #await ctx.send()
    else:
      if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel!")
      else:
        voice_channel = ctx.author.voice.channel

      if ctx.voice_client is None:
        await voice_channel.connect()

      if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        
      FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
      YDL_OPTIONS = {'format': "bestaudio"}
      vc = ctx.voice_client
      with YoutubeDL(YDL_OPTIONS) as ydl:
        print("Trying to show video by url")
        info = ydl.extract_info(url, download = False)
        
        url2=""
        for i in range(len(info['formats'])):
          url2 = info['formats'][i]['url']
          if("videoplayback" in url2):
            break;
        #url2 = info['formats'][0]['url']
        #result = f'{url2}'
        #print("url2: " + result)
        #print("Playing M.mp3")
        source = await discord.FFmpegOpusAudio.from_probe(url2, method='fallback')
        # if not duration.is_playing:
        #   await ctx.send('finished playing')
        vc.play(source)
        
      #await ctx.send("Cannot download video because it's been forbidden/There was an error while installing it")

    #vc.play(source, after=lambda e: repeat(ctx.guild, vc, source))

    # def repeat(guild, voice, audio):
    #   voice.play(audio, after=lambda e: repeat(guild, voice, audio))
    #   voice.is_playing()

    #   if voice_channel and not vc.is_playing():
    #       audio = source
    #       vc.play(audio, after=lambda e: repeat(ctx.guild, vc, audio))
    #       vc.is_playing()
#     song_there = os.path.isfile("song.mp3")
# if song_there:
#    os.remove('song.mp3')

# voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

# ydl_opts = {
#    'format': 'bestaudio/best',
#    'postprocessors': [{
#       'key': 'FFmpegExtractAudio',
#       'preferredcodec': 'mp3',
#       'preferredquality': '192',
#    }],
# }
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#    ydl.download([url])
# for file in os.listdir("./"):
#    if file.endswith(".mp3"):
#    os.rename(file, "song.mp3")
# voice.play(discord.FFmpegPCMAudio("song.mp3"))

    # except:
    #   FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    #   YDL_OPTIONS = {'format': "bestaudio"}
    #   vc = ctx.voice_client

    #   with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    #     info = ydl.extract_info(url, download = False)
    #     url2 = info['formats'][0]['url']
    #     source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
    #     vc.play(source, after=lambda e: repeat(ctx.guild, vc, source))

    #   def repeat(guild, voice, audio):
    #     voice.play(audio, after=lambda e: repeat(guild, voice, audio))
    #     voice.is_playing()

    #   if voice_channel and not vc.is_playing():
    #     audio = source
    #     vc.play(audio, after=lambda e: repeat(ctx.guild, vc, audio))
    #     vc.is_playing()
    #     # if not duration.is_playing:
    #     #   await ctx.send('finished playing')

@commands.command()
async def pause(self,ctx):
  await ctx.voice_client.pause()
  await ctx.send("paused")

@commands.command()
async def resume(self,ctx):
  await ctx.voice_client.resume()
  await ctx.send("resumed")

@commands.command()
async def loop(self,ctx, arg1):
  db['loop'] = arg1
  await ctx.send("Set to " + db['loop'])

def songtoplay(self, ctx, msg):
    num = int(msg)
    return num
# @commands.command()
  # async def addsong(self, ctx, url):
  #   if 'songs' in db.keys():
  #     songs = db['songs']
  #     songs.append(str(url))
  #     db['songs'] = songs
  #   else:
  #     db['songs'] = [str(url)]
  #   await ctx.send(db['songs'])
  # @commands.command()
  # async def addSong(ctx, url):
  #   YDL_OPTIONS = {'format': "bestaudio"}
  #   with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
  #     info = ydl.extract_info(url, download = False)
  #     url2 = info['formats'][0]['url']
  #     print(bytes(url))
  #     print(bytes(url2))
  # if 'songs' in db.keys():
  #   songs = db['songs']
  #   songs.append(str(url))
  #   db['songs'] = songs
  # else:
  #   db['songs'] = [str(url)]
  # await ctx.send(db['songs'])

  # @commands.command()
  # async def playallsongs(self, ctx):
  #   if 'songs' in db.keys():
  #     songs = db['songs']
  #     if ctx.author.voice is None:
  #       await ctx.send("You're not in a voice channel!")
  #     voice_channel = ctx.author.voice.channel
  #     if ctx.voice_client is None:
  #       await voice_channel.connect()
  #     for i in range(len(songs)):
  #       waitTime = 1
  #       try:
  #         ctx.voice_client.stop()
  #         FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  #         YDL_OPTIONS = {'format': "bestaudio"}
  #         vc = ctx.voice_client
  #         if not vc:
  #             channel = ctx.author.voice.channel
  #             vc = await channel.connect()

  #         with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
  #           info = ydl.extract_info(songs[i], download = False)
  #           url2 = info['formats'][0]['url']
  #           source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
  #           vc.play(source)
  #           while vc.is_playing:
  #             waitTime+=waitTime
  #             print(waitTime)
  #           time.sleep(waitTime)
  #           # if vc.is_playing:
  #           #   waitTime = vc.get_duration / 1000
  #           #   print(waitTime)
  #           # time.sleep(waitTime)
  #       except:
  #         FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  #         YDL_OPTIONS = {'format': "bestaudio"}
  #         vc = ctx.voice_client
  #         if not vc:
  #           channel = ctx.author.voice.channel
  #           vc = await channel.connect()
  #         with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
  #           info = ydl.extract_info(songs[i], download = False)
  #           url2 = info['formats'][0]['url']
  #           source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
  #           vc.play(source)
  #           # while voicec.is_playing:
  #           #   waitTime+=waitTime
  #           #   print(waitTime)
  #           # time.sleep(waitTime)
  #   else:
  #     await ctx.send("There are no songs to play!")

async def setup(client):
  await client.add_cog(music(client))
  print("Added cog!");

#add a fav song save feature which when called, adds a new song to the list
#add a play fav songs feauture which when called, plays all of your favourite songs!