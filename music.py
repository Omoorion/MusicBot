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
      # FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} !Optional!
      YDL_OPTIONS = {'format': "bestaudio"}
      vc = ctx.voice_client
      html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url)
      video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
      if not video_ids:
        ctx.send("No results were found!")
        
      videourl = "https://www.youtube.com/watch?v=" + video_ids[0]
      with YoutubeDL(YDL_OPTIONS) as ydl:
        print("Trying to show video by name")
        info = ydl.extract_info(videourl, download = False)
        url2=""
        for i in range(len(info['formats'])):
          url2 = info['formats'][i]['url']
          if("videoplayback" in url2):
            break;
            
        source = await discord.FFmpegOpusAudio.from_probe(url2, method='fallback')
        vc.play(source)
        
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
        source = await discord.FFmpegOpusAudio.from_probe(url2, method='fallback')
        vc.play(source)

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
  
async def setup(client):
  await client.add_cog(music(client))
  print("Added cog!");
