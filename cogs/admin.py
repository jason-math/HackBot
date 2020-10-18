from discord.ext import commands
import discord
import datetime


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help_command="!unload <cog>", description="Unload a cog")
    @commands.check(commands.has_role("Organizer"))
    async def unload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send("Could not unload cog")
            print(e)
            return
        await ctx.send("Cog unloaded")

    @commands.command(help_command="!load <cog>", description="Load a cog")
    @commands.check(commands.has_role("Organizer"))
    async def load(self, ctx, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not load cog")
            print(e)
            return
        await ctx.send("Cog loaded")

    @commands.command(help_command="!reload <cog>", description="Reload a cog")
    @commands.check(commands.has_role("Organizer"))
    async def reload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not reload cog")
            return
        await ctx.send("Cog reloaded")

    @commands.command(help_command="!stats", description="Get server stats")
    @commands.check(commands.has_role("Organizer"))
    async def stats(self, ctx):
        guild = ctx.guild

        num_voice_channels = len(guild.voice_channels)
        num_text_channels = len(guild.text_channels)

        embed = discord.Embed(description="Server Stats", colour=discord.Colour.dark_purple())
        embed.add_field(name="Server Name", value=guild.name, inline=False)
        online = 0
        members = await guild.members
        for member in members:
            print("%s's status: %s" % (member, member.status))
            if member.status != discord.Status.offline and not member.bot:
                online += 1
        embed.add_field(name="Online hackers", value=str(online), inline=False)
        embed.add_field(name="# Voice Channels", value=str(num_voice_channels))
        embed.add_field(name="# Text Channels", value=str(num_text_channels))
        embed.set_author(name=self.bot.user.name)
        embed.set_footer(text=str(datetime.datetime.now()))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
