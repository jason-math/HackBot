from discord.ext import commands
from utils import text_to_owo
# from utils import get_wave


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def owo(self, ctx):
        await ctx.send(text_to_owo(ctx.message.content))

    @commands.command()
    async def lina(self, ctx):
        await ctx.send("Lina Bad")

# ctx.message.author.name
    """""
    @commands.command()
    async def wave(self, ctx, member: discord.Member = None):
        wave = await get_waves()
        if member is not None:
            await ctx.send("%s %s" %(wave, member))
        else:
            await ctx.send("%s" %wave)
    """""
    # @commands.command(help_command="!list", description="List all public channels")
    # async def list(ctx, event):
    #     guild = ctx.guild
    #     channel_list = guild.voice_channels
        
    #     await ctx.send("Available channels: " + channel_list)

def setup(bot):
    bot.add_cog(Test(bot))
