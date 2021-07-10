from datetime import datetime, timedelta
from pprint import pprint

from . import category, game, utils
from .resource import Resource
from .user import User


class Run(Resource):

    endpoint = 'runs'

    def __init__(self, data, http, place=None):
        super().__init__(data, http)

        self._players = data['players']
        self._game = data['game']
        self._category = data['category']
        self.place = place
        self.comment = data['comment']

        self.date = data['date']
        if self.date:
            self.date = datetime.strptime(self.date, '%Y-%m-%d')

        # Convert seconds to a human readable format
        self.time = str(timedelta(seconds=data['times']['primary_t']))

        videos = utils.safeget(data, ('videos', 'links'), ())
        self.videos = [link['uri'] for link in videos]

        self.splits = utils.safeget(data, ('splits', 'uri'))

    async def players(self):
        return [
            User(
                (await self._http._get(player['uri']))['data'],
                self._http
            ) for player in self._players
        ]

    async def player(self):
        return User(
            (await self._http._get(self._players[0]['uri']))['data'],
            self._http
        )

    async def game(self):
        resp = await self._http.get(f'games/{self._game}')
        return game.Game(resp['data'], self._http)

    async def category(self):
        resp = await self._http.get(f'categories/{self._category}')
        return category.Category(resp['data'], self._http)

    async def platform(self):
        return await utils.get_link(self, 'platform')

    async def region(self):
        return await utils.get_link(self, 'region')

    async def examiner(self):
        user = await utils.get_link(self, 'examiner')
        return User(user['data'], self._http)
