""" import discord
from discord.ext import commands
import json
import random
import os
from discord import File
from typing import Optional
from easy_pil import Editor, load_image_async, Font
from discord.ext.commands import Bot, has_permissions, CheckFailure

class exp(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            with open("levels.json", "r") as f:
                data = json.load(f)
                
            if str(message.guild.id) in data:
                if str(message.author.id) in data[str(message.guild.id)]:
                    xp = data[str(message.guild.id)][str(message.author.id)]['xp']
                    lvl = data[str(message.guild.id)][str(message.author.id)]['level']
                    
                    increased_xp = xp + random.randint(10,20) #tăng giá trị điểm ngẫu nhiên
                    level_up = int(increased_xp/100)   #lấy số nguyên dương
                    
                    data[str(message.guild.id)][str(message.author.id)]['xp']=increased_xp
                    
                    with open("levels.json", "w") as f:
                        json.dump(data, f,indent=4)
            
                    if lvl < level_up:
                        await message.channel.send(f"{message.author.mention} bạn đã lên lv {level_up}!!!")
                        data[str(message.guild.id)][str(message.author.id)]['level']=level_up
                        data[str(message.guild.id)][str(message.author.id)]['xp']=random.randint(10,30)
                        cost=data[str(message.guild.id)][str(message.author.id)]['cost']
                        cost+=10000
                        data[str(message.guild.id)][str(message.author.id)]['cost']=cost
                        
                        with open("levels.json", "w") as f:
                            json.dump(data, f,indent=4)
                    return        
                    
            if str(message.guild.id) in data:
                data[str(message.guild.id)][str(message.author.id)] = {}
                data[str(message.guild.id)][str(message.author.id)]['xp'] = 0
                data[str(message.guild.id)][str(message.author.id)]['level'] = 1
                data[str(message.guild.id)][str(message.author.id)]['cost']=10000
            else:
                data[str(message.guild.id)]={}
                data[str(message.guild.id)][str(message.author.id)] = {}
                data[str(message.guild.id)][str(message.author.id)]['xp'] = 0
                data[str(message.guild.id)][str(message.author.id)]['level'] = 1
                data[str(message.guild.id)][str(message.author.id)]['cost']=10000
                    
            with open("levels.json", "w") as f:
                json.dump(data, f,indent=4)

    @commands.command()
    async def rank(self, ctx, range_num:int = 5):
        if range_num > 20:
            range_num=20

        with open("levels.json", "r") as f:
            data = json.load(f)

        l = {}
        total_xp = []

        for userid in data[str(ctx.guild.id)]:
            xp = int(data[str(ctx.guild.id)][str(userid)]['xp'] + (int(data[str(ctx.guild.id)][str(userid)]['level'])*100)) # tổng xp đã nhận dc
            l[xp] = f"{userid};{data[str(ctx.guild.id)][str(userid)]['level']};{data[str(ctx.guild.id)][str(userid)]['xp']}"
            total_xp.append(xp)

        total_xp = sorted(total_xp, reverse=True)
        index=1

        embed = discord.Embed(title="Bảng Vàng Mít Con",color=0xf96ee2)
        
        for amt in total_xp: 
            id_ = int(str(l[amt]).split(";")[0])
            level = int(str(l[amt]).split(";")[1])
            xp = int(str(l[amt]).split(";")[2])
            
            member = await self.client.fetch_user(id_)
            embed.set_thumbnail(url=ctx.guild.icon)
            if member is not None:
                embed.add_field(name=f"{index}.{member.name}",value=f"Level: **{level}** | XP: **{xp}**",inline=False)
                if index == range_num:
                    break
                else:
                    index += 1
        await ctx.send(embed = embed)
    
    
    @commands.command()
    async def xp(self, ctx, userr: Optional[discord.Member]):
        userr = userr or ctx.author
        
        with open("levels.json", "r") as f:
            data = json.load(f)
            xp = data[str(userr.id)]["xp"]
            lvl = data[str(userr.id)]["level"]

            next_level_xp = (lvl+1) * 100
            xp_need = next_level_xp
            xp_have = data[str(userr.id)]["xp"]
            percentage = int(((xp_have * 100)/ xp_need))

            if percentage < 1:
                percentage = 0
            
            ## Rank card
            background = Editor(f"zIMAGE.png")
            profile = await load_image_async(str(userr.avatar))
            profile = Editor(profile).resize((150, 150)).circle_image()
            
            poppins = Font.poppins(size=45)
            poppins_small = Font.poppins(size=35)

            background.paste(profile.image, (30, 30))

            background.rectangle((30, 220), width=550, height=40, fill="#fff", radius=20)
            background.bar(
                (30, 220),
                max_width=550,
                height=40,
                percentage=percentage,
                fill="#74ff7c",
                radius=20,
            )
            background.text((200, 40), str(userr.name), font=poppins, color="#7022ff")
            background.rectangle((200, 100), width=400, height=3, fill="#7022ff")
            background.text(
                (200, 130),
                f"Level : {lvl}   "
                + f" XP : {xp} / {(lvl+1) * 100}",
                font=poppins_small,
                color="#7022ff",
            )
            card = File(fp=background.image_bytes, filename="Card_xp.png")
            await ctx.send(file=card)
    
    @commands.command()
    async def addcash(self, ctx, cost_add:int):

        userr = ctx.author
        
        with open("levels.json", "r") as f:
            data = json.load(f)
            
        cost = data[str(ctx.guild.id)][str(userr.id)]["cost"]
        cost=cost+cost_add
        data[str(ctx.guild.id)][str(userr.id)]["cost"]=cost
        
        with open("levels.json", "w") as f:
            json.dump(data, f,indent=4)
        await ctx.author.send(f"Tài khoản của bạn đã được cộng {cost_add:,d}") # phản hồi thông qua tin nhắn
            
    @commands.command()
    async def cash(self, ctx):
        userr = ctx.author
        with open("levels.json", "r") as f:
            data = json.load(f)
        cost = data[str(ctx.guild.id)][str(userr.id)]["cost"]
        if cost>0:
            embed=discord.Embed(title="",color=0x63ede0)
            embed.add_field(name="",value=f"💰Bạn đang có số tiền là : **{cost:,d}**")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="",color=0x63ede0)
            embed.add_field(name="",value=f"Bạn không còn tiền trong tài khoản")
            await ctx.send(embed=embed)   
    
    @commands.command()
    async def daily(self,ctx):
        userr = ctx.author
        with open("levels.json", "r") as f:
            
            data = json.load(f)
            cost_add=data[str(ctx.guild.id)][str(userr.id)]["cost"]
            bonus=random.randint(40000,50000)
            cost_add=cost_add+bonus
            
        with open("levels.json", "w") as f:
            json.dump(data, f,indent=4)
        await ctx.send(f"Ngày mới tốt lành hôm nay bạn đã nhận được **💷{bonus:,d}**")
        
        
    @commands.command()
    async def give(self,ctx, member:discord.Member|None, money:int|str ):
        if member == None:
            await ctx.send("Hãy tag tên người nhận tiền!")
            return
        else:
            if type(money) == str:
                await ctx.send("Số tiền không hợp lệ!")
                return  
        author=ctx.author
        with open("levels.json", "r") as f:
            data = json.load(f)
            
            cost_author=data[str(ctx.guild.id)][str(author.id)]["cost"]
            cost_member=data[str(ctx.guild.id)][str(member.id)]["cost"]
            
        if int(cost_author) < money:
            await ctx.send("Bạn không đủ tiền để chuyển khoản")
            return
        
        cost_author=cost_author-money
        cost_member=cost_member+money
            
        data[str(ctx.guild.id)][str(author.id)]["cost"]=cost_author
        data[str(ctx.guild.id)][str(member.id)]["cost"]=cost_member
            
        with open("levels.json", "w") as f:
            json.dump(data, f,indent=4)
        await ctx.send(f"💳|Bạn đã chuyển **{money:,d}** tiền cho {member.name}#{member.discriminator}")    
            
            
    @commands.command(aliases=['cf'])
    async def coinflip(self, ctx, check:str='h', cost_add: int|str = 1 ):
        if str(cost_add)=='all':
            cost_add=200000
        
        userr = ctx.author
        check_bot=['h','t']
        ans=random.choice(check_bot)
        with open("levels.json", "r") as f:
                    data = json.load(f)    
                    cost_user = data[str(ctx.guild.id)][str(userr.id)]["cost"]
        if cost_add > cost_user:
            await ctx.send("bạn không đủ tiền để đặt cược")
            return
        
        if check == ans:
            if ans in ['h','H'] :
                await ctx.send(f"**{userr.display_name}** Bạn đã cược **💷{cost_add:,d}** vào **Heads**")
                with open("levels.json", "r") as f:
                    data = json.load(f)
                
                cost = data[str(userr.id)]["cost"]
                cost=cost+cost_add
                data[str(ctx.guild.id)][str(userr.id)]["cost"]=cost
                with open("levels.json", "w") as f:
                    json.dump(data, f,indent=4)       
                await ctx.send(f"Kết quả là **Heads** Bạn đã nhận được **💷{cost_add:,d}**")
            elif ans in ['t','T'] :
                await ctx.send(f"**{userr.name}** Bạn đã cược  **💷{cost_add:,d}** vào **Tails**")
                with open("levels.json", "r") as f:
                    data = json.load(f)
                
                cost = data[str(ctx.guild.id)][str(userr.id)]["cost"]
                cost=cost+cost_add
                data[str(ctx.guild.id)][str(userr.id)]["cost"]=cost
                with open("levels.json", "w") as f:
                    json.dump(data, f,indent=4)       
                await ctx.send(f"Kết quả là **Tails** Bạn đã nhận được **💷{cost_add:,d}**")
        else:
            if check=='h':
                with open("levels.json", "r") as f:
                    data = json.load(f)
                    
                cost = data[str(ctx.guild.id)][str(userr.id)]["cost"]
                cost=cost-cost_add
                data[str(ctx.guild.id)][str(userr.id)]["cost"]=cost
                
                with open("levels.json", "w") as f:
                    json.dump(data, f,indent=4)    
                await ctx.send(f"**{userr.name}** Bạn đã cược  **💷{cost_add:,d}** vào **Heads**")
                await ctx.send(f"Rất tiết kết quả là **Tails** bạn đã đã mất **💷{cost_add:,d}**")
            else:
                with open("levels.json", "r") as f:
                    data = json.load(f)
                    
                cost = data[str(userr.id)]["cost"]
                cost=cost-cost_add
                data[str(userr.id)]["cost"]=cost
                
                with open("levels.json", "w") as f:
                    json.dump(data, f,indent=4)    
                await ctx.send(f"**{userr.name}** Bạn đã cược  **💷{cost_add:,d}** vào **Tails**")
                await ctx.send(f"Rất tiết kết quả là ** Heads** bạn đã đã mất **💷{cost_add:,d}**")
    
async def setup(client):
    await client.add_cog(exp(client))     """