import aiohttp
from twitchio.ext import commands


class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=120, bucket=commands.Bucket.channel)
    async def reputation(self, ctx: commands.Context):
        await ctx.send('Halo')

def prepare(bot: commands.Bot):
    bot.add_cog(Test(bot))
