from discord.ext import commands


class Sponsors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help_command="!a4c",
                      description="Learn about A4C who helped host this event!",
                      help="Learn about A4C who helped host this event!")
    async def a4c(self, ctx):
        await ctx.send("ACM for Change (A4C) is a student-led council with a mission to improve the UTCS department in the areas of Diversity, Equity, Inclusion, Mental Health, and Ethics. Reach out at a4c@texasacm.org!")

    @commands.command(help_command="!sponsor",
                      description="Learn about 8VC, who is sponsoring this event!",
                      help="Learn about 8VC, who is sponsoring this event!")
    async def sponsor(self, ctx):
        await ctx.send("8VC is a California based Venture Capital that has just moved into Austin! Our team is a dynamic group of entrepreneurs, engineers, investors, and philosophers and together we seek to build lasting technology platforms to create long-term economic and societal value.")

def setup(bot):
    bot.add_cog(Sponsors(bot))
