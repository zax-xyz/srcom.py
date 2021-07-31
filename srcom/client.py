from .http import HTTPClient
from .dataclasses import Category, Game, Run, Series, User


class Client:
    def __init__(self):
        self.http = HTTPClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.close()

    async def get_games(self, **kwargs):
        """|coro|

        Searches for games and returns all results

        Parameters
        ------------
        name: Optional[str]
            performs a fuzzy search across game names and abbreviations
        abbreviation: Optional[str]
            performs an exact-match search for this abbreviation
        released: Optional[int]
            restricts to games released in that year
        gametype: Optional[str]
            game type ID; restricts to that game type
        platform: Optional[str]
            platform ID; restricts to that platform
        region: Optional[str]
            region ID; restricts to that region
        genre: Optional[str]
            genre ID; restricts to that genre
        engine: Optional[str]
            engine ID; restricts to that engine
        developer: Optional[str]
            developer ID; restricts to that developer
        publisher: Optional[str]
            publisher ID; restricts to that publisher
        moderator: Optional[str]
            moderator ID; restricts to games moderated by that user
        romhack: Optional[bool]
            legacy parameter; whether or not to include games with game
            types
        _bulk: Optional[bool]
            enable bulk access
        max: Optional[int]
            maximum number of results to return

        Returns
        ---------
        List[Game]
            List of games matching the search. Could be empty if none
            matched.
        """
        resp = await self.http.get("games", kwargs)
        return [Game(game, self.http) for game in resp["data"]]

    async def get_game(self, **kwargs):
        """|coro|

        Searches for a game and returns the first result.

        Parameters
        ------------
        id: Optional[str]
            the ID of the game to fetch; disables all other paramters
        name: Optional[str]
            performs a fuzzy search across game names and abbreviations
        abbreviation: Optional[str]
            performs an exact-match search for this abbreviation
        released: Optional[int]
            restricts to games released in that year
        gametype: Optional[str]
            game type ID; restricts to that game type
        platform: Optional[str]
            platform ID; restricts to that platform
        region: Optional[str]
            region ID; restricts to that region
        genre: Optional[str]
            genre ID; restricts to that genre
        engine: Optional[str]
            engine ID; restricts to that engine
        developer: Optional[str]
            developer ID; restricts to that developer
        publisher: Optional[str]
            publisher ID; restricts to that publisher
        moderator: Optional[str]
            moderator ID; restricts to games moderated by that user
        romhack: Optional[bool]
            legacy parameter; whether or not to include games with game
            types
        _bulk: Optional[bool]
            enable bulk access
        """
        if "id" in kwargs:
            return Game.from_id(kwargs["id"], self.http)

        games = await self.get_games(**kwargs, max=1)
        return games[0]

    async def get_users(self, **kwargs):
        """|coro|

        Searches for users and returns all results

        Parameters
        ------------
        lookup: Optional[str]
            searches the value (case-insensitive, exact) across user
            names, URLS, and social profiles; disabled all other filters
        name: Optional[str]
            filters to users whose name/URL contains this value
            (case-insensitive)
        twitch: Optional[str]
            searches for Twitch usernames
        hitbox: Optional[str]
            searches for Hitbox usernames
        twitter: Optional[str]
            searches for Twitter usernames
        speedrunslive: Optional[str]
            searches for SpeedRunsLive usernames
        max: Optional[int]
            maximum number of results to return
        """
        resp = await self.http.get("users", kwargs)
        return [User(user, self.http) for user in resp["data"]]

    async def get_user(self, **kwargs):
        """|coro|

        Searches for users and returns the first results

        Parameters
        ------------
        id: Optional[str]
            the ID of the user to fetch; disables all other paramters
        lookup: Optional[str]
            searches the value (case-insensitive, exact) across user
            names, URLS, and social profiles; disabled all other filters
        name: Optional[str]
            filters to users whose name/URL contains this value
            (case-insensitive)
        twitch: Optional[str]
            searches for Twitch usernames
        hitbox: Optional[str]
            searches for Hitbox usernames
        twitter: Optional[str]
            searches for Twitter usernames
        speedrunslive: Optional[str]
            searches for SpeedRunsLive usernames
        """
        if "id" in kwargs:
            return User.from_id(kwargs["id"], self.http)

        users = await self.get_users(**kwargs, max=1)
        return users[0]

    async def get_category(self, id):
        """|coro|

        Gets a category by ID

        parameters
        ------------
        id: str
            the ID of the category to fetch
        """
        return Category.from_id(id, self.http)

    async def close(self):
        """Closes the http client"""
        await self.http.close()
