from datetime import timedelta, timezone as tz, datetime as dt
from functools import partial

from utils import *

import discord
from discord.ext import commands

# hackathon time zone
cst = tz(timedelta(hours=-5))  # cst is 5h behind utc

# hackathon start and end times
<<<<<<< HEAD
start = dt.fromtimestamp(1635613200, tz=cst)  # 12pm cst oct 30 2021
end = dt.fromtimestamp(1635699600, tz=cst)  # 12pm cst oct 31 2021

austin = partial(dt.now, tz=cst)  # gives current time in austin, use instead of dt.now() for uniformity

# October 30-31, 2021
# event format is (time, event name, event link if available)
sched = {
    30: [
=======
start = dt.fromtimestamp(1620481500, tz=cst)  # 8:45am cst may 8 2021
end = dt.fromtimestamp(1620579600, tz=cst)  # 12pm cst may 9 2021

austin = partial(dt.now, tz=cst)  # gives current time in austin, use instead of dt.now() for uniformity

# May 8-9, 2021
# event format is (time, event name, event link if available)
sched = {
    8: [
>>>>>>> fb1d025f3d8eed90f94d9173a47e8da755c3bba1
        ("8:45 am", "Opening Ceremony", ""),
        ("9:00 am", "Tech track Ideation Workshop", "http://utexas.zoom.us/my/balloon.room"),
        ("9:00 am", "Idea track Ideation with A4C", "http://utexas.zoom.us/my/stars.room"),
        ("10:00 am", "Intro to Git/Collaboration", "http://utexas.zoom.us/my/mountain.room"),
        ("10:00 am", "Intro to social entrepreneurship/design thinking with SELL", "http://utexas.zoom.us/my/cloud.room"),
        ("11:00 am", "Programming Basics", "http://utexas.zoom.us/my/balloon.room"),
        ("11:00 am", "TPEO Project Management", "http://utexas.zoom.us/my/stars.room"),
<<<<<<< HEAD
        ("12:00 pm", "App Dev", "http://utexas.zoom.us/my/mountain.room"),
        ("12:00 pm", "Civic Tech Project Talk", "http://utexas.zoom.us/my/cloud.room"),
        ("1:00 pm", "Web Dev", "http://utexas.zoom.us/my/balloon.room"),
=======
        ("12:00 pm", "Web Dev", "http://utexas.zoom.us/my/mountain.room"),
        ("12:00 pm", "Civic Tech Project Talk", "http://utexas.zoom.us/my/cloud.room"),
        ("1:00 pm", "App Dev", "http://utexas.zoom.us/my/balloon.room"),
>>>>>>> fb1d025f3d8eed90f94d9173a47e8da755c3bba1
        ("1:00 pm", "Mental Health at Hackathons with A4C", "http://utexas.zoom.us/my/stars.room"),
        ("2:00 pm", "Databases", "http://utexas.zoom.us/my/mountain.room"),
        ("3:00 pm", "Tech & Society with A4C", "http://utexas.zoom.us/my/balloon.room"),
        ("5:00 pm", "Bob Ross Painting", "http://utexas.zoom.us/my/mountain.room"),
        ("9:00 pm", "Submissions Due", ""),
        ("9:00 pm", "Trivia", "http://utexas.zoom.us/my/cloud.room"),
        ("10:00 pm", "Games", "http://utexas.zoom.us/my/cloud.room"),
    ],
<<<<<<< HEAD
    31: [
=======
    9: [
>>>>>>> fb1d025f3d8eed90f94d9173a47e8da755c3bba1
        ("10:00 am", "Judging", ""),
        ("12:00 pm", "Closing Ceremony", ""),
    ],
}


def time_left(event):
    # returns string with duration composed
    diff = event - austin()
    d = diff.days
    h, m = divmod(diff.seconds, 3600)  # 3600 seconds in an hour
    m, s = divmod(m, 60)

    return (
        (f"{d} day{'s' * bool(d - 1)}, " if d else "")
        + (f"{h} hour{'s' * bool(h - 1)}, " if h else "")
        + (f"{m} minute{'s' * bool(m - 1)}" if m else "")
    )


def time_elapsed(event):
    # returns string with time since event started
    diff = austin() - event
    d = diff.days
    h, m = divmod(diff.seconds, 3600)  # 3600 seconds in an hour
    m, s = divmod(m, 60)

    return (
        (f"{d} day{'s' * bool(d - 1)}, " if d else "")
        + (f"{h} hour{'s' * bool(h - 1)}, " if h else "")
        + (f"{m} minute{'s' * bool(m - 1)}" if m else "")
    )


class Times(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 60, commands.BucketType.user)
    @in_bot_commands()
    @commands.command(name="when",
                      help_command="!when",
                      description="Check when the hackathon starts or ends",
                      help="Check when the hackathon starts or ends"
                      )
    async def hack_times(self, ctx):
        if start > austin():
            event = start  # hackathon yet to start
        else:
            event = end  # hackathon started so give time till end
        if austin() > end:
<<<<<<< HEAD
            breakdown = "HackTX 2021 has ended. Come back next year :))"
        else:
            # compose string accordingly
            breakdown = (
                "HackTX 2021 " + ("begins " if start > austin() else "ends ") + "in " + time_left(event)
=======
            breakdown = "Changeathon has ended. Come back next year :))"
        else:
            # compose string accordingly
            breakdown = (
                "Changeathon " + ("begins " if start > austin() else "ends ") + "in " + time_left(event)
>>>>>>> fb1d025f3d8eed90f94d9173a47e8da755c3bba1
            )

        await ctx.send(breakdown)

    @commands.cooldown(1, 60, commands.BucketType.guild)
    @in_bot_commands()
    @commands.command(name="schedule",
                      help_command="!schedule",
                      description="See the hackathon schedule",
                      help="See the hackathon schedule"
                      )
    async def schedule(self, ctx):
        embeds = []

        for day, events in sched.items():
            if day >= austin().day:
<<<<<<< HEAD
                full_day = ["Saturday", "Sunday"][day - 30]  # 30 since that was the first day

                embed = discord.Embed(
                    title="HackTX 2021 Schedule :scroll:",
                    description=f"**{full_day}, October {day}** \nso much fun to be had :')",
=======
                full_day = ["Saturday", "Sunday"][day - 8]  # 8 since that was the first day

                embed = discord.Embed(
                    title="Changeathon 2021 Schedule :scroll:",
                    description=f"**{full_day}, May {day}** \nso much fun to be had :')",
>>>>>>> fb1d025f3d8eed90f94d9173a47e8da755c3bba1
                    color=discord.Colour.dark_purple(),
                )

                for num, event in enumerate(events):
<<<<<<< HEAD
                    event_time, event_name, link = event
                    left = dt.strptime(f"2021 October {day} {event_time}", "%Y %b %d %I:%M %p").replace(tzinfo=cst)
=======
                    event_time, event_name, link = event                  
                    left = dt.strptime(f"2021 May {day} {event_time}", "%Y %b %d %I:%M %p").replace(tzinfo=cst)
>>>>>>> fb1d025f3d8eed90f94d9173a47e8da755c3bba1
                    if left > austin():  # check if event hasn't already passed
                        embed.add_field(
                            name=f"{num + 1}. {event_name} at {event_time}",
                            value=(f"in {time_left(left)} CT" + (f", [**link**]({link})" if link else "")),
                            inline=False,
                        )

                embeds.append(embed)

        await paginate_embed(self.bot, ctx.channel, embeds)

    @commands.cooldown(1, 60, commands.BucketType.guild)
    @in_bot_commands()
    @commands.command(name="soon",
                      help_command="!soon",
                      description="Check on upcoming events.",
                      help="Check on upcoming events."
                      )
    async def soon(self, ctx):
        embeds = []

        val = 1
        for day, events in sched.items():
            if day >= austin().day:
                full_day = ["Saturday", "Sunday"][day - 8]  # 8 since that was the first day

                embed = discord.Embed(
                    title="Upcoming Events! :alarm_clock:",
                    description="See what's happening in the next hour!",
                    color=discord.Colour.dark_purple(),
                )

                #assumes events in list are in chronological order
                for num, event in enumerate(events):
<<<<<<< HEAD
                    event_time, event_name, link = event
                    left = dt.strptime(f"2021 October {day} {event_time}", "%Y %b %d %I:%M %p").replace(tzinfo=cst)
=======
                    event_time, event_name, link = event                  
                    left = dt.strptime(f"2021 May {day} {event_time}", "%Y %b %d %I:%M %p").replace(tzinfo=cst)
>>>>>>> fb1d025f3d8eed90f94d9173a47e8da755c3bba1
                    if left > austin(): #check that event hasn't passed
                        if (dt.__sub__(left, austin()).total_seconds()) <= 60:  # event happening in the next minute
                            text = f"{event_name} starting now!"
                            embed.add_field(
                                name=f"{val}. {event_name} at {event_time} CT",
                                value=("in < 1 minute" + (f", [**link**]({link})" if link else "")),
                                inline=False,
                            )
                        elif (dt.__sub__(left, austin()).total_seconds()) <= 3600:  # event happening in the next hour 
                            embed.add_field(
                                name=f"{val}. {event_name} at {event_time} CT",
                                value=(f"in {time_left(left)}" + (f", [**link**]({link})" if link else "")),
                                inline=False,
                            )
                            val = val + 1
                        else: 
                            break

                if val == 1: 
                    embed.add_field(
                        name="No upcoming events!",
                        value="Check the schedule to see future events.",
                        inline=False,
                    )
                embeds.append(embed)
                break
        await paginate_embed(self.bot, ctx.channel, embeds)

    @commands.cooldown(1, 60, commands.BucketType.guild)
    @in_bot_commands()
    @commands.command(name="time",
                      help_command="!time",
                      description="Check when a certain event is",
                      help="Check when a certain event is"
                      )
    async def time(self, ctx, *, contents):

        text = "Oops! This event isn't on the schedule!" 
        for day, events in sched.items():

            for num, event in enumerate(events):
                event_time, event_name, link = event             
                if(contents == event_name):
<<<<<<< HEAD
                    left = dt.strptime(f"2021 October {day} {event_time}", "%Y %b %d %I:%M %p").replace(tzinfo=cst)
=======
                    left = dt.strptime(f"2021 May {day} {event_time}", "%Y %b %d %I:%M %p").replace(tzinfo=cst)
>>>>>>> fb1d025f3d8eed90f94d9173a47e8da755c3bba1
                    if left > austin(): # check if event hasn't already passed 
                        text = f"{event_name} starts at {event_time} CT (in {time_left(left)})"
                        # if event is starting within one minute, otherwise 
                        if (dt.__sub__(left, austin()).total_seconds()) <= 60:  
                            text = f"{event_name} starts now at {event_time} CT!"

                    else:
                        text = f"{event_name} has already passed! Try the \"!soon\" command to see what's coming up."
                        #event might be going on if it started within 2 hrs ago
                        if (dt.__sub__(austin(), left).total_seconds()) <= (2*3600): 
                            text = f"{event_name} started at {event_time} CT ({time_elapsed(left)} ago)!"


                    break
 
        await ctx.send(text)


def setup(bot):
    bot.add_cog(Times(bot))
