import asyncio
import time
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from youtube_dl import YoutubeDL
import requests

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


async def gettime(self):
    while self.voice_client.is_playing() == True:
        self.time += 1
        await asyncio.sleep(1)
async def nextque(self):
    while self.query != []:
        if self.voice_client != None:
            if self.lop == False:
                if self.voice_client.is_playing() == False:
                    if self.voice_client.is_paused() == False:
                        self.query.pop(0)
                        if self.query != []:
                            self.time = 0
                            video = self.query[0]
                            self.np = video['title']
                            source = video['formats'][0]['url']
                            self.voice_client.play(FFmpegPCMAudio(source,**FFMPEG_OPTIONS))#, executable="C:\\ffmpeg\\bin\\ffmpeg.exe"))  For Windows system
                            emb = discord.Embed(title="Now playing", description=f"[{video['title']}]({video['webpage_url']})\n**Uploader:** {video['uploader']}", color=0xff2700)
                            emb.set_thumbnail(url=video['thumbnail'])
                            await self.voice_context.send(embed=emb)
                            await gettime(self)
            if self.lop == True:
                if self.voice_client.is_playing() == False:
                    if self.voice_client.is_paused() == False:
                        self.time = 0
                        video = self.query[0]
                        source = video['formats'][0]['url']
                        self.voice_client.play(FFmpegPCMAudio(source,**FFMPEG_OPTIONS))#, executable="C:\\ffmpeg\\bin\\ffmpeg.exe"))  For Windows system
                        emb = discord.Embed(title="Now playing", description=f"[{video['title']}]({video['webpage_url']})\n**Uploader:** {video['uploader']}", color=0xff2700)
                        emb.set_thumbnail(url=video['thumbnail'])
                        await self.voice_context.send(embed=emb)
                        await gettime(self)
        await asyncio.sleep(.01)
def search(query):
    with YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
        try:
            requests.get(query)
        except:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        else:
            info = ydl.extract_info(query, download=False)
    return info

class musi_cog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.query = []
        self.voice_client = None
        self.voice_context = None
        self.np = None
        self.lop = False
        self.time = 0
        import aiohttp
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Loop",help="Loops the current song that is playing",aliases=["loop"])
    async def loop(self, context):
        if self.query != []:
            fin = False
            if self.lop == False:
                if fin == False:
                    fin = True
                    self.lop = True
            if self.lop == True:
                if fin == False:
                    fin = True
                    self.lop = False
            await context.reply(f"Set loop to: {self.lop}")
    @commands.command(name="NowPlaying",help="shows what is currently playing",aliases=["nowplaying","NP","np"])
    async def nowplaying(self, context):
        x = time.strftime('%H:%M:%S', time.gmtime(self.time))
        y = time.strftime('%H:%M:%S', time.gmtime(int(self.query[0]["duration"])))
        emb = discord.Embed(title="Đang phát", description=f"**{self.np}**\n{x}/{y}",color=0xff2700)
        await context.send(embed=emb)
    @commands.command(name="ClearQueue",help="clears the queue", aliases=["clearqueue","cq","CQ"])
    async def clearqueue(self, context):
        now = True
        for item in self.query:
            if now == True:
                now = False
            else:
                self.query.remove(item)
        await context.send("Đã xóa toàn bộ danh sách chờ")
    @commands.command(name="Skip,",help="skips the current song",aliases=["skip","S","s"])
    async def skip(self, context):
        self.voice_client.stop()
        await context.send("Đổi bài")
    @commands.command(name="Queue",help="lists songs in queue",aliases=["queue","Q","q"])
    async def queue(self, context):
        now = True
        num = 0 
        queue = self.query
        desc = ""
        for item in queue:
            if now != True:
                num +=1
                desc += f"**{num}. {item['title']}**\n"
            else:
                now = False
                desc += f"**Đang phát: {item['title']}**\n\n"
        if desc == "":
            desc = "Danh sách chờ đang trống"
        emb = discord.Embed(title="Queue", description=desc)
        await context.send(embed=emb)
    @commands.command(name="Remove",help="Removes an item in the queue.", aliases=["remove"])
    async def remove(self, context, message: int):
        queue = self.query
        now = True
        items = 0

        for item in queue:
            if now != True:
                items += 1
            else:
                now = False
        if message <= items:
            if message <= 0:
                await context.send("Không có bài hát trong hàng chờ")
            else:
                video = queue[0]
                queue.pop(message)
                await context.send(f"Đã xóa **{video['title']}** khỏi hàng chờ!")
        else:
            await context.send("Bài hát không tồn tại trong hàng chờ")
        
    @commands.command(name="Join",help="joins the channel the author is in", aliases=["join", "J", "j"])
    async def join(self, context):
        member_voice = context.author.voice
        if member_voice and member_voice.channel:
            if context.voice_client:
                await context.send("Tôi đang trong room khác mất rồi hẹn gặp lại sau nhé:")
            else:
                try:
                    await member_voice.channel.connect()
                    self.voice_client = context.voice_client
                    await context.send("Đã kết nối với room!")
                except:
                    embed=discord.Embed()
                    embed.add_field(name="**Lỗi rồi**",value="Lỗi bạn có chắc mình đang trong room không!")
                    await context.reply(embed=embed)
        else:
            await context.send("Bạn phải ở trong một kênh!")
    @commands.command(name="Pause",help="Pauses the current song that's playing", aliases=["pause"])
    async def pause(self, context):
        if self.voice_client.is_playing() == False:
            if self.voice_client.is_paused() == False:
                embed=discord.Embed()
                embed.add_field(name="**Lỗi rồi**",value="Ai lại tạm dừng 1 bài hát trong khi nó còn chưa được bắt đầu!")
                await context.reply(embed=embed)
        if self.voice_client.is_paused() == True:
            await context.send("Đã tạm dừng bài hát")
        else:
            self.voice_client.pause()
            await context.message.add_reaction("✅")
    @commands.command(name="Resume",help="Resumes the song that was playing", aliases=["resume", "R", "r"])
    async def resume(self, context):
        if self.voice_client.is_paused() == True:
            self.voice_client.resume()
            await context.message.add_reaction("✅")
        else:
            embed=discord.Embed()
            embed.add_field(name="**Lỗi rồi**",value="Tôi đang hát rồi bắt đầu làm gì nữa!")
            await context.reply(embed=embed)
    @commands.command(name="Stop",help="Stops the current song that's playing", aliases=["stop"])
    async def stop(self, context):
        self.query.clear()
        self.voice_client.stop()
        self.lop = False
        await context.message.add_reaction("✅")
    @commands.command(name="Leave",help="Leaves the channel the bot is currently in", aliases=["leave", "L", "l","dis","Dis","disconnect","Disconnect"])
    async def Leave(self, context):
        member_voice = context.author.voice
        if member_voice and member_voice.channel:
            if context.voice_client:
                if member_voice.channel == context.voice_client.channel:
                    try:
                        if context.voice_client.is_playing():
                            context.voice_client.stop()
                            await context.voice_client.disconnect()
                            await context.send("Tạm biệt cảm ơn vì đã giành thời gian với tôi ^_^")
                            self.voice_client = None
                            self.voice_context = None
                            self.query = None
                            self.np = None
                            self.lop = False
                        else:
                            await context.voice_client.disconnect()
                            await context.send("Đã ngắt kết nối thành công với kênh thoại!")
                    except:
                        embed=discord.Embed()
                        embed.add_field(name="**Lỗi rồi**",value="Liên hệ admin hoặc thử lại nhé")
                        await context.reply(embed=embed)
                else:
                    embed=discord.Embed()
                    embed.add_field(name="**Lỗi rồi**",value="Bạn có chắc đang trong room của mình không")
                    await context.reply(embed=embed)
            else:
                await context.send("Tôi đang không có trong room")
    @commands.command(name="Play",help="Plays a song", aliases=["play","P","p"])
    async def play(self, context,*,query):
        member_voice = context.author.voice
        if member_voice and member_voice.channel:
            if context.voice_client:
                pass
            else:
                await member_voice.channel.connect()
            if self.query != []:
                video = search(query)
                emb = discord.Embed(title=f"✅ Queued {video['title']}", color=0xff2700)
                self.query.append(video)
                await context.send(embed=emb)
            if self.query == []:
                client_voice = context.voice_client
                self.voice_client = context.voice_client
                self.voice_context = context
                video = search(query)
                source = video['formats'][0]['url']
                emb = discord.Embed(title="Đang phát", description=f"[{video['title']}]({video['webpage_url']})\n**Uploader:** {video['uploader']}", color=0xff2700)
                emb.set_thumbnail(url=video['thumbnail'])
                client_voice.play(FFmpegPCMAudio(source,**FFMPEG_OPTIONS))#,executable="C:\\ffmpeg\\bin\\ffmpeg.exe")) For Windows system
                self.np = video["title"]
                self.query.append(video)
                await context.send(embed=emb)
                await gettime(self)
                await nextque(self)
async def setup(client):
    await client.add_cog(musi_cog(client))   