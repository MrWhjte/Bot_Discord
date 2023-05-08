import discord
from discord.ext import commands
import json
import random
import os
import datetime
from discord import File
from typing import Optional
from easy_pil import Editor, load_image_async, Font
from discord.ext.commands import Bot, has_permissions, CheckFailure

mcoin='<:mcoin:1075257285649109012>'
class exp(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            with open("levels.json", "r") as f:
                data = json.load(f)
                if str(message.author.id) in data:
                    xp = data[str(message.author.id)]['xp']
                    lvl = data[str(message.author.id)]['level']
                    
                    increased_xp = xp + random.randint(10,20) #tăng giá trị điểm ngẫu nhiên
                    level_up = int(increased_xp/100)   #lấy số nguyên dương
                    
                    data[str(message.author.id)]['xp']=increased_xp
                    
                    with open("levels.json", "w") as f:
                        json.dump(data, f,indent=4)
            
                    if lvl < level_up:
                        await message.channel.send(f"{message.author.mention} bạn đã lên lv {level_up}!!!",delete_after=8)
                        data[str(message.author.id)]['level']=level_up
                        data[str(message.author.id)]['xp']=random.randint(10,20)
                        cost=data[str(message.author.id)]['cost']
                        cost+=10000
                        data[str(message.author.id)]['cost']=cost
                        
                        with open("levels.json", "w") as f:
                            json.dump(data, f,indent=4)
                else:
                    data[str(message.author.id)] = {}
                    data[str(message.author.id)]['xp'] = 0
                    data[str(message.author.id)]['level'] = 1
                    data[str(message.author.id)]['cost']=10000
                    
            with open("levels.json", "w") as f:
                json.dump(data, f,indent=4)

    @commands.command()
    async def topxp(self, ctx, range_num:int = 5):
        if range_num > 20:
            range_num=20

        with open("levels.json", "r") as f:
            data = json.load(f)

        l = {}
        total_coin = []
        for userid in data:
            xp = int(data[str(userid)]['xp'] + (int(data[str(userid)]['level'])*100)) # tổng xp đã nhận dc
            l[xp] = f"{userid};{data[str(userid)]['level']};{data[str(userid)]['xp']}"
            total_coin.append(xp)

        total_coin = sorted(total_coin, reverse=True)
        index=1

        embed = discord.Embed(title="",color=0xc6e15b)
        embed.set_author(name="Bảng vàng Mit Con",icon_url=ctx.guild.icon)
        for amt in total_coin:
            id_ = int(str(l[amt]).split(";")[0])
            level = int(str(l[amt]).split(";")[1])
            xp = int(str(l[amt]).split(";")[2])
            
            member = await self.client.fetch_user(id_)
            
            if member is not None:
                embed.add_field(name=f"",value=f"`{index}`|**{member.name}**(Level:**{level}**-XP:**{xp}**)",inline=False)
                if index == range_num:
                    break
                else:
                    index += 1
        await ctx.send(embed = embed)
    
    @commands.command()
    async def topcoin(self, ctx, range_num:int = 5):
        if range_num > 20:
            range_num=20

        with open("levels.json", "r") as f:
            data = json.load(f)

        l = {}
        total_coin = []

        for userid in data:
            coin = int(data[str(userid)]['cost']) 
            l[coin] = f"{userid};{data[str(userid)]['cost']}"
            total_coin.append(coin)

        total_coin = sorted(total_coin, reverse=True)
        index=1

        embed = discord.Embed(title="",color=0xc6e15b)
        embed.set_author(name="Đại Gia Mitcoin",icon_url=ctx.guild.icon)
        for amt in total_coin: 
            id_ = int(str(l[amt]).split(";")[0])
            coin = int(str(l[amt]).split(";")[1])

            member = await self.client.fetch_user(id_)
            
            if member is not None:
                embed.add_field(name="",value=f"`{index}`|**{member.name}** | coin : **{coin:,d}**",inline=False)
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
            profile = Editor(profile).resize((160, 160)).circle_image()

            poppins = Font.poppins(size=45)
            poppins_small = Font.poppins(size=35)

            background.paste(profile.image, (20, 30))

            background.rectangle((20, 220), width=580, height=40, fill="#fff", radius=20)
            background.bar(
                (20, 220),
                max_width=550,
                height=40,
                percentage=percentage,
                fill="#74ff7c",
                radius=20,
            )
            
            t=(lvl+1)*100
            if 1000< t <999999 : #100.000 1.000 10.000
                exp_rank=f"{round((t/1000),1)}K"
            elif t > 1000000  :
                exp_rank=f"{round((t/1000000),1)}M"
            else :
               exp_rank=(lvl+1)*100
            
            t_xp=xp
            if 1000< t_xp <999999 : #100.000 1.000 10.000
                xp_rank=f"{round((t_xp/1000),1)}K"
            elif t_xp > 1000000  :
                xp_rank=f"{round((t_xp/1000000),1)}M"
            else :
               xp_rank=xp
            name_id=f"{str(userr.name)}#{userr.discriminator}"
            background.text((200, 40), name_id, font=poppins, color="#7022ff") #tên
            background.rectangle((200, 100), width=400, height=3, fill="#7022ff") #kẻ ngang
            background.text(
                (200, 130),
                f"Level : {lvl}  "
                + f" XP : {xp_rank} / {exp_rank}",
                font=poppins_small,
                color="#7022ff",
            )# chỉ số
            card = File(fp=background.image_bytes, filename="Card_xp.png")
            await ctx.send(file=card)
    
    
               
    @commands.command()
    async def cash(self, ctx):
        userr = ctx.author
        with open("levels.json", "r") as f:
            data = json.load(f)
        cost = data[str(userr.id)]["cost"]
        if cost>0:
            await ctx.send(f"**{mcoin} | {userr.name}**, Bạn đang có **{cost:,d} Mitcoin!**")
        else:
            value=f"{mcoin} | **{userr.name}**, Bạn đang có **{cost:,d} Mitcoin!**"
            await ctx.send(value)
            await ctx.send("``Có thể bạn đã biết: lệnh daily sẽ cho bạn 1 số tiền vào mỗi ngày đấy!!``")
            
    
    @commands.command()
    @commands.cooldown(1, 60*60*24, commands.BucketType.user)
    async def daily(self,message):
        with open("levels.json", "r") as f:
            data = json.load(f)
            
            cost_add=data[str(message.author.id)]["cost"]
            bonus=random.randint(10000,20000)
            
            data[str(message.author.id)]["cost"]=(bonus+cost_add)
            with open("levels.json","w") as f:
                json.dump(data, f,indent=4)
            await message.send(f"Ngày mới tốt lành hôm nay bạn đã nhận được **{mcoin}{bonus:,d} Mitcoin**")
       
    @daily.error
    async def cooldown_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            per=int(error.retry_after)
            gio=per%86400//3600
            phut=per%86400%3600//60
            giay=per%86400%3600%60
            
            hour=f"{gio}:{phut}:{giay}" # 12:34:65
            msg=f"**⏲ | **Bạn đã nhận thưởng ngày hôm nay hãy quay lại sau **{hour}**"
            await ctx.send(msg)             
                
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
            
            cost_author=data[str(author.id)]["cost"]
            cost_member=data[str(member.id)]["cost"]
            
        if int(cost_author) < money:
            await ctx.send("Bạn không đủ tiền để chuyển khoản")
            return
        
        cost_author=cost_author-money
        cost_member=cost_member+money
            
        data[str(author.id)]["cost"]=cost_author
        data[str(member.id)]["cost"]=cost_member
            
        with open("levels.json", "w") as f:
            json.dump(data, f,indent=4)
        await ctx.send(f"**💳 | **Bạn đã chuyển **{money:,d} Mitcoin ** cho {member.name}#{member.discriminator}")
        
    @commands.command()
    async def ac(self,ctx, member:discord.Member|None, money:int):
        if member == None:
            await ctx.send("Hãy tag tên người nhận tiền!")
            return
        else:
            if type(money) == str:
                await ctx.send("Số tiền không hợp lệ!")
                return   
        author = ctx.author
        with open("levels.json", "r") as f:
            data = json.load(f)
        
        cost_member=data[str(member.id)]["cost"] 
        IdAuthor=author.id
        if(IdAuthor!=755412019351519284):
            await ctx.send('Bạn không đủ điều kiện sử dụng lệnh này')
        else:
            cost_member=cost_member+money
            data[str(member.id)]["cost"]=cost_member
            user = self.client.get_user(member.id)
            await user.send(f"**💳 | ** **{member.name}#{member.discriminator}** Bạn đã nhận được **{money:,d} Mitcoin ** từ bụt")
            # await ctx.send(f"**💳 | ** {member.name}#{member.discriminator} Bạn đã nhận được**{money:,d} Mitcoin ** từ bụt")
        with open("levels.json", "w") as f:
                json.dump(data, f,indent=4)
             
        
    @commands.command()
    async def sc(self,ctx, member:discord.Member|None, money:int):
        if member == None:
            await ctx.send("Hãy tag tên người bạn muốn trừ tiền!")
            return
        else:
            if type(money) == str:
                await ctx.send("Số tiền không hợp lệ!")
                return
        
        author = ctx.author
        with open("levels.json", "r") as f:
            data = json.load(f)
        
        cost_member=data[str(member.id)]["cost"] 
        
        IdAuthor=author.id
        if(IdAuthor!=755412019351519284):
            await ctx.send('Bạn không đủ điều kiện sử dụng lệnh này')
        else:
            cost_member=cost_member-money
            data[str(member.id)]["cost"]=cost_member
            user=self.client.get_user(member.id)
            await user.send(f"**💳 | ** **{member.name}#{member.discriminator}** Bạn đã bị bụt phạt **{money:,d} Mitcoin **")
            # await ctx.send(f"**💳 | ** {member.name}#{member.discriminator} Bạn đã bị bụt phạt **{money:,d} Mitcoin **")   
        with open("levels.json", "w") as f:
                json.dump(data, f,indent=4)
        
async def setup(client):
    await client.add_cog(exp(client))    