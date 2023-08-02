import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import asyncio
import ffmpeg
import ffprobe
from replit import db
import urllib.request
import re

class music(commands.Cog):
  def __init__(self, client):
    self.client = client

  global songs
  songs = []
  
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
  async def disconnect(self,ctx):
    await ctx.voice_client.disconnect()
  
  @commands.command()
  async def p(self, ctx, *args):
    url = " ".join(args[:])
    

    if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel!")
    else:
      voice_channel = ctx.author.voice.channel
      
      if ctx.voice_client is None:
        await voice_channel.connect()
      
      vc = ctx.voice_client
      
      videourl = ""
      
      if "https://www.youtube.com/watch?v=" not in url:
        print("Searching by name!")
        url = re.sub("[$@&',]","",url)
        url = url.replace(" ", "+")
        
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        if not video_ids:
          await ctx.send("No results were found!")
        else:  
          videourl = "https://www.youtube.com/watch?v=" + video_ids[0]
      else:
        print("Searching by url!")
        videourl = url  

      songs.append(videourl)

      print("song added to songs list!")
      try: #bugged with 429 for some reason
        await ctx.send("Added song to queue!")
      except:
        print("couldn't send message due to 429 error")
      #plays the song
      if(not ctx.voice_client.is_playing()):
        await self.play_song(ctx)
    
  async def play_song(self, ctx):
    track = songs.pop(-1) #track = videourl

    #FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': "bestaudio"}
    with YoutubeDL(YDL_OPTIONS) as ydl:
      print("Trying to show video by url")
      info = ydl.extract_info(track, download = False)
      
      url2=""
      for i in range(len(info['formats'])):
        url2 = info['formats'][i]['url']
        if("videoplayback" in url2):
          break;
      
      try:
        await ctx.send(content="playing track {}".format(track))
      except:
        print("couldn't send message due to 429 error")
      loop = asyncio.get_event_loop()
      ctx.voice_client.play(
          await discord.FFmpegOpusAudio.from_probe(source=url2, method='fallback'),
          after=lambda ex: loop.create_task(self.after(ctx))
      )
    ctx.voice_client.is_playing()
  
  async def after(self, ctx):

    if len(songs) >= 1  and not ctx.voice_client.is_playing():
      await self.play_song(ctx)
    else:
      print("Problem occured: songs length: " + str(len(songs)))

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
    if(str(arg1).lower() == "true" or str(arg1).lower() == "false"):
      db['loop'] = arg1
      await ctx.send("Set to " + str(db['loop']))
    else:
      await ctx.send("enter a valid argument to the command!")

  @commands.command()
  async def skip(self, ctx):
    if ctx.voice_client.is_playing():
          ctx.voice_client.stop()
          #will automatically play next song because the function is activated when no songs are playing.
          #if 'songs' in db.keys():
            #songs = db['songs']            
          await ctx.send("Skipped song!");
    else:
      ctx.send("I am not playing anything!")

async def setup(client):
  await client.add_cog(music(client))
  print("Added cog!");

#add a fav song save feature which when called, adds a new song to the list
#add a play fav songs feauture which when called, plays all of your favourite songs!
