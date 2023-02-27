import os
from configparser import ConfigParser
from twitchio.ext import commands


class Bot(commands.Bot):

    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')

        super().__init__(token=self.config.get('twitch', 'token'),
                         prefix=self.config.get('bot', 'prefix'),
                         initial_channels=[self.config.get('twitch', 'channel')])
        
        # load module
        if (
            self.config.getboolean('bot', 'sot.announcements.enabled') or
            self.config.getboolean('bot', 'sot.balance.enabled') or
            self.config.getboolean('bot', 'sot.reputation.enabled') or
            self.config.getboolean('bot', 'sot.winrate.enabled')
        ):
            self.load_module('cogs.sot')

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')



bot = Bot()
bot.run()
