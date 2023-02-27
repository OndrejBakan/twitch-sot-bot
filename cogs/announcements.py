import aiohttp
from twitchio.ext import commands, routines


class Announcements(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.event('event_channel_joined')
    async def channel_joined(self, channel):
        self.announce.start(channel)

    @routines.routine(seconds=600.0)
    async def announce(self, ctx):
        content = 'Vyzkoušej příkazy: !reputation | !balance | !winrate'

        await ctx.send(content=content)

def prepare(bot: commands.Bot):
    bot.add_cog(Announcements(bot))
