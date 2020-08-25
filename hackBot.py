import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


# PERIPHERALS - Here are all of the things that will run in the background. I will re-organize the file structure later

# TODO: Spam prevention - Don't let users send messages or commands too fast.
# TODO: Terms of service - Users must react with an emoji to our terms of service to access the rest of the server
# TODO: Calendar - Bot should by synced with a google calendar and send messages about events (Refer to SummerHacks)

# TODO: HackTX login verification - Verify users must be accepted to HackTX in order to have access to the server

# BOT COMMANDS - Here are all of the commands users will be able to call. Let me know if you think of any more!

# TODO: Team formation commands - Currently unplanned or decided. Let me know if you have any ideas!

# private_room
# @input *msg - The list of mentioned members
# Should create a private voice channel only available to the mentioned members
@bot.command(name='room', help='Creates a private voice channel with mentioned member')
async def private_room(ctx, *msg):

    # your code here
    # should have an inactivity timer that counts down when no one is in the channel
    # and resets if someone joins
    # should only work for 2-8 users, with override by organizers
    # should delete a user's private voice channel if they create another one (only 1 at a time)

    await ctx.send("Private room created!")


# join_event
# @input event - The event the attendee wants to join
# Should add the user to the related voice and text channels
@bot.command(name='join', help='Join voice and text channels related to a specific event')
async def join_event(ctx, event):

    # your code here
    # should give an error message if the user has already joined
    # should output a list of open events if the event given by the user does not exist
    # should increment a global variable for # of attendees attending the specific event

    await ctx.send(f"Joined {event} channels!")


# leave_event
# @input event - The event the attendee wants to leave
# Should remove the user from the related voice and text channels
@bot.command(name='leave', help='Leave voice and text channels related to a specific event')
async def leave_event(ctx, event):

    # your code here
    # should give an error message if the user is not in the event
    # should output a list of events the user is currently in if the event given by the user does not exist
    # should decrement a global variable for # of attendees attending the specific event

    await ctx.send(f"Joined {event} channels!")


# give_feedback
# Should add the user to the related voice and text channels
@bot.command(name='feedback', help='Give the organizers feedback about the hackathon!')
async def give_feedback(ctx):

    # your code here
    # should private message the user asking for feedback
    # the user's next private message should be recorded
    # should prompt the user to confirm their feedback and store it if confirmed

    await ctx.send(f"Placeholder")


# report
# @input user - The user being reported
# Should report the mentioned user
@bot.command(name='report', help='Report a mischievous hacker')
async def report(ctx, user):

    # your code here
    # Should private message an organizer with details of the report
    # Currently undecided what this will do (generate text channel history, ask for details, etc.)
    # Implement whatever you think will be useful!

    await ctx.send("Report Received!")


# request
# @input user_type - The type user being requested
# Should notify the requested type of user (organizer, sponsor, mentor) that this user would like to talk
@bot.command(name='report', help='Report a mischievous hacker')
async def report(ctx, user_type):

    # your code here
    # Should private message someone from the type of user requested that this user is requesting them

    await ctx.send("Request Received!")


# generate_stats [ORGANIZER ONLY]
# Private messages the organizer a list of hackathon stats
@bot.command(name='stats')
async def generate_stats(ctx):

    # Should only allow the command to be run by organizers
    # Brownie points if you make it so non-organizers can't even see this is a command
    # Should generate useful stats such as total attendees, number of people registered for each event,
    # number of teams, number of people without a team, etc. Anything else you think is useful!

    await ctx.send("Placeholder")


# Here are two misc functions so you can see some useful functionality. Everything else you will have to find yourself
@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)
