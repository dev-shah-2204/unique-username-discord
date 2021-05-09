import discord, random
import hex_colors

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType

def bool_str(variable): #Function to convert boolean values to string: Yes/No
    if variable == True:
        return 'Yes'
    if variable == False:
        return 'No'

class serverInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'serverinfo', help = 'Information about the server', usage = '')
    @commands.cooldown(1, 10, BucketType.guild)
    async def serverinfo(self, ctx):
        guild = server = ctx.guild

        #Many of these variables aren't necessary but since the embed has many fields, I didn't want the code to be messy
        created = server.created_at.strftime("%d %B %Y at %I %p")
        emoji_limit = server.emoji_limit
        emojis = server.emojis
        members = server.member_count
        owner = server.owner
        level = server.verification_level
        region = server.region
        boost_level = server.premium_tier
        large = server.large

        roles = len(ctx.guild.roles)

        subs = server.premium_subscribers

        boosters = ""
        for person in subs:
            boosters += f'{person.mention} '

        if boosters == "":
            boosters = 'None'

        em = discord.Embed(title = f"Here's the information I found on {ctx.guild.name}", color = random.choice(hex_colors.colors))
        em.set_thumbnail(url = server.icon_url)
        em.add_field(name = 'ID', value = server.id, inline = False)
        em.add_field(name = 'Owner', value = owner, inline = False)
        em.add_field(name = 'Server Region', value = str(region).capitalize(), inline = False)
        em.add_field(name = 'Created on', value = created, inline = False)
        em.add_field(name = 'Is this server considered a big server?', value = bool_str(large), inline = False)
        em.add_field(name = 'Member Count', value = members)
        em.add_field(name = 'Number of roles', value = roles-1, inline = False) #To ignore @everyone role
        em.add_field(name = 'Security Level', value = level, inline = False)
        em.add_field(name = 'Server Boosters', value = boosters, inline = False)
        em.add_field(name = 'Server level', value = boost_level, inline = False)
        em.set_footer(text = f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em)

def setup(client):
    client.add_cog(serverInfo(client))
    print('serverInfo')