import random
import discord
from discord.ext import commands

class info(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=["avt"])
    async def avatar(self,ctx, member :discord.Member=None):
        if  member == None:
            member = ctx.message.author
        embed=discord.Embed(title=f"{member.name}'s Avata ", color=0x000333)
        embed.set_image(url=member.avatar)
        embed.set_footer(text=f"được gọi bởi {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def ping(self,ctx) :
        delay = round(self.client.latency * 1000)
        await ctx.send(f"pong! Ping hiện tại: **{delay}** ms")
        
    @commands.command(aliases =["info","in4","in"])
    async def userinfo(self,ctx, member: discord.Member=None):
        if  member == None:
            member = ctx.message.author
        roles = [role for role in member.roles]   
        embed=discord.Embed(title="Thông tin thành viên", color=0xa6abf2) 
        embed.add_field(name="Tên",value=f"{member.name}#{member.discriminator}")
        embed.add_field(name="Biệt danh:",value=member.display_name)
        embed.add_field(name="ID",value=member.id)
        embed.add_field(name="Ngày vào sever:",value=member.joined_at.strftime("%#d-%m-%Y"))
        embed.add_field(name="Ngày dùng discord",value=member.created_at.strftime("%#d-%m-%Y"))
        embed.add_field(name="role",value=",".join([role.mention for role in roles]))
        embed.add_field(name="Top role",value=member.top_role.mention)
        embed.add_field(name="Trạng thái: ",value=member.status)
        embed.add_field(name="Bot",value=member.bot)
        embed.set_thumbnail(url=member.avatar)
        await ctx.send(embed=embed)
    
    @commands.command(aliases =["svinfo","sv"])
    async def severinfo(self,ctx):
        embed=discord.Embed(title=f"Thông tin sever : {ctx.guild.name}",color=0x33e689)
        embed.add_field(name="Chủ sever: ",value=ctx.guild.owner.mention)
        embed.add_field(name="Ngày thành lập: ",value=ctx.guild.created_at.strftime("%#d-%m-%Y"))
        embed.add_field(name="Mô tả sever: ",value=ctx.guild.description)
        embed.add_field(name="Số thành viên: ",value=ctx.guild.member_count)
        embed.add_field(name="Số role: ",value=f"{len(ctx.guild.roles)} roles") 
        embed.add_field(name="Số kênh: ",value=f"{len(ctx.guild.text_channels)} Chat | {len(ctx.guild.voice_channels)} Voice")
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=["h"])
    async def help(self,ctx, member :discord.Member=None):
        if  member == None:
            member = ctx.message.author
        embed=discord.Embed(title="",description='',color=0x32f5f2)
        embed.add_field(name="",value="Bạn có thể xem qua tất cả cách lệnh của mình nhé\nPrefix mặc định sẽ là `m` nếu không sử dụng được hay liên hệ các mod nhé")
        embed.add_field(name="🛠**Admin**",value="`ban` `kich` `unban` `setprefix`",inline=False)
        embed.add_field(name="💵**Money**",value="`cash` `topxp` `topcoin` `xp` `give`",inline=False)
        embed.add_field(name="🎭**funny**",value="`cry` `hug` `kill` `kiss` `pat` `punch` `wave` `slap` `lick` `poke` `ga` ",inline=False)
        embed.add_field(name="🎲**Game**",value="`doanso` `roll` `coinflip` `math` `xx`",inline=False)
        embed.add_field(name="🖼**Info**",value="`avatar` `ping` `severinfo` `userinfo` `whoami`",inline=False)
        embed.add_field(name="🎶**Music**",value="`join` `leave` `loop` `NowPlaying` `play` `pause` `resume` `skip` `stop` `queue` `remove` ",inline=False)
        embed.set_author(name="Danh Sách Lệnh",icon_url=member.avatar)
        await ctx.send(embed=embed)
         
async def setup(client):
    await client.add_cog(info(client))