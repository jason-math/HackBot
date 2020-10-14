import aiohttp
from discord.ext import commands
from discord.utils import get
import requests
import json


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx):
        user = ctx.message.author
        msg = ctx.message.content.split(" ")
        token = msg[1]
        data = {'token': token, 'user': user}
        await ctx.message.delete()
        url = 'http://localhost:3000/auth/discord/verify_user/'
        response = requests.post(url, data=data, verify=False)
        channel = await ctx.author.create_dm()
        if response.ok:
            json_format = json.loads(response.text)
            print(json_format["status"]["confirmed"])
            if json_format["status"]["confirmed"] is True:
                if json_format["sponsor"] is True:
                    role = get(user.server.roles, name="Sponsor")
                else:
                    role = get(user.server.roles, name="Hacker")
                await self.bot.add_roles(user, role)
                await channel.send("You have been successfully verified! Happy hacking.")
            else:
                await channel.send("Verification failed. Please contact an organizer if you think this is incorrect.")
        else:
            await channel.send("Verification failed. Please contact an organizer if you think this is incorrect.")


def setup(bot):
    bot.add_cog(Verify(bot))