from . import game, run, utils
from .resource import Resource


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
        return game.Game(resp['data'], self._http)

    async def variables(self):
        """Gets the variables for this category"""
        return await utils.get_link(self, 'variables')

    async def records(self, top=3):
        """Gets the top runs in this category. Defaults to top 3"""
        records = (await utils.get_link(self, 'records', {'top': top}))['data']

        return {
            entry['category']: [
                run.Run(r['run'], self._http) for r in entry['runs']
            ] for entry in records
        }

    async def runs(self):
        """Gets all runs in the category"""
        runs = await utils.get_link(self, 'runs')
        return [run.Run(run, self._http) for run in runs['data']]

    async def leaderboard(self, top=None):
        """Gets the leaderboard (all verified current PBs) in this category

        If top is not specified, gets all runs in the leaderboard"""
        if top is not None:
            params = {'top': top}
        else:
            params = None

        board = await utils.get_link(self, 'leaderboard', params)

        return [run.Run(r['run'], self._http) for r in board['data']['runs']]
