import aiohttp
from twitchio.ext import commands


class Winrate(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.aiohttp_session = aiohttp.ClientSession(
            cookies={'rat': ''}
        )

    @commands.command()
    @commands.cooldown(rate=1, per=120, bucket=commands.Bucket.channel)
    async def winrate(self, ctx: commands.Context):
        captaincy = await self.get_captaincy()
        
        for alignment in captaincy.get('Pirate').get('Alignments'):
            if alignment.get('Title') == 'The Guardian':
                for accolade in alignment.get('Accolades'):
                    if accolade.get('LocalisedTitle') == 'Battles Completed (as Guardians)':
                        for stat in accolade.get('Stats'):
                            if stat.get('LocalisedTitle') == 'Battles Completed (as Guardians) (Crew):':
                                guardians_battles_completed = stat.get('Value')
                    
                    if accolade.get('LocalisedTitle') == 'Battles Won as Guardians by Seeking a Foe':
                        for stat in accolade.get('Stats'):
                            if stat.get('LocalisedTitle') == 'Battles Won as Guardians by Seeking Foe (Crew):':
                                guardians_battles_won_seeking = stat.get('Value')
                    
                    if accolade.get('LocalisedTitle') == 'Battles Won as Guardians by Repelling a Foe':
                        for stat in accolade.get('Stats'):
                            if stat.get('LocalisedTitle') == 'Battles Won as Guardians by Repelling Foe (Crew):':
                                guardians_battles_won_repelling = stat.get('Value')
            
            if alignment.get('Title') == 'The Servant':
                for accolade in alignment.get('Accolades'):
                    if accolade.get('LocalisedTitle') == 'Battles Completed (as Servants)':
                        for stat in accolade.get('Stats'):
                            if stat.get('LocalisedTitle') == 'Battles Completed (as Servants) (Crew):':
                                servants_battles_completed = stat.get('Value')
                    
                    if accolade.get('LocalisedTitle') == 'Battles Won as Servants by Seeking a Foe':
                        for stat in accolade.get('Stats'):
                            if stat.get('LocalisedTitle') == 'Battles Won as Servants by Seeking Foe (Crew):':
                                servants_battles_won_seeking = stat.get('Value')
                    
                    if accolade.get('LocalisedTitle') == 'Battles Won as Servants by Repelling a Foe':
                        for stat in accolade.get('Stats'):
                            if stat.get('LocalisedTitle') == 'Battles Won as Servants by Repelling Foe (Crew):':
                                servants_battles_won_repelling = stat.get('Value')

        winrate_guardian = ((guardians_battles_won_seeking +  guardians_battles_won_repelling) / guardians_battles_completed) * 100
        winrate_servant = ((servants_battles_won_seeking +  servants_battles_won_repelling) / servants_battles_completed) * 100
        winrate_overall = ((guardians_battles_won_repelling + guardians_battles_won_seeking + servants_battles_won_repelling + servants_battles_won_seeking) / (guardians_battles_completed + servants_battles_completed)) * 100

        content = (
            f"Winrate (as Guardian): {winrate_guardian:.1f} % | "
            f"Winrate (as Servant): {winrate_servant:.1f} % | "
            f"Winrate (overall): {winrate_overall:.1f} %"
        )

        await ctx.send(content=content)

    async def get_captaincy(self):
        async with self.aiohttp_session.get(
            url='https://www.seaofthieves.com/api/profilev2/captaincy',
            headers={'Referer': 'https://www.seaofthieves.com/profile/captaincy/milestones/7938ad38-9a3b-430a-b9f7-6e23a27eded4'}
        ) as response:
            return await response.json()
    
    async def cog_unload(self):
        await self.aiohttp_session.close()

def prepare(bot: commands.Bot):
    bot.add_cog(Winrate(bot))
