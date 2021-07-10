from . import game, utils
from .resource import Resource
from .user import User


class Series(Resource):

    endpoint = 'series'

    def __init__(self, data, http):
        super().__init__(data, http)

        self.name = data['names']['international']
        self.abbr = data['abbreviation']
        self.created = data['created']
        self.assets = data['assets']
        self._moderators = data['moderators']

    async def games(self):
        """Gets the games in this series"""
        resp = await utils.get_link(self, 'game')
        return [game.Game(g, self._http) for g in resp['data']]

    async def moderators(self):
        """Gets the leaderboard moderators for this series"""
        return [await User.from_id(id, self._http) for id in self._moderators]
