import aiohttp
import discord
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
        url = 'https://register.hacktx.com/auth/discord/verify_user/'
        response = requests.post(url, data=data, verify=False)
        channel = await ctx.author.create_dm()
        if response.ok:
            json_format = json.loads(response.text)
            print(json_format)
            if json_format["status"]["confirmed"] is True:
                print(user.guild.roles);
                if json_format["sponsor"] is True:
                    role = get(user.guild.roles, name="Sponsor")
                else:
                    role = get(user.guild.roles, name="Hacker")
                await user.add_roles(role)
                await channel.send("You have been successfully verified! Happy hacking.")
            else:
                await channel.send("Verification failed. Please contact an organizer if you think this is incorrect.")
        else:
            await channel.send("Verification failed. Please contact an organizer if you think this is incorrect.")


def setup(bot):
    bot.add_cog(Verify(bot))
