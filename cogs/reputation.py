import aiohttp
from twitchio.ext import commands


class Reputation(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.aiohttp_session = aiohttp.ClientSession(
            cookies={'rat': ''}
        )

    @commands.command()
    @commands.cooldown(rate=1, per=120, bucket=commands.Bucket.channel)
    async def reputation(self, ctx: commands.Context):
        reputation = await self.get_reputation()
        
        content = (
            f"Reaper's Bones: {reputation.get('ReapersBones').get('Level')} | "
            f"Gold Hoarders: {reputation.get('GoldHoarders').get('Level')} | "
            f"Order of Souls: {reputation.get('OrderOfSouls').get('Level')} | "
            f"Merchant Alliance: {reputation.get('MerchantAlliance').get('Level')} | "
            f"Hunter's Call: {reputation.get('HuntersCall').get('Level')} | "
            f"Athena's Fortune: {reputation.get('AthenasFortune').get('Level')} | "
            f"Guardians of Fortune: {reputation.get('PirateLord').get('Level')} | "
            f"Servants of the Flame: {reputation.get('Flameheart').get('Level')}"
        )

        await ctx.send(content=content)

    async def get_reputation(self):
        async with self.aiohttp_session.get(
            url='https://www.seaofthieves.com/api/profilev2/reputation',
            headers={'Referer': 'https://www.seaofthieves.com/profile/reputation'}
        ) as response:
            return await response.json()
    
    async def cog_unload(self):
        await self.aiohttp_session.close()

def prepare(bot: commands.Bot):
    bot.add_cog(Reputation(bot))
