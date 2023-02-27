import aiohttp
from twitchio.ext import commands


class Balance(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.aiohttp_session = aiohttp.ClientSession(
            cookies={'rat': ''}
        )

    @commands.command()
    @commands.cooldown(rate=1, per=120, bucket=commands.Bucket.channel)
    async def balance(self, ctx: commands.Context):
        balance = await self.get_balance()

        content = (
            f"Gold: {balance.get('gold'):,} | "
            f"Doubloons: {balance.get('doubloons'):,} | "
            f"Ancient Coins: {balance.get('ancientCoins'):,}"
        )

        await ctx.send(content=content)

    async def get_balance(self):
        async with self.aiohttp_session.get(
            url='https://www.seaofthieves.com/api/profilev2/balance',
            headers={'Referer': 'https://www.seaofthieves.com/profile/overview'}
        ) as response:
            return await response.json()
    
    async def cog_unload(self):
        await self.aiohttp_session.close()

def prepare(bot: commands.Bot):
    bot.add_cog(Balance(bot))
