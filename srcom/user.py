from . import game, run, utils
from .resource import Resource


class User(Resource):

    endpoint = 'users'

    def __init__(self, data, http):
        super().__init__(data, http)

        self.guest = 'id' not in data
        if self.guest:
            self.name = data['name']
        else:
            self.name = data['names']['international']

        country = utils.safeget(data, ('location', 'country'), {})
        self.country = utils.safeget(country, ('names', 'international'))
        self.country_code = country.get('code')

        region = utils.safeget(data, ('location', 'region'), {})
        self.region = utils.safeget(region, ('names', 'international'))
        self.region_code = region.get('code')

        self.twitch = utils.safeget(data, ('twitch', 'uri'))
        self.hitbox = utils.safeget(data, ('hitbox', 'uri'))
        self.youtube = utils.safeget(data, ('youtube', 'uri'))
        self.twitter = utils.safeget(data, ('twitter', 'uri'))
        self.srl = utils.safeget(data, ('speedrunslive', 'uri'))

    async def runs(self):
        runs = await utils.get_data(self, 'runs')
        return [run.Run(r, self._http) for r in runs]

    async def games(self):
        games = await utils.get_data(self, 'games')
        return [game.Game(g, self._http) for g in games]

    async def personal_bests(self):
        runs = await utils.get_data(self, 'personal-bests')
        return [run.Run(r['runs'], self._http, r['place']) for r in runs]
