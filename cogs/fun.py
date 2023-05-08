import discord
import random
from discord.ext import commands
from discord import app_commands, colour
import giphy_client
from giphy_client.rest import ApiException
import io
import textwrap
import urllib
import aiohttp
import datetime

#pip install giphy_client

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    
    @commands.command()
    async def ga(self,ctx, member: discord.Member | None):
        if member == None:
            member = 'Tất cả mọi người'
        else:
            member=member.name
        lst=['zzALYeLqMLDa6PEV2C','rZ7A5ayCa2zVcMgsvl','l2Sq8wyY1Zfndp6Lu']
        giff= random.choice(lst)
        embed=discord.Embed(title="")
        embed.add_field(name=f'{member} là con gà',value="")
        embed.set_image(url=f'https://media.giphy.com/media/{giff}/giphy.gif')
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def hug(self,ctx, member: discord.Member=None):
        if member == None:
            member = 'Tất cả mọi người'
        else:
            member=member.name
        api_instance = giphy_client.DefaultApi()
        api_key = '3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK'   #id 3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK
        name='anime hug'
        try: 
            api_response = api_instance.gifs_search_get(api_key, name, limit=15, rating='g')
            lst=list(api_response.data)
            giff= random.choice(lst) 
            embed=discord.Embed(title="")
            embed.add_field(name=f'{ctx.author.name} đã ôm {member}',value="")
            embed.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.channel.send(embed=embed)
            
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
            
    @commands.command()
    async def kill(self,ctx, member: discord.Member=None):
        if member == None:
            member = 'Tất cả mọi người'
        else:
            member=member.name    
        api_instance = giphy_client.DefaultApi()
        api_key = '3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK'   #id 3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK
        name='anime kill'
        
        try: 
            api_response = api_instance.gifs_search_get(api_key, name, limit=15, rating='g')
            lst=list(api_response.data)
            giff= random.choice(lst) 
            embed=discord.Embed(title="")
            embed.add_field(name=f'{ctx.author.name} đã giết {member}',value="")
            embed.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.channel.send(embed=embed)
            
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
                  
              

    @commands.command()
    async def poke(self,ctx, member: discord.Member=None):
        if member == None:
            member = 'Tất cả mọi người'
        else:
            member=member.name    
        api_instance = giphy_client.DefaultApi()
        api_key = '3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK'   #id 3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK
        name='anime poke'
        
        try: 
            api_response = api_instance.gifs_search_get(api_key, name, limit=15, rating='g')
            lst=list(api_response.data)
            giff= random.choice(lst) 
            embed=discord.Embed(title="")
            embed.add_field(name=f'{ctx.author.name} đã chọc {member}',value="")
            embed.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.channel.send(embed=embed)
            
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
            
    @commands.command()
    async def cry(self,ctx):
        api_instance = giphy_client.DefaultApi()
        api_key = '3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK'   #id 3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK
        name='cry anime'
        
        try: 
            api_response = api_instance.gifs_search_get(api_key, name, limit=15, rating='g')
            lst=list(api_response.data)
            giff= random.choice(lst) 
            embed=discord.Embed(title="")
            embed.add_field(name=f'{ctx.author.name} đã bật khóc',value="")
            embed.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.channel.send(embed=embed)
            
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)       
            
    @commands.command()
    async def slap(self,ctx, member: discord.Member=None):
        if member == None:
            member = 'Tất cả mọi người'
        else:
            member=member.name    
        api_instance = giphy_client.DefaultApi()
        api_key = '3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK'   #id 3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK
        name='anime slap'
        
        try: 
            api_response = api_instance.gifs_search_get(api_key, name, limit=15, rating='g')
            lst=list(api_response.data)
            giff= random.choice(lst) 
            embed=discord.Embed(title="")
            embed.add_field(name=f'{ctx.author.name} đã tát {member}',value="")
            embed.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.channel.send(embed=embed)
            
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)        
            
    @commands.command()
    async def kiss(self,ctx, member: discord.Member=None):
        if member == None:
            member = 'Tất cả mọi người'
        else:
            member=member.name    
        api_instance = giphy_client.DefaultApi()
        api_key = '3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK'   #id 3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK
        name='kiss anime'
        
        try: 
            api_response = api_instance.gifs_search_get(api_key, name, limit=15, rating='g')
            lst=list(api_response.data)
            giff= random.choice(lst) 
            embed=discord.Embed(title="")
            embed.add_field(name=f'{ctx.author.name} đã hôn {member}',value="")
            embed.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.channel.send(embed=embed)
            
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)        
            
    @commands.command()
    async def lick(self,ctx, member: discord.Member=None):
        if member == None:
            member = 'Tất cả mọi người'
        else:
            member=member.name    
        api_instance = giphy_client.DefaultApi()
        api_key = '3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK'   #id 3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK
        name=' anime lick'
        
        try: 
            api_response = api_instance.gifs_search_get(api_key, name, limit=15, rating='g')
            lst=list(api_response.data)
            giff= random.choice(lst) 
            embed=discord.Embed(title="")
            embed.add_field(name=f'{ctx.author.name} đã liếm {member}',value="")
            embed.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.channel.send(embed=embed)
            
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)        
            
    @commands.command()
    async def pat(self,ctx, member: discord.Member=None):
        if member == None:
            member = 'Tất cả mọi người'
        else:
            member=member.name    
        api_instance = giphy_client.DefaultApi()
        api_key = '3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK'   #id 3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK
        name='pats anime'
        
        try: 
            api_response = api_instance.gifs_search_get(api_key, name, limit=15, rating='g')
            lst=list(api_response.data)
            giff= random.choice(lst) 
            embed=discord.Embed(title="")
            embed.add_field(name=f'{ctx.author.name} đã xoa đầu {member}',value="")
            embed.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.channel.send(embed=embed)
            
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)        
            
    @commands.command()
    async def wave(self,ctx, member: discord.Member=None):
        if member == None:
            member = 'Tất cả mọi người'
        else:
            member=member.name    
        api_instance = giphy_client.DefaultApi()
        api_key = '3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK'   #id 3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK
        name='waving hands anime'
        
        try: 
            api_response = api_instance.gifs_search_get(api_key, name, limit=15, rating='g')
            lst=list(api_response.data)
            giff= random.choice(lst) 
            embed=discord.Embed(title="")
            embed.add_field(name=f'{ctx.author.name} vãy tay với {member}',value="")
            embed.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.channel.send(embed=embed)
            
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e) 
            
    @commands.command()
    async def punch(self,ctx, member: discord.Member=None):
        if member == None:
            member = 'Tất cả mọi người'
        else:
            member=member.name    
        api_instance = giphy_client.DefaultApi()
        api_key = '3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK'   #id 3HU1HLIW0FsejcyqAPUqycHWEUrBWIOK
        name='anime punch'
        
        try: 
            api_response = api_instance.gifs_search_get(api_key, name, limit=10, rating='g')
            lst=list(api_response.data)
            giff= random.choice(lst) 
            embed=discord.Embed()
            embed.add_field(name=f'{ctx.author.name} đã đánh {member}',value="")
            embed.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.channel.send(embed=embed)
            
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)        
           
                   
async def setup(client):
    await client.add_cog(fun(client))
 