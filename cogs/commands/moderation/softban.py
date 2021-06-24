import discord, random

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType
import hex_colors

colors = hex_colors.colors

class SoftBan(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'softban', help = 'Ban and unban a member from the server so their messages get deleted', usage = '<member> <reason>')
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def soft_ban(self, ctx, member:discord.Member, *, reason = "No reason provided"): #Default reason is "No reason provided"
        """
        It's same as the ban command, just the unban part is new
        """

        if member == self.client.user: #If  the 'member' is the bot
            await ctx.send("I don't know what the procedure is here, but I cannot leave like this. You'll have to remove me from the server manually. If I caused any problem, DM it to me, with details so my developer can fix me.")
            return

        #If the 'member' is the person who invoked the command
        if member == ctx.author:
            await ctx.send("Why do you wanna ban your self?")
            return

        #Checking if the other person has a higher role
        if member.top_role.position >= ctx.author.top_role.position:
            await ctx.send(f"{member.mention} has a higher role than you/same role as you. You cannot ban them")
            return

        try:
            await member.ban(reason = reason)
        except:
            await ctx.send(f"{member}'s role is higher than me, I cant ban them")
            return

        em = discord.Embed(color = hex_colors.m_red)
        em.set_author(name = f"{ctx.author} banned {member}", icon_url = ctx.author.avatar_url)
        em.set_thumbnail(url = member.avatar_url)
        em.add_field(name = 'Reason:', value = reason)

        await ctx.message.delete()
        await ctx.send(embed = em)
        await member.unban(reason = f"Soft-banned by {ctx.author}")

def setup(client):
    client.add_cog(SoftBan(client))
    print('SoftBan')