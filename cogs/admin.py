import discord
import random
import datetime
import asyncio
import os
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot, has_permissions, CheckFailure


class admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()  
    @commands.has_permissions(administrator=True)
    async def kick(self,ctx, member: discord.Member, reason="không có lý do"):
            await ctx.send(f"{member.mention} đã bị kích khỏi sever | lý do: {reason}")
            await member.kick(reason=reason)
        
    @kick.error
    async def kich_error(self,ctx, error):
        if isinstance(error,CheckFailure ):
            await ctx.send(f"{ctx.message.author.mention} Bạn không có quyền để thực hiện điều này ") 
            
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self,ctx, member: discord.Member, reason="không có lý do"):
        await ctx.send(f" {member.mention} đã bị ban khỏi sever | lý do: {reason}")
        await member.ban(reason=reason)
        
    @ban.error
    async def ban_error(self,ctx, error):
        if isinstance(error,CheckFailure ):
            await ctx.send(f"{ctx.message.author.mention} Bạn không có quyền để thực hiện điều này ")     
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self,ctx, member: discord.Member):
        await ctx.send(f" {member.mention} đã được unban  khỏi sever ")
        await member.unban()
        
    @unban.error
    async def unban_error(self,ctx, error):
        if isinstance(error,CheckFailure ):
            await ctx.send(f"{ctx.message.author.mention} Bạn không có quyền để thực hiện điều này ")     
        
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def whoami(self,ctx):
        msg = "Bạn là admin {}".format(ctx.message.author.mention)  
        await ctx.reply(msg)

    @whoami.error
    async def whoami_error(self,ctx, error):
        if isinstance(error,CheckFailure ):
            msg = "{} Bạn chỉ là dân thường ^_^".format(ctx.message.author.mention)
            await ctx.reply(msg)         

async def setup(client):
    await client.add_cog(admin(client))
 