from datetime import timedelta, timezone as tz, datetime as dt
from functools import partial

from utils import *

import discord
from discord.ext import commands

# hackathon time zone
cst = tz(timedelta(hours=-5))  # cst is 5h behind utc

# hackathon start and end times
start = dt.fromtimestamp(1603508400, tz=cst)  # 9pm cst oct 2 2020
end = dt.fromtimestamp(1603641600, tz=cst)  # 9am cst oct 4 2020

austin = partial(dt.now, tz=cst)  # gives current time in austin, use instead of dt.now() for uniformity

# Oct 2-4, 2020
# event format is (time, event name, event link if available)
sched = {
    23: [
        ("10:00 pm", "Opening Ceremony", ""),
        ("10:30 pm", "Teambuilding", ""),
    ],
    24: [
        ("7:00 am", "Teambuilding", ""),
        ("8:00 am", "Beginner Intro to Hackathons", ""),
        ("9:00 am", "Beginner Intro to Git", ""),
        ("9:30 am", "Bob Ross MS Paint Party", ""),
        ("10:00 am", "Beginner Mobile Dev", ""),
        ("10:00 am", "Intro to GCP", ""),
        ("11:00 am", "Beginner Web Dev", ""),
        ("11:00 am", "EchoAR Workshop", ""),
        ("11:00 am", "Guest Speaker: Anant Bhardwaj", ""),
        ("12:00 pm", "Intro to ML w/ MLDS", ""),
        ("12:00 pm", "Industry Panel", ""),
        ("1:00 pm", "Microsoft Event", ""),
        ("2:00 pm", "Game Dev w/ EGADS", ""),
        ("2:00 pm", "KuzoClass Workshop", ""),
        ("2:30 pm", "Guest Speaker: Bill Mannel", ""),
        ("3:00 pm", "Instabase Event", ""),
        ("3:30 pm", "Workout w/ HACS", ""),
        ("4:00 pm", "Wayfair Event", ""),
        ("4:00 pm", "Diversity Discussion", ""),
        ("4:30 pm", "Professional Development", ""),
        ("5:00 pm", "Glimpse Career Fair", ""),
        ("7:00 pm", "Design Workshop", ""),
        ("7:00 pm", "GCP x MongoDB: Cloud Hero", ""),
        ("7:00 pm", "HackTEXIMATHON", ""),
        ("7:30 pm", "Hackathon Organizer Meetup", ""),
        ("7:30 pm", "ATLA Watch Party", ""),
        ("9:30 pm", "Trivia Night", ""),
        ("10:30 pm", "Game Night", ""),
    ],
    25: [
        ("1:00 am", "Super Smash Bros. Ultimate Tourney", ""),
        ("2:00 am", "League of Legends 1v1 Tourney", ""),
        ("8:00 am", "Instabase Event", ""),
        ("9:00 am", "Pitching Workshop w/ Convergent", ""),
        ("10:00 am", "Submission Office Hours", ""),
        ("11:00 am", "Submissions Due!", ""),
        ("11:30 am", "Judging", ""),
        ("1:00 pm", "Project Fair", ""),
        ("2:00 pm", "Closing Ceremony", ""),
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
            breakdown = "HackTX has ended. Come back next year :))"
        else:
            # compose string accordingly
            breakdown = (
                "HackTX 2020 " + ("begins " if start > austin() else "ends ") + "in " + time_left(event)
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
                full_day = ["Friday", "Saturday", "Sunday"][day - 23]  # 23 since that was the first day

                embed = discord.Embed(
                    title="HackTX 2020 Schedule :scroll:",
                    description=f"**{full_day}, Oct {day}** \nso much fun to be had :')",
                    color=discord.Colour.dark_purple(),
                )

                for num, event in enumerate(events):
                    event_time, event_name, link = event
                    left = dt.strptime(f"2020 Oct {day} {event_time}", "%Y %b %d %I:%M %p").replace(tzinfo=cst)
                    if left > austin():  # check if event hasn't already passed
                        embed.add_field(
                            name=f"{num + 1}. {event_name} at {event_time}",
                            value=(f"in {time_left(left)}" + (f", [**link**]({link})" if link else "")),
                            inline=False,
                        )

                embeds.append(embed)

        await paginate_embed(self.bot, ctx.channel, embeds)


def setup(bot):
    bot.add_cog(Times(bot))
