from discord.ext import commands
from privaterooms import *
from utils import *


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        print(ex)
        channel = await ctx.author.create_dm()
        if ctx.message.channel.name == 'bot-commands':
            await channel.send(ex)
        else:
            await channel.send("Please keep bot interactions within the #bot-commands channel.")

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @in_bot_commands()
    async def ping(self, ctx):
        if len(ctx.message.content) > 5:
            dm = await ctx.author.create_dm()
            await dm.send("Too many arguments for !ping (try just !ping)")
            return
        await ctx.send(f"Online! Latency: {self.bot.latency * 1000:.03f}ms")

    @commands.command(help_command="!room @user1 @user2 ...",
                      description="Create a private voice channel with select users")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.check_any(commands.has_role("Hacker"), commands.has_role("Organizer"),
                        commands.has_role("Mentor"), commands.has_role("Sponsor"))
    @in_bot_commands()
    async def room(self, ctx):
        guild = ctx.guild
        author = ctx.author
        room = PrivateRoom()
        if len(ctx.message.mentions) == 0:
            dm = await ctx.author.create_dm()
            await dm.send("Please specify 1 or more specific members (using @) when using !room")
            return
        channel = await create_channel(guild, author, ctx.message.mentions)
        await room.assign_channel(channel)
        await ctx.send("Room created!")
        while room.private_channel is not None:
            await room.active_checker()
        await ctx.send("%s's room deleted due to inactivity" % author.name)

    @commands.command(help_command="!invite", description="Create a server invite to share with others")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.check(commands.has_role("Hacker") or commands.has_role("Organizer") or
                    commands.has_role("Mentor") or commands.has_role("Sponsor"))
    @in_bot_commands()
    async def invite(self, ctx):
        if len(ctx.message) > 0:
            dm = await ctx.author.create_dm()
            await dm.send("Too many arguments for !invite (try just !invite)")
            return
        link = await ctx.channel.create_invite(max_age=300)
        await ctx.send(link)


def setup(bot):
    bot.add_cog(Basic(bot))
