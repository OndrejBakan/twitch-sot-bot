import aiohttp
from twitchio.ext import commands, routines


class AnnouncementsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.event('event_channel_joined')
    async def channel_joined(self, channel):
        self.announce.start(channel)

    @routines.routine(seconds=self.config.get('bot', 'sot.announcements.interval'))
    async def announce(self, ctx):
        content = 'Vyzkoušej příkazy: !reputation | !balance | !winrate'

        await ctx.send(content=content)


class BalanceCog(commands.Cog):
    def __init__(self, bot: commands.Bot, http_client: aiohttp.ClientSession):
        self.bot = bot
        self.http_client = http_client


class ReputationCog(commands.Cog):
    def __init__(self, bot: commands.Bot, http_client: aiohttp.ClientSession):
        self.bot = bot
        self.http_client = http_client
    
    @commands.command()
    @commands.cooldown(rate=1, per=120, bucket=commands.Bucket.channel)
    async def reputation(self, ctx: commands.Context):
        if self.config.getboolean('bot', 'sot.reputation.enabled'):
            await ctx.send('Reputation')


class WinrateCog(commands.Cog):
    def __init__(self, bot: commands.Bot, http_client: aiohttp.ClientSession):
        self.bot = bot
        self.http_client = http_client


def prepare(bot: commands.Bot):

    http_client = aiohttp.ClientSession(
        cookies = {
            'rat': bot.config.get('seaofthieves.com', 'rat')
        }
    )

    if bot.config.getboolean('bot', 'sot.announcements.enabled', fallback=False):
        bot.add_cog(AnnouncementsCog(bot))
    
    if bot.config.getboolean('bot', 'sot.balance.enabled', fallback=False):
        bot.add_cog(BalanceCog(bot, http_client))
    
    if bot.config.getboolean('bot', 'sot.reputation.enabled', fallback=False):
        bot.add_cog(ReputationCog(bot, http_client))
    
    if bot.config.getboolean('bot', 'sot.winrate.enabled', fallback=False):
        bot.add_cog(WinrateCog(bot, http_client))
