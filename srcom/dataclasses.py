from datetime import datetime, timedelta

from .abcs import Resource
from . import utils


class Category(Resource):

    endpoint = 'categories'

    def __init__(self, data, http):
        super().__init__(data, http)

        self.name = data['name']
        self.type = data['type']
        self.rules = data['rules']
        self.players = data['players']
        self.misc = data['miscellaneous']

    async def game(self):
        """Gets the game this category belongs to"""
        resp = await utils.get_link(self, 'game')
        return Game(resp['data'], self._http)

    async def variables(self):
        """Gets the variables for this category"""
        return await utils.get_link(self, 'variables')

    async def records(self, top=3):
        """Gets the top runs in this category. Defaults to top 3"""
        records = (await utils.get_link(self, 'records', {'top': top}))['data']

        return {
            entry['category']: [
                Run(r['run'], self._http) for r in entry['runs']
            ] for entry in records
        }

    async def runs(self):
        """Gets all runs in the category"""
        runs = await utils.get_link(self, 'runs')
        return [Run(run, self._http) for run in runs['data']]

    async def leaderboard(self, top=None):
        """Gets the leaderboard (all verified current PBs) in this category

        If top is not specified, gets all runs in the leaderboard"""
        if top is not None:
            params = {'top': top}
        else:
            params = None

        board = await utils.get_link(self, 'leaderboard', params)

        return [Run(r['run'], self._http) for r in board['data']['runs']]


class Game(Resource):

    endpoint = 'games'

    def __init__(self, data, http):
        super().__init__(data, http)

        self.name = data['names']['international']
        self.jp_name = data['names']['japanese']
        self.twitch_name = data['names']['twitch']
        self.abbr = data['abbreviation']

        self.release_year = data['released']
        self.release_date = data['release-date']

        self.ruleset = data['ruleset']
        self.romhack = data['romhack']
        self.gametypes = data['gametypes']

    async def runs(self):
        """Gets all the runs for the current game"""
        runs = await utils.get_link(self, 'runs')
        return [Run(run, self._http) for run in runs['data']]

    async def levels(self):
        """Gets all the levels for the current game"""
        return await utils.get_link(self, 'levels')

    async def categories(self):
        """Gets all the categories for the current game"""
        categories = await utils.get_link(self, 'categories')
        return [Category(c, self._http) for c in categories]

    async def variables(self):
        """Gets all the variables for the current game"""
        return await utils.get_link(self, 'variables')

    async def records(self, top=3):
        """Gets the top runs in this game. Defaults to top 3"""
        resp = await utils.get_link(self, 'records', {'top': top})

        return {
            entry['category']: [
                Run(run['run'], self._http) for run in entry['runs']
            ] for entry in resp['data']
        }

    async def record(self, category=None):
        """Gets the top run in this game.

        If category is not specified, then uses the leaderboard's default
        category
        """
        records = await self.leaderboard(1, category)
        return records[0]

    async def series(self):
        """Gets the series this game belongs to"""
        resp = await utils.get_link(self, 'series')
        return Series(resp['data'], self._http)

    async def derived_games(self):
        """Gets a list of games derived from this one"""
        resp = await utils.get_link(self, 'derived-games')
        return [Game(g, self._http) for g in resp['data']]

    async def romhacks(self):
        """Gets a list of romhack games based on this one"""
        resp = await utils.get_link(self, 'romhacks')
        return [Game(g, self._http) for g in resp['data']]

    async def leaderboard(self, top=None, category=None):
        """Gets the leaderboard (all verified current PBs) in this game for a
        particular leaderboard

        If top is not specified, gets all runs in the leaderboard. If category
        is not specified, then uses the leaderboard's default category
        """
        if top is not None:
            params = {'top': top}
        else:
            params = None

        if category is None:
            board = await utils.get_link(self, 'leaderboard', params)
        else:
            board = await self._http.get(
                f'leaderboards/{self.id}/category/{category}', params
            )

        return [Run(run['run'], self._http) for run in board['data']['runs']]


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
        return Game(resp['data'], self._http)

    async def category(self):
        resp = await self._http.get(f'categories/{self._category}')
        return Category(resp['data'], self._http)

    async def platform(self):
        return await utils.get_link(self, 'platform')

    async def region(self):
        return await utils.get_link(self, 'region')

    async def examiner(self):
        user = await utils.get_link(self, 'examiner')
        return User(user['data'], self._http)


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
        return [Game(g, self._http) for g in resp['data']]

    async def moderators(self):
        """Gets the leaderboard moderators for this series"""
        return [await User.from_id(id, self._http) for id in self._moderators]


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
        return [Run(r, self._http) for r in runs]

    async def games(self):
        games = await utils.get_data(self, 'games')
        return [Game(g, self._http) for g in games]

    async def personal_bests(self):
        runs = await utils.get_data(self, 'personal-bests')
        return [Run(r['runs'], self._http, r['place']) for r in runs]
