from discord.ext import commands
from privaterooms import *
from utils import *
from discord import CategoryChannel

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        channel = await ctx.author.create_dm()
        print(ex)
        if ctx.message.channel.name == 'bot-commands':
            await channel.send("Something went wrong. Please DM an organizer if you believe this is not intended.")
        else:
            await channel.send("Please keep bot interactions within the #bot-commands channel.")

    @commands.command(help_command="!list", description="List all public voice and text channels")
    @in_bot_commands()
    async def list(self, ctx):
        guild = ctx.guild
        voice_channel_list = [channel.name for channel in guild.voice_channels]
        text_channel_list = [channel.name for channel in guild.text_channels]

        await ctx.send("Available public voice channels: " + str(voice_channel_list)[1:-1])
        await ctx.send("Available public text channels: " + str(text_channel_list)[1:-1])

    @commands.command(help_command="!join <channel_name>", description="Join related channels")
    @commands.check_any(commands.has_role("Hacker"), commands.has_role("Organizer"),
                    commands.has_role("Mentor"), commands.has_role("Sponsor"))
    @in_bot_commands()
    async def join(self, ctx, args):
        guild = ctx.guild
        author = ctx.author

        channel = None
        for available_channel in guild.channels:
            if available_channel.name == args:
                channel = available_channel
                break
        if channel != None:
            await author.move_to(channel)
            await ctx.send("Joined channel!")
        else:
            await ctx.send("No such channel exists!")

    @commands.command(help_command="!leave <channel_name>", description="Leave related channels")
    @commands.check_any(commands.has_role("Hacker"), commands.has_role("Organizer"),
                    commands.has_role("Mentor"), commands.has_role("Sponsor"))
    @in_bot_commands()
    async def leave(self, ctx, args):
        author = ctx.author

        await author.move_to(None)

    @commands.command()
    @commands.command(help_command="!ping",
                      description="Ping the bot",
                      help="Ping the bot")
    @commands.cooldown(1, 60, commands.BucketType.user)
    @in_bot_commands()
    async def ping(self, ctx):
        if len(ctx.message.content) > 5:
            dm = await ctx.author.create_dm()
            await dm.send("Too many arguments for !ping (try just !ping)")
            return
        await ctx.send(f"Online! Latency: {self.bot.latency * 1000:.03f}ms")

    @commands.command(help_command="!room @user1 @user2 ...",
                      description="Create a private voice channel with select users",
                      help="Create a private voice channel with select users")
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

    @commands.command(help_command="!invite", description="Create a server invite to share with others", help="Create a server invite for a friend.")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.check(commands.has_role("Hacker") or commands.has_role("Organizer") or
                    commands.has_role("Mentor") or commands.has_role("Sponsor"))
    @in_bot_commands()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=300)
        await ctx.send(link)

    @commands.command(help_command="!sponsors", description="See our list of sponsors.",
                      help="See our list of sponsors.")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.check(commands.has_role("Hacker") or commands.has_role("Organizer") or
                    commands.has_role("Mentor") or commands.has_role("Sponsor"))
    @in_bot_commands()
    async def sponsors(self, ctx):
        guild = ctx.guild
        sponsor_category = None
        for category in guild.categories:
            if category.name == "Sponsors":
                sponsor_category = category
                break
        if sponsor_category is None:
            return
        message = ""
        for channel in sponsor_category.channels:
            if channel.name != "sponsor-general":
                message += f"{channel}, "
        message = message[:-2]
        await ctx.send(message)


    @commands.command(help_command="!request <organizer/mentor/sponsor> [company_name] message", help="Request help from an organizer, sponsor, or mentor.")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.check_any(commands.has_role("Hacker"), commands.has_role("Organizer"),
                        commands.has_role("Mentor"), commands.has_role("Sponsor"))
    @in_bot_commands()
    async def request(self, ctx, *args):
        guild = ctx.guild
        author = ctx.author
        user_to_alert = args[0].lower()

        if user_to_alert == "organizer" or user_to_alert == "mentor" or user_to_alert == "sponsor":
            channel_name = args[1].lower() if user_to_alert == "sponsor" else user_to_alert + "s"
            message = " ".join(args[2:]) if user_to_alert == "sponsor" else " ".join(args[1:])

            # this part assumes each company has its own channel called "#google", "#microsoft", etc
            # also assumes there is "#mentors" and "#organizers"
            channel_to_alert = discord.utils.get(guild.text_channels, name=channel_name)
            
            if channel_to_alert is not None:
                await channel_to_alert.send(f"{channel_to_alert.mention} From {author.mention}: {message}")
            else:
                # should never get here except if company is mispelled, as long as we have "#organizers" and "#mentors"
                dm = await ctx.author.create_dm()
                if user_to_alert == "sponsor":
                    await dm.send(f"Make sure you spelt the company name right. If the error still persists, please contact an organizer.")
                    if "organizer" in [role.name.lower() for role in author.roles]:
                        await dm.send(f"Since you are an organizer, consider making the channel \"#{channel_name}\" to prevent this from happening again?")
                else:
                    await dm.send(f"Oops! We've made an error on our end. Please let one of the organizers know (through other means) immediately!")
                return
        else: 
            dm = await ctx.author.create_dm()
            await dm.send(f"{user_to_alert} is not a valid argument. The available options are: organizer, sponsor, and mentor.")
            return

        await ctx.send("Request received! Someone will be in touch shortly. ")


def setup(bot):
    bot.add_cog(Basic(bot))
