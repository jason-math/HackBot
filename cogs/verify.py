import aiohttp
from discord.ext import commands
from discord.utils import get
import requests
import json
from utils import *


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @in_bot_commands()
    async def verify(self, ctx):
        user = ctx.message.author
        msg = ctx.message.content.split(" ")
        token = msg[1]
        data = {'token': token, 'user': user}
        await ctx.message.delete()
        url = 'http://register.hacktx.com/auth/discord/verify_user/'
        response = requests.post(url, data=data, verify=False)
        channel = await ctx.author.create_dm()
        if response.ok:
            json_format = json.loads(response.text)
            print(json_format["status"]["confirmed"])
            if json_format["status"]["confirmed"] is True:
                if json_format["sponsor"] is True:
                    role = get(user.guild.roles, name="Sponsor")
                else:
                    role = get(user.guild.roles, name="Hacker")
                await self.bot.add_roles(user, role)
                await channel.send("You have been successfully verified! Happy hacking.")
            else:
                await channel.send("Verification failed. Please contact an organizer if you think this is incorrect.")
        else:
            await channel.send("Verification failed. Please contact an organizer if you think this is incorrect.")


def setup(bot):
    bot.add_cog(Verify(bot))
