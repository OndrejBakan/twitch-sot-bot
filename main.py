import os
from configparser import ConfigParser
from twitchio.ext import commands


class Bot(commands.Bot):

    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')

        super().__init__(token=config.get('twitch', 'token'),
                         prefix=config.get('bot', 'prefix'),
                         initial_channels=[config.get('twitch', 'channel')])
        
        # load module
        if (
            config.getboolean('bot', 'sot.balance.enabled') or
            config.getboolean('bot', 'sot.reputation.enabled') or
            config.getboolean('bot', 'sot.winrate.enabled')
        ):
            self.load_module('cogs.sot')

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')



bot = Bot()
bot.run()
