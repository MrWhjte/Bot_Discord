import discord
import os
import json
import config
from discord.ext import commands, tasks
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.guilds=True
intents.dm_messages=True

def get_server_prefix(client,message) :
    with open("prefixes.json","r") as f:
     prefix = json.load(f)
    return prefix[str(message.guild.id)]
      
class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = get_server_prefix,intents = discord.Intents.all())
    
    async def setup_hook(self): 
        print(f"Logged in as {client.user}")
        cogs_folder = f"{os.path.abspath(os.path.dirname(__file__))}/cogs"
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")

client = Client()    
@client.event
async def on_ready(): # khi bot được bật lên thì 
    synced = await client.tree.sync()
    print(f"đồng bộ hóa hoàn tất với {str(len(synced))} lệnh ")
    await client.change_presence(activity=discord.Game("Đang Xem live stream"))
    
@client.tree.context_menu(name="helu") # lệnh để tương tác bằng ứng dụng
async def helu(interaction: discord.Interaction, message: discord.Message):
     await interaction.response.send_message("heey")
     
@client.tree.context_menu(name="ga") # lệnh để tương tác bằng ứng dụng
async def ga(interaction: discord.Interaction, message: discord.Message):
     await interaction.response.send_message("chang khùng")    
client.remove_command("help") # xóa lệnh mặc định help của bot
## thay đổi prefix
@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)
        
    prefix[str(guild.id)] = "m"
    
    with open("prefixes.json" ,"w") as f:
        json.dump(prefix, f,indent=4)


   
             
@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)
        prefix.pop(str(guild.id))
    with open("prefixes.json" ,"w") as f:
        json.dump(prefix, f,indent=4)
        
@client.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, *, newprefix: str):
    with open("prefixes.json" ,"r") as f:
        prefix=json.load(f)
    prefix[str(ctx.guild.id)] = newprefix
    with open("prefixes.json" ,"w") as f:
        json.dump(prefix, f,indent=4)
        
    embed=discord.Embed()
    embed.add_field(name="Thành công:",value=f"prefix đã được đổi thành `{newprefix}`")
    await ctx.send(embed=embed)
    
@setprefix.error
async def setprefix_erro(ctx, error):
        if isinstance(error,CheckFailure ):
            await ctx.send(f"{ctx.message.author.mention} Bạn không phải là admin ")      
    
### kết thúc thay đổi prefix

client.run(config.TOKEN)
  