import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot, CheckFailure
import json

mcoin='<:mcoin:1075257285649109012>'

class game(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def loto(self,ctx):
        embed=discord.Embed(title="Trò chơi lô tô",color=0x21f531)
        embed.add_field(name=f'{ctx.author} bạn đã nhận được 1 vé để chơi lô tô',value="")
        embed.set_image(url='https://cdn.discordapp.com/attachments/1065567041362329620/1095963594375565412/zIMAGE.png')
        await ctx.send(embed=embed)
  
        
    @commands.command(aliases=["rand","random"])
    async def roll(self,ctx,min:int, max: int|None):
        if max is None:
            max = min
            min=0
        if min > max:
            t=max
            max=min
            min=t       
        n=random.randint(min,max)
        await ctx.send(f"**:game_die: | **Con số may mắn: {n}")

    @commands.command(aliases=["tinh"])
    async def math(self,ctx,exp:str):
        check=['+','-','*','/','%',]
        if any(s in exp for s in check):
            caculator = eval(exp)
        else:
            await ctx.send(f"**{exp}** Không phải là 1 biểu thức toán học")
        embed=discord.Embed(title="Kết quả",color=0xe4ec6f)
        embed.add_field(name="",value=f" **Phép tính:** {exp}",inline=False)
        embed.add_field(name="",value=f"**Kết quả:** {caculator}",inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['game'])
    async def doanso(self,ctx, max:int=10):
        max_step = 100
        number=random.randint(1,max)
        await ctx.send(f"{ctx.author.name} Game đã bắt đầu!\nHãy đoán 1 con số nằm trong khoảng từ **1-{max}**")
        def check(n):
            return n.author == ctx.author and n.channel == ctx.message.channel
        for i in range(max_step):
            doan = await   self.client.wait_for('message',check=check)
            try:
                int(doan.content)
                if doan.content == str(number):
                    await ctx.send(f":confetti_ball: BingGo!{format(ctx.message.author.mention)} Bạn đã đoán trúng với **{i+1}** lần đoán")
                    break
                elif doan.content <= str(number):
                    await ctx.send("Lớn hơn 1 chút!")
                elif doan.content >= str(number):
                    await ctx.send("Nhỏ hơn 1 chút!")
                else:
                    ctx.send("nhập sai dữ liệu")
            except:
                await ctx.send(f"Đáp án được chấp nhận là **Số** và < **{max}**") 
        else: 
            await ctx.send(f"Kết thúc game bạn đã nhập sai tối đa {max_step} lần")
            
    @doanso.error
    async def error_text(self,ctx,error):
        if isinstance(error,commands.BadArgument):
            msg=f"Hãy nhập 1 con số"
            await ctx.send(msg)
    
    @commands.command(aliases=['xx'])
    async def xucxac(self,ctx):
        check=['Xấp','Ngữa']
        ans=random.choice(check)
        embed=discord.Embed(title=f"Tung đồng xu : ",color=0xe4ec6f)
        embed.add_field(name=f"Kết quả: ",value=f"**{ans}**")
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['cf'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coinflip(self, ctx, check:str='h', cost_add: str|int = 1 ):
        if str(cost_add)=='all':
            cost_add=200000
        userr = ctx.author
        check_bot=['h','t']
        ans=random.choice(check_bot)
        with open("levels.json", "r") as f:
                    data = json.load(f)    
                    cost_user = data[str(userr.id)]["cost"]
        if cost_add > cost_user:
            await ctx.send("bạn không đủ tiền để đặt cược")
            return
        if check == ans:
            if ans in ['h','H'] :
                await ctx.send(f"**{userr.display_name}** Bạn đã cược **💷{cost_add:,d} Mitcoin** vào **Heads**")
                with open("levels.json", "r") as f:
                    data = json.load(f)
                
                cost = data[str(userr.id)]["cost"]
                cost=cost+cost_add
                data[str(userr.id)]["cost"]=cost
                with open("levels.json", "w") as f:
                    json.dump(data, f,indent=4)       
                await ctx.send(f"Kết quả là **🪙Heads** Bạn đã nhận được **💷{cost_add:,d} Mitcoin**")
            elif ans in ['t','T'] :
                await ctx.send(f"**{userr.name}** Bạn đã cược  **💷{cost_add:,d} Mitcoin** vào **Tails**")
                with open("levels.json", "r") as f:
                    data = json.load(f)
                
                cost = data[str(userr.id)]["cost"]
                cost=cost+cost_add
                data[str(userr.id)]["cost"]=cost
                with open("levels.json", "w") as f:
                    json.dump(data, f,indent=4)       
                await ctx.send(f"Kết quả là **🪙Tails** Bạn đã nhận được **💷{cost_add:,d} Mitcoin**")
        else:
            if check=='h':
                with open("levels.json", "r") as f:
                    data = json.load(f)
                    
                cost = data[str(userr.id)]["cost"]
                cost=cost-cost_add
                data[str(userr.id)]["cost"]=cost
                
                with open("levels.json", "w") as f:
                    json.dump(data, f,indent=4)    
                await ctx.send(f"**{userr.name}** Bạn đã cược  **💷{cost_add:,d} Mitcoin** vào **Heads**")
                await ctx.send(f"**Rất tiết**  kết quả là **🪙Tails** bạn đã đã mất **💷{cost_add:,d} Mitcoin**")
            else:
                with open("levels.json", "r") as f:
                    data = json.load(f)
                    
                cost = data[str(userr.id)]["cost"]
                cost=cost-cost_add
                data[str(userr.id)]["cost"]=cost
                
                with open("levels.json", "w") as f:
                    json.dump(data, f,indent=4)    
                await ctx.send(f"**{userr.name}** Bạn đã cược  **💷{cost_add:,d} Mitcoin** vào **Tails**")
                await ctx.send(f"**Rất tiết** kết quả là **🪙Heads** bạn đã đã mất **💷{cost_add:,d} Mitcoin**")
    @coinflip.error
    async def cooldown_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            msg=f"**⏳ | **Bạn sử dụng bot hơi nhanh rồi! thử lại sau `{int(error.retry_after)}s`"
            await ctx.send(msg,delete_affter=5)
                        
    @commands.command(aliases=["bj"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def blackjack(self,ctx,money:int|str=1):
        member=ctx.author
        if str(money)=='all':
            money=200000
        with open("levels.json", "r") as f:
                    data = json.load(f)    
                    cost_user = data[str(member.id)]["cost"]
        if money > cost_user:
            await ctx.send("Bạn không đủ tiền để đặt cược")

        idcard=("<:ba1:1073818900141191178>",
                "<:ba4:1073818920240304179>",
                "<:ba3:1073818915249062038>",
                "<:ba2:1073818907753861200>",
                "<:thy4:1073819913497608325>",
                "<:thy3:1073819905981435976>",
                "<:thy2:1073819898842710056>",
                "<:thy1:1073819893327208519>") # lấy id thẻ
        bimat=("<:bimat10:1073831379554533418>")
        
        la1_bot=random.randint(2,11)
        la1_nguoi=random.randint(2,11)
        
        la2_bot=random.randint(2,11)
        la2_nguoi=random.randint(2,11)
        
        tong2la_bot=la2_bot+la2_bot
        tong2la_nguoi=la1_nguoi+la2_nguoi
        
        la3_bot=random.randint(2,11)
        la3_nguoi=random.randint(2,11)
        
        la4_bot=random.randint(2,11)
        la4_nguoi=random.randint(2,11)
        
        tong3la_bot   = tong2la_bot+la3_bot
        tong3la_nguoi = tong2la_nguoi+la3_nguoi
        
        tong4la_bot=tong3la_bot+la4_bot
        tong4la_nguoi=tong3la_nguoi+la4_nguoi
        
        idbot1=random.choice(idcard)
        idbot2=random.choice(idcard)
        idbot3=random.choice(idcard)
        idbot4=random.choice(idcard)
        iduser1=random.choice(idcard)
        iduser2=random.choice(idcard)
        iduser3=random.choice(idcard)
        iduser4=random.choice(idcard)
        
        if tong2la_nguoi==tong2la_bot==22:
            embed=discord.Embed(title="",color=0xd8ef59) #0xd8ef59 vàng
            embed.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
            embed.add_field(name=f"Bot [21]",value=f"{idbot1}{idbot2}",inline=False)
            embed.add_field(name=f"Bạn [21]",value=f"{iduser1}{iduser2}",inline=False)
            embed.set_footer(text=f"2 bên bằng điểm ván này hòa")
            check=1
        elif tong2la_bot==22:
            embed=discord.Embed(title="",color=0xf31126) #0xf31126 đỏ
            embed.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
            embed.add_field(name=f"Bot [21]",value=f"{idbot1}{idbot2}",inline=False)
            embed.add_field(name=f"Bạn {[tong2la_nguoi]}",value=f"{iduser1}{iduser2}",inline=False)
            embed.set_footer(text=f"Cái 21 điểm bạn thua {money:,d}")
            check=1
            with open("levels.json", "r") as f:
                data = json.load(f)
                
                cost_user = data[str(member.id)]["cost"]
                cost_user = cost_user- money
                data[str(member.id)]["cost"]=cost_user
                        
            with open("levels.json", "w") as f:
                json.dump(data, f,indent=4)
                  
        elif tong2la_nguoi==21:
            embed=discord.Embed(title="",color=0x2cf932) #0x2cf932 xanh
            embed.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
            embed.add_field(name=f"Bot [{tong2la_bot}]",value=f"{idbot2}{idbot1}",inline=False)
            embed.add_field(name=f"Bạn [21]",value=f"{iduser1}{iduser2}",inline=False)
            embed.set_footer(text=f"Bạn 21 điểm bạn thắng {money:,d}")
            check=1
            with open("levels.json", "r") as f:
                data = json.load(f)
                
                cost_user = data[str(member.id)]["cost"]
                cost_user = cost_user + money
                data[str(member.id)]["cost"]=cost_user
                        
            with open("levels.json", "w") as f:
                json.dump(data, f,indent=4)
        elif tong2la_nguoi==22:
            embed=discord.Embed(title="",color=0x2cf932) #0x2cf932 xanh
            embed.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
            embed.add_field(name=f"Bot [{tong2la_bot}]",value=f"{idbot2}{idbot1}",inline=False)
            embed.add_field(name=f"Bạn [21]",value=f"{iduser1}{iduser2}",inline=False)
            embed.set_footer(text=f"Bạn 21 điểm bạn thắng {money:,d}")
            check=1
            with open("levels.json", "r") as f:
                data = json.load(f)
                
                cost_user = data[str(member.id)]["cost"]
                cost_user = cost_user + money
                data[str(member.id)]["cost"]=cost_user
                        
            with open("levels.json", "w") as f:
                json.dump(data, f,indent=4)
        elif  tong2la_bot==21:
            embed=discord.Embed(title="",color=0xf31126) #0xf31126 đỏ
            embed.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
            embed.add_field(name=f"Bot [21]",value=f"{idbot1}{idbot2}",inline=False)
            embed.add_field(name=f"Bạn [{tong2la_nguoi}]",value=f"{iduser1}{iduser2}",inline=False)
            embed.set_footer(text=f"Cái 21 điểm bạn thua {money:,d}")
            check=1
            with open("levels.json", "r") as f:
                data = json.load(f)
                
                cost_user = data[str(member.id)]["cost"]
                cost_user = cost_user - money
                data[str(member.id)]["cost"]=cost_user
                        
            with open("levels.json", "w") as f:
                json.dump(data, f,indent=4)
        else:        
            embed=discord.Embed(title="",color=0x2cf932) #0xf31126 đỏ
            embed.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
            embed.add_field(name=f"Bot {la1_bot}+[?]",value=f"{bimat}{idbot2}",inline=False)
            embed.add_field(name=f"Bạn [{tong2la_nguoi}]",value=f"{iduser1}{iduser2}",inline=False)
            embed.set_footer(text="Đang chơi")
            check=0
           
        class blacjackbutton(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=15)
            @discord.ui.button(label="Dằn dơ",style=discord.ButtonStyle.red, emoji="✋")
            async def dan_do(self,Interaction:discord.Interaction,button:discord.ui.Button):
                if tong2la_bot<16:
                    if tong3la_bot>21:
                        embed1=discord.Embed(title="",colour=0x2cf932)
                        embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                        embed1.add_field(name=f"Bot [{tong3la_bot}]",value=f"{idbot1}{idbot2}{idbot3}",inline=False)
                        embed1.add_field(name=f"Bạn [{tong2la_nguoi}]",value=f"{iduser1}{iduser2}",inline=False)
                        embed1.set_footer(text=f"Bạn thắng {money:,d}")
                        with open("levels.json", "r") as f:
                            data = json.load(f)
                            
                            cost_user = data[str(member.id)]["cost"]
                            cost_user = cost_user + money
                            data[str(member.id)]["cost"]=cost_user
                                    
                        with open("levels.json", "w") as f:
                            json.dump(data, f,indent=4)
                        await Interaction.message.edit(embed=embed1,view=None)
                    else:# tông 3 lá bot <21
                        if tong3la_bot<15:
                            if  tong4la_bot<tong2la_nguoi:
                                embed1=discord.Embed(title="",colour=0x2cf932)
                                embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                embed1.add_field(name=f"Bot [{tong4la_bot}]",value=f"{idbot1}{idbot2}{idbot3}{idbot4}",inline=False)
                                embed1.add_field(name=f"Bạn [{tong2la_nguoi}]",value=f"{iduser1}{iduser2}",inline=False)
                                embed1.set_footer(text=f"Bạn thắng {money:,d}")
                                with open("levels.json", "r") as f:
                                    data = json.load(f)
                                    
                                    cost_user = data[str(member.id)]["cost"]
                                    cost_user = cost_user + money
                                    data[str(member.id)]["cost"]=cost_user
                                        
                                with open("levels.json", "w") as f:
                                    json.dump(data, f,indent=4)
                                await Interaction.message.edit(embed=embed1,view=None)
                            elif tong4la_bot>tong2la_nguoi:
                                embed1=discord.Embed(title="",colour=0xf31126)
                                embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                embed1.add_field(name=f"Bot [{tong4la_bot}]",value=f"{idbot1}{idbot2}{idbot3}{idbot4}",inline=False)
                                embed1.add_field(name=f"Bạn [{tong2la_nguoi}]",value=f"{iduser1}{iduser2}",inline=False)
                                embed1.set_footer(text=f"Bạn thua {money:,d}")
                                with open("levels.json", "r") as f:
                                    data = json.load(f)
                                    
                                    cost_user = data[str(member.id)]["cost"]
                                    cost_user = cost_user - money
                                    data[str(member.id)]["cost"]=cost_user
                                            
                                with open("levels.json", "w") as f:
                                    json.dump(data, f,indent=4)
                                await Interaction.message.edit(embed=embed1,view=None)
                            else:
                                embed1=discord.Embed(title="",colour=0xd8ef59)
                                embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                embed1.add_field(name=f"Bot [{tong4la_bot}]",value=f"{idbot1}{idbot2}{idbot3}{idbot4}",inline=False)
                                embed1.add_field(name=f"Bạn [{tong2la_nguoi}]",value=f"{iduser1}{iduser2}",inline=False)
                                embed1.set_footer(text=f"Cả 2 bằng điểm ván này hòa")
                                await Interaction.message.edit(embed=embed1,view=None)    
                        else:#tong3la_bot>15:
                            if tong2la_nguoi>tong3la_bot:
                                embed1=discord.Embed(title="",colour=0x2cf932)
                                embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                embed1.add_field(name=f"Bot [{tong3la_bot}]",value=f"{idbot1}{idbot2}{idbot3}",inline=False)
                                embed1.add_field(name=f"Bạn [{tong2la_nguoi}]",value=f"{iduser1}{iduser2}",inline=False)
                                embed1.set_footer(text=f"Bạn thắng {money:,d}")
                                with open("levels.json", "r") as f:
                                    data = json.load(f)
                                    
                                    cost_user = data[str(member.id)]["cost"]
                                    cost_user = cost_user + money
                                    data[str(member.id)]["cost"]=cost_user
                                        
                                with open("levels.json", "w") as f:
                                    json.dump(data, f,indent=4)
                                await Interaction.message.edit(embed=embed1,view=None) 
                            elif tong2la_nguoi<tong3la_bot:
                                embed1=discord.Embed(title="",colour=0xf31126)
                                embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                embed1.add_field(name=f"Bot [{tong3la_bot}]",value=f"{idbot1}{idbot2}{idbot3}",inline=False)
                                embed1.add_field(name=f"Bạn [{tong2la_nguoi}]",value=f"{iduser1}{iduser2}",inline=False)
                                embed1.set_footer(text=f"Bạn thua {money:,d}")
                                with open("levels.json", "r") as f:
                                    data = json.load(f)
                                    
                                    cost_user = data[str(member.id)]["cost"]
                                    cost_user = cost_user - money
                                    data[str(member.id)]["cost"]=cost_user
                                            
                                with open("levels.json", "w") as f:
                                    json.dump(data, f,indent=4)
                                await Interaction.message.edit(embed=embed1,view=None) 
                            else:
                                embed1=discord.Embed(title="",colour=0xd8ef59)
                                embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                embed1.add_field(name=f"Bot [{tong3la_bot}]",value=f"{idbot1}{idbot2}{idbot3}",inline=False)
                                embed1.add_field(name=f"Bạn [{tong2la_nguoi}]",value=f"{iduser1}{iduser2}",inline=False)
                                embed1.set_footer(text=f"Cả 2 bằng điểm ván này hòa")
                                await Interaction.message.edit(embed=embed1,view=None)        
                else:   # 2 la bot >16
                    if tong2la_bot>tong2la_nguoi:
                        embed1=discord.Embed(title="",colour=0xf31126)
                        embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                        embed1.add_field(name=f"Bot [{tong2la_bot}]",value=f"{idbot1}{idbot2}",inline=False)
                        embed1.add_field(name=f"Bạn [{tong2la_nguoi}]",value=f"{iduser1}{iduser2}",inline=False)
                        embed1.set_footer(text=f"Bạn thua {money:,d}")
                        with open("levels.json", "r") as f:
                                data = json.load(f)
                                
                                cost_user = data[str(member.id)]["cost"]
                                cost_user = cost_user - money
                                data[str(member.id)]["cost"]=cost_user
                                        
                        with open("levels.json", "w") as f:
                            json.dump(data, f,indent=4)
                        await Interaction.message.edit(embed=embed1,view=None)      
                    elif tong2la_bot<tong2la_nguoi:
                        embed1=discord.Embed(title="",colour=0x2cf932)
                        embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                        embed1.add_field(name=f"Bot [{tong2la_bot}]",value=f"{idbot1}{idbot2}",inline=False)
                        embed1.add_field(name=f"Bạn [{tong2la_nguoi}]",value=f"{iduser1}{iduser2}",inline=False)
                        embed1.set_footer(text=f"Bạn thắng {money:,d}")
                        with open("levels.json", "r") as f:
                            data = json.load(f)
                            
                            cost_user = data[str(member.id)]["cost"]
                            cost_user = cost_user + money
                            data[str(member.id)]["cost"]=cost_user
                                    
                        with open("levels.json", "w") as f:
                            json.dump(data, f,indent=4)
                        await Interaction.message.edit(embed=embed1,view=None) 
                    else:
                        embed1=discord.Embed(title="",colour=0xd8ef59)
                        embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                        embed1.add_field(name=f"Bot [{tong2la_bot}]",value=f"{idbot1}{idbot2}",inline=False)
                        embed1.add_field(name=f"Bạn [{tong2la_nguoi}]",value=f"{iduser1}{iduser2}",inline=False)
                        embed1.set_footer(text=f"Cả 2 bằng điểm ván này hòa")
                        await Interaction.message.edit(embed=embed1,view=None)
                        
            @discord.ui.button(label="Rút bài",style=discord.ButtonStyle.green, emoji=f"{bimat}")
            async def rut(self,Interaction:discord.Interaction,button:discord.ui.Button):
                if tong2la_bot < 16:
                    if tong3la_bot > 21: 
                        if tong3la_nguoi<=21:# thêm điều kiện rút lá thứ 4 ở đây
                            embed1=discord.Embed(title="",colour=0x2cf932)
                            embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                            embed1.add_field(name=f"Bot [{tong3la_bot}]",value=f"{idbot1}{idbot2}{idbot3}",inline=False)
                            embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                            embed1.set_footer(text=f"Bạn thắng {money:,d}")
                            with open("levels.json", "r") as f:
                                data = json.load(f)
                                
                                cost_user = data[str(member.id)]["cost"]
                                cost_user = cost_user + money
                                data[str(member.id)]["cost"]=cost_user
                                        
                            with open("levels.json", "w") as f:
                                json.dump(data, f,indent=4)
                            await Interaction.message.edit(embed=embed1,view=None)
                        else:
                            embed1=discord.Embed(title="",colour=0xd8ef59)
                            embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                            embed1.add_field(name=f"Bot [{tong3la_bot}]",value=f"{idbot1}{idbot2}{idbot3}",inline=False)
                            embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                            embed1.set_footer(text=f"Ván này hòa")
                            await Interaction.message.edit(embed=embed1,view=None)    
                    else:# tong 3 la bot <= 21
                        if tong3la_nguoi<=21:
                            if tong3la_bot<15:
                                if  tong4la_bot<tong3la_nguoi:
                                    embed1=discord.Embed(title="",colour=0x2cf932)
                                    embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                    embed1.add_field(name=f"Bot [{tong4la_bot}]",value=f"{idbot1}{idbot2}{idbot3}{idbot4}",inline=False)
                                    embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                                    embed1.set_footer(text=f"Bạn thắng {money:,d}")
                                    with open("levels.json", "r") as f:
                                        data = json.load(f)
                                        
                                        cost_user = data[str(member.id)]["cost"]
                                        cost_user = cost_user + money
                                        data[str(member.id)]["cost"]=cost_user
                                            
                                    with open("levels.json", "w") as f:
                                        json.dump(data, f,indent=4)
                                    await Interaction.message.edit(embed=embed1,view=None)
                                elif tong4la_bot>tong3la_nguoi:
                                    embed1=discord.Embed(title="",colour=0xf31126)
                                    embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                    embed1.add_field(name=f"Bot [{tong4la_bot}]",value=f"{idbot1}{idbot2}{idbot3}{idbot4}",inline=False)
                                    embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                                    embed1.set_footer(text=f"Bạn thua {money:,d}")
                                    with open("levels.json", "r") as f:
                                        data = json.load(f)
                                        
                                        cost_user = data[str(member.id)]["cost"]
                                        cost_user = cost_user - money
                                        data[str(member.id)]["cost"]=cost_user
                                                
                                    with open("levels.json", "w") as f:
                                        json.dump(data, f,indent=4)
                                    await Interaction.message.edit(embed=embed1,view=None)
                                else:
                                    embed1=discord.Embed(title="",colour=0xd8ef59)
                                    embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                    embed1.add_field(name=f"Bot [{tong4la_bot}]",value=f"{idbot1}{idbot2}{idbot3}{idbot4}",inline=False)
                                    embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                                    embed1.set_footer(text=f"Cả 2 bằng điểm ván này hòa")
                                    await Interaction.message.edit(embed=embed1,view=None)
                            else:#
                                if tong3la_nguoi <= 21:
                                    if tong3la_nguoi < tong3la_bot:
                                        embed1=discord.Embed(title="",colour=0xf31126)
                                        embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                        embed1.add_field(name=f"Bot [{tong3la_bot}]",value=f"{idbot1}{idbot2}{idbot3}",inline=False)
                                        embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                                        embed1.set_footer(text=f"Bạn thua {money:,d}")
                                        with open("levels.json", "r") as f:
                                            data = json.load(f)
                                            
                                            cost_user = data[str(member.id)]["cost"]
                                            cost_user = cost_user - money
                                            data[str(member.id)]["cost"]=cost_user
                                                    
                                        with open("levels.json", "w") as f:
                                            json.dump(data, f,indent=4)
                                        await Interaction.message.edit(embed=embed1,view=None) 
                                    elif tong3la_nguoi > tong3la_bot:
                                        embed1=discord.Embed(title="",colour=0x2cf932)
                                        embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                        embed1.add_field(name=f"Bot [{tong3la_bot}]",value=f"{idbot1}{idbot2}{idbot3}",inline=False)
                                        embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                                        embed1.set_footer(text=f"Bạn thắng {money:,d}")
                                        with open("levels.json", "r") as f:
                                            data = json.load(f)
                                            
                                            cost_user = data[str(member.id)]["cost"]
                                            cost_user = cost_user + money
                                            data[str(member.id)]["cost"]=cost_user
                                                    
                                        with open("levels.json", "w") as f:
                                            json.dump(data, f,indent=4)
                                        await Interaction.message.edit(embed=embed1,view=None)
                                    else:    
                                        embed1=discord.Embed(title="",colour=0xd8ef59)
                                        embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                        embed1.add_field(name=f"Bot [{tong3la_bot}]",value=f"{idbot1}{idbot2}{idbot3}",inline=False)
                                        embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                                        embed1.set_footer(text=f"Cả 2 bằng điểm ván này hòa")
                                        await Interaction.message.edit(embed=embed1,view=None)
                        else:#tong3la_nguoi>21: tong 3 la bot <21
                            embed1=discord.Embed(title="",colour=0xf31126)
                            embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                            embed1.add_field(name=f"Bot [{tong3la_bot}]",value=f"{idbot1}{idbot2}{idbot3}",inline=False)
                            embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                            embed1.set_footer(text=f"Bạn thua {money:,d}")
                            with open("levels.json", "r") as f:
                                data = json.load(f)
                                
                                cost_user = data[str(member.id)]["cost"]
                                cost_user = cost_user - money
                                data[str(member.id)]["cost"]=cost_user
                                        
                            with open("levels.json", "w") as f:
                                json.dump(data, f,indent=4)
                            await Interaction.message.edit(embed=embed1,view=None)
                else:#tong2la_bot>16: bot chỉ có 2 lá
                    if tong2la_bot<21: #
                        if tong3la_nguoi>21: # 
                            embed1=discord.Embed(title="",colour=0xf31126)
                            embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                            embed1.add_field(name=f"Bot [{tong2la_bot}]",value=f"{idbot1}{idbot2}",inline=False)
                            embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                            embed1.set_footer(text=f"Bạn thua {money:,d}")
                            with open("levels.json", "r") as f:
                                data = json.load(f)
                                
                                cost_user = data[str(member.id)]["cost"]
                                cost_user = cost_user - money
                                data[str(member.id)]["cost"]=cost_user
                                        
                            with open("levels.json", "w") as f:
                                json.dump(data, f,indent=4)
                            await Interaction.message.edit(embed=embed1,view=None)
                        else:#tong 3 la nguoi <21
                            if tong3la_nguoi < tong2la_bot:
                                embed1=discord.Embed(title="",colour=0xf31126)
                                embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                embed1.add_field(name=f"Bot [{tong2la_bot}]",value=f"{idbot1}{idbot2}",inline=False)
                                embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                                embed1.set_footer(text=f"Bạn thua {money:,d}")
                                with open("levels.json", "r") as f:
                                    data = json.load(f)
                                    
                                    cost_user = data[str(member.id)]["cost"]
                                    cost_user = cost_user - money
                                    data[str(member.id)]["cost"]=cost_user
                                            
                                with open("levels.json", "w") as f:
                                    json.dump(data, f,indent=4)
                                await Interaction.message.edit(embed=embed1,view=None)
                            elif tong3la_nguoi > tong2la_bot:
                                embed1=discord.Embed(title="",colour=0x2cf932)
                                embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                embed1.add_field(name=f"Bot [{tong2la_bot}]",value=f"{idbot1}{idbot2}",inline=False)
                                embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                                embed1.set_footer(text=f"Bạn thắng {money:,d}")
                                with open("levels.json", "r") as f:
                                    data = json.load(f)
                                    
                                    cost_user = data[str(member.id)]["cost"]
                                    cost_user = cost_user + money
                                    data[str(member.id)]["cost"]=cost_user
                                            
                                with open("levels.json", "w") as f:
                                    json.dump(data, f,indent=4)
                                await Interaction.message.edit(embed=embed1,view=None)
                            else:
                                embed1=discord.Embed(title="",colour=0xd8ef59)
                                embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                                embed1.add_field(name=f"Bot [{tong2la_bot}]",value=f"{idbot1}{idbot2}",inline=False)
                                embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                                embed1.set_footer(text=f"Cả 2 bằng điểm ván này hòa")
                                await Interaction.message.edit(embed=embed1,view=None)
                    else:#tong 2 la bot = 21
                        if tong3la_nguoi == tong2la_bot:
                            embed1=discord.Embed(title="",colour=0x2cf932)
                            embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                            embed1.add_field(name=f"Bot [{tong2la_bot}]",value=f"{idbot1}{idbot2}",inline=False)
                            embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                            embed1.set_footer(text=f"Cả 2 bằng điểm ván này hòa")
                            await Interaction.message.edit(embed=embed1,view=None)
                        else:
                            embed1=discord.Embed(title="",colour=0xf31126)
                            embed1.set_author(name=f"{member.name} Bạn đã cược {money:,d} để chơi xì dách",icon_url=member.avatar)
                            embed1.add_field(name=f"Bot [{tong2la_bot}]",value=f"{idbot1}{idbot2}",inline=False)
                            embed1.add_field(name=f"Bạn [{tong3la_nguoi}]",value=f"{iduser1}{iduser2}{iduser3}",inline=False)
                            embed1.set_footer(text=f"Bạn thua {money:,d}")
                            with open("levels.json", "r") as f:
                                data = json.load(f)
                                
                                cost_user = data[str(member.id)]["cost"]
                                cost_user = cost_user - money
                                data[str(member.id)]["cost"]=cost_user
                                        
                            with open("levels.json", "w") as f:
                                json.dump(data, f,indent=4)
                            await Interaction.message.edit(embed=embed1,view=None)
                              
            """ async def on_timeout(self):
                    await ctx.send("TimeOut!!! bạn **không** mất tiền cho lần chơi này!") """
        if check==0:
            await ctx.send(embed=embed,view=blacjackbutton())
        else:
            await ctx.send(embed=embed,view=None)
        
    @blackjack.error
    async def cooldown_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            time=int(error.retry_after)
            msg=f"**⏳ | **Nghiện thì cũng phải bình tĩnh đừng vội vàng quá!! Hãy đợi thêm **{time}s**"
            await ctx.send(msg,delete_after=time)
    
    @commands.command()
    async def test(self,ctx):
        
        embed=discord.Embed(title="a")
        embed.add_field(name="ban",value="")
        
        class bcs(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)
                @discord.ui.button(label="rut lần 2",style=discord.ButtonStyle.green, emoji="⏯")
                async def test2(self, Interaction: discord.Interaction,Button: discord.ui.Button):
                    embed=discord.Embed(title="con tây")
                    embed.add_field(name="nut play",value="")
                    await Interaction.message.edit(embed=embed,view=None)
                
                @discord.ui.button(label="next",style=discord.ButtonStyle.red,emoji="⏭")
                async def test3(self, Interaction: discord.Interaction,Button: discord.ui.Button):
                    embed=discord.Embed(title="a")
                    embed.add_field(name="nut next",value="")
                    await Interaction.message.edit(embed=embed,view=None) 
        
        class TestButtons(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)

            @discord.ui.button(label="rút",style=discord.ButtonStyle.green, emoji="⏯")
            async def test2(self, Interaction: discord.Interaction,Button: discord.ui.Button):
                embed=discord.Embed(title="a")
                embed.add_field(name="con 4",value="")
                await Interaction.message.edit(embed=embed,view=bcs())

        await ctx.send(embed=embed,view=TestButtons())    
    
               
async def setup(client):
    await client.add_cog(game(client)) 
    