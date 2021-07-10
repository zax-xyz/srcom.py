from .category import Category
from .resource import Resource
from .run import Run
from .series import Series
from . import utils


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
