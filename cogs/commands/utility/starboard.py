import discord 
import hex_colors 

from db import *
from discord.ext import commands

db = database.cursor()
class StarboardCommands(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.group(name = 'starboard', help = 'Commands related to starboard')
    @commands.has_permissions(manage_messages = True)
    async def starboard_commands(self, ctx):
        em = discord.Embed(
            title = "Starboard Commands",
            description = """
`channel` - Set the starboard channel
`enable`  - Enable starboard for the server
`disable` - Disable starboard for the server
            """,
            color = hex_colors.l_yellow)

        await ctx.send(embed = em)

    @starboard_commands.command(name = 'channel', help = "Set the starboard channel")
    async def channel(self, ctx, channel:discord.TextChannel):
        db.execute(f"INSERT INTO Starboard(guild, channel, state) VALUES ('{ctx.guild.id}','{channel}','enabled')")
        database.commit()
        await ctx.send(f"Starboard set to <#{channel.id}>")

    @starboard_commands.command(name = 'disable', help = "Disable starboard")
    async def disable(self, ctx):
        try:
            db.execute(f"UPDATE Starboard SET state = 'disabled' WHERE guild = '{ctx.guild}'")
            database.commit()
            await ctx.send("Disabled starboard")
        except:
            await ctx.send("Starboard was never enabled for this server")

    @starboard_commands.command(name = 'enable', help = "Enable starboard")
    async def enable(self, ctx):
        try:
            db.execute(f"UPDATE Starboard SET state = 'enabled' WHERE guild = '{ctx.guild}'")
            database.commit()
            await ctx.send("Enabled starboard for this server")
        except:
            await ctx.send("Starboard has not been set in this server. First run the `starboard channel` command")


def setup(client):
    client.add_cog(StarboardCommands(client))
    print('StarboardCommands')